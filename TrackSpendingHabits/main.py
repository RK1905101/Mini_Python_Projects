from expense_tracker import add_expense
from budget_manager import set_budget, view_budgets
from report_generator import generate_report

def main():
    while True:
        try:
            print("\n💡 Smart Budget Tracker")
            print("1. Add Expense")
            print("2. Set Budget")
            print("3. View Report")
            print("4. View Budgets")
            print("5. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                category = input("Category: ").strip()
                amount = float(input("Amount: ").strip())
                note = input("Note (optional): ").strip()
                add_expense(category, amount, note)

            elif choice == "2":
                category = input("Category to set budget for: ").strip()
                amount = float(input("Set budget amount: ").strip())
                set_budget(category, amount)

            elif choice == "3":
                generate_report()

            elif choice == "4":
                view_budgets()

            elif choice == "5":
                print("👋 Exiting Smart Budget Tracker. Stay financially smart!")
                break

            else:
                print("❌ Invalid option. Please enter 1-5.")

        except ValueError:
            print("⚠️ Please enter a valid numeric value for amount.")
        except KeyboardInterrupt:
            print("\n🛑 Program interrupted. Exiting gracefully.")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")

if __name__ == "__main__":
    main()

