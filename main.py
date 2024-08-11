import tkinter as tk
from tkinter import filedialog, messagebox
import pyaudio
import wave
import threading

class Recorder:
    def __init__(self):
        # Initialize the recorder with settings for audio recording
        self.chunk = 1024  # Size of each audio chunk
        self.format = pyaudio.paInt16  # Format of the audio (16-bit PCM)
        self.channels = 1  # Number of audio channels (1 for mono)
        self.rate = 44100  # Sample rate (samples per second)
        self.recording = False  # Flag to indicate if recording is ongoing

    def start_recording(self, filename):
        # Start the recording process
        self.recording = True
        self.filename = filename  # Name of the file where audio will be saved
        self.frames = []  # List to store audio frames

        try:
            # Initialize PyAudio
            self.p = pyaudio.PyAudio()

            # Open a new audio stream
            self.stream = self.p.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)

            # Start a new thread for recording to avoid blocking the UI
            self.record_thread = threading.Thread(target=self.record)
            self.record_thread.start()
        except Exception as e:
            # If an error occurs, stop recording and show an error message
            self.recording = False
            messagebox.showerror("Error", f"Failed to start recording: {e}")

    def record(self):
        # The recording loop that captures audio data
        try:
            while self.recording:
                # Read audio data from the stream
                data = self.stream.read(self.chunk)
                # Append the data to the frames list
                self.frames.append(data)
        except Exception as e:
            # If an error occurs during recording, stop and show an error message
            self.recording = False
            messagebox.showerror("Error", f"Recording error: {e}")

    def stop_recording(self):
        # Stop the recording process
        self.recording = False
        # Wait for the recording thread to finish
        self.record_thread.join()

        # Stop and close the audio stream
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()

        # Terminate the PyAudio object
        if hasattr(self, 'p'):
            self.p.terminate()

        # Save the recorded audio to a WAV file
        try:
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))  # Write the audio frames to the file
        except Exception as e:
            # If an error occurs while saving, show an error message
            messagebox.showerror("Error", f"Failed to save file: {e}")

class App:
    def __init__(self, root):
        # Initialize the main application window
        root.geometry("450x150")  # Set the window size
        self.root = root
        self.recorder = Recorder()  # Create an instance of the Recorder class

        # Start Recording button
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        # Stop Recording button
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        # Label to display the current status of the application
        self.status_label = tk.Label(root, text="Ready to record")
        self.status_label.pack(pady=10)

    def start_recording(self):
        # Handler for the Start Recording button click
        filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if filename:
            # If the user provides a filename, start recording
            self.recorder.start_recording(filename)
            # Update the status label to indicate recording has started
            self.status_label.config(text="Recording started")

    def stop_recording(self):
        # Handler for the Stop Recording button click
        self.recorder.stop_recording()
        # Update the status label to indicate recording has stopped
        self.status_label.config(text="Recording stopped")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Recorder")  # Set the window title
    app = App(root)  # Create an instance of the App class
    root.mainloop()  # Start the Tkinter event loop
