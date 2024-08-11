import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
from datetime import datetime

class VoiceRecorder:
    def __init__(self):
        # Initialize the main Tkinter window
        self.root = tk.Tk()
        self.root.title("Voice Recorder")  # Set the title of the window
        self.root.resizable(False, False)  # Disable resizing of the window
        
        # Create a button to start/stop recording with large red dot as the label
        self.button = tk.Button(self.root, text="●", font=("Arial", 120, "bold"), command=self.click_handler)
        self.button.pack(pady=20)  # Add some padding for spacing
        
        # Label to display the recording time (in hours:minutes:seconds)
        self.label = tk.Label(self.root, text="00:00:00", font=("Arial", 24))
        self.label.pack()  # Add the label to the window
        
        self.recording = False  # Flag to indicate if recording is ongoing
        self.record_thread = None  # Thread that will handle the recording process
        self.start_time = None  # Variable to store the start time of the recording
        
        # Start the Tkinter event loop
        self.root.mainloop()

    def click_handler(self):
        # Toggle recording on/off when the button is clicked
        if self.recording:
            self.recording = False  # Stop the recording
            self.button.config(fg="Black")  # Change button color to black
        else:
            self.recording = True  # Start recording
            self.button.config(fg="Red")  # Change button color to red
            self.start_time = time.time()  # Record the current time as the start time
            self.record_thread = threading.Thread(target=self.record)  # Create a new thread for recording
            self.record_thread.start()  # Start the recording thread
            self.update_timer()  # Start updating the timer on the label

    def update_timer(self):
        # Update the timer label with the elapsed recording time
        if self.recording:
            elapsed = time.time() - self.start_time  # Calculate elapsed time
            secs = elapsed % 60
            mins = elapsed // 60 % 60
            hours = elapsed // 3600
            # Update the label with the formatted time
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
            # Call this method again after 1 second to keep updating the timer
            self.root.after(1000, self.update_timer)

    def record(self):
        # Function to handle the actual recording process
        audio = pyaudio.PyAudio()  # Initialize PyAudio
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []  # List to store audio frames

        while self.recording:
            # Read audio data from the stream and append it to frames
            data = stream.read(1024)
            frames.append(data)
        
        # Stop and close the stream once recording is stopped
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded frames to a file
        file_path = self.get_next_file_name()  # Get the next available file name
        with wave.open(file_path, "wb") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b"".join(frames))  # Write the frames to the file

    def get_next_file_name(self):
        # Generate the next available file name to avoid overwriting existing files
        base_name = "recording"
        ext = ".wav"
        i = 1
        # Increment the file index until a non-existing file name is found
        while os.path.exists(f"{base_name}{i}{ext}"):
            i += 1
        return f"{base_name}{i}{ext}"  # Return the new file name

if __name__ == "__main__":
    VoiceRecorder()  # Create an instance of the VoiceRecorder class and run the application
