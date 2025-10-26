# Expense Splitter

**Expense Splitter** is a Python CLI tool to track group expenses, calculate who owes whom, and generate clear summaries for easy sharing among friends or roommates. It leverages `rich` for pretty terminal tables and `tabulate` for shareable text summaries.

---

## Features

- Add participants interactively
- Add expenses and split them among participants
- Calculate net balances
- Generate settlement plan (who pays whom)
- Rich console output and shareable tables

---

## Setup

### 1. Clone or download the project
```bash
git clone https://github.com/RK1905101/Mini_Python_Projects.git
cd Mini_Python_Projects/Expense_Tracker
````

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

* **Linux / macOS**

```bash
source .venv/bin/activate
```

* **Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Run the CLI

```bash
python cli.py
```

### 2. Follow interactive prompts

* Enter participant names.
* Enter expenses:

  * Who paid
  * Amount
  * Description
  * Split between which participants

The CLI will then:

* Show net balances for all participants using `rich`
* Generate a settlement plan showing who owes whom
* Provide a shareable text summary using `tabulate`

### 3. Optional demo mode

You can also run a preloaded demo with:

```bash
python demo.py
```


## File Structure

```
Expense_Tracker/
├── cli.py           # Interactive CLI
├── ledger.py        # Core logic for balance computation
├── models.py        # Data models (Participant, Expense, Settlement)
├── reports.py       # Display & summary functions
├── requirements.txt # Python dependencies
├── __init__.py      # empty (optional)
```

---

## Dependencies

* Python 3.10+
* `rich`
* `tabulate`
