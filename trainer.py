import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sounddevice as sd
import numpy as np
import wave
import csv

WORDS_DIR = "words"
BUTTON_COLOR_GREEN = "#4CAF50"  # Green color for the "Next Word" button
BUTTON_COLOR_BLUE = "#2196F3"   # Blue color for the "Re-record Last Word" button

class WordRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Recorder")

        self.imported_csv_files = set()  # Set to store imported CSV file names

        self.import_csv_button = ttk.Button(root, text="Import CSV", command=self.import_csv)
        self.import_csv_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.next_word_button = ttk.Button(root, text="Next Word", command=self.next_word, style="Green.TButton")
        self.next_word_button.grid(row=1, column=0, columnspan=2, pady=10)
        self.next_word_button.grid_remove()  # Initially hidden

        self.re_record_button = ttk.Button(root, text="Re-record Last Word", command=self.re_record_last_word, style="Blue.TButton")
        self.re_record_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.re_record_button.grid_remove()  # Initially hidden

        self.info_label = ttk.Label(root, text="")
        self.info_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.word_count_label = ttk.Label(root, text="")
        self.word_count_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.word_list = []
        self.remaining_words = []
        self.current_index = 0

        # Configure the style for the "Next Word" button
        self.root.style = ttk.Style()
        self.root.style.configure("Green.TButton", foreground="white", background=BUTTON_COLOR_GREEN)

        # Configure the style for the "Re-record Last Word" button
        self.root.style.configure("Blue.TButton", foreground="black", background=BUTTON_COLOR_BLUE)

    def load_word_list(self):
        existing_files = [filename[:-4] for filename in os.listdir(WORDS_DIR) if filename.endswith(".wav")]
        return existing_files

    def next_word(self):
        if self.current_index < len(self.remaining_words):
            missing_word = self.remaining_words[self.current_index]

            response = messagebox.askokcancel("Record Word", f"Please record the word '{missing_word}'.")

            if response:
                output_path = os.path.join(WORDS_DIR, f"{missing_word.lower()}.wav")

                self.info_label.config(text=f"Recording '{missing_word}'...")

                fs = 44100
                duration = 1.0
                recording = sd.rec(int(fs * duration), samplerate=fs, channels=1, dtype=np.int16)
                sd.wait()

                with wave.open(output_path, 'w') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(fs)
                    wf.writeframes(recording.tobytes())

                self.info_label.config(text=f"Recording of '{missing_word}' completed and saved.")
                self.current_index += 1
                self.update_buttons_visibility()  # Update visibility after recording
                self.update_word_count_label()  # Update word count label
            else:
                self.info_label.config(text="Recording skipped.")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if file_path:
            # Check if the file has already been imported
            if file_path in self.imported_csv_files:
                messagebox.showwarning("Duplicate Import", "This CSV file has already been imported.")
                return

            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                imported_words = [word.lower() for row in csv_reader for word in row if word]

            # Filter out imported words that already have corresponding audio files
            imported_words = [word for word in imported_words if not os.path.exists(os.path.join(WORDS_DIR, f"{word}.wav"))]

            self.word_list.extend(imported_words)
            self.remaining_words.extend(imported_words)

            self.imported_csv_files.add(file_path)  # Add the imported file to the set
            self.info_label.config(text="CSV file imported. Words added to the training list.")
            self.update_buttons_visibility()  # Update visibility after importing CSV
            self.update_word_count_label()  # Update word count label

    def re_record_last_word(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.info_label.config(text="Re-recording the last word.")
            self.next_word()
        else:
            self.info_label.config(text="No previous word to re-record.")

    def update_buttons_visibility(self):
        if self.current_index < len(self.remaining_words):
            self.next_word_button.grid()
        else:
            self.next_word_button.grid_remove()

        if self.current_index > 0:
            self.re_record_button.grid()
        else:
            self.re_record_button.grid_remove()

    def update_word_count_label(self):
        word_count_text = f"{self.current_index}/{len(self.word_list)}"
        self.word_count_label.config(text=word_count_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordRecorder(root)
    root.mainloop()
