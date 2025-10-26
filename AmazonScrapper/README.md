# Amazon Product Scraper API

A FastAPI-based web scraper that extracts product information from Amazon India search results.

## Features

- Scrapes product details including name, price, URL, and rating
- Filters out sponsored products
- Configurable number of results
- REST API endpoint for easy integration

## Requirements

- Python 3.7+
- Chrome browser installed (for Selenium WebDriver)
- Required Python packages (see requirements.txt)


### API Endpoints

- `GET /`: Check if the API is running
- `POST /amazonData`: Get product data
  - Request body:
    ```json
    {
        "text": "search query",
        "amount": 5
    }
    ```
  - Response:
    ```json
    {
        "Search Data": [
            {
                "Name": "Product Name",
                "url": "Product URL",
                "price": "₹Price",
                "rating": "Rating"
            }
        ],
        "Amount": 5
    }
    ```

## Note

- This scraper is for educational purposes only
- Please respect Amazon's robots.txt and terms of service
- Consider implementing rate limiting for production use