import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import time
import json
import os

HIGHSCORE_FILE = "highscore.json"
TEST_DURATION = 60  # Test duration in seconds

# --- Sentences by difficulty ---
easy_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes perfect in every skill.",
    "Time and tide wait for no man.",
    "Honesty is the best policy.",
    "Actions speak louder than words.",
    "Better late than never.",
    "Knowledge is power.",
    "All that glitters is not gold.",
    "Rome was not built in a day.",
    "The early bird catches the worm.",
    "A picture is worth a thousand words.",
    "Birds of a feather flock together.",
    "Absence makes the heart grow fonder.",
    "Curiosity killed the cat.",
    "Every cloud has a silver lining.",
    "Look before you leap.",
    "Patience is a virtue.",
    "No man is an island.",
    "Two heads are better than one.",
    "Fools rush in where angels fear to tread."
]

medium_sentences = [
    "Artificial Intelligence is transforming the world.",
    "OpenAI develops advanced AI technologies.",
    "Better late than never is sometimes true.",
    "Necessity is the mother of invention.",
    "Curiosity killed the cat, but satisfaction brought it back.",
    "Fortune favors the bold in most undertakings.",
    "A rolling stone gathers no moss in life or work.",
    "The pen is mightier than the sword in many cases.",
    "Discretion is the better part of valor in complex situations.",
    "Practice what you preach consistently.",
    "Rome wasn’t built in a day, and neither are skills.",
    "Too many cooks spoil the broth in teamwork.",
    "The grass is always greener on the other side of the fence.",
    "You can’t have your cake and eat it too simultaneously.",
    "When the going gets tough, the tough get going.",
    "Out of sight, out of mind applies to many situations.",
    "A watched pot never boils, literally and figuratively.",
    "Haste makes waste when rushing important tasks.",
    "Money doesn’t grow on trees, as everyone knows.",
    "Look before you leap, especially in investments."
]

hard_sentences = [
    "The road to hell is paved with good intentions, as history shows repeatedly.",
    "Brevity is the soul of wit, yet verbosity often confuses readers.",
    "Discretion is the better part of valor in complex situations.",
    "A rolling stone gathers no moss, illustrating impermanence vividly.",
    "Two wrongs don’t make a right, a principle crucial in ethics.",
    "Ignorance is bliss until one faces the consequences of choices.",
    "The proof of the pudding is in the eating, not the promise.",
    "United we stand, divided we fall, a timeless lesson in cooperation.",
    "Variety is the spice of life, making experiences richer and more diverse.",
    "Where there’s smoke, there’s fire, a cautionary tale in suspicion.",
    "The squeaky wheel gets the grease, yet sometimes silence is golden.",
    "Nothing ventured, nothing gained, encouraging calculated risks.",
    "Good things come to those who wait, patience often pays off.",
    "Blood is thicker than water, emphasizing family bonds strongly.",
    "Familiarity breeds contempt, a warning in relationships.",
    "A fool and his money are soon parted, highlighting poor judgment.",
    "The apple doesn’t fall far from the tree, inheritance of traits.",
    "Do not bite the hand that feeds you, wise counsel in loyalty.",
    "Clothes make the man, yet character defines him more fully.",
    "The early bird catches the worm, success favors the proactive."
]

