from expense_tracker import load_budgets, save_budgets

def set_budget(category, amount):
    budgets = load_budgets()
    budgets[category] = amount
    save_budgets(budgets)
    print(f"✅ Budget for '{category}' set to ₹{amount}")

def view_budgets():
    budgets = load_budgets()
    if not budgets:
        print("📭 No budgets set yet.")
        return
    print("\n📊 Current Budgets:")
    for cat, amt in budgets.items():
        print(f" - {cat}: ₹{amt}")

