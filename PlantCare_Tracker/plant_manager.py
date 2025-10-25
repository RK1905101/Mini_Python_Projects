from datetime import datetime
from storage import load_data, save_data

def add_plant(name, interval_days):
    data = load_data()
    new_plant = {
        "name": name,
        "watering_interval_days": interval_days,
        "last_watered": str(datetime.today().date()),
        "notes": []
    }
    data["plants"].append(new_plant)
    save_data(data)
    print(f"\n✅ Added {name} with watering interval {interval_days} days.")

def mark_watered(name):
    data =  load_data()
    for plant in data["plants"]:
        if plant["name"].lower() == name.lower():
            plant["last_watered"] = str(datetime.today().date())
            save_data(data)
            print(f"\n💧 Updated watering date for {name}.")
            return
    print("\n❌ Plant not found.")


def add_note(name, note):
    data = load_data()
    for plant in data["plants"]:
        if plant["name"].lower() == name.lower():
            plant["notes"].append({
                "note": note,
                "date": str(datetime.today().date())
            })
            save_data(data)
            print(f"\n📝 Added note for {name}.")
            return
    print("\n❌ Plant not found.")

def view_plants():
    data = load_data()
    if not data["plants"]:
        print("\n🌼 No plants added yet.")
        return
    for p in data["plants"]:
        print(f"\n🌿 {p['name']} | Last Watered: {p['last_watered']} | Interval: {p['watering_interval_days']} days")
        if p["notes"]:
            print("\n    Notes:")
            for n in p["notes"]:
                print(f"\n    - {n['note']} ({n['date']})")



