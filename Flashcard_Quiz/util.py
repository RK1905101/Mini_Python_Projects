import json

def load_flashcards(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading flashcards: {e}")
        return []

def normalize(text):
    return text.strip().lower()