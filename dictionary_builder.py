import tkinter as tk
from tkinter import messagebox
import csv
import nltk

class DictionaryGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Dictionary Generator")

        self.label = tk.Label(master, text="Select the number of words:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.generate_button = tk.Button(master, text="Generate Dictionary", command=self.generate_dictionary)
        self.generate_button.pack()

    def generate_dictionary(self):
        try:
            num_words = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        nltk.download('stopwords')
        nltk.download('corpora')
        nltk.download('words')

        stopwords = set(nltk.corpus.stopwords.words('english'))
        word_freq_list = nltk.FreqDist(nltk.corpus.words.words()).most_common()

        # Filter out stopwords and include prepositions and articles
        common_words = [word.lower() for word, freq in word_freq_list if word.lower() not in stopwords]
        prepositions_and_articles = ["the", "an", "in", "on", "at", "with", "by", "for", "of", "to", "from", "through", "after", "before", "between", "under", "over", "above", "below", "around", "along", "across", "beside", "beneath", "near", "among", "throughout", "against", "beyond"]

        common_words = prepositions_and_articles + common_words

        with open("dictionary.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Common Words"])

            for word in common_words[:num_words]:
                writer.writerow([word])

        messagebox.showinfo("Success", f"Dictionary with {num_words} most common words generated as 'dictionary.csv'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryGenerator(root)
    root.mainloop()
