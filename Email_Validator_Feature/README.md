📝 Description

This app lets users verify if an email is valid. It checks:
Syntax using regex
Domain existence using socket
and displays color-coded results.

⚙️ Features

✅ Format validation
🌐 Domain verification
🎨 Color-coded feedback (Green / Orange / Red)
🧩 Flask backend + HTML frontend

🚀 Run Locally
git clone (url)
cd Email-Validator
pip install flask
python app.py
Then visit 👉 http://127.0.0.1:5000/

🧪 Test Cases
Input	Expected Result
test@gmail.com	✅ Valid email
invalid@@mail	❌ Invalid format

💡 Future Enhancements

MX record check
Disposable email detection

Author: Pranjali Randive
Built with: Flask, Python, HTML, CSS