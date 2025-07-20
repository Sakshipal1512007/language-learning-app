import tkinter as tk
from tkinter import messagebox
from firebase_admin import credentials, firestore, initialize_app
import random

# Firebase setup
cred = credentials.Certificate("firebase_credentials.json")
initialize_app(cred)
db = firestore.client()

# Sample data
LESSONS = {
    "Vocabulary": [("hello", "नमस्ते", "nuh-muh-stay"), ("thank you", "धन्यवाद", "dhun-ya-vaad")],
    "Grammar": [("I am eating", "मैं खा रहा हूँ", "mein kha raha hoon")]
}
QUIZ = {
    "Vocabulary": [("How do you say 'hello' in Hindi?", "नमस्ते")],
    "Grammar": [("Translate: I am eating", "मैं खा रहा हूँ")]
}

# Main App
class LanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning App")
        self.category = tk.StringVar(value="Vocabulary")
        self.lesson_index = 0

        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Select Category").pack()
        for cat in LESSONS.keys():
            tk.Radiobutton(self.root, text=cat, variable=self.category, value=cat).pack()

        tk.Button(self.root, text="Start Daily Lesson", command=self.show_lesson).pack()
        tk.Button(self.root, text="Take Quiz", command=self.start_quiz).pack()

    def show_lesson(self):
        cat = self.category.get()
        word, translation, pronunciation = LESSONS[cat][self.lesson_index]
        messagebox.showinfo("Lesson", f"{word} → {translation}\nPronunciation: {pronunciation}")
        self.lesson_index = (self.lesson_index + 1) % len(LESSONS[cat])
        self.save_progress("lesson", word)

    def start_quiz(self):
        cat = self.category.get()
        question, answer = random.choice(QUIZ[cat])
        user_answer = tk.simpledialog.askstring("Quiz", question)
        if user_answer.strip() == answer:
            messagebox.showinfo("Quiz", "Correct!")
        else:
            messagebox.showinfo("Quiz", f"Incorrect. Correct answer: {answer}")
        self.save_progress("quiz", question)

    def save_progress(self, mode, content):
        data = {"mode": mode, "content": content}
        db.collection("user_progress").add(data)

# Launch the App
if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageApp(root)
    root.mainloop()