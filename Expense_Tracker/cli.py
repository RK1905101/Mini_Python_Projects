from decimal import Decimal, InvalidOperation
from typing import List
from models import Participant, Expense
from ledger import Ledger
from reports import print_balances, print_settlements, text_summary
from storage import JsonStorage

DATA_FILE = "data.json"

def load_data():
    storage = JsonStorage(DATA_FILE)
    raw = storage.load()
    participants = [Participant(**p) for p in raw.get("participants", [])]
    expenses = [Expense(**e) for e in raw.get("expenses", [])]
    return participants, expenses, storage

def save_data(participants: List[Participant], expenses: List[Expense], storage: JsonStorage):
    storage.save({
        "participants": [p.__dict__ for p in participants],
        "expenses": [e.__dict__ for e in expenses]
    })

def choose_participant(participants: List[Participant], prompt: str) -> Participant:
    print("\nParticipants:")
    for idx, p in enumerate(participants, start=1):
        print(f"{idx}. {p.name}")
    while True:
        choice = input(prompt)
        if choice.isdigit() and 1 <= int(choice) <= len(participants):
            return participants[int(choice) - 1]
        else:
            print("Invalid choice, try again.")

def add_participant(participants: List[Participant]):
    name = input("Enter participant name: ").strip()
    if name:
        p = Participant(name=name)
        participants.append(p)
        print(f"Added participant: {name}")
    else:
        print("Name cannot be empty.")

def add_expense(participants: List[Participant], expenses: List[Expense]):
    if not participants:
        print("No participants yet. Add participants first.")
        return

    payer = choose_participant(participants, "Select the payer number: ")

    while True:
        amt_str = input("Enter amount: ").strip()
        try:
            amount = Decimal(amt_str)
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except InvalidOperation:
            print("Invalid number. Try again.")

    description = input("Enter description (optional): ").strip()

    print("\nSplit between participants (comma-separated numbers):")
    for idx, p in enumerate(participants, start=1):
        print(f"{idx}. {p.name}")

    while True:
        split_input = input("Enter numbers: ").strip()
        try:
            indices = [int(i)-1 for i in split_input.split(",")]
            split_ids = [participants[i].id for i in indices if 0 <= i < len(participants)]
            if not split_ids:
                print("Must select at least one participant.")
                continue
            break
        except ValueError:
            print("Invalid input. Use comma-separated numbers.")
    
    expense = Expense(
        payer_id=payer.id,
        amount=amount,
        currency="USD",
        split_between=split_ids,
        description=description
    )
    expenses.append(expense)
    print(f"Added expense: {amount} by {payer.name} for {description or 'No description'}")

def show_balances(ledger: Ledger):
    balances = ledger.compute_balances()
    print_balances(ledger.participants, balances)
    print("\nShareable summary:")
    print(text_summary(ledger.participants, balances))

def show_settlements(ledger: Ledger):
    settlements = ledger.settle_debts_greedy()
    if not settlements:
        print("All balances are settled.")
    else:
        print_settlements(settlements, ledger.participants)

def main():
    participants, expenses, storage = load_data()
    ledger = Ledger(participants, expenses)

    menu = """
Expense Splitter Menu:
1. Add participant
2. Add expense
3. Show balances
4. Show settlement plan
5. Exit
"""

    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_participant(participants)
            save_data(participants, expenses, storage)
        elif choice == "2":
            add_expense(participants, expenses)
            save_data(participants, expenses, storage)
        elif choice == "3":
            show_balances(ledger)
        elif choice == "4":
            show_settlements(ledger)
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
