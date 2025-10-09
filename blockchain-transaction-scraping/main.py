from src.blockchain_scraper import BlockchainScraper
from src.utils import save_to_csv, generate_filename, print_transaction_summary, validate_date_format, get_network_config
import pandas as pd
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description='Blockchain Transaction Scraper')
    parser.add_argument('--network', type=str, help='Blockchain network name')
    parser.add_argument('--rpc-url', type=str, help='RPC endpoint URL')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--start-block', type=int, help='Start block number')
    parser.add_argument('--end-block', type=int, help='End block number')
    parser.add_argument('--batch-size', type=int, help='Batch size for processing')
    parser.add_argument('--block-interval', type=int, help='Interval between blocks to scan')
    parser.add_argument('--info', action='store_true', help='Show network information only')

    args = parser.parse_args()

    try:
        # Initialize scraper with command line arguments or environment variables
        scraper = BlockchainScraper(
            network_name=args.network,
            rpc_url=args.rpc_url,
            batch_size=args.batch_size,
            block_interval=args.block_interval
        )

        # Show network information if requested
        if args.info:
            network_info = scraper.get_network_info()
            print("\n=== Network Information ===")
            for key, value in network_info.items():
                print(f"{key}: {value}")
            return

        # Determine scraping method and parameters
        if args.start_block is not None and args.end_block is not None:
            # Scrape by block range
            print(f"Scraping {scraper.network_name} network from block {args.start_block} to {args.end_block}")
            df = scraper.scrape_by_block_range(args.start_block, args.end_block, args.batch_size)
            filename = f'{scraper.network_name}_eoa_to_eoa_transactions_blocks_{args.start_block}_to_{args.end_block}.csv'
        else:
            # Scrape by date range
            start_date = args.start_date or os.getenv('START_DATE', '2024-01-01')
            end_date = args.end_date or os.getenv('END_DATE', '2024-01-31')

            # Validate date formats
            if not validate_date_format(start_date) or not validate_date_format(end_date):
                print("Error: Invalid date format. Please use YYYY-MM-DD format.")
                return

            print(f"Scraping {scraper.network_name} network from {start_date} to {end_date}")
            df = scraper.scrape_by_date_range(start_date, end_date, args.batch_size)
            filename = generate_filename(scraper.network_name, start_date, end_date)

        if len(df) == 0:
            print(f"No EOA-to-EOA transactions found for {scraper.network_name} in the specified range")
            return

        output_path = save_to_csv(df, filename)
        print(f"\nResults saved to: {output_path}")

        print_transaction_summary(df, scraper.network_name)

        print(f"\n=== Additional Analysis ===")
        print(f"Data columns: {', '.join(df.columns)}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

        # Top active addresses
        if len(df) > 0:
            from_counts = df['from_address'].value_counts().head(5)
            to_counts = df['to_address'].value_counts().head(5)

            print(f"\nTop 5 most active sender addresses:")
            for addr, count in from_counts.items():
                print(f"  {addr}: {count} transactions")

            print(f"\nTop 5 most active recipient addresses:")
            for addr, count in to_counts.items():
                print(f"  {addr}: {count} transactions")

    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"Error during scraping process: {str(e)}")
        print(f"Network: {getattr(scraper, 'network_name', 'Unknown') if 'scraper' in locals() else 'Unknown'}")
        print(f"RPC URL: {getattr(scraper, 'rpc_url', 'Unknown') if 'scraper' in locals() else 'Unknown'}")

def show_available_networks():
    """Display information about available blockchain networks."""
    print("\n=== Available Blockchain Networks ===")
    networks = [
        'ethereum', 'scroll', 'polygon', 'arbitrum',
        'optimism', 'bsc', 'avalanche', 'base'
    ]

    for network in networks:
        config = get_network_config(network)
        print(f"\n{network.upper()}:")
        print(f"  Name: {config['name']}")
        print(f"  Default RPC: {config['rpc_url']}")
        print(f"  Chain ID: {config['chain_id']}")
        print(f"  Currency: {config['currency']}")

if __name__ == "__main__":
    if len(os.sys.argv) > 1 and os.sys.argv[1] == '--help-networks':
        show_available_networks()
    else:
        main()
