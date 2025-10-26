import cv2
import pytesseract
import numpy as np
import re
import webbrowser

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    return eroded

def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = ' '.join(text.split())
    return text

def extract_text_from_image(img):
    preprocessed_img = preprocess_image(img)
    text = pytesseract.image_to_string(preprocessed_img, config='--psm 3')
    cleaned_text = clean_text(text)
    return cleaned_text


def main(input_image_path, output_text_path):
    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError("Image not found")
    extracted_text = extract_text_from_image(img)
    search_query(extracted_text)

def search_query(text):
    query = text.replace(' ', '+')  # Format the query for URL
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)