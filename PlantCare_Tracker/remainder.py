def check_remainders():
    today =  datatime.today().date()
    data = load_data()
    due_today = []

    for plant in data["plants"]:
        last_watered = datetime.strptime(plant["last_watered"],"%Y-%m-%d").date()
        next_due = last_watered + timedelta(plant["watering_interval_days"])

        if (today >= next_due):
            due_today.append(plant["name"])

    if due_today:
        print("🚿 Plants that need watering today:")
        for name in due_today:
            print(f" - {name}")
    else:
        print("✨ All plants are well-watered today!")
