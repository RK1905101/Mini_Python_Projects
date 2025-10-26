import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import time
import json
import os

HIGHSCORE_FILE = "highscore.json"

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
    "The early bird catches the worm."
]

medium_sentences = [
    "Typing speed improves with consistent and mindful practice.",
    "Programming languages require logic, patience, and creativity.",
    "Every day is another chance to become a better version of yourself.",
    "Curiosity drives learning and innovation.",
    "Discipline is the bridge between goals and accomplishment.",
    "Mistakes are proof that you are trying.",
    "Reading expands the mind and imagination.",
    "Collaboration leads to better solutions."
]

hard_sentences = [
    "Artificial intelligence is transforming industries through automation and data analysis.",
    "Sustainability requires balancing environmental, social, and economic factors responsibly.",
    "The complexity of modern software systems demands efficient algorithms and optimized design.",
    "Globalization affects economic, cultural, and political landscapes simultaneously.",
    "Cryptography ensures secure communication over untrusted networks.",
    "Machine learning models require vast amounts of quality data for accuracy.",
    "Problem-solving skills are enhanced by critical thinking and creativity.",
    "Leadership is about inspiring others toward a common goal."
]


class TimedTypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Timed Typing Test")
        self.root.geometry("900x780")
        self.root.resizable(False, False)

        # state
        self.highscore = self.load_highscore()
        self.running = False
        self.test_duration = 60
        self.current_text = ""
        self.custom_text = ""

        # per-sentence tracking
        self.sentence_start_time = None
        self.processed_up_to = 0  # char index in typed_text we've processed sentences up to
        self.sentence_results = []  # list of (wpm, accuracy, words, errors)

        # UI
        self.text_area = scrolledtext.ScrolledText(root, height=10, width=100, font=("Arial", 12))
        self.text_area.pack(pady=10)
        self.text_area.config(state=tk.DISABLED)

        self.input_area = scrolledtext.ScrolledText(root, height=6, width=100, font=("Arial", 12))
        self.input_area.pack(pady=6)
        self.input_area.config(state=tk.DISABLED)

        # Info labels
        info_frame = tk.Frame(root)
        info_frame.pack(pady=4)
        self.timer_label = tk.Label(info_frame, text=f"Time Left: {self.test_duration} s", font=("Arial", 12), fg="blue")
        self.timer_label.grid(row=0, column=0, padx=8)
        self.live_wpm_label = tk.Label(info_frame, text="Live WPM: 0.00", font=("Arial", 12), fg="purple")
        self.live_wpm_label.grid(row=0, column=1, padx=8)
        self.error_label = tk.Label(info_frame, text="Errors: 0", font=("Arial", 12), fg="red")
        self.error_label.grid(row=0, column=2, padx=8)
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
        self.result_label.pack(pady=4)

        # per-sentence label
        self.sentence_info_label = tk.Label(root, text="Sentence WPM: - | Avg WPM: - | Total Errors: 0",
                                            font=("Arial", 11))
        self.sentence_info_label.pack(pady=3)

        # Difficulty & timer controls
        controls = tk.Frame(root)
        controls.pack(pady=6)
        self.difficulty_var = tk.StringVar(value="Easy")
        modes = ["Easy", "Medium", "Hard", "Custom"]
        for idx, m in enumerate(modes):
            cmd = self.open_custom_window if m == "Custom" else None
            tk.Radiobutton(controls, text=m, variable=self.difficulty_var, value=m, command=cmd).grid(row=0, column=idx, padx=6)

        tk.Label(root, text="Select Test Duration:", font=("Arial", 11)).pack()
        tframe = tk.Frame(root)
        tframe.pack(pady=4)
        self.timer_var = tk.IntVar(value=60)
        for i, sec in enumerate([30, 60, 120]):
            tk.Radiobutton(tframe, text=f"{sec}s", variable=self.timer_var, value=sec, command=self.update_timer_label).grid(row=0, column=i, padx=8)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Start Test", command=self.start_test, bg="lightgreen", width=16).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Reset", command=self.reset_test, bg="#f0ad4e", width=12).grid(row=0, column=1, padx=8)

        # Highscore
        self.highscore_label = tk.Label(root, text=f"Highscore: {self.highscore} WPM", font=("Arial", 12))
        self.highscore_label.pack(pady=4)

    # ---------- persistence ----------
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return json.load(f).get("highscore", 0)
            except Exception:
                return 0
        return 0

    def save_highscore(self, wpm):
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                json.dump({"highscore": wpm}, f)
        except Exception:
            pass

    # ---------- custom text ----------
    def open_custom_window(self):
        win = tk.Toplevel(self.root)
        win.title("Custom Text")
        win.geometry("750x350")
        tk.Label(win, text="Enter custom text (use sentences ending with a period):").pack(pady=6)
        box = scrolledtext.ScrolledText(win, height=12, width=90)
        box.pack(padx=8, pady=6)
        box.insert(tk.END, self.custom_text)

        def save_and_close():
            txt = box.get("1.0", tk.END).strip()
            if not txt:
                messagebox.showwarning("Warning", "Custom text cannot be empty.")
                return
            self.custom_text = txt
            win.destroy()

        tk.Button(win, text="Save & Close", command=save_and_close, bg="lightblue").pack(pady=6)

    # ---------- timer ----------
    def update_timer_label(self):
        self.test_duration = self.timer_var.get()
        self.timer_label.config(text=f"Time Left: {self.test_duration} s")

    # ---------- pick sentences ----------
    def generate_sentence(self):
        diff = self.difficulty_var.get()
        if diff == "Easy":
            return random.choice(easy_sentences)
        elif diff == "Medium":
            return random.choice(medium_sentences)
        elif diff == "Hard":
            return random.choice(hard_sentences)
        else:
            return self.custom_text or "Please add custom text."

    # ---------- test lifecycle ----------
    def start_test(self):
        # reset per-run state
        self.test_duration = self.timer_var.get()
        self.result_label.config(text="")
        self.sentence_results.clear()
        self.sentence_start_time = None
        self.processed_up_to = 0

        # show initial sentence(s)
        first = self.generate_sentence()
        self.current_text = first
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, self.current_text)
        self.text_area.config(state=tk.DISABLED)

        self.input_area.config(state=tk.NORMAL)
        self.input_area.delete("1.0", tk.END)
        self.input_area.focus_set()

        self.start_time = time.time()
        self.sentence_start_time = self.start_time
        self.running = True

        # bind and start timers
        self.input_area.bind("<KeyRelease>", self.check_input)
        self.update_timer()
        self.update_live_wpm()

    def reset_test(self):
        self.running = False
        self.input_area.config(state=tk.DISABLED)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.input_area.delete("1.0", tk.END)
        self.timer_label.config(text=f"Time Left: {self.timer_var.get()} s")
        self.live_wpm_label.config(text="Live WPM: 0.00")
        self.error_label.config(text="Errors: 0")
        self.result_label.config(text="")
        self.sentence_info_label.config(text="Sentence WPM: - | Avg WPM: - | Total Errors: 0")
        self.sentence_results.clear()
        self.processed_up_to = 0

    # ---------- helpers to find words with positions ----------
    def _words_with_spans(self, text):
        """
        Return a list of (word, start_index, end_index) for words in text.
        Words are contiguous non-space runs.
        """
        words = []
        i = 0
        n = len(text)
        while i < n:
            # skip spaces
            while i < n and text[i].isspace():
                i += 1
            if i >= n:
                break
            start = i
            while i < n and not text[i].isspace():
                i += 1
            end = i  # one past last char of word
            words.append((text[start:end], start, end))
        return words

    # ---------- main input checking (word-level + char-level highlighting) ----------
    def check_input(self, event=None):
        typed_text = self.input_area.get("1.0", tk.END).rstrip("\n")
        ref_text = self.text_area.get("1.0", tk.END).rstrip("\n")

        # build words + spans for typed and reference
        typed_words = self._words_with_spans(typed_text)
        ref_words = self._words_with_spans(ref_text)

        # clear previous tags
        self.input_area.tag_remove("error", "1.0", tk.END)
        self.input_area.tag_config("error", foreground="red")

        errors_chars = 0
        # compare word-by-word, highlight only mismatched characters inside words
        for i, (t_word, t_start, t_end) in enumerate(typed_words):
            if i < len(ref_words):
                r_word, r_start, r_end = ref_words[i]
                # compare char-by-char within the word
                minlen = min(len(t_word), len(r_word))
                for j in range(minlen):
                    if t_word[j] != r_word[j]:
                        # tag the exact character in input widget (position = t_start + j)
                        start_index = f"1.0 + {t_start + j}c"
                        end_index = f"1.0 + {t_start + j + 1}c"
                        self.input_area.tag_add("error", start_index, end_index)
                        errors_chars += 1
                # extra typed chars beyond reference word
                if len(t_word) > len(r_word):
                    extra = len(t_word) - len(r_word)
                    for j in range(len(r_word), len(t_word)):
                        start_index = f"1.0 + {t_start + j}c"
                        end_index = f"1.0 + {t_start + j + 1}c"
                        self.input_area.tag_add("error", start_index, end_index)
                    errors_chars += extra
                # if typed shorter than ref word, don't mark missing letters (they are not typed)
            else:
                # typed an extra whole word beyond reference -> mark the whole word as error chars
                for j in range(len(t_word)):
                    start_index = f"1.0 + {t_start + j}c"
                    end_index = f"1.0 + {t_start + j + 1}c"
                    self.input_area.tag_add("error", start_index, end_index)
                errors_chars += len(t_word)

        self.error_label.config(text=f"Errors: {errors_chars}")

        # -------------------
        # Per-sentence processing:
        # When user types a period '.' that completes a sentence, compute WPM & accuracy for that sentence.
        # We'll process any new completed sentences since last processed position.
        # -------------------
        # find next '.' in typed_text after processed_up_to
        idx = self.processed_up_to
        while True:
            dot_pos = typed_text.find('.', idx)
            if dot_pos == -1:
                break
            # sentence slice from processed_up_to to dot_pos (inclusive)
            sentence_typed = typed_text[self.processed_up_to:dot_pos+1].strip()
            # take corresponding reference sentence from ref_text at same relative length:
            # safer approach: find the same slice length in ref_text (assuming auto-append keeps them aligned)
            sentence_ref = ref_text[self.processed_up_to: self.processed_up_to + len(sentence_typed)].strip()
            # compute words and errors within that sentence
            typed_words_in_sentence = [w for w, s, e in self._words_with_spans(sentence_typed)]
            ref_words_in_sentence = [w for w, s, e in self._words_with_spans(sentence_ref)]
            # count correct words (exact match)
            correct_words = sum(1 for k in range(min(len(typed_words_in_sentence), len(ref_words_in_sentence)))
                                if typed_words_in_sentence[k] == ref_words_in_sentence[k])
            # count errors in chars for that sentence
            # we can reuse the char comparisons: compare character by character in the sentence slice
            char_errors = 0
            for p, ch in enumerate(sentence_typed):
                if p < len(sentence_ref):
                    if ch != sentence_ref[p]:
                        char_errors += 1
                else:
                    char_errors += 1
            # sentence time: from sentence_start_time to now
            now = time.time()
            elapsed_sentence = now - (self.sentence_start_time or self.start_time)
            words_count = len(typed_words_in_sentence)
            sentence_wpm = (words_count / elapsed_sentence * 60) if elapsed_sentence > 0 else 0.0
            sentence_accuracy = (correct_words / max(1, len(ref_words_in_sentence))) * 100 if ref_words_in_sentence else 0.0
            self.sentence_results.append((sentence_wpm, sentence_accuracy, words_count, char_errors))
            # update sentence start time and processed pointer
            self.sentence_start_time = now
            self.processed_up_to = dot_pos + 1
            idx = self.processed_up_to
            # update sentence info label
            avg_wpm = sum(s[0] for s in self.sentence_results) / len(self.sentence_results) if self.sentence_results else 0.0
            last_wpm = self.sentence_results[-1][0]
            total_errors = sum(s[3] for s in self.sentence_results)
            self.sentence_info_label.config(text=f"Last sentence WPM: {last_wpm:.2f} | Avg WPM: {avg_wpm:.2f} | Total Errors: {total_errors}")

        # -------------------
        # Auto-append next sentence: if typed has completed all words of current ref (user finished current sentence),
        # append a new random sentence to ref_text so user can keep typing until timer ends.
        # We append only when typed_text contains at least all ref words typed (i.e., user finished current sentence)
        # and last typed character is punctuation '.' (so they intentionally finished sentence).
        # -------------------
        # Simple check: if typed_text endswith '.' and len(typed_text) >= len(ref_text) (they reached end),
        # then append a new sentence.
        if typed_text.endswith('.') and len(typed_text) >= len(ref_text):
            new_sentence = self.generate_sentence()
            # append to reference area
            self.current_text += " " + new_sentence
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, " " + new_sentence)
            self.text_area.config(state=tk.DISABLED)

    # ---------- timer & finalize ----------
    def update_timer(self):
        if not self.running:
            return
        elapsed = int(time.time() - self.start_time)
        remaining = self.test_duration - elapsed
        if remaining > 0:
            self.timer_label.config(text=f"Time Left: {remaining} s")
            self.root.after(1000, self.update_timer)
        else:
            self.end_test()

    def end_test(self):
        self.running = False
        self.input_area.config(state=tk.DISABLED)

        typed_text = self.input_area.get("1.0", tk.END).strip()
        ref_text = self.text_area.get("1.0", tk.END).strip()

        typed_words = [w for w, s, e in self._words_with_spans(typed_text)]
        ref_words = [w for w, s, e in self._words_with_spans(ref_text)]

        correct = sum(1 for i in range(min(len(typed_words), len(ref_words))) if typed_words[i] == ref_words[i])
        accuracy = (correct / len(ref_words) * 100) if ref_words else 0.0
        elapsed = time.time() - self.start_time
        wpm = (len([w for w in typed_words]) / (elapsed / 60)) if elapsed > 0 else 0.0

        messagebox.showinfo("Calculating WPM...", "Your typing session is finished!")

        self.result_label.config(text=f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

        # update sentence info final
        if self.sentence_results:
            avg_wpm = sum(s[0] for s in self.sentence_results) / len(self.sentence_results)
            total_errors = sum(s[3] for s in self.sentence_results)
            self.sentence_info_label.config(text=f"Last sentence WPM: {self.sentence_results[-1][0]:.2f} | Avg WPM: {avg_wpm:.2f} | Total Errors: {total_errors}")

        # save highscore
        if wpm > self.highscore:
            self.highscore = round(wpm, 2)
            self.highscore_label.config(text=f"Highscore: {self.highscore} WPM")
            self.save_highscore(self.highscore)
            messagebox.showinfo("New Highscore!", f"🎉 You set a new highscore: {self.highscore} WPM!")

    # ---------- live WPM updates ----------
    def update_live_wpm(self):
        if not self.running:
            return
        elapsed = time.time() - self.start_time
        # count only finished words (words followed by space or punctuation)
        typed_text = self.input_area.get("1.0", tk.END).rstrip("\n")
        words_spans = self._words_with_spans(typed_text)
        finished_words = 0
        for word, start, end in words_spans:
            # finished if there's a separating char after the word (space) or word ends with punctuation or it's at end and endswith punctuation
            if end < len(typed_text):
                if typed_text[end].isspace():
                    finished_words += 1
                else:
                    # if the next char isn't space, consider it unfinished unless word ends with punctuation
                    if word and word[-1] in ".!?":
                        finished_words += 1
            else:
                # at end of typed_text: consider finished only if ends with punctuation
                if word and word[-1] in ".!?":
                    finished_words += 1

        if elapsed > 0:
            live_wpm = finished_words / (elapsed / 60)
        else:
            live_wpm = 0.0
        self.live_wpm_label.config(text=f"Live WPM: {live_wpm:.2f}")
        self.root.after(1000, self.update_live_wpm)


if __name__ == "__main__":
    root = tk.Tk()
    app = TimedTypingTest(root)
    root.mainloop()
