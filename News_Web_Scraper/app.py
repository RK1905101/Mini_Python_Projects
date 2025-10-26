from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

app = Flask(__name__)

def scrape_news(url, keyword=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return [{"headline": "Error fetching URL", "date": "", "content": str(e), "link": url}]

    articles = []
    # Flexible scraping: headlines inside h1/h2/h3 and first paragraph nearby
    for headline_tag in soup.find_all(['h1','h2','h3'])[:20]:
        headline_text = headline_tag.text.strip()
        link_tag = headline_tag.find('a')
        link = link_tag['href'] if link_tag else url
        if link and not link.startswith("http"):
            link = url.rstrip('/') + link
        # Try to get next sibling paragraph
        content_tag = headline_tag.find_next('p')
        content_text = content_tag.text.strip() if content_tag else "No Content"
        # Try to get date
        date_tag = headline_tag.find_next('time')
        date_text = date_tag['datetime'] if date_tag else "No Date"

        if keyword and keyword.lower() not in headline_text.lower() and keyword.lower() not in content_text.lower():
            continue

        articles.append({
            "headline": headline_text,
            "date": date_text,
            "content": content_text,
            "link": link
        })

    if not articles:
        articles.append({"headline": "No articles found", "date": "", "content": "", "link": url})
    return articles

@app.route('/', methods=['GET', 'POST'])
def home():
    url = request.form.get('url')
    keyword = request.form.get('keyword')
    news = []
    if url:
        news = scrape_news(url, keyword)
    return render_template('index.html', news=news, url=url or '', keyword=keyword or '')

@app.route('/export', methods=['GET'])
def export_news():
    url = request.args.get('url')
    keyword = request.args.get('keyword')
    if not url:
        return jsonify({"message": "No URL provided"})
    news = scrape_news(url, keyword)
    df = pd.DataFrame(news)
    filename = f"news_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    return jsonify({"message": f"News exported to {filename}"})

if __name__ == "__main__":
    app.run(debug=True)
