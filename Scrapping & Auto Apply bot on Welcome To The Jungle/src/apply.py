from datetime import datetime

import json
import IDS
from CONST import *
from functions import *
from SELECTORS import *

# Function to add a company name to a file (applied or ignored)
def add_companies_in_file(file, company_name):
    exist_data = get_companies_list(file) if get_companies_list(file) else []

    with open(file, "w", encoding="utf-8") as f:
        if company_name not in exist_data:
            exist_data.append(company_name)

        json.dump(exist_data , f, indent=4, ensure_ascii=False)

# Function to get the list of companies from a file (applied or ignored)
def get_companies_list(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, UnicodeDecodeError):
        # If the file does not exist, create it and return an empty list
        logger.warning(f"File {file} not found or cannot be read. Creating a new file.")
        try:
            with open(file, "w") as f:
                json.dump([], f)
        except Exception as e:
            logger.error(f"An error occurred while creating the file {file}: {e}")
    with open(file, "w") as f:
        return []

# Function to write the cover letter to the input field
def write_cover_letter(element, company):
    try:
        element.clear()
        element.send_keys(IDS.COVER_LETTER(
            date=datetime.today().strftime("%d/%m/%Y"), # Current date
            name=company.name, # Company name
            avgAge=int(company.avg_age) if company.avg_age else 28  # Default to 28 if avg_age is not a valid number
        ))
        logger.info(f"Cover letter written for {company.name}.")
        return True
    except Exception as e:
        logger.error(f"Error writing cover letter for {company.name}: {e}")
        return False

# Function to connect to the application
def connect(driver):
    get_url(driver, LOGIN_URL)

    # Find email input field and write it
    email_input = find_element(driver, 18)
    if not email_input:
        logger.error("Email input field not found.")
        driver.quit()
        exit(1)
    email_input.send_keys(IDS.MAIL)

    # Write password
    password_input = find_element(driver, 19)
    if not password_input:
        logger.error("Password input field not found.")
        driver.quit()
        exit(1)
    password_input.send_keys(IDS.PASSWORD)

    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, CSS_SELECTORS[17]).click()

# Function to apply to a company
def apply_to_company(driver,company):

    link = company.url_wtj 
    job_link = urljoin(link.split("?")[0]+'/', "jobs")
    get_url(driver, job_link)

    # Wait for the page to load and find the applying button to click
    steps = [
        (find_and_click, 20, "Failed to click applying button"), # Applying button
        (lambda d, c: write_cover_letter(find_element(d, 21), c), None, "Failed to write cover letter"), # Cover letter
        (find_and_click, 22, "Failed to click submit button"), # Submit button
        (find_and_click, 23, "Failed to click confirmation button"), # Confirmation button
        (find_and_click, 25, "Failed to finalize application"), # Finalize application
    ]

    # Execute each step in the process
    for func, selector, error_msg in steps:
        if func == find_and_click:
            if not func(driver, selector, company.name):
                logger.error(f"{error_msg} for {company.name}.")
                return False
        else:
            if not func(driver, company):
                logger.error(f"{error_msg} for {company.name}.")
                return False

    logger.info(f"Application successfully submitted for {company.name}.")
    return True

if __name__ == "__main__":

    # Initialize the WebDriver
    driver = init_driver()

    # Connect to the application
    connect(driver)

    # Get all companies from the JSON file and filter them
    cps = Companies([])
    
    # data = cps.get_companies_from_json(JSON_FILE).companies
    data = cps.get_companies_from_sqlite(DB_FILE).companies
    if not data:
        logger.error("No companies found in the DB file.")
        exit(1)

    # Get the list of applied and ignored companies
    applied_companies = get_companies_list(APPLIED)
    ignored_companies = get_companies_list(IGNORED)

    # Filter companies based on location, spontaneity, and domain
    filtered_companies = [c for c in data if c.spontane == "Yes"
                            and c.name not in applied_companies + ignored_companies]
    
    print(len(filtered_companies))
    # Check if there are companies to apply to
    if not filtered_companies:
        logger.info("No companies found to apply to.")
        driver.quit()
        exit(0)

    # Apply to each company
    for company in filtered_companies:
        # # Apply to the company and check for success
        if not apply_to_company(driver, company):
            add_companies_in_file(IGNORED, company.name)
            logger.info(f"Application failed for {company.name}.")
            print(f"Application failed for {company.name}.")
        else:
            add_companies_in_file(APPLIED, company.name)
            logger.info(f"Application succeeded for {company.name}.")
            print(f"Application succeeded for {company.name}.")

    driver.quit()
    # End of the script
