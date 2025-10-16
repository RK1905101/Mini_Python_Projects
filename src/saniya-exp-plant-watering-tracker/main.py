import pandas as pd
from datetime import datetime, timedelta
import os
import time

# 🌱 Welcome Message
print("🌷🌸🌿 Welcome to the Virtual Plant Watering Tracker & Reminder! 🌿🌸🌷")
print("-------------------------------------------------------------")
print("🌞 Let's keep your plants happy, hydrated, and blooming! 💧🪴\n")

# 📊 Read the CSV
data = pd.read_csv("plants.csv")
data['last_watered'] = pd.to_datetime(data['last_watered'])
if 'notes' not in data.columns:
    data['notes'] = ""

# 🪴 Helper functions
def show_all_plants():
    print("\n📋 Your Current Garden Overview:")
    print(data.to_string(index=False))
    print("-------------------------------------------------------------\n")

def check_reminders():
    today = datetime.now().date()
    print("\n💧 Checking which plants need watering today...\n")
    time.sleep(1)
    due_plants = []
    for _, row in data.iterrows():
        next_due = row['last_watered'].date() + timedelta(days=row['water_interval_days'])
        if today >= next_due:
            due_plants.append((row['plant_name'], next_due))
    if due_plants:
        print("🌿 These plants need watering today 🌿:\n")
        for name, next_due in due_plants:
            print(f"🌸 {name} — was due on {next_due}")
    else:
        print("✅ Great job! All your plants are well-watered and happy! 🪴💦")
    print("\n-------------------------------------------------------------\n")

def update_watered():
    print("\n🪻 Time to refresh your plants! 🪻")
    print("🌼 Available plants:", ", ".join(data['plant_name']))
    plants_input = input("💧 Enter the names of plants you watered today (comma separated): ")
    watered = [p.strip().capitalize() for p in plants_input.split(",")]
    today = datetime.now()
    found_any = False
    for name in watered:
        if name in list(data['plant_name']):
            data.loc[data['plant_name'] == name, 'last_watered'] = today
            print(f"💦 Watered {name}! Updated successfully.")
            found_any = True
        else:
            print(f"⚠️ Plant '{name}' not found in your garden. Maybe check spelling?")
    if found_any:
        data.to_csv("plants.csv", index=False)
        print("✅ All updates saved successfully!\n")
    print("-------------------------------------------------------------\n")

def add_new_plant():
    print("\n🌱 Let's add a new plant to your garden! 🌱")
    name = input("🪴 Enter the plant name: ").capitalize()
    try:
        interval = int(input("📅 Enter watering interval (in days): "))
        today = datetime.now().strftime("%Y-%m-%d")
        new_entry = pd.DataFrame([[name, today, interval, ""]], columns=data.columns)
        updated = pd.concat([data, new_entry], ignore_index=True)
        updated.to_csv("plants.csv", index=False)
        print(f"🌼 Successfully added {name} to your garden! 💚")
    except ValueError:
        print("⚠️ Invalid input! Please enter a number for interval.")
    print("-------------------------------------------------------------\n")

def show_next_due():
    print("\n📆 Checking next watering dates for all your plants...\n")
    time.sleep(1)
    for _, row in data.iterrows():
        next_due = row['last_watered'].date() + timedelta(days=row['water_interval_days'])
        print(f"🌺 {row['plant_name']} → Next watering due on {next_due}")
    print("\n-------------------------------------------------------------\n")

def add_growth_notes():
    print("\n📝 Add Growth Notes for Your Plants")
    print("🌱 Available plants:", ", ".join(data['plant_name']))
    plant_input = input("💧 Enter the plant name: ").capitalize()
    if plant_input in list(data['plant_name']):
        note = input("✍️ Enter your growth note: ")
        if pd.isna(data.loc[data['plant_name'] == plant_input, 'notes']).all():
            data.loc[data['plant_name'] == plant_input, 'notes'] = note
        else:
            data.loc[data['plant_name'] == plant_input, 'notes'] += " | " + note
        data.to_csv("plants.csv", index=False)
        print(f"✅ Note added for {plant_input} successfully!\n")
    else:
        print(f"⚠️ Plant '{plant_input}' not found!")
    print("-------------------------------------------------------------\n")

# 🌿 Main interactive loop
while True:
    print("🌻 What would you like to do?")
    print("1️⃣  💧 Check watering reminders")
    print("2️⃣  🪴 Update watered plants")
    print("3️⃣  🌱 Add a new plant")
    print("4️⃣  📊 View all plants")
    print("5️⃣  📆 See next watering dates")
    print("6️⃣  📝 Add growth notes")
    print("7️⃣  🚪 Exit\n")

    choice = input("👉 Enter your choice (1-7): ").strip()

    if choice == "1":
        check_reminders()
    elif choice == "2":
        update_watered()
    elif choice == "3":
        add_new_plant()
    elif choice == "4":
        show_all_plants()
    elif choice == "5":
        show_next_due()
    elif choice == "6":
        add_growth_notes()
    elif choice == "7":
        print("\n👋 Goodbye, Plant Parent! 🌼")
        print("💧 Keep nurturing your green friends with love. 🌿✨")
        print("-------------------------------------------------------------\n")
        break
    else:
        print("⚠️ Oops! Invalid choice. Try again please.\n")

       