# --- Typing Test Class ---
class TimedTypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Timed Typing Test")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        self.highscore = self.load_highscore()
        self.start_time = None
        self.running = False

        # Reference text
        self.text_area = scrolledtext.ScrolledText(root, height=10, width=90, font=("Arial", 12))
        self.text_area.pack(pady=10)
        self.text_area.config(state=tk.DISABLED)

        # Typing input area
        self.input_area = scrolledtext.ScrolledText(root, height=5, width=90, font=("Arial", 12))
        self.input_area.pack(pady=10)
        self.input_area.config(state=tk.DISABLED)

        # Timer label
        self.timer_label = tk.Label(root, text=f"Time Left: {TEST_DURATION} s", font=("Arial", 12), fg="blue")
        self.timer_label.pack(pady=5)

        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
        self.result_label.pack(pady=5)

        # Difficulty selector
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_frame = tk.Frame(root)
        tk.Label(difficulty_frame, text="Select Difficulty:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty_var, value="Easy").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(difficulty_frame, text="Medium", variable=self.difficulty_var, value="Medium").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(difficulty_frame, text="Hard", variable=self.difficulty_var, value="Hard").pack(side=tk.LEFT, padx=10)
        difficulty_frame.pack(pady=10)

        # Buttons
        self.start_button = tk.Button(root, text="Start Test", command=self.start_test,
                                      font=("Arial", 12), bg="#4CAF50", fg="white")
        self.start_button.pack(pady=10)

        self.highscore_label = tk.Label(root, text=f"Highscore: {self.highscore} WPM", font=("Arial", 12), fg="darkgreen")
        self.highscore_label.pack(pady=5)

    # Highscore management
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                try:
                    data = json.load(f)
                    return data.get("highscore", 0)
                except:
                    return 0
        return 0

    def save_highscore(self, wpm):
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": wpm}, f)

    # Generate reference text based on difficulty
    def generate_reference_text(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            return " ".join(random.choices(easy_sentences, k=10))
        elif difficulty == "Medium":
            return " ".join(random.choices(medium_sentences, k=10))
        else:
            return " ".join(random.choices(hard_sentences, k=10))

    # Start the test
    def start_test(self):
        self.input_area.delete('1.0', tk.END)
        self.result_label.config(text="")
        self.reference_text = self.generate_reference_text()

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, self.reference_text)
        self.text_area.config(state=tk.DISABLED)

        self.input_area.config(state=tk.NORMAL)
        self.input_area.focus()
        self.start_time = time.time()
        self.running = True

        # Bind real-time error highlighting
        self.input_area.bind("<KeyRelease>", self.highlight_errors)

        self.update_timer()

    # Real-time error highlighting
    def highlight_errors(self, event=None):
        typed_text = self.input_area.get('1.0', tk.END).strip()
        typed_words = typed_text.split()
        reference_words = self.reference_text.split()

        self.input_area.tag_remove("error", "1.0", tk.END)

        for i, word in enumerate(typed_words):
            if i >= len(reference_words):
                break
            if word != reference_words[i]:
                start_idx = f"1.0 + {sum(len(w)+1 for w in typed_words[:i])} chars"
                end_idx = f"1.0 + {sum(len(w)+1 for w in typed_words[:i+1])-1} chars"
                self.input_area.tag_add("error", start_idx, end_idx)

        self.input_area.tag_config("error", foreground="red")

    # Timer update
    def update_timer(self):
        if not self.running:
            return
        elapsed = time.time() - self.start_time
        remaining = max(0, TEST_DURATION - int(elapsed))
        self.timer_label.config(text=f"Time Left: {remaining} s")
        if remaining > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.end_test()

    # End the test and calculate results
    def end_test(self):
        self.running = False
        self.input_area.config(state=tk.DISABLED)

        typed_text = self.input_area.get('1.0', tk.END).strip()
        typed_words = typed_text.split()
        reference_words = self.reference_text.split()

        correct_words = sum(1 for i, word in enumerate(typed_words)
                            if i < len(reference_words) and word == reference_words[i])
        total_words = len(typed_words)

        wpm = round(total_words / (TEST_DURATION / 60), 2)
        accuracy = round((correct_words / total_words) * 100, 2) if total_words > 0 else 0

        self.result_label.config(text=f"WPM: {wpm} | Accuracy: {accuracy}%")

        # Update highscore
        if wpm > self.highscore:
            self.highscore = wpm
            self.highscore_label.config(text=f"Highscore: {self.highscore} WPM")
            self.save_highscore(wpm)
            messagebox.showinfo("New Highscore!", f"Congratulations! New highscore: {wpm} WPM")

# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TimedTypingTest(root)
    root.mainloop()
