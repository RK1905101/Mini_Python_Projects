# 🖼️ AI Background Remover

An AI-powered desktop tool that automatically removes image backgrounds and saves the subject as a transparent PNG — perfect for designers, students, and automation scripts.

✅ Built with Python
✅ Uses `rembg` + U²-Net AI model
✅ Works with JPG & PNG images
✅ GUI + Command Line Interface
✅ Hacktoberfest friendly 🎉

---

## 🚀 Features

| Feature                  | Description                               |
| ------------------------ | ----------------------------------------- |
| ✂️ AI Background Removal | Removes background using machine learning |
| 🖥️ Streamlit GUI        | Upload → Preview → Remove BG → Download   |
| 💻 CLI Tool              | Command-line support for automation       |
| 📦 Output                | Saves transparent PNG                     |
| 🔰 Beginner Friendly     | Simple folder structure + clean code      |

---

## 📌 Project Structure

```
AI-Background-Remover/
│
├── src/
│   ├── streamlit_app.py     # Streamlit UI version
│   ├── cli_app.py           # Command-line background remover
│
├── assets/
│   ├── sample1.png
│   ├── sample2.png
│
├── requirements.txt
└── README.md
```

---

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RK1905101/Mini_Python_Projects/AI-Background-Remover
cd AI-Background-Remover
```

### 2️⃣ Install Dependencies

> Recommended: Use a virtual environment ✅

```bash
pip install -r requirements.txt
```

If `onnxruntime` or `rembg` fails on your system:

```bash
pip install rembg onnxruntime
```

---

## 🖼️ Streamlit GUI Usage

Run the application:

```bash
streamlit run src/streamlit_app.py
```

Then open the browser link shown in the terminal ✅
Upload your image → Click **Remove Background** → Download PNG

---

## 💻 CLI Tool Usage

```bash
python src/cli_app.py input.jpg -o output.png
```

## 📸 Screenshots

| Before                              | 
| ----------------------------------- | 
| <img width="200" height="1024" alt="bgremover" src="https://github.com/user-attachments/assets/5b93d1ae-e3cc-424c-a5e6-c5a3bbc75e69" />
| After                             | 
<img width="200" height="1024" alt="output2" src="https://github.com/user-attachments/assets/7087cf33-b6eb-444d-81b2-187a498d4a1d" />|

