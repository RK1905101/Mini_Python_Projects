# Music Visualizer

This is a simple music visualizer application built with Python, PySide6, pyqtgraph, sounddevice, and soundfile.

## Features

- Load audio files (WAV, FLAC, OGG, MP3)
- Play/Pause audio
- Seek through audio using a slider or by clicking on the waveform
- Real-time waveform display
- Real-time spectrum (FFT) visualization

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd python-tetris
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ./venv/Scripts/activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the `music_visualizer.py` file:

```bash
python music_visualizer.py
```

Once the application is running:

- Click the "Load" button to select an audio file.
- Use the "Play" and "Pause" buttons to control playback.
- Drag the slider or click on the waveform to seek to a specific position in the audio.

## Dependencies

- `numpy`
- `PySide6`
- `pyqtgraph`
- `sounddevice`
- `soundfile`
