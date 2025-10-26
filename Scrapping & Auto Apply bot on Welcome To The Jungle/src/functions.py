# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
import logging

from SELECTORS import *
from CONST import *
from Company import Company
from Companies import Companies

# Logger setup
def setup_logger():
    """
    Set up and return a logger instance.
    """
    try:
        logging.basicConfig(
            filemode='a',
            filename=LOGGING_FILE,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
        )
    except FileNotFoundError:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
        )
    return logging.getLogger(__name__)

logger = setup_logger()

def init_driver( opt = ""):
    """
    Initialize and return a Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    try:
        if opt == "a":
            return webdriver.Firefox()
        return webdriver.Chrome()
    except Exception as e:
        logger.error(f"ERROR INITIALIZING THE WEBDRIVER, message : {e}")
        return None

def get_url(driver, url):
    """
    Load a URL with the WebDriver.
    """
    try:
        driver.get(url)
    except Exception as e:
        logger.error(f"ERROR TRYING TO GET URL, CHECK YOUR URL : {e}")

def find_element(driver, selectors_key, name="", number="one", timeout=10):
    """
    Find element(s) by CSS selector with wait.
    """
    try:
        if number == "one":
            logger.info(f"Finding {name} element with selector: {CSS_SELECTORS[selectors_key]}")
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTORS[selectors_key]))
            )
        else:
            logger.info(f"Finding {name} elements with selector: {CSS_SELECTORS[selectors_key]}")
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, CSS_SELECTORS[selectors_key]))
            )
    except Exception as e:
        logger.error(f"ERROR FINDING ELEMENT, : {e}")
        return None

def click_on_element(driver, element, name=""):
    """
    Click an element using JavaScript.
    """
    try:
        time.sleep(3)
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        logger.error(f"CLICK ON THE ELEMENT : {name} field. Message : {e}")
        return False

def find_and_click(driver, selectors_key, name="", number="one", timeout=10):
    """
    Find and click an element by selector.
    """
    element = find_element(driver, selectors_key, name, number, timeout)
    if element:
        return click_on_element(driver, element, name)
    else:
        logger.error(f"Element [{name}] not found.")
        return False

def get_number_of_pages(driver, url, timeout=15):
    """
    Return the number of pages for pagination.
    """
    driver.get(url)
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, CSS_SELECTORS[5]))
        )
        li_items = find_element(driver, 6, "pagination", "all", timeout)
        page_numbers = []
        for li in li_items:
            try:
                a_tag = li.find_element(By.TAG_NAME, "a")
                text = a_tag.text.strip()
                if text.isdigit():
                    page_numbers.append(int(text))
            except:
                continue
        if page_numbers:
            return max(page_numbers)
        return None
    except Exception as e:
        logger.error(f"[!] Error retrieving pagination: {e}")
        return None

def get_all_pages_url(main_url, number_of_pages):
    """
    Build URLs for all pages.
    """
    all_pages = [main_url]
    all_pages.extend([main_url.replace(f"page=1", f"page={i+1}") for i in range(1, number_of_pages)])
    return all_pages

def construct_company_object(infos):
    """
    Build a Company object from a dict.
    """
    try:
        name = infos.get("Name", None)
        url_vitrine = infos.get("Link", None)
        url_web_site = infos.get("Web Site", None)
        domain = infos.get("Domain", None)
        location = infos.get("Location", None)
        number_salaries = infos.get("Collaborateurs", None)
        average_age = infos.get("Âge moyen", None)
        offers = infos.get("Offer", None)
        all_offers = infos.get("Offres", [])
        spontaneous_application = infos.get("Candidature spontanée", "Non")

        return Company(
            name,
            url_vitrine,
            url_web_site,
            domain,
            location,
            int(number_salaries) if str(number_salaries).isdigit() else None,
            int(str(average_age).split(' ')[0]) if str(str(average_age).split(' ')[0]).isdigit() else None,
            int(str(offers.split(' '))[0]) if str(str(offers.split(' '))[0]).isdigit() else 1 if spontaneous_application == "Oui" else None,
            all_offers,
            spontaneous_application
        )
    except Exception as e:
        logger.error(f"Error initialising Company Object. : {e}")
        return 0

def get_element_by_web_driver(driver, url, wait_time=0):
    """
    Get and parse HTML with Selenium and BeautifulSoup.
    """
    try:
        get_url(driver, url)
        if wait_time > 0:
            time.sleep(wait_time)
        html = driver.page_source
        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        logger.error(f"[!] Erreur chargement page WebDriver : {url}, {e}")
        return None

def get_companys_blocks(driver, url):
    """
    Get company blocks from a page.
    """
    soup = get_element_by_web_driver(driver, url, 5)
    if not soup:
        return []
    try:
        return soup.select(CSS_SELECTORS[7])
    except Exception as e:
        logger.error(f"Error getting company blocks: {e}")
        return []

def get_companys_infos(driver, block, existing_companies = []):
    """
    Extract company info from a block.
    """
    try:
        # Extracting company information from the block
        name = block.select_one(CSS_SELECTORS[8]).text if block.select_one(CSS_SELECTORS[8]).text else "N/A" 
        if name in existing_companies:
            logger.info(f"Company {name} already exists. Skipping.")
            return {}
        details = block.select(CSS_SELECTORS[9]) if block.select(CSS_SELECTORS[9]) else []
        domain = details[-3].text if len(details) > 2 else "N/A"
        location = details[-2].text if len(details) > 1 else "N/A"
        offer = block.select_one(CSS_SELECTORS[10]).text if block.select_one(CSS_SELECTORS[10]).text else "N/A"
        link = urljoin(MAIN_URL, block.select_one(CSS_SELECTORS[11])['href']) if block.select_one(CSS_SELECTORS[11]) else "N/A"
        infos = {
            "Name": name,
            "Domain": domain,
            "Location": location,
            "Offer": offer,
            "Link": link
        }

        jobs_link = urljoin(link.split("?")[0]+'/', "jobs")
        offres = job_offers(driver, jobs_link)
        infos["Offres"] = offres 

        if "Candidature spontanée" in offres:
            infos["Candidature spontanée"] = "Yes"
        else:
            infos["Candidature spontanée"] = "No"

        infos = infos | get_other_infos(driver, link)
        return infos

    except Exception as e:
        logger.error(f"Error retrieving information for {block.select_one(CSS_SELECTORS[8]).text} \n Message {e}")
        return {}

def get_other_infos(driver, url):
    """
    Get extra company info from a URL.
    """
    block_dict = {}
    # soup = get_element_by_requests(url, 1)
    soup = get_element_by_web_driver(driver, url, 1)
    if not soup:
        return block_dict

    try:
        block_dict["Web Site"] = soup.select_one(CSS_SELECTORS[12])['href'] #if soup.select_one(CSS_SELECTORS[12]) else None
    except Exception as e:
        logger.error(f"Web site not found for {url} - {e}")
        block_dict["Web Site"] = "N/A"

    block_details = soup.select(CSS_SELECTORS[13])
    for block in block_details:
        try:
            titre = block.select_one(CSS_SELECTORS[14]).text
            contenu = block.select_one(CSS_SELECTORS[15]).text
            block_dict[titre] = contenu
        except:
            logger.error(f"Error extracting details from block: {block}")
            block_dict[titre] = "N/A"
            continue
    return block_dict

def job_offers(driver, urljobs):
    """
    Get job offers from a jobs URL.
    """
    soup = get_element_by_web_driver(driver, urljobs, 2)
    if not soup:
        logger.error(f"Failed to retrieve job offers from {urljobs} or the page is not exists.")
        return []
    jobs = soup.select(CSS_SELECTORS[16])
    formatted_jobs = [job.text for job in jobs]
    spontane = soup.select_one(CSS_SELECTORS[20])
    if spontane:
        formatted_jobs.append("Candidature spontanée")
    return formatted_jobs if formatted_jobs else ["Aucune offre d'emploi disponible"]

if __name__ == "__main__":
    pass