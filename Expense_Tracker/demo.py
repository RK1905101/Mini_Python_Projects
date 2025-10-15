import argparse
from decimal import Decimal
from models import Participant, Expense
from ledger import Ledger
from reports import print_balances, print_settlements, text_summary
from storage import JsonStorage

def demo_data():
    # quick demo participants + expenses
    a = Participant(name="Alice")
    b = Participant(name="Bob")
    c = Participant(name="Carol")
    exp1 = Expense(payer_id=a.id, amount=Decimal("120.00"), currency="USD", split_between=[a.id,b.id,c.id], description="Groceries")
    exp2 = Expense(payer_id=b.id, amount=Decimal("45.00"), currency="USD", split_between=[a.id,b.id], description="Taxi")
    return [a,b,c], [exp1, exp2]

def main():
    parser = argparse.ArgumentParser(prog="expense_splitter", description="Keep group expenses tidy.")
    parser.add_argument("--demo", action="store_true", help="run demo dataset")
    args = parser.parse_args()

    if args.demo:
        participants, expenses = demo_data()
        ledger = Ledger(participants, expenses)
        balances = ledger.compute_balances()
        print_balances(participants, balances)
        settlements = ledger.settle_debts_greedy()
        print_settlements(settlements, participants)
        print("\nText summary (shareable):")
        print(text_summary(participants, balances))
    else:
        print("Run with --demo to see a working example.")

if __name__ == "__main__":
    main()
