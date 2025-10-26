"""
Quick demonstration of the Universal Blockchain Transaction Scraper.
This shows how to use the scraper for different networks and configurations.
"""

from src.blockchain_scraper import BlockchainScraper
from src.utils import save_to_csv, print_transaction_summary

def demo_quick_test():
    """Quick test with a small block range."""
    print("=== Quick Demo: Scraping 10 blocks from Scroll ===")

    # Initialize scraper
    scraper = BlockchainScraper(
        network_name='scroll',
        rpc_url='https://rpc.scroll.io',
        batch_size=50,
        block_interval=1
    )

    # Get current block and scrape last 10 blocks
    current_block = scraper.w3.eth.block_number
    start_block = current_block - 10
    end_block = current_block

    print(f"Scraping blocks {start_block} to {end_block}")

    # Scrape transactions
    df = scraper.scrape_by_block_range(start_block, end_block)

    if len(df) > 0:
        filename = f'demo_scroll_blocks_{start_block}_to_{end_block}.csv'
        save_to_csv(df, filename)
        print_transaction_summary(df, 'scroll')
    else:
        print("No EOA-to-EOA transactions found in this range")

if __name__ == "__main__":
    try:
        demo_quick_test()
        print("\n✓ Demo completed successfully!")
        print("\nTo run more advanced examples:")
        print("  python examples.py")
        print("\nTo configure and scrape your own data:")
        print("  python configure.py --setup")
        print("  python main.py")
    except Exception as e:
        print(f"Demo failed: {str(e)}")
        print("\nMake sure you have internet connection and try again.")
