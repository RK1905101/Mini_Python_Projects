import requests
import concurrent.futures
import time
import sys
import os

# --- Core Link Checking Function ---

def check_single_link(url, timeout=5):
    """Checks a single URL and returns its status."""
    try:
        # Set a User-Agent to mimic a browser and avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # HEAD request is faster as it only downloads headers, but we use GET
        # to properly handle redirects and errors for a full check.
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        status_code = response.status_code
        final_url = response.url
        
        if status_code == 200:
            status = "OK"
        elif 300 <= status_code < 400:
            status = f"Redirect ({status_code})"
        elif status_code == 404:
            status = "BROKEN (404)"
        elif status_code >= 400:
            status = f"Client/Server Error ({status_code})"
        else:
            status = f"Unknown Status ({status_code})"
            
        return url, status, final_url
        
    except requests.exceptions.Timeout:
        return url, "TIMEOUT", url
    except requests.exceptions.ConnectionError:
        return url, "CONNECTION ERROR", url
    except requests.exceptions.RequestException as e:
        return url, f"Request Failed ({type(e).__name__})", url
    except Exception as e:
        return url, f"Unexpected Error ({type(e).__name__})", url


# --- Concurrency Manager ---

def check_links_concurrently(url_list, max_workers=20):
    """Manages the checking of all links using a thread pool."""
    start_time = time.time()
    results = []
    
    # Use ThreadPoolExecutor for I/O-bound tasks like network requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the check_single_link function to the list of URLs
        future_to_url = {executor.submit(check_single_link, url): url for url in url_list}
        
        # Retrieve results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                url = future_to_url[future]
                results.append((url, f"Worker Error ({type(exc).__name__})", url))

    end_time = time.time()
    total_time = end_time - start_time
    
    return results, total_time


# --- Main Logic and Reporting ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python concurrent_link_checker.py <path_to_url_list_file.txt>")
        print("Or: Enter URLs separated by commas.")
        
        url_input = input("Enter URLs (comma-separated): ").strip()
        if not url_input:
            print("No input provided. Exiting.")
            return

        urls = [u.strip() for u in url_input.split(',')]
        
    else:
        # Load URLs from a file
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: URL list file not found at '{file_path}'")
            return

    if not urls:
        print("No URLs found to check.")
        return

    print(f"\n--- Checking {len(urls)} Links Concurrently ---")
    results, total_time = check_links_concurrently(urls)

    print("\n--- Summary Report ---")
    print(f"Total links checked: {len(results)}")
    print(f"Time taken: {total_time:.2f} seconds")
    
    # Print detailed report
    print("\nDetailed Results:")
    for original_url, status, final_url in sorted(results, key=lambda x: x[1]): # Sort by status for readability
        print(f"[{status:<18}] {original_url}")
        if status.startswith("Redirect"):
            print(f"{'':<18} -> Redirects to: {final_url}")

if __name__ == "__main__":
    main()