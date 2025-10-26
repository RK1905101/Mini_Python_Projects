from datetime import datetime, timedelta
from storage import load_data

def check_remainders():
    today =  datetime.today().date()
    data = load_data()
    due_today = []

    for plant in data["plants"]:
        last_watered = datetime.strptime(plant["last_watered"],"%Y-%m-%d").date()
        next_due = last_watered + timedelta(days=plant["watering_interval_days"])

        if (today >= next_due):
            due_today.append(plant["name"])

    if due_today:
        print("\n🚿 Plants that need watering today:")
        for name in due_today:
            print(f"\n  - {name}")
    else:
        print("\n✨ All plants are well-watered today!")
