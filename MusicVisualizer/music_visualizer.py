# Dependencies:
# pip install PySide6 sounddevice soundfile pyqtgraph
#
# Run instructions:
# python visualizer_fixed.py

import sys
import threading
import numpy as np

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QPushButton, QSlider, QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

import pyqtgraph as pg
import sounddevice as sd
import soundfile as sf

class AudioEngine:
    """
    Manages audio loading, playback, and real-time analysis.
    Uses sounddevice for audio output and soundfile for loading various audio formats.
    """
    def __init__(self):
        self.audio = None          # Stores the loaded audio data (float32, shape (frames, channels))
        self.sr = None             # Sampling rate of the loaded audio
        self.channels = 0          # Number of audio channels
        self.position = 0          # Current playback position in frames
        self.playing = False       # Playback state (True if playing, False otherwise)
        self.blocksize = 1024      # Number of frames processed in each audio callback
        self.lock = threading.RLock() # Lock to protect shared audio data during multi-threaded access
        self.stream = None         # sounddevice OutputStream object

        # Analysis buffers for FFT
        self.window = None         # Hanning window for spectral analysis
        self.fft_buffer = np.zeros(1024, dtype='float32') # Buffer to store audio data for FFT

    def load(self, path):
        """
        Loads an audio file from the given path.
        Resets playback and analysis parameters.
        """
        audio, sr = sf.read(path, dtype='float32', always_2d=True)
        with self.lock:
            self.audio = audio
            self.sr = sr
            self.channels = audio.shape[1]
            self.position = 0
            self.playing = False
            self.blocksize = 1024
            self.window = np.hanning(self.blocksize).astype('float32') # Initialize Hanning window
            self.fft_buffer = np.zeros(self.blocksize, dtype='float32') # Reset FFT buffer

    def frames_total(self):
        """Returns the total number of frames in the loaded audio."""
        return 0 if self.audio is None else self.audio.shape[0]

    def duration_seconds(self):
        """Returns the total duration of the loaded audio in seconds."""
        return 0.0 if self.audio is None else self.frames_total() / float(self.sr)

    def set_position_seconds(self, t):
        """
        Sets the current playback position in seconds.
        Clips the position to be within the valid range of the audio.
        """
        if self.audio is None:
            return
        idx = int(np.clip(t * self.sr, 0, max(0, self.frames_total() - 1)))
        with self.lock:
            self.position = idx

    def toggle_play(self, state: bool):
        """Toggles the playback state (play/pause)."""
        with self.lock:
            self.playing = state

    def ensure_stream(self):
        """
        Ensures that the sounddevice output stream is active.
        If no stream exists and audio is loaded, it creates and starts a new stream.
        """
        if self.stream is None and self.audio is not None:
            self.stream = sd.OutputStream(
                samplerate=self.sr,
                channels=self.channels,
                blocksize=self.blocksize,
                dtype='float32',
                callback=self._callback # Assigns the audio callback function
            )
            self.stream.start()

    def close(self):
        """
        Stops and closes the sounddevice output stream.
        """
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def _callback(self, outdata, frames, time_info, status):
        """
        Callback function for the sounddevice OutputStream.
        This function is called whenever new audio data is needed for playback.
        It fills `outdata` with audio samples and updates the FFT buffer.
        """
        with self.lock:
            if self.audio is None or not self.playing:
                outdata[:] = 0 # Output silence if no audio or not playing
                return

            start = self.position
            end = min(start + frames, self.frames_total())
            chunk = self.audio[start:end]

            # Pad with zeros if the end of the audio is reached
            if end - start < frames:
                pad = np.zeros((frames - (end - start), self.channels), dtype='float32')
                chunk = np.vstack([chunk, pad])
                self.playing = False # Stop playing when audio finishes

            outdata[:] = chunk # Copy audio chunk to output buffer

            # Prepare data for FFT analysis: convert to mono, apply window
            mono = chunk.mean(axis=1) # Convert to mono by averaging channels
            # Ensure fixed-size fft_buffer by copying or zero-padding
            if mono.shape[0] >= self.blocksize:
                seg = mono[:self.blocksize] * self.window
                self.fft_buffer = seg.astype('float32', copy=True)
            else:
                buf = np.zeros(self.blocksize, dtype='float32')
                n = mono.shape[0]
                if n > 0:
                    buf[:n] = mono * self.window[:n]
                self.fft_buffer = buf

            self.position = start + frames # Update playback position

    def get_time_position(self):
        """Returns the current playback time in seconds."""
        with self.lock:
            if self.audio is None:
                return 0.0
            return self.position / float(self.sr)

    def get_fft(self):
        """
        Performs a Real Fast Fourier Transform (RFFT) on the audio buffer.
        Returns frequencies and magnitudes for spectral visualization.
        This method is called from the GUI thread.
        """
        with self.lock:
            if self.sr is None or self.fft_buffer is None or self.fft_buffer.size == 0:
                return None, None
            fb = self.fft_buffer.copy() # Get a copy of the FFT buffer
            sr = self.sr
        spec = np.fft.rfft(fb) # Compute RFFT
        mag = np.abs(spec)     # Get magnitudes
        freqs = np.fft.rfftfreq(fb.size, d=1.0 / sr) # Get corresponding frequencies
        return freqs, mag

class VisualizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Visualizer (Load, Play, Seek)")
        pg.setConfigOptions(antialias=True) # Enable anti-aliasing for smoother plots

        self.engine = AudioEngine()
        self.seeking = False
        self.wave_x = None
        self.wave_y = None

        # UI Controls
        self.load_btn = QPushButton("Load") # Button to load audio files
        self.play_btn = QPushButton("Play") # Button to start playback
        self.pause_btn = QPushButton("Pause") # Button to pause playback
        self.pos_slider = QSlider(Qt.Horizontal) # Slider to show and control playback position
        self.pos_slider.setRange(0, 1000)
        self.time_lbl = QLabel("00:00 / 00:00") # Label to display current time and total duration

        # Waveform Plot
        self.wave_plot = pg.PlotWidget() # Widget to display the audio waveform
        self.wave_plot.setLabel('bottom', 'Time (s)')
        self.wave_plot.setLabel('left', 'Amplitude')
        self.wave_curve = self.wave_plot.plot(pen=pg.mkPen((90, 200, 255), width=1.5)) # Waveform curve
        self.playhead_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('y', width=2)) # Playhead indicator
        self.wave_plot.addItem(self.playhead_line)
        self.wave_plot.setMouseEnabled(x=True, y=False) # Enable mouse interaction for seeking

        # Spectrum Plot (line plot)
        self.spec_plot = pg.PlotWidget() # Widget to display the audio spectrum
        self.spec_plot.setLogMode(x=True, y=False) # Set X-axis to logarithmic scale for frequency
        self.spec_plot.setLabel('bottom', 'Frequency (Hz)')
        self.spec_plot.setLabel('left', 'Magnitude (dB)')
        self.spec_plot.setYRange(0, 80, padding=0)
        self.spec_curve = self.spec_plot.plot(pen=pg.mkPen('#55ffaa', width=2)) # Spectrum curve

        # Layouts
        ctrl = QHBoxLayout() # Horizontal layout for control buttons and slider
        ctrl.addWidget(self.load_btn)
        ctrl.addWidget(self.play_btn)
        ctrl.addWidget(self.pause_btn)
        ctrl.addWidget(self.pos_slider)
        ctrl.addWidget(self.time_lbl)

        layout = QVBoxLayout() # Main vertical layout for all widgets
        layout.addLayout(ctrl)
        layout.addWidget(self.wave_plot)
        layout.addWidget(self.spec_plot)
        self.setLayout(layout)

        # Signal Connections
        self.load_btn.clicked.connect(self.on_load) # Connect load button to on_load method
        self.play_btn.clicked.connect(self.on_play) # Connect play button to on_play method
        self.pause_btn.clicked.connect(self.on_pause) # Connect pause button to on_pause method
        self.pos_slider.sliderPressed.connect(self.on_seek_start) # Connect slider press for seeking
        self.pos_slider.sliderReleased.connect(self.on_seek_end) # Connect slider release for seeking
        self.wave_plot.scene().sigMouseClicked.connect(self.on_wave_click) # Connect mouse click on waveform for seeking

        # UI Update Timer
        self.ui_timer = QTimer(self) # Timer to periodically update the UI elements
        self.ui_timer.timeout.connect(self.on_ui_tick)
        self.ui_timer.start(33)  # ~30 FPS update rate

    def on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Audio", "", "Audio Files (*.wav *.flac *.ogg *.mp3)")
        if not path:
            return
        self.engine.close()
        self.engine.load(path)
        self.engine.ensure_stream()
        self.render_waveform()
        self.update_time_label(0.0)
        self.pos_slider.setValue(0)
        self.playhead_line.setPos(0)

    def on_play(self):
        if self.engine.audio is None:
            return
        self.engine.ensure_stream()
        self.engine.toggle_play(True)

    def on_pause(self):
        self.engine.toggle_play(False)

    def on_seek_start(self):
        self.seeking = True

    def on_seek_end(self):
        if self.engine.audio is None:
            self.seeking = False
            return
        val = self.pos_slider.value() / 1000.0
        t = val * self.engine.duration_seconds()
        self.engine.set_position_seconds(t)
        self.seeking = False

    def on_wave_click(self, ev):
        if self.engine.audio is None:
            return
        if not self.wave_plot.sceneBoundingRect().contains(ev.scenePos()):
            return
        mouse_point = self.wave_plot.plotItem.vb.mapSceneToView(ev.scenePos())
        x = float(np.clip(mouse_point.x(), 0, self.engine.duration_seconds()))
        self.engine.set_position_seconds(x)

    def render_waveform(self):
        if self.engine.audio is None:
            self.wave_curve.setData([], [])
            return
        audio = self.engine.audio
        sr = self.engine.sr
        mono = audio.mean(axis=1)
        total = mono.shape[0]
        target = 5000
        if total > target:
            step = total // target
            ds = mono[:step * target].reshape(-1, step).mean(axis=1)
            y = ds.astype('float32', copy=False)
            x = (np.arange(ds.shape[0]) * (step / float(sr))).astype('float32', copy=False)
        else:
            y = mono.astype('float32', copy=False)
            x = (np.arange(total) / float(sr)).astype('float32', copy=False)
        self.wave_x = x
        self.wave_y = y
        self.wave_curve.setData(x, y)
        self.wave_plot.setXRange(0, self.engine.duration_seconds(), padding=0.01)
        ymin = float(y.min()) if y.size else -1.0
        ymax = float(y.max()) if y.size else 1.0
        if ymin == ymax:
            ymax = ymin + 1e-3
        self.wave_plot.setYRange(ymin * 1.1, ymax * 1.1, padding=0.1)

    def on_ui_tick(self):
        # Time/slider/playhead
        if self.engine.audio is not None:
            t = self.engine.get_time_position()
            self.update_time_label(t)
            if not self.seeking:
                dur = self.engine.duration_seconds()
                self.pos_slider.blockSignals(True)
                self.pos_slider.setValue(int(1000 * (t / dur if dur > 0 else 0)))
                self.pos_slider.blockSignals(False)
            self.playhead_line.setPos(t)

            # Spectrum update (GUI thread)
            freqs, mag = self.engine.get_fft()
            if freqs is not None and mag is not None and freqs.size and mag.size:
                # Limit to 30..16kHz and bin for stability
                mask = (freqs >= 30) & (freqs <= 16000)
                f = freqs[mask]
                m = mag[mask]
                if f.size and m.size:
                    bins = min(200, f.size)
                    idx = np.linspace(0, f.size - 1, bins).astype(int)
                    f_b = f[idx]
                    m_b = m[idx]
                    db = 20 * np.log10(m_b + 1e-6)
                    db = np.clip(db, -80, 0) + 80  # 0..80
                    # setData requires matching lengths
                    self.spec_curve.setData(f_b.astype('float32', copy=False),
                                           db.astype('float32', copy=False))

    def update_time_label(self, tcur):
        dur = self.engine.duration_seconds()
        def fmt(t):
            m = int(t // 60)
            s = int(t % 60)
            return f"{m:02d}:{s:02d}"
        self.time_lbl.setText(f"{fmt(tcur)} / {fmt(dur)}")

    def closeEvent(self, ev):
        try:
            self.engine.close()
        finally:
            super().closeEvent(ev)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = VisualizerApp()
    w.resize(1100, 700)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
