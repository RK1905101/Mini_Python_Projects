import json
from collections import defaultdict
import matplotlib.pyplot as plt
import os

def generate_report():
    if not os.path.exists("data/expenses.json"):
        print("⚠️ No expense data found!")
        return

    with open("data/expenses.json", "r") as f:
        expenses = json.load(f)

    category_totals = defaultdict(float)
    for day in expenses.values():
        for e in day:
            category_totals[e["category"]] += e["amount"]

    if not category_totals:
        print("⚠️ No expenses recorded yet!")
        return

    print("\n📊 Expense Report:")
    for cat, total in category_totals.items():
        print(f" - {cat}: ₹{total}")

    plt.figure(figsize=(6, 6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
    plt.title("Spending by Category")

    os.makedirs("data", exist_ok=True)
    plt.savefig("data/spending_report.png")
    print("✅ Report saved as data/spending_report.png")
