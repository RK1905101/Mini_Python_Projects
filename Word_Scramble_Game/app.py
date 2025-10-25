import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time
import threading

words = {
    "python": "A popular programming language",
    "flask": "A lightweight Python web framework",
    "algorithm": "A step-by-step procedure for calculations",
    "database": "Organized collection of structured information",
    "keyboard": "An input device for typing"
}

scoreboard_file = "scoreboard.json"

def load_scoreboard():
    if os.path.exists(scoreboard_file):
        with open(scoreboard_file, "r") as f:
            return json.load(f)
    return {}

def save_scoreboard(scoreboard):
    with open(scoreboard_file, "w") as f:
        json.dump(scoreboard, f, indent=4)

def scramble_word(word):
    scrambled = list(word)
    random.shuffle(scrambled)
    return ''.join(scrambled)

class WordScrambleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Word Scramble Game")
        self.root.geometry("500x400")
        self.root.config(bg="#f4f4f4")

        self.score = 0
        self.attempts = 0
        self.timer_mode = False
        self.time_limit = 30
        self.remaining_time = self.time_limit
        self.current_word = ""
        self.hint = ""
        self.timer_running = False

        self.scoreboard = load_scoreboard()

        self.create_widgets()
        self.new_word()

    def create_widgets(self):
        tk.Label(self.root, text="Word Scramble Game", font=("Helvetica", 18, "bold"), bg="#f4f4f4").pack(pady=10)

        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f4f4f4", fg="red")
        self.timer_label.pack()

        self.scrambled_label = tk.Label(self.root, text="", font=("Helvetica", 22, "bold"), bg="#f4f4f4")
        self.scrambled_label.pack(pady=20)

        tk.Label(self.root, text="Your Guess:", bg="#f4f4f4").pack()
        self.entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.entry.pack(pady=5)

        self.submit_btn = tk.Button(self.root, text="Submit", command=self.check_guess, width=15, bg="#4CAF50", fg="white")
        self.submit_btn.pack(pady=5)

        self.hint_label = tk.Label(self.root, text="", font=("Helvetica", 11), bg="#f4f4f4", fg="blue")
        self.hint_label.pack(pady=5)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 12), bg="#f4f4f4")
        self.score_label.pack(pady=10)

        self.timer_mode_btn = tk.Button(self.root, text="Toggle Timer Mode", command=self.toggle_timer_mode, bg="#2196F3", fg="white")
        self.timer_mode_btn.pack(pady=5)

        self.next_btn = tk.Button(self.root, text="Next Word", command=self.new_word, width=15, bg="#9C27B0", fg="white")
        self.next_btn.pack(pady=10)

    def toggle_timer_mode(self):
        self.timer_mode = not self.timer_mode
        if self.timer_mode:
            self.timer_mode_btn.config(text="Timer Mode: ON")
        else:
            self.timer_mode_btn.config(text="Timer Mode: OFF")

    def start_timer(self):
        self.remaining_time = self.time_limit
        self.timer_running = True

        def countdown():
            while self.remaining_time > 0 and self.timer_running:
                self.timer_label.config(text=f"⏱️ Time left: {self.remaining_time}s")
                time.sleep(1)
                self.remaining_time -= 1
            if self.remaining_time == 0 and self.timer_running:
                self.timer_running = False
                messagebox.showinfo("Time's up!", f"⏰ The word was '{self.current_word}'")
                self.new_word()

        threading.Thread(target=countdown, daemon=True).start()

    def new_word(self):
        self.attempts = 0
        self.hint_label.config(text="")
        self.entry.delete(0, tk.END)
        word, self.hint = random.choice(list(words.items()))
        self.current_word = word
        scrambled = scramble_word(word)
        self.scrambled_label.config(text=scrambled)

        if self.timer_mode:
            self.start_timer()
        else:
            self.timer_label.config(text="")

    def check_guess(self):
        guess = self.entry.get().strip().lower()
        if not guess:
            return

        if guess == self.current_word:
            messagebox.showinfo("Correct!", "🎉 You guessed it right!")
            self.score += max(10 - self.attempts, 1)
            self.score_label.config(text=f"Score: {self.score}")
            self.timer_running = False
            self.update_scoreboard()
            self.new_word()
        else:
            self.attempts += 1
            messagebox.showwarning("Wrong!", "❌ Try again!")
            if self.attempts == 3:
                self.hint_label.config(text=f"💡 Hint: {self.hint}")

    def update_scoreboard(self):
        name = os.getlogin()
        self.scoreboard[name] = self.score
        save_scoreboard(self.scoreboard)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WordScrambleGame(root)
    root.mainloop()
