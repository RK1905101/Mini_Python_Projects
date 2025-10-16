import tkinter as tk
from tkinter import ttk
import random

# Tarot Card Database
TAROT_CARDS = {
    "The Fool": "New beginnings, innocence, spontaneity, free spirit",
    "The Magician": "Manifestation, resourcefulness, power, inspired action",
    "The High Priestess": "Intuition, sacred knowledge, divine feminine, subconscious",
    "The Empress": "Femininity, beauty, nature, nurturing, abundance",
    "The Emperor": "Authority, establishment, structure, father figure",
    "The Hierophant": "Spiritual wisdom, religious beliefs, conformity, tradition",
    "The Lovers": "Love, harmony, relationships, values alignment, choices",
    "The Chariot": "Control, willpower, success, action, determination",
    "Strength": "Strength, courage, persuasion, influence, compassion",
    "The Hermit": "Soul searching, introspection, being alone, inner guidance",
    "Wheel of Fortune": "Good luck, karma, life cycles, destiny, turning point",
    "Justice": "Justice, fairness, truth, cause and effect, law",
    "The Hanged Man": "Pause, surrender, letting go, new perspectives",
    "Death": "Endings, change, transformation, transition",
    "Temperance": "Balance, moderation, patience, purpose, meaning",
    "The Devil": "Shadow self, attachment, addiction, restriction, sexuality",
    "The Tower": "Sudden change, upheaval, chaos, revelation, awakening",
    "The Star": "Hope, faith, purpose, renewal, spirituality",
    "The Moon": "Illusion, fear, anxiety, subconscious, intuition",
    "The Sun": "Positivity, fun, warmth, success, vitality",
    "Judgement": "Judgement, rebirth, inner calling, absolution",
    "The World": "Completion, accomplishment, travel, fulfillment"
}

class TarotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Mystical Tarot Reader ✨")
        self.root.geometry("700x600")
        self.root.configure(bg="#0d1b2a")
        self.root.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = tk.Label(
            self.root,
            text="✨ MYSTICAL TAROT READER ✨",
            font=("Arial", 24, "bold"),
            bg="#0d1b2a",
            fg="#e0e1dd"
        )
        header.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Choose your reading type",
            font=("Arial", 12),
            bg="#0d1b2a",
            fg="#778da9"
        )
        subtitle.pack(pady=5)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg="#0d1b2a")
        button_frame.pack(pady=30)
        
        # Reading Type Buttons
        btn_style = {
            "font": ("Arial", 12),
            "bg": "#1b263b",
            "fg": "#e0e1dd",
            "activebackground": "#415a77",
            "activeforeground": "#e0e1dd",
            "relief": "flat",
            "borderwidth": 0,
            "padx": 20,
            "pady": 15,
            "width": 25,
            "cursor": "hand2"
        }
        
        single_btn = tk.Button(
            button_frame,
            text="🎴 Single Card Reading",
            command=lambda: self.perform_reading(1),
            **btn_style
        )
        single_btn.pack(pady=8)
        
        three_btn = tk.Button(
            button_frame,
            text="🔮 Three Card Reading",
            command=lambda: self.perform_reading(3),
            **btn_style
        )
        three_btn.pack(pady=8)
        
        celtic_btn = tk.Button(
            button_frame,
            text="✨ Celtic Cross (5 cards)",
            command=lambda: self.perform_reading(5),
            **btn_style
        )
        celtic_btn.pack(pady=8)
        
        # Results Frame with Scrollbar
        result_container = tk.Frame(self.root, bg="#0d1b2a")
        result_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(result_container)
        scrollbar.pack(side="right", fill="y")
        
        self.result_text = tk.Text(
            result_container,
            font=("Arial", 11),
            bg="#1b263b",
            fg="#e0e1dd",
            wrap="word",
            relief="flat",
            padx=15,
            pady=15,
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # Disclaimer
        disclaimer = tk.Label(
            self.root,
            text="⚠️ For entertainment purposes only",
            font=("Arial", 9, "italic"),
            bg="#0d1b2a",
            fg="#778da9"
        )
        disclaimer.pack(pady=10)
        
    def perform_reading(self, num_cards):
        cards = random.sample(list(TAROT_CARDS.keys()), num_cards)
        
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        
        if num_cards == 1:
            self.result_text.insert(tk.END, "🌙 SINGLE CARD READING\n", "header")
            self.result_text.insert(tk.END, "Your current energy\n\n", "subheader")
            self.display_card(cards[0])
            
        elif num_cards == 3:
            self.result_text.insert(tk.END, "🌙 THREE CARD READING\n", "header")
            self.result_text.insert(tk.END, "Past • Present • Future\n\n", "subheader")
            positions = ["PAST", "PRESENT", "FUTURE"]
            for card, pos in zip(cards, positions):
                self.display_card(card, pos)
                
        elif num_cards == 5:
            self.result_text.insert(tk.END, "🌙 CELTIC CROSS READING\n", "header")
            self.result_text.insert(tk.END, "A comprehensive spread\n\n", "subheader")
            positions = ["PRESENT", "CHALLENGE", "FOUNDATION", "RECENT PAST", "OUTCOME"]
            for card, pos in zip(cards, positions):
                self.display_card(card, pos)
        
        self.result_text.config(state="disabled")
        
        # Configure tags for styling
        self.result_text.tag_config("header", font=("Arial", 14, "bold"), foreground="#e0e1dd")
        self.result_text.tag_config("subheader", font=("Arial", 10), foreground="#778da9")
        self.result_text.tag_config("position", font=("Arial", 10, "bold"), foreground="#d4a373")
        self.result_text.tag_config("card", font=("Arial", 12, "bold"), foreground="#e0e1dd")
        self.result_text.tag_config("meaning", font=("Arial", 10), foreground="#a8b2c1")
        
    def display_card(self, card_name, position=None):
        if position:
            self.result_text.insert(tk.END, f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "meaning")
            self.result_text.insert(tk.END, f"{position}\n", "position")
        
        self.result_text.insert(tk.END, f"🎴 {card_name}\n", "card")
        self.result_text.insert(tk.END, f"{TAROT_CARDS[card_name]}\n\n", "meaning")

def main():
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()