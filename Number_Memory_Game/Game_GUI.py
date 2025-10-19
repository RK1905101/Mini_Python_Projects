import tkinter as tk
import random
import time
import json
import os

class NumberMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Number Memory Game")
        self.root.geometry("520x500")

        # --- Themes ---
        self.dark_theme = {"bg": "#1e1e2f", "fg": "white", "accent": "#FFD700"}
        self.light_theme = {"bg": "#f5f5f5", "fg": "#222", "accent": "#2196F3"}
        self.theme = "dark"
        self.colors = self.dark_theme

        # --- Game Variables ---
        self.level = "Easy"
        self.sequence = ""
        self.score = 0
        self.streak = 0
        self.high_scores = self.load_high_scores()

        # --- UI Setup ---
        self.root.config(bg=self.colors["bg"])
        self.title_label = tk.Label(root, text="🧠 Number Memory Game", font=("Poppins", 20, "bold"),
                                    fg=self.colors["accent"], bg=self.colors["bg"])
        self.title_label.pack(pady=20)

        self.theme_btn = tk.Button(root, text="🌙 Switch Theme", font=("Poppins", 10),
                                   bg=self.colors["accent"], fg="white", relief="flat",
                                   command=self.toggle_theme, cursor="hand2")
        self.theme_btn.pack(pady=5)

        self.main_frame = tk.Frame(root, bg=self.colors["bg"])
        self.main_frame.pack(pady=20)

        self.label = tk.Label(self.main_frame, text="", font=("Poppins", 14),
                              fg=self.colors["fg"], bg=self.colors["bg"])
        self.label.pack(pady=10)

        self.info_label = tk.Label(self.main_frame, text="", font=("Poppins", 12),
                                   fg="#9E9E9E", bg=self.colors["bg"])
        self.info_label.pack(pady=5)

        self.input_entry = tk.Entry(self.main_frame, font=("Poppins", 16), justify="center",
                                    relief="flat", bg="#f5f5f5")
        self.submit_btn = tk.Button(self.main_frame, text="Submit", font=("Poppins", 12, "bold"),
                                    bg="#2196F3", fg="white", width=12, relief="flat",
                                    command=self.check_answer, cursor="hand2")

        # Start screen
        self.start_screen()

    # ---------------- SCREENS ---------------- #
    def start_screen(self):
        self.clear_screen()
        self.label.config(text="Welcome to the Number Memory Game!\nTest how good your memory is 🔢",
                          fg=self.colors["accent"])
        tk.Button(self.main_frame, text="Start Game", font=("Poppins", 14, "bold"),
                  bg="#4CAF50", fg="white", width=14, relief="flat",
                  command=self.select_difficulty, cursor="hand2").pack(pady=20)

    def select_difficulty(self):
        self.clear_screen()
        self.label.config(text="Choose Difficulty", fg=self.colors["fg"])
        frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        frame.pack(pady=20)
        for lvl, color in [("Easy", "#4CAF50"), ("Medium", "#FF9800"), ("Hard", "#E91E63")]:
            tk.Button(frame, text=lvl, font=("Poppins", 12, "bold"),
                      bg=color, fg="white", width=10, relief="flat",
                      command=lambda l=lvl: self.start_game(l),
                      cursor="hand2").pack(side="left", padx=10)

    def end_screen(self):
        self.clear_screen()
        self.label.config(text="❌ Game Over!", fg="#E91E63")
        summary = f"Your Score: {self.score}\nLongest Streak: {self.streak}\nHighest Score: {max(self.high_scores)}"
        tk.Label(self.main_frame, text=summary, font=("Poppins", 12),
                 fg=self.colors["fg"], bg=self.colors["bg"]).pack(pady=10)

        tk.Button(self.main_frame, text="🏆 View Leaderboard", font=("Poppins", 12, "bold"),
                  bg="#2196F3", fg="white", width=14, relief="flat",
                  command=self.show_leaderboard, cursor="hand2").pack(pady=5)

        tk.Button(self.main_frame, text="🔁 Play Again", font=("Poppins", 12, "bold"),
                  bg="#FF9800", fg="white", width=14, relief="flat",
                  command=self.select_difficulty, cursor="hand2").pack(pady=5)

        tk.Button(self.main_frame, text="🚪 Exit", font=("Poppins", 12, "bold"),
                  bg="#9E9E9E", fg="white", width=14, relief="flat",
                  command=self.root.quit, cursor="hand2").pack(pady=5)

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    # ---------------- GAME FLOW ---------------- #
    def start_game(self, level):
        self.level = level
        self.score = 0
        self.streak = 0
        self.clear_screen()
        self.countdown(3)

    def countdown(self, seconds):
        self.clear_screen()
        if seconds > 0:
            self.label.config(text=f"Starting in {seconds}...", fg=self.colors["accent"])
            self.label.pack(pady=40)
            self.root.after(1000, self.countdown, seconds - 1)
        else:
            self.next_round()

    def next_round(self):
        self.clear_screen()
        self.sequence = self.generate_sequence()
        self.label.config(text="Memorize this sequence:", fg=self.colors["accent"])
        self.label.pack(pady=10)
        self.info_label.config(text=f"{self.sequence}")
        self.info_label.pack()
        self.root.update()
        time.sleep(2 if self.level == "Easy" else 1.5 if self.level == "Medium" else 1)
        self.show_input_screen()

    def show_input_screen(self):
        self.clear_screen()
        self.label.config(text="Now type the sequence:", fg=self.colors["fg"])
        self.label.pack(pady=10)
        self.input_entry.delete(0, tk.END)
        self.input_entry.pack(pady=10)
        self.submit_btn.pack(pady=5)

    def generate_sequence(self):
        length = 3 + self.score if self.level == "Easy" else 4 + self.score if self.level == "Medium" else 5 + self.score
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def check_answer(self):
        answer = self.input_entry.get()
        if answer == self.sequence:
            self.score += 1
            self.streak = max(self.streak, self.score)
            self.label.config(text="✅ Correct!", fg="#4CAF50")
            self.info_label.config(text=f"Score: {self.score} | Longest Streak: {self.streak}")
            self.root.after(1000, self.next_round)
        else:
            self.update_high_scores(self.score)
            self.end_screen()

    # ---------------- LEADERBOARD ---------------- #
    def load_high_scores(self):
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as f:
                return json.load(f)
        return []

    def update_high_scores(self, new_score):
        self.high_scores.append(new_score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:5]
        with open("highscores.json", "w") as f:
            json.dump(self.high_scores, f)

    def show_leaderboard(self):
        top = tk.Toplevel(self.root)
        top.title("🏆 Leaderboard")
        top.geometry("300x300")
        top.config(bg=self.colors["bg"])
        tk.Label(top, text="Top 5 High Scores", font=("Poppins", 14, "bold"),
                 fg=self.colors["accent"], bg=self.colors["bg"]).pack(pady=10)
        for i, score in enumerate(self.high_scores, start=1):
            tk.Label(top, text=f"{i}. {score}", font=("Poppins", 12),
                     fg=self.colors["fg"], bg=self.colors["bg"]).pack()

    # ---------------- THEME SWITCH ---------------- #
    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.colors = self.light_theme if self.theme == "light" else self.dark_theme
        self.apply_theme()

    def apply_theme(self):
        self.root.config(bg=self.colors["bg"])
        self.main_frame.config(bg=self.colors["bg"])
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=self.colors["bg"], fg=self.colors["fg"])
            elif isinstance(widget, tk.Button):
                widget.config(bg=self.colors["accent"], fg="white")
        self.label.config(fg=self.colors["fg"])
        self.title_label.config(fg=self.colors["accent"], bg=self.colors["bg"])
        self.theme_btn.config(bg=self.colors["accent"], fg="white")

# ---------------- RUN GAME ---------------- #
root = tk.Tk()
game = NumberMemoryGame(root)
root.mainloop()
