from functions import *
from IDS import *
from SELECTORS import *
from CONST import *
from apply import *

def main():
    """
    Main function to scrape company data and save it to SQLite and JSON files.
    """
    # Flags to track connection and saving status
    connected = False
    saved = False

    # Retrieve existing companies from the database
    companies = Companies([])
    try:
        existing_companies_names = [comp.name for comp in companies.companies]
    except Exception as e:
        logger.error(f"Error retrieving existing companies: {e}")
        existing_companies_names = []
        
    logger.info("Starting the company scraping process...")
    driver = init_driver()
    if not driver:
        # If driver initialization fails, log the error and exit
        logger.error("Failed to initialize the web driver. Exiting.")
        exit(1)

    get_url(driver, COMPANIES_URL)
    time.sleep(2)
    find_and_click(driver, 1, "SECTOR")
    find_and_click(driver, 3, "TECH")
    find_and_click(driver, 4, "SEARCH BUTTON")

    # You can comment the the five previous lines and uncomment the following line to skip directly to a specific page
    # get_url(driver, MAIN_TECH_PAGE_URL) # or you can use any other page url
    # time.sleep(2)
    page = driver.current_url
    number_of_pages = get_number_of_pages(driver, page)
    all_pages = get_all_pages_url(page, number_of_pages)
    try:
        for page in all_pages:
            logger.info(f"Processing page: {page}")
            blocks = get_companys_blocks(driver, page)
            for block in blocks:
                infos = get_companys_infos(driver, block, existing_companies_names)
                if infos:
                    company = construct_company_object(infos)
                    companies.companies.append(company)
                    existing_companies_names.append(company.name)
                    # Option to apply to the company
                    # Uncomment the following lines to enable application functionality and add the filter conditions you need
                    # try:
                        #Filter conditions for applying to a company
                    #     if company.spontane == "Oui" and "Paris" in company.location:
                    #         if not connected:
                    #             driver_for_apply = init_driver()
                    #             if not driver_for_apply:
                    #                 logger.error("Failed to initialize the web driver for application. Skipping application process.")
                    #                 continue
                    #             connect(driver_for_apply)
                    #             connected = True
                    #         applied_companies = get_companies_list(APPLIED)
                    #         ignored_companies = get_companies_list(IGNORED)
                    #         if company.name not in applied_companies + ignored_companies:
                    #             apply_to_company(driver_for_apply, company)
                    # except Exception as e:
                    #     logger.error(f"An error occurred while applying to {company.name}: {e}")
                    #     continue
    except KeyboardInterrupt as e:
        if len(companies.companies) > 0:
            logger.info(f"Total companies found: {len(companies.companies)}")
            # Save the companies data to SQLite and JSON files
            try:
                companies.save_companies_to_sqlite(DB_FILE)
                companies.save_companies_to_json(JSON_FILE)
                logger.info(f"Companies data saved to {DB_FILE} and {JSON_FILE}")
                saved = True
            except (FileExistsError, FileNotFoundError) as e:
                logger.error(f"Error saving companies data to files: {DB_FILE} or {JSON_FILE}. Please check the file paths.")
            except Exception as e:
                logger.error(f"An unexpected error occurred while saving companies data: {e}")
            if not saved:
                logger.error("Saved companies data to defines files failed. Saving it in othet files data.db and data.json")
                companies.save_companies_to_sqlite("data.db")
                companies.save_companies_to_json("data.json")
        else:
            logger.info("No companies found to save.")

    driver.quit()
    logger.info("Company scraping process completed successfully.")

if __name__ == "__main__":
    # import os
    # os.makedirs("log", exist_ok=True)
    # os.makedirs("data", exist_ok=True)
    # main()
    cps = Companies([])
    existing_companies = cps.get_companies_from_json(JSON_FILE)
    existing_companies.save_companies_to_sqlite(DB_FILE)
