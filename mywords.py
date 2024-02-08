import tkinter as tk
from tkinter import ttk
from pydub import AudioSegment
import os

WORDS_DIR = "words"

class TextToSpeechConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech Converter")

        self.label = ttk.Label(root, text="Enter text to convert to speech:")
        self.label.grid(row=0, column=0, pady=10)

        self.text_entry = ttk.Entry(root, width=50)
        self.text_entry.grid(row=1, column=0, pady=10)

        self.convert_button = ttk.Button(root, text="Convert to Speech", command=self.convert_to_speech)
        self.convert_button.grid(row=2, column=0, pady=10)

        self.play_speed_label = ttk.Label(root, text="Playback Speed:")
        self.play_speed_label.grid(row=3, column=0, pady=5)

        self.play_speed_var = tk.DoubleVar()
        self.play_speed_slider = ttk.Scale(root, from_=1.0, to=5.0, length=200, orient="horizontal", variable=self.play_speed_var, command=self.update_speed_label)
        self.play_speed_slider.set(1.0)
        self.play_speed_slider.grid(row=4, column=0, pady=5)

        self.speed_label = ttk.Label(root, text="Speed: 1.0")
        self.speed_label.grid(row=5, column=0, pady=5)

    def update_speed_label(self, value):
        speed_value = round(float(value), 2)
        self.speed_label.config(text=f"Speed: {speed_value}")

    def convert_to_speech(self):
        text_input = self.text_entry.get().lower()
        words = text_input.split()

        for word in words:
            word_file = f"{word}.wav"
            word_path = os.path.join(WORDS_DIR, word_file)
            if os.path.exists(word_path):
                speed = float(self.play_speed_var.get())
                
                if speed == 1.0:
                    # If speed is 1.0, simply play the audio without modifying the speed
                    os.system(f"paplay {word_path}")
                else:
                    # Adjust playback speed if it's not 1.0
                    audio = AudioSegment.from_file(word_path, format="wav")
                    audio = audio.speedup(playback_speed=speed)
                    audio.export("output.mp3", format="mp3")  # Export to MP3 for compatibility
                    os.system("paplay output.mp3")  # Adjust the playback command for compatibility

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechConverter(root)
    root.mainloop()
