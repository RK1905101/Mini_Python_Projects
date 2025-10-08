import tkinter as tk
from tkinter import filedialog, messagebox
import handwriting
import bwprocess
import colorprocess
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(app_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

def browse_file():
    filename = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if filename:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, filename)

def run_handwriting_extraction():
    input_path = entry_file_path.get()
    if input_path:
        output_path = os.path.join(output_dir, 'extracted_text.txt')
        handwriting.main(input_path, output_path)
        messagebox.showinfo("Success", "Text extracted successfully!")
    else:
        messagebox.showerror("Error", "Please select an input image.")

def run_bw_image_improvement():
    input_path = entry_file_path.get()
    if input_path:
        output_path = os.path.join(output_dir, 'enhanced_image_bw.jpg')
        bwprocess.improve_image_quality(input_path, output_path)
        messagebox.showinfo("Success", "Black & White Image enhanced successfully!")
        try:
            os.startfile(output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    else:
        messagebox.showerror("Error", "Please select an input image.")

def run_color_image_improvement():
    input_path = entry_file_path.get()
    if input_path:
        output_path = os.path.join(output_dir, 'enhanced_image_color.jpg')
        colorprocess.enhance_color_image(input_path, output_path)
        messagebox.showinfo("Success", "Color Image enhanced successfully!")
        try:
            os.startfile(output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    else:
        messagebox.showerror("Error", "Please select an input image.")

def on_enter(e):
    e.widget['background'], e.widget['foreground'] = e.widget['foreground'], e.widget['background']

def on_leave(e):
    e.widget['background'], e.widget['foreground'] = e.widget.original_bg, e.widget.original_fg

def style_button(btn, bg_color, fg_color):
    btn.configure(bg=bg_color, fg=fg_color, font=("Helvetica", 12, "bold"), relief="raised", bd=2, padx=10, pady=5)
    btn.original_bg = bg_color
    btn.original_fg = fg_color
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root = tk.Tk()
root.title("Re:Draw")
root.geometry("450x400")  # Increased height a little
root.configure(bg="#E8E5F2")

frame = tk.Frame(root, bg="#1B2250", bd=2, relief=tk.RIDGE)
frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

title_label = tk.Label(frame, text="Re:Draw", font=("Helvetica", 24, "bold"), bg="#1B2250", fg="#E8E5F2")
title_label.pack(pady=(15, 15))

entry_file_path = tk.Entry(frame, width=45, font=("Helvetica", 11))
entry_file_path.pack(pady=(10, 10))

btn_browse = tk.Button(frame, text="Browse Image", command=browse_file)
style_button(btn_browse, "#E8E5F2", "#623FC6")
btn_browse.pack(pady=(5, 20))

btn_handwriting = tk.Button(frame, text="Search For Solution", command=run_handwriting_extraction)
style_button(btn_handwriting, "#623FC6", "#E8E5F2")
btn_handwriting.pack(pady=(5, 10))

btn_improve = tk.Button(frame, text="Enhance B&W Image", command=run_bw_image_improvement)
style_button(btn_improve, "#623FC6", "#E8E5F2")
btn_improve.pack(pady=(0, 10))

btn_color_improve = tk.Button(frame, text="Enhance Color Image", command=run_color_image_improvement)
style_button(btn_color_improve, "#623FC6", "#E8E5F2")
btn_color_improve.pack(pady=(0, 10))

root.mainloop()
