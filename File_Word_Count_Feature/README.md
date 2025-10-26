📄 File Word Count Web Application

A simple Flask-based web application that allows users to upload a text file, analyze its content, and view the word frequency count along with a bar chart visualization and downloadable CSV file.

🚀 Features

Upload any .txt file for analysis.
Displays top N most frequent words.
Option to ignore common stopwords.
Automatically generates a bar chart of word frequencies.
Export results as a CSV file.

🛠️ Tech Stack

Frontend: HTML, CSS
Backend: Python (Flask)
Libraries: matplotlib, collections.Counter, csv, re

⚙️ Setup & Run
# 1. Clone the repository
git clone url

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows

# 3. Install dependencies
pip install flask matplotlib

# 4. Run the app
python app.py
Then visit 👉 http://127.0.0.1:5000/
 in your browser.

📊 Example Output

Table: Top N words with counts
Chart: Bar graph visualization
Download: CSV file of all word frequencies