import tkinter as tk
import random
import time

class ColorMindGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Mind")
        self.root.geometry("600x700")
        self.root.configure(bg="#323232")
        self.root.resizable(False, False)
        
        # Game variables
        self.sequence = []
        self.player_sequence = []
        self.score = 0
        self.game_state = "START"
        self.is_showing = False
        
        # Title
        self.title_label = tk.Label(
            root, 
            text="COLOR MIND", 
            font=("Arial", 36, "bold"),
            bg="#323232",
            fg="white"
        )
        self.title_label.pack(pady=20)
        
        # Score label
        self.score_label = tk.Label(
            root,
            text="Press Start to Play!",
            font=("Arial", 20),
            bg="#323232",
            fg="white"
        )
        self.score_label.pack(pady=10)
        
        # Button frame
        self.button_frame = tk.Frame(root, bg="#323232")
        self.button_frame.pack(pady=30)
        
        # Create color buttons
        self.buttons = []
        self.button_colors = [
            ("#C80000", "#FF0000", "red"),      # Red
            ("#00C800", "#00FF00", "green"),    # Green
            ("#0000C8", "#0000FF", "blue"),     # Blue
            ("#C8C800", "#FFFF00", "yellow")    # Yellow
        ]
        
        # Top row (Red, Green)
        for i in range(2):
            btn = tk.Button(
                self.button_frame,
                width=15,
                height=8,
                bg=self.button_colors[i][0],
                activebackground=self.button_colors[i][1],
                relief="raised",
                bd=5,
                command=lambda idx=i: self.button_clicked(idx)
            )
            btn.grid(row=0, column=i, padx=10, pady=10)
            self.buttons.append(btn)
        
        # Bottom row (Blue, Yellow)
        for i in range(2, 4):
            btn = tk.Button(
                self.button_frame,
                width=15,
                height=8,
                bg=self.button_colors[i][0],
                activebackground=self.button_colors[i][1],
                relief="raised",
                bd=5,
                command=lambda idx=i: self.button_clicked(idx)
            )
            btn.grid(row=1, column=i-2, padx=10, pady=10)
            self.buttons.append(btn)
        
        # Start button
        self.start_button = tk.Button(
            root,
            text="START GAME",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            command=self.start_game
        )
        self.start_button.pack(pady=20)
        
        # Message label
        self.message_label = tk.Label(
            root,
            text="Click START to begin!",
            font=("Arial", 14),
            bg="#323232",
            fg="white"
        )
        self.message_label.pack(pady=10)
    
    def start_game(self):
        self.sequence = []
        self.player_sequence = []
        self.score = 0
        self.game_state = "PLAYING"
        self.score_label.config(text=f"Score: {self.score}")
        self.message_label.config(text="Watch carefully!")
        self.start_button.config(state="disabled")
        self.add_to_sequence()
        self.root.after(500, self.show_sequence)
    
    def add_to_sequence(self):
        self.sequence.append(random.randint(0, 3))
    
    def show_sequence(self):
        self.is_showing = True
        self.show_next_button(0)
    
    def show_next_button(self, index):
        if index >= len(self.sequence):
            self.is_showing = False
            self.message_label.config(text="Your turn!")
            return
        
        button_index = self.sequence[index]
        self.light_up_button(button_index)
        self.root.after(600, lambda: self.light_off_button(button_index))
        self.root.after(800, lambda: self.show_next_button(index + 1))
    
    def light_up_button(self, index):
        self.buttons[index].config(bg=self.button_colors[index][1])
        # Simple beep sound using system bell
        self.root.bell()
    
    def light_off_button(self, index):
        self.buttons[index].config(bg=self.button_colors[index][0])
    
    def button_clicked(self, button_index):
        if self.game_state != "PLAYING" or self.is_showing:
            return
        
        # Light up button briefly
        self.light_up_button(button_index)
        self.root.after(300, lambda: self.light_off_button(button_index))
        
        # Add to player sequence
        self.player_sequence.append(button_index)
        
        # Check if correct
        current_step = len(self.player_sequence) - 1
        if self.player_sequence[current_step] != self.sequence[current_step]:
            self.root.after(400, self.game_over)
            return
        
        # Check if sequence complete
        if len(self.player_sequence) == len(self.sequence):
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.message_label.config(text="Correct!")
            self.player_sequence = []
            self.root.after(1000, self.next_round)
    
    def next_round(self):
        self.add_to_sequence()
        self.message_label.config(text="Watch carefully!")
        self.root.after(500, self.show_sequence)
    
    def game_over(self):
        self.game_state = "GAME_OVER"
        self.message_label.config(text=f"Game Over! Final Score: {self.score}")
        self.start_button.config(state="normal", text="PLAY AGAIN")
        
        # Flash all buttons
        self.flash_buttons(0, 3)
    
    def flash_buttons(self, count, max_flashes):
        if count >= max_flashes:
            for i in range(4):
                self.light_off_button(i)
            return
        
        # Light up all
        for i in range(4):
            self.light_up_button(i)
        
        # Light off all after 200ms
        self.root.after(200, lambda: self.flash_off(count, max_flashes))
    
    def flash_off(self, count, max_flashes):
        for i in range(4):
            self.light_off_button(i)
        
        # Next flash after 200ms
        self.root.after(200, lambda: self.flash_buttons(count + 1, max_flashes))

# Create and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ColorMindGame(root)
    root.mainloop()