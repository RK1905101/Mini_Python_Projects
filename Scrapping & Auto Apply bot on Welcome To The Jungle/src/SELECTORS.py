from urllib.parse import urljoin


#_______________________________FOR APPLICATION___________________________________________
BUTTON_CONNECT = "#login-button-submit"
MAIL_INPUT = "#email_login"
PASSWORD_INPUT = "#password"
# APPLYING_BUTTON = "button[data-testid='company_jobs-button-apply']"
# APPLYING_BUTTON = "#app > div > div > div > main > div > div > section > div.sc-iorCAc.imcUbI > div > div > div > div > div.sc-brzPDJ.jijEDz.sc-dUrdUa.jRFTsL > div > ul > li.sc-brzPDJ > div > div > div > button"
APPLYING_BUTTON = ".kOnLvx"
MESSAGE_TEXTAREA = "#cover_letter"
CONDITIONS_CHECKBOX = "#consent"
POSTULER = "#apply-form-submit"
CLOSE_LAYOUT = "button svg path"
VALIDE = ".eVRzDd"
# CLOSE_LAYOUT = ".eVRzDd > header:nth-child(1) > button:nth-child(1).eVRzDd > header:nth-child(1) > button:nth-child(1)"

#______________________________________FOR RETRIEVING DATA____________________________________

MAIN_URL = "https://www.welcometothejungle.com/"
COMPANIES_URL = urljoin(MAIN_URL, "en/companies")
LOGIN_URL = urljoin(MAIN_URL, "en/signin")

# CSS Selectors as constants
SECTOR_CSS_SELECTOR = ".sc-fvtCpz > header:nth-child(1)"
TECH_CSS_SELECTOR = "span[data-testid='companies-search-search-widgets-sectors_name-19-trigger']"
CHECKBOX_TECH_SELECTOR =  "div.sc-brzPDJ:nth-child(20) > div:nth-child(1) > span:nth-child(1) > input:nth-child(1)"
SEARCH_BUTTON_CSS_SELECTOR = "button.sc-kWJkYy:nth-child(5) > span:nth-child(2)"

PAGINATION_NAV_SELECTOR = "[data-testid='companies-search-pagination'] nav ul"
PAGINATION_LI_SELECTOR = PAGINATION_NAV_SELECTOR + " li"
COMPANY_BLOCK_SELECTOR = "article[data-role='companies:thumb'][data-testid='company-card']"
COMPANY_NAME_SELECTOR = "div header a span"
COMPANY_DETAILS_SELECTOR = "ul li"
COMPANY_OFFER_SELECTOR = "footer a span"
COMPANY_LINK_SELECTOR = "a"
COMPANY_WEBSITE_SELECTOR = ".sc-bFQvPF"
COMPANY_DETAILS_BLOCK_SELECTOR = ".dyNymF section"
COMPANY_DETAILS_TITLE_SELECTOR = "p"
COMPANY_DETAILS_CONTENT_SELECTOR = "span"
COMPANY_JOBS_SELECTOR = "div div a h2"
COMPANY_SPONTANEOUS_SELECTOR = "div.sc-iorCAc.imcUbI > div > div > div > div > div.sc-brzPDJ.jijEDz.sc-dUrdUa.jRFTsL > div > ul > li.sc-brzPDJ > div > div > div > button"

# ____________________________ALL SELECTORS IN A DICTIONNARY_____________________________________________

CSS_SELECTORS = {
    # For retrieving data
    1: SECTOR_CSS_SELECTOR,
    2: TECH_CSS_SELECTOR,
    3: CHECKBOX_TECH_SELECTOR,
    4: SEARCH_BUTTON_CSS_SELECTOR,
    5: PAGINATION_NAV_SELECTOR,
    6: PAGINATION_LI_SELECTOR,
    7: COMPANY_BLOCK_SELECTOR,
    8: COMPANY_NAME_SELECTOR,
    9: COMPANY_DETAILS_SELECTOR,
    10: COMPANY_OFFER_SELECTOR,
    11: COMPANY_LINK_SELECTOR,
    12: COMPANY_WEBSITE_SELECTOR,
    13: COMPANY_DETAILS_BLOCK_SELECTOR,
    14: COMPANY_DETAILS_TITLE_SELECTOR,
    15: COMPANY_DETAILS_CONTENT_SELECTOR,
    16: COMPANY_JOBS_SELECTOR,
    
    # For Application
    17: BUTTON_CONNECT,
    18: MAIL_INPUT,
    19: PASSWORD_INPUT,
    20: APPLYING_BUTTON,
    21: MESSAGE_TEXTAREA,
    22: CONDITIONS_CHECKBOX,
    23: POSTULER,
    24: CLOSE_LAYOUT,
    25: VALIDE
}


MAIN_TECH_PAGE_URL = "https://www.welcometothejungle.com/fr/companies?page=1&query=&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=SaaS%20%2F%20Cloud%20Services&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Logiciels&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Intelligence%20artificielle%20%2F%20Machine%20Learning&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Application%20mobile&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Big%20Data&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Cybers%C3%A9curit%C3%A9&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Objets%20connect%C3%A9s&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Robotique&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Blockchain"
