# 🖋️ Re:Draw

**Re:Draw** is an OpenCV-based desktop application designed to convert handwritten notes or questions into digital text. It enhances low-quality images, removes noise, and simplifies digitization — making it easier for students and educators to organize and share learning materials.

---

## 🧠 Features

### 🪶 1. Extract Text
- Upload any handwritten or printed image.
- The app extracts text using **OCR (Optical Character Recognition)**.
- Automatically searches the extracted text on Google for related results or answers.
- Especially useful for quickly finding solutions to handwritten questions.

### 🌈 2. Enhance Image
- Improves the clarity of low-quality or unclear images.
- Multiple enhancement modes available:
  - **B&W Enhancement** – Perfect for notes and diagrams.
  - **Color Enhancement** – Great for colorful or highlighted documents.
- Saves and opens the enhanced image for instant review.

### 💻 3. GUI Interface
- Built with **Tkinter** for a clean and intuitive design.
- Responsive interface with real-time feedback and file previews.
- Simple operation — no command-line complexity.

---

## ⚙️ Installation & Usage

1. Clone or download this repository.
2. Ensure you have **Python 3.x** installed.
3. Install the required libraries:
   ```bash
   pip install opencv-python pytesseract pillow
