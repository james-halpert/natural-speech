import tkinter as tk
from tkinter import messagebox, IntVar
import csv
import nltk

class DictionaryGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Dictionary Generator")

        self.label_num_words = tk.Label(master, text="Select the number of words:")
        self.label_num_words.pack()

        self.entry_num_words = tk.Entry(master)
        self.entry_num_words.pack()

        self.label_file_name = tk.Label(master, text="Enter the file name (without extension):")
        self.label_file_name.pack()

        self.entry_file_name = tk.Entry(master)
        self.entry_file_name.pack()

        self.use_adjectives_var = IntVar()
        self.checkbox_adjectives = tk.Checkbutton(master, text="Generate only adjectives", variable=self.use_adjectives_var)
        self.checkbox_adjectives.pack()

        self.generate_button = tk.Button(master, text="Generate Dictionary", command=self.generate_dictionary)
        self.generate_button.pack()

    def generate_dictionary(self):
        try:
            num_words = int(self.entry_num_words.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        file_name = self.entry_file_name.get()
        use_adjectives = self.use_adjectives_var.get()

        nltk.download('stopwords')
        nltk.download('corpora')
        nltk.download('words')

        stopwords = set(nltk.corpus.stopwords.words('english'))
        word_freq_list = nltk.FreqDist(nltk.corpus.words.words()).most_common()

        # Filter out stopwords and include prepositions and articles
        common_words = [word.lower() for word, freq in word_freq_list if word.lower() not in stopwords]
        prepositions_and_articles = ["the", "an", "in", "on", "at", "with", "by", "for", "of", "to", "from", "through", "after", "before", "between", "under", "over", "above", "below", "around", "along", "across", "beside", "beneath", "near", "among", "throughout", "against", "beyond"]

        common_words = prepositions_and_articles + common_words

        if use_adjectives:
            adjectives = set(word.lower() for word, tag in nltk.pos_tag(nltk.corpus.words.words()) if tag == 'JJ')
            common_words = list(filter(lambda word: word in adjectives, common_words))

        file_path = f"{file_name}.csv"

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for word in common_words[:num_words]:
                writer.writerow([word])

        messagebox.showinfo("Success", f"Dictionary with {num_words} {'adjectives' if use_adjectives else 'words'} generated as '{file_path}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryGenerator(root)
    root.mainloop()
