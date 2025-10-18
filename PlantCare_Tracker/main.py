from plant_manager import add_plant, mark_watered, add_note, view_plants
from reminder import check_remainders

def main():
    while True:
        print("\n=== 🌱 Plant Care Tracker ===")
        print("1. Add new plant")
        print("2. View all plants")
        print("3. Mark plant as watered")
        print("4. Add growth note")
        print("5. Check watering reminders")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            name = input("\nEnter plant name: ")
            interval = int(input("\nEnter watering interval(in days): "))
            add_plant(name, interval)
        elif choice == "2":
            view_plants()
        elif choice == "3":
            name =  input("\nEnter plant name: ")
            mark_watered(name)
        elif choice == "4":
            name = input("\nEnter plant name: ")
            note = input("\nEnter note: ")
            add_note(name, note)
        elif choice == "5":
            check_remainders()
        elif choice == "6":
            print("\n👋 Goodbye! Keep your plants happy!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
