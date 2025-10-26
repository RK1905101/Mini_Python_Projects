import json
import os
from datetime import date

EXPENSE_FILE = "data/expenses.json"
BUDGET_FILE = "data/budgets.json"

# ------------------ Utility Functions ------------------

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except json.JSONDecodeError:
        return {}

def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ Expense Functions ------------------

def load_expenses():
    return load_json(EXPENSE_FILE)

def save_expenses(expenses):
    save_json(EXPENSE_FILE, expenses)

def load_budgets():
    return load_json(BUDGET_FILE)

def save_budgets(budgets):
    save_json(BUDGET_FILE, budgets)

def add_expense(category, amount, note=""):
    expenses = load_expenses()
    budgets = load_budgets()
    today = str(date.today())

    if today not in expenses:
        expenses[today] = []

    expenses[today].append({
        "category": category,
        "amount": amount,
        "note": note
    })

    save_expenses(expenses)

    # Compute total spent in this category
    total_spent = sum(
        e["amount"]
        for day in expenses.values()
        for e in day
        if e["category"] == category
    )

    print(f"✅ Added ₹{amount} to {category} (Total spent: ₹{total_spent})")

    # Check for budget overspending
    if category in budgets:
        limit = budgets[category]
        if total_spent > limit:
            print(f"⚠️ WARNING: You’ve exceeded your ₹{limit} budget for {category} by ₹{total_spent - limit}!")
        elif total_spent > 0.9 * limit:
            print(f"⚠️ ALERT: You’re nearing your ₹{limit} budget for {category}! ({total_spent}/{limit})")

    return total_spent



