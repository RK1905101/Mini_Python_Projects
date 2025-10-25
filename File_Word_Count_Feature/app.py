from flask import Flask, render_template, request, send_file
import os
import re
from collections import Counter
import csv
from matplotlib import pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

stop_words = {"the", "and", "is", "a", "an", "in", "of", "to"}  # customizable

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        top_n = int(request.form.get("top_n", 10))
        ignore_stopwords = request.form.get("ignore_stopwords") == "on"

        if not file:
            return "No file uploaded", 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        # Word processing
        words = re.findall(r'\b\w+\b', text.lower())
        word_counts = Counter(words)

        if ignore_stopwords:
            word_counts = {w: c for w, c in word_counts.items() if w not in stop_words}

        top_words = dict(Counter(word_counts).most_common(top_n))

        # Visualization
        plt.figure(figsize=(10,5))
        plt.bar(top_words.keys(), top_words.values(), color='skyblue')
        plt.xticks(rotation=45)
        plt.tight_layout()
        img_path = os.path.join('static', 'chart.png')
        plt.savefig(img_path)
        plt.close()

        # Export CSV
        csv_path = os.path.join('uploads', 'word_counts.csv')
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Word", "Count"])
            for w, c in word_counts.items():
                writer.writerow([w, c])

        return render_template("result.html", word_counts=top_words, chart='chart.png', csv_file='word_counts.csv')

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join('uploads', filename), as_attachment=True)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
