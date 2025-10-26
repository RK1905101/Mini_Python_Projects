# 🖼️ AI Background Remover

This project is a simple, fast, and AI-powered background removal tool built using **Streamlit** and **rembg** (ONNX-based background removal).  
Users can upload any image, preview it, and download the background-removed output instantly.

---

## 🚀 Features

✔ Upload JPG/PNG images  
✔ AI-powered background removal  
✔ Live preview of original & processed image  
✔ Download final output as PNG  
✔ Fast & lightweight Streamlit UI  

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| AI Model | rembg (U2-Net ONNX model) |
| Image Handling | Pillow (PIL) |
| Language | Python 3.8+ |

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
https://github.com/RK1905101/Mini_Python_Projects
cd AI-Background-Remover
2️⃣ Create & Activate Virtual Environment (Recommended)

conda create -n bgremove python=3.9 -y
conda activate bgremove
or using venv ⬇️


python -m venv venv
venv\Scripts\activate  # Windows
3️⃣ Install Required Packages
pip install -r requirements.txt

If you face onnxruntime errors on Windows:
pip install onnxruntime

▶️ Run the App
streamlit run src/streamlit_app.py
Streamlit will open the app in your browser automatically ✅
If not, open the URL shown in the terminal (e.g., http://localhost:8501)

📂 Project Structure
AI-Background-Remover/
│
├── src/
│   └── streamlit_app.py     # Main UI app
│   └── cli_app.py     
│
├── requirements.txt         # Dependencies
├── README.md                # Project Documentation
└── assets/                  # Demo images (optional)
📸 Screenshots
Original	Background Removed


📜 License
This project is for educational and personal use. Please refer to the license file for more details.


