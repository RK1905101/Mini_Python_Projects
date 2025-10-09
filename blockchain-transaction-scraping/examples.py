"""
Example usage of the Universal Blockchain Transaction Scraper.
This script demonstrates various ways to use the scraper.
"""

from src.blockchain_scraper import BlockchainScraper
from src.utils import save_to_csv, generate_filename, print_transaction_summary
import pandas as pd
from datetime import datetime, timedelta

def example_basic_scraping():
    """Example 1: Basic scraping with default settings."""
    print("=== Example 1: Basic Ethereum Scraping ===")

    # Initialize scraper for Ethereum
    scraper = BlockchainScraper(
        network_name='ethereum',
        rpc_url='https://eth.llamarpc.com'
    )

    # Get recent date range (last 3 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    print(f"Scraping from {start_date_str} to {end_date_str}")

    # Scrape transactions
    df = scraper.scrape_by_date_range(start_date_str, end_date_str, batch_size=100)

    if len(df) > 0:
        filename = generate_filename('ethereum', start_date_str, end_date_str)
        save_to_csv(df, filename)
        print_transaction_summary(df, 'ethereum')
    else:
        print("No transactions found")

def example_multi_network():
    """Example 2: Compare multiple networks."""
    print("\n=== Example 2: Multi-Network Comparison ===")

    networks = [
        ('scroll', 'https://rpc.scroll.io'),
        ('polygon', 'https://polygon-rpc.com'),
        ('arbitrum', 'https://arb1.arbitrum.io/rpc')
    ]

    # Use a smaller date range for this example
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    results = {}

    for network_name, rpc_url in networks:
        try:
            print(f"\nScraping {network_name}...")
            scraper = BlockchainScraper(
                network_name=network_name,
                rpc_url=rpc_url,
                batch_size=50,
                block_interval=10  # Sample every 10th block for speed
            )

            df = scraper.scrape_by_date_range(start_date_str, end_date_str)
            results[network_name] = len(df)

            if len(df) > 0:
                filename = generate_filename(network_name, start_date_str, end_date_str)
                save_to_csv(df, filename)
                print(f"✓ {network_name}: {len(df)} transactions")
            else:
                print(f"✓ {network_name}: No transactions found")

        except Exception as e:
            print(f"✗ {network_name}: Error - {str(e)}")
            results[network_name] = 0

    print(f"\n=== Network Comparison Summary ===")
    for network, count in results.items():
        print(f"{network}: {count} transactions")

def example_block_range_scraping():
    """Example 3: Scrape specific block range."""
    print("\n=== Example 3: Block Range Scraping ===")

    # Scrape a specific range of blocks from Scroll
    scraper = BlockchainScraper(
        network_name='scroll',
        rpc_url='https://rpc.scroll.io',
        batch_size=100
    )

    # Get current block and scrape last 1000 blocks
    try:
        current_block = scraper.w3.eth.block_number
        start_block = max(1, current_block - 1000)
        end_block = current_block

        print(f"Scraping Scroll blocks {start_block} to {end_block}")

        df = scraper.scrape_by_block_range(start_block, end_block)

        if len(df) > 0:
            filename = f'scroll_blocks_{start_block}_to_{end_block}.csv'
            save_to_csv(df, filename)
            print_transaction_summary(df, 'scroll')
        else:
            print("No transactions found in block range")

    except Exception as e:
        print(f"Error: {str(e)}")

def example_network_info():
    """Example 4: Get network information."""
    print("\n=== Example 4: Network Information ===")

    networks = ['ethereum', 'scroll', 'polygon']

    for network_name in networks:
        try:
            scraper = BlockchainScraper(network_name=network_name)
            info = scraper.get_network_info()

            print(f"\n{network_name.upper()} Network Info:")
            for key, value in info.items():
                print(f"  {key}: {value}")

        except Exception as e:
            print(f"\n{network_name.upper()}: Connection failed - {str(e)}")

def example_custom_configuration():
    """Example 5: Custom configuration example."""
    print("\n=== Example 5: Custom Configuration ===")

    # Custom scraper configuration
    scraper = BlockchainScraper(
        network_name='ethereum',
        rpc_url='https://eth.llamarpc.com',
        batch_size=200,           # Larger batches
        block_interval=5,         # Sample every 5th block
        request_delay=0.05,       # Faster requests
        max_retries=5             # More retries
    )

    print("Custom configuration:")
    print(f"  Network: {scraper.network_name}")
    print(f"  Batch size: {scraper.batch_size}")
    print(f"  Block interval: {scraper.block_interval}")
    print(f"  Request delay: {scraper.request_delay}s")
    print(f"  Max retries: {scraper.max_retries}")

    # Quick test with small date range
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')

    print(f"\nTesting with date range: {yesterday} to {today}")

    try:
        df = scraper.scrape_by_date_range(yesterday, today)
        print(f"Found {len(df)} transactions with custom configuration")

        if len(df) > 0:
            # Show first few transactions
            print("\nSample transactions:")
            print(df.head(3).to_string())

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Run all examples."""
    print("Universal Blockchain Transaction Scraper - Examples")
    print("=" * 60)

    try:
        # Run examples (comment out any you don't want to run)
        example_network_info()          # Quick - just connection tests
        # example_basic_scraping()      # Moderate - scrapes recent data
        # example_block_range_scraping() # Moderate - scrapes block range
        # example_multi_network()       # Slow - tests multiple networks
        # example_custom_configuration() # Quick - shows configuration options

        print(f"\n=== Examples Complete ===")
        print("Check the 'output' directory for generated CSV files.")

    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"Error running examples: {str(e)}")

if __name__ == "__main__":
    main()
