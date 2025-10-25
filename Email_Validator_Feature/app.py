from flask import Flask, render_template, request
import re
import socket

app = Flask(__name__)

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def domain_exists(email):
    try:
        domain = email.split('@')[1]
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ''
    color = ''
    if request.method == 'POST':
        email = request.form['email']

        if not validate_email_format(email):
            result = "❌ Invalid format! Please check the email syntax."
            color = 'red'
        elif not domain_exists(email):
            result = "⚠️ Domain not found! The email domain doesn’t exist."
            color = 'orange'
        else:
            result = "✅ Valid Email! Domain exists and format is correct."
            color = 'green'

    return render_template('index.html', result=result, color=color)

if __name__ == '__main__':
    app.run(debug=True)
