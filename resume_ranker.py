import os
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def read_text_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def calculate_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)  # percentage match

def main():
    parser = argparse.ArgumentParser(description="AI Resume Ranker")
    parser.add_argument('--resume', required=True, help="Path to resume file (.txt or .pdf)")
    parser.add_argument('--jd', required=True, help="Path to job description (.txt)")

    args = parser.parse_args()

    resume_path = args.resume
    jd_path = args.jd

    # Load resume
    if resume_path.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.lower().endswith(".txt"):
        resume_text = read_text_file(resume_path)
    else:
        print("Unsupported resume file type. Use .pdf or .txt")
        return

    # Load job description
    jd_text = read_text_file(jd_path)

    if not resume_text.strip() or not jd_text.strip():
        print("Both resume and job description must contain text.")
        return

    score = calculate_similarity(resume_text, jd_text)
    print(f"\n🔍 Resume Match Score: {score}%")

    if score > 80:
        print("✅ Strong match! Consider applying.")
    elif score > 60:
        print("⚠️ Decent match. Tailoring may help.")
    else:
        print("❌ Low match. Consider improving the resume.")

if __name__ == "__main__":
    main()
