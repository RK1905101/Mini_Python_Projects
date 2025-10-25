# Company Scraper & Auto-Apply Bot

This project is a Python automation tool that scrapes company data from [Welcome to the Jungle](https://www.welcometothejungle.com/) and can automatically apply to jobs using Selenium. It collects company information, saves it to JSON and SQLite, and automates job applications with a personalized cover letter.

## Features

- **Scraping**: Collects company data (name, domain, location, website, offers, etc.) from the Tech sector.
- **Data Storage**: Saves data to both a JSON file and a SQLite database.
- **Filtering**: Filters companies by location, domain, and whether they accept spontaneous applications.
- **Auto-Apply**: Uses Selenium to log in and apply to filtered companies with a custom cover letter.
- **Logging**: Logs all actions and errors to a log file.
- **Application Tracking**: Keeps track of companies already applied to.

## Project Structure

```
.
├── data/
│   ├── applied           # List of companies already applied to
│   └── data.json         # Scraped company data in JSON format
├── log/
│   └── process.log       # Log file for scraping and application process
├── src/
│   ├── apply.py          # Script for automated job applications
│   ├── Companies.py      # Companies collection class
│   ├── Company.py        # Company data model and persistence
│   ├── functions.py      # Scraping and utility functions
│   ├── IDS.py            # Credentials and cover letter template
│   ├── main.py           # Main entry point for scraping
│   ├── SELECTORS.py      # CSS selectors and constants
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- Google Chrome (for Selenium)
- ChromeDriver (auto-managed)
- [pip](https://pip.pypa.io/en/stable/)

### Python Packages

Install dependencies with:

```sh
pip install selenium webdriver-manager beautifulsoup4
```

## Usage

### 1. Scrape Company Data (actually only tech sector)

Run the main scraper to collect company data:

```sh
python src/main.py
```
- This will create at at first `data` and `log` folders if they don't exist.
- Then will populate `data/data.json` and `data/data.db` with company information.

### 2. Auto-Apply to Companies

**Warning:** This will use your credentials (see `src/IDS.py`) to log in and apply to jobs.

```sh
python src/apply.py
```

- The script logs in, filters companies (e.g., Paris, Logiciels, spontaneous application), and applies with a generated cover letter.
- Applied companies are tracked in `data/applied` to avoid duplicates.

### 3. Configuration

- **Credentials**: Set your email and password in [`src/IDS.py`](src/IDS.py).
- **Selectors**: CSS selectors for scraping and applying are in [`src/SELECTORS.py`](src/SELECTORS.py).
- **Logging**: All logs are written to [`log/process.log`](log/process.log).

## Customization

- **Cover Letter**: Edit the `COVER_LETTER` function in [`src/IDS.py`](src/IDS.py) to personalize your message.
- **Filtering**: Change the filter logic in [`src/apply.py`](src/apply.py) to target different locations, domains, or application types.

## File Descriptions

- [`src/Company.py`](src/Company.py): Defines the `Company` class and methods for saving/loading data.
- [`src/Companies.py`](src/Companies.py): Manages a collection of `Company` objects.
- [`src/functions.py`](src/functions.py): Contains scraping, parsing, and Selenium utility functions.
- [`src/apply.py`](src/apply.py): Automates the application process.
- [`src/IDS.py`](src/IDS.py): Stores credentials and the cover letter template.
- [`src/SELECTORS.py`](src/SELECTORS.py): All CSS selectors and file path constants.

## Notes

- **Ethics**: Use this tool responsibly. Automated applications may violate terms of service of some websites.
- **Security**: Your credentials are stored in plain text in `src/IDS.py`. Do not share this file.
- **Maintenance**: If the website structure changes, update the selectors in `src/SELECTORS.py`.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.