import feedparser
from collections import Counter
import re

def fetch_news(feed_url, num_articles=5):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:num_articles]:
        articles.append({
            "title": entry.title,
            "summary": entry.summary if "summary" in entry else "",
            "link": entry.link
        })
    return articles

def summarize_text(text, num_sentences=2):
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) <= num_sentences:
        return text
    words = re.findall(r'\w+', text.lower())
    freq = Counter(words)
    ranked_sentences = sorted(
        sentences,
        key=lambda s: sum(freq.get(w.lower(), 0) for w in re.findall(r'\w+', s)),
        reverse=True
    )
    return ' '.join(ranked_sentences[:num_sentences])

if __name__ == "__main__":
    rss_url = "http://feeds.bbci.co.uk/news/rss.xml"
    articles = fetch_news(rss_url)

    for i, article in enumerate(articles, 1):
        print(f"Article {i}: {article['title']}")
        print(f"The News Summary: {article['summary'][:150]}...")
        print("Link:", article['link'])
        print("-" * 50)
