# 💡 Smart Budget Tracker (TrackSpendingHabits)

A simple yet powerful **Python mini project** that helps you **track expenses**, **set budgets**, and **get real-time warnings** for overspending.  
Perfect for Hacktoberfest and beginner Python contributors! 🚀  

---

## 📘 Features

✅ **Add Expenses** by category (e.g., Food, Essentials, Entertainment)  
✅ **Set Budgets** for each category  
✅ **Real-time Alerts** when nearing or exceeding your budget  
✅ **View Budget Reports** with spending breakdown  
✅ **Graceful Error Handling** for invalid input or interruptions  
✅ **Persistent Storage** using JSON (no database required)

---

## 🏗️ Project Structure



TrackSpendingHabits/
│
├── main.py # Entry point for the CLI app
├── expense_tracker.py # Handles adding & storing expenses
├── budget_manager.py # Manages category budgets
├── report_generator.py # Generates spending reports
└── data/
├── expenses.json # Stores daily expense records
└── budgets.json # Stores category budgets


---

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/PythonMiniProjects.git
   cd PythonMiniProjects/TrackSpendingHabits


Run the Program

python3 main.py


Enjoy Tracking Your Spending!

💻 Usage

Example CLI session:

💡 Smart Budget Tracker
1. Add Expense
2. Set Budget
3. View Report
4. View Budgets
5. Exit
Enter choice: 1
Category: Essentials
Amount: 20000
Note: Food expenses for the month
✅ Added ₹20000 to Essentials (Total spent: ₹20000)
⚠️ ALERT: You’re nearing your ₹20000 budget for Essentials! (20000/20000)

📊 Example Output

When you exceed your budget:

⚠️ WARNING: You’ve exceeded your ₹20000 budget for Essentials by ₹500!

🧠 How It Works

All data is stored locally in JSON files under the /data directory.

expense_tracker.py handles logging and computing totals.

budget_manager.py manages category limits and warnings.

The main CLI (main.py) orchestrates everything smoothly.

🛡️ Error Handling

Gracefully exits on Ctrl+C (KeyboardInterrupt).

Prevents crashes on invalid numeric inputs.

Automatically initializes missing JSON files.

🧰 Dependencies

No external dependencies required!
(Optional: Install colorama for colorful terminal output)

pip install colorama

🌟 Contribution Guidelines (for Hacktoberfest 🎃)

Fork this repository 🍴

Create a new branch:

git checkout -b feature/add-your-feature


Add your changes or improvements

Commit and push:

git commit -m "Added <your feature>"
git push origin feature/add-your-feature


Create a Pull Request and wait for review ✅

💬 Ideas for Contributors

Add color-coded CLI using colorama

Add charts or graphs in report_generator.py

Add monthly summary export as CSV

Add login system for multiple users

📜 License

This project is open-source and available under the MIT License.