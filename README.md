# Voice Recorder

The Voice Recorder is a simple Python GUI application that allows you to record audio using your microphone. This application is built using the Tkinter library for the graphical user interface and PyAudio for handling audio input. The recorded audio is saved as a `.wav` file.

## Features

- **Start/Stop Recording**: Easily start and stop audio recording with a single button click.
- **Timer Display**: A real-time timer shows the duration of the current recording.
- **Automatic File Naming**: Each recording is automatically saved with a unique filename to prevent overwriting existing files.

## Requirements

- Python 3.x
- Tkinter (comes pre-installed with Python)
- PyAudio
- Wave

## Installation

### Clone the Repository:

```bash
git clone https://github.com/Suhas26-05/voice-recorder.git
cd voice-recorder
```

### Install the Required Packages:

You can install the required packages using pip:

```bash
pip install pyaudio
```

**Note**: For some systems, you may need to install additional dependencies for PyAudio. On Ubuntu, you can install it using:

```bash
sudo apt-get install python3-pyaudio
```

## Run the Application

```bash
python voice_recorder.py
```

## Usage

### Starting the Application:

When you run the application, a window will appear with a large button and a timer.

### Recording:

- Click the large red button to start recording. The timer will start counting the recording duration.
- Click the button again to stop the recording. The audio file will be saved automatically.

### File Saving:

- The recording will be saved in the current directory with a filename like `recording1.wav`, `recording2.wav`, etc.
- The application ensures that each new recording gets a unique filename.

## Code Overview

- **VoiceRecorder Class**: The main class that manages the recording process, including starting and stopping the recording and saving the file.
- **Tkinter GUI**: The user interface is built using Tkinter, with a button for controlling the recording and a label to display the timer.
- **Recording Thread**: The recording process runs in a separate thread to ensure the GUI remains responsive.

---
