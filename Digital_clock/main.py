import tkinter as tk
import time
from datetime import datetime

# Create main window
root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x200")
root.resizable(False, False)
root.config(bg="#1e1e1e")

# Time label
time_label = tk.Label(root, text="", font=("Segoe UI", 48, "bold"), fg="#00ff99", bg="#1e1e1e")
time_label.pack(pady=20)

# Date label
date_label = tk.Label(root, text="", font=("Segoe UI", 16), fg="#ffffff", bg="#1e1e1e")
date_label.pack()

# Function to update time and date
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A, %d %B %Y")
    
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    
    root.after(1000, update_clock)  # Update every 1 second

# Start the clock
update_clock()

# Run the application
root.mainloop()
