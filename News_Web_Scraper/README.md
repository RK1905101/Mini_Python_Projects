# News Scraper

A simple Flask web application to scrape news headlines and content from any website. Users can filter articles by keyword and export results to a CSV file.

---

## Features

- Scrape headlines (`h1`, `h2`, `h3`) and first paragraph from news websites.
- Filter articles by keyword.
- Toggle content visibility for each article.
- Export scraped news to CSV.

---

## Tech Stack

- Python 3
- Flask
- Requests
- BeautifulSoup4
- Pandas
- HTML, CSS, JavaScript, Bootstrap 5

---

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-folder>

Create and activate virtual environment:
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

Install dependencies:
pip install flask requests beautifulsoup4 pandas

Run the app:
python app.py
Open in browser: http://127.0.0.1:5000/

Usage
Enter a news website URL.

(Optional) Enter a keyword to filter articles.

Click Scrape to view articles.

Click Export CSV to download results.

Example
URL: https://www.bbc.com/news

Keyword: AI