import json
import os

DATA_FILE = "data/plants.json"

def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        os.makedirs("data", exist_ok = True)
        with open(DATA_FILE, "w") as f:
            json.dump({"plants": []}, f)
    
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
