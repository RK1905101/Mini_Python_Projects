# Zetamac Solver

An automated solver for Zetamac arithmetic problems using Selenium WebDriver. This tool automatically solves math problems on the Zetamac website (https://arithmetic.zetamac.com/) by parsing the problems, calculating the answers, and submitting them.

## Requirements

- Python 3.7+
- Chrome browser installed
- ChromeDriver (automatically managed by Selenium)

## Installation

1. Clone this repository

2. Create a virtual environment:
```bash
cd ZetamacSolver
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirement.txt
```

## Notes

- The solver waits 2 minutes after completion before automatically closing the browser
- Make sure you have a stable internet connection
- Chrome browser must be installed for the WebDriver to work
