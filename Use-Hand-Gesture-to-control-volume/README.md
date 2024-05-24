# Hand Gesture Volume Control

![Hand Gesture Volume Control](https://img.shields.io/badge/Hand_Gesture_Volume_Control-v1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange.svg)

## Overview

Control your system volume with the wave of your hand! This project uses a webcam to capture real-time hand movements and adjusts the volume based on the distance between your thumb and index finger.

## Features

- **Real-time Hand Tracking**: Utilizes MediaPipe for accurate hand detection.
- **Volume Control**: Adjust system volume by varying the distance between your thumb and index finger.
- **Visual Feedback**: Interactive graphics to show current volume and hand landmarks.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Visual Feedback](#visual-feedback)

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- PulseAudio

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/harshaparida/Controlling_volume_using_hand-gestures.git
   cd Controlling_volume_using_hand-gestures
   ```

2. **Install the required packages**:
   ```sh
   pip install opencv-python mediapipe pulsectl
   ```

## Usage

Run the following command to start the volume control application:
```sh
python hand_gesture_control.py
```

## How It Works

1. **Capture Video**: The webcam captures video frames.
2. **Process Frames**: MediaPipe processes the frames to detect hand landmarks.
3. **Calculate Distance**: The distance between the thumb and index finger is calculated.
4. **Adjust Volume**: The system volume is adjusted based on the distance.

## Visual Feedback

- **Hand Landmarks**: The thumb and index finger are highlighted with green circles.
- **Connecting Line**: A green line connects the thumb and index finger.
- **Background Color**: The background color changes based on the volume level.
- **Volume Display**: Current volume percentage is displayed on the frame.

---

Enhance your multimedia experience with just a wave of your hand. Happy coding!

---
