import requests
from bs4 import BeautifulSoup
import time
import sys

# NOTE: For real-world use, replace this with a URL to a static e-commerce page.
# Using a dummy URL here to demonstrate structure.
DEFAULT_URL = "https://www.example.com"
DEFAULT_THRESHOLD = 50.00  # Price target for alert

def check_price(url, target_price):
    """
    Scrapes a webpage to find a price and alerts the user if it's below the target.
    """
    # Headers to mimic a real browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print(f"Checking URL: {url}...")
    
    try:
        # 1. Make the request
        page = requests.get(url, headers=headers)
        page.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # 2. Parse the content
        soup = BeautifulSoup(page.content, 'html.parser')

        # 3. Find the price element (This is highly dependent on the target website's HTML)
        # We will look for an element that might contain the price based on common classes/tags.
        # In a real scenario, you'd inspect the target page and customize this line:
        price_text = soup.find(class_="price-value") # Replace "price-value" with actual class or ID
        
        if not price_text:
             # Fallback to checking a more generic structure
            price_text = soup.find(text=re.compile(r'\$\d+'))
            
        if not price_text:
            print("Error: Could not find the price element. Check HTML structure or CSS class.")
            return

        # 4. Clean and convert the price
        raw_price = price_text.get_text(strip=True).replace('$', '').replace(',', '')
        current_price = float(raw_price)

        # 5. Alert logic
        print("-" * 40)
        print(f"Product Price: ${current_price:.2f}")
        print(f"Target Price:  ${target_price:.2f}")

        if current_price <= target_price:
            print(f"\nALERT! Price has dropped below ${target_price:.2f}! Buy now!")
        else:
            print("\nPrice is still above the target. Monitoring...")
        print("-" * 40)
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the URL: {e}")
    except ValueError:
        print(f"Error: Could not convert '{raw_price}' to a number. Price format issue.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    import re
    
    print("--- Simple Web Price Tracker ---")
    
    target_url = input(f"Enter the product URL (Default: {DEFAULT_URL}): ").strip() or DEFAULT_URL
    target_price_str = input(f"Enter the target price to alert on (Default: ${DEFAULT_THRESHOLD:.2f}): ").strip()
    
    if target_price_str:
        try:
            target_price = float(target_price_str)
        except ValueError:
            print("Invalid target price entered. Exiting.")
            sys.exit(1)
    else:
        target_price = DEFAULT_THRESHOLD

    check_price(target_url, target_price)