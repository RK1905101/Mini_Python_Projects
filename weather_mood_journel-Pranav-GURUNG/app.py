from flask import Flask, request, jsonify
import csv
from datetime import datetime
import os
import random

from db import MOOD_MAP

app = Flask(__name__)

CSV_FILE = "mood_journal.csv"

# Initialize CSV with headers if not present
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "date", "weather", "mood"])


@app.route("/log", methods=["POST"])
def log_mood():
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    date = data.get("date")
    weather = data.get("weather")
    mood = data.get("mood")

    if not date or not weather:
        return jsonify({"error": "Fields 'date' and 'weather' are required"}), 400

  
    if not mood:
        mood_options = MOOD_MAP.get(weather, MOOD_MAP["Undefined"])
        mood = random.choice(mood_options)


    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), date, weather, mood])

    return jsonify({
        "message": "Mood entry logged successfully",
        "weather": weather,
        "mood": mood
    }), 201


@app.route("/entries", methods=["GET"])
def get_entries():
   
    entries = []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return jsonify(entries), 200


@app.route("/analytics", methods=["GET"])
def analytics():
    
    weather_count = {}
    mood_count = {}

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            weather = row["weather"]
            mood = row["mood"]
            weather_count[weather] = weather_count.get(weather, 0) + 1
            mood_count[mood] = mood_count.get(mood, 0) + 1

    return jsonify({
        "weather_summary": weather_count,
        "mood_summary": mood_count
    }), 200


@app.route("/moods", methods=["GET"])
def get_weather_moods():
    
    weather = request.args.get("weather")
    if not weather:
        return jsonify({"error": "Missing 'weather' query parameter"}), 400

    moods = MOOD_MAP.get(weather, MOOD_MAP["Undefined"])
    return jsonify({"weather": weather, "suggested_moods": moods}), 200

@app.route("/update/<timestamp>", methods=["PUT"])
def update_entry(timestamp):
    """
    Update an entry by its timestamp.
    JSON body can include any of: date, weather, mood, notes
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    updated = False
    all_entries = []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["timestamp"] == timestamp:
                # Update fields
                row["date"] = data.get("date", row["date"])
                row["weather"] = data.get("weather", row["weather"])
                row["mood"] = data.get("mood", row["mood"])
                row["notes"] = data.get("notes", row["notes"])
                # Recalculate sentiment if notes changed
                row["sentiment"] = analyze_sentiment(row["notes"])
                updated = True
            all_entries.append(row)

    if not updated:
        return jsonify({"error": "Entry not found"}), 404

    # Rewrite CSV
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_entries[0].keys())
        writer.writeheader()
        writer.writerows(all_entries)

    return jsonify({"message": "Entry updated successfully"}), 200


@app.route("/delete/<timestamp>", methods=["DELETE"])
def delete_entry(timestamp):
    """
    Delete an entry by its timestamp
    """
    deleted = False
    all_entries = []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["timestamp"] == timestamp:
                deleted = True
                continue
            all_entries.append(row)

    if not deleted:
        return jsonify({"error": "Entry not found"}), 404

    # Rewrite CSV
    if all_entries:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_entries[0].keys())
            writer.writeheader()
            writer.writerows(all_entries)
    else:
        # If no entries left, recreate header
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "date", "weather", "mood", "notes", "sentiment"])

    return jsonify({"message": "Entry deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
