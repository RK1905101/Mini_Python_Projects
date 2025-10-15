from plyer import notification
import schedule
import time

# 📝 Get user input
title = input("Enter title: ")
message = input("Enter message: ")
repeat = input("Repeat every (day/hour/minute)? ").lower()
count_limit = int(input("How many times should the notification be sent? "))

# 🕒 If daily, ask for specific time
if repeat == "day":
    time_str = input("Enter time (HH:MM): ")

# 🔔 Notification function with counter
count = 0
def show_notification():
    global count
    if count < count_limit:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
        count += 1
    else:
        schedule.clear()
        print("✅ Notification sent", count_limit, "times. Scheduler stopped.")

# 📆 Schedule based on repeat type
if repeat == "day":
    schedule.every().day.at(time_str).do(show_notification)
elif repeat == "hour":
    schedule.every().hour.do(show_notification)
elif repeat == "minute":
    schedule.every().minute.do(show_notification)
else:
    print("❌ Invalid repeat option. Please choose day, hour, or minute.")
    exit()

# 🔁 Run the scheduler loop
print(f"✅ Notification scheduled: {title} → {message} ({repeat}, {count_limit} times)")
while True:
    schedule.run_pending()
    time.sleep(1)