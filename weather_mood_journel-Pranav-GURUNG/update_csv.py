import csv
import os

old_file = "mood_journal.csv"
new_file = "mood_journal_new.csv"

with open(old_file, "r", newline="") as infile, open(new_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
 
    fieldnames = ["timestamp", "user", "date", "weather", "mood", "notes", "sentiment"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row["user"] = "default_user" 
        writer.writerow(row)

os.replace(new_file, old_file)

print("CSV updated successfully with 'user' column!")
