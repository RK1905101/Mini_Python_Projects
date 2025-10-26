"""
Enhanced scraper that can capture different types of transactions and provide better insights.
"""

from src.blockchain_scraper import BlockchainScraper
from src.utils import save_to_csv, print_transaction_summary
import pandas as pd
from datetime import datetime, timedelta

def test_ethereum_mainnet():
    """Test with Ethereum mainnet which has more EOA-to-EOA activity."""
    print("=== Testing Ethereum Mainnet (Higher Activity) ===")

    try:
        scraper = BlockchainScraper(
            network_name='ethereum',
            rpc_url='https://eth.llamarpc.com',
            batch_size=20,
            block_interval=1
        )

        # Get current block and scrape last 10 blocks
        current_block = scraper.w3.eth.block_number
        start_block = current_block - 10
        end_block = current_block

        print(f"Scraping Ethereum blocks {start_block} to {end_block}")

        df = scraper.scrape_by_block_range(start_block, end_block)

        if len(df) > 0:
            print(f"✓ Found {len(df)} EOA-to-EOA transactions!")
            filename = f'ethereum_test_{start_block}_to_{end_block}.csv'
            save_to_csv(df, filename)
            print_transaction_summary(df, 'ethereum')

            # Show some examples
            print("\nSample transactions:")
            sample = df[['from_address', 'to_address', 'value_eth', 'block_number']].head(3)
            print(sample)

        else:
            print("No EOA-to-EOA transactions found on Ethereum either")

    except Exception as e:
        print(f"Ethereum test failed: {str(e)}")

def test_with_date_range():
    """Test scraping by date range instead of block range."""
    print("\n=== Testing Date Range Scraping ===")

    try:
        scraper = BlockchainScraper(
            network_name='ethereum',
            rpc_url='https://eth.llamarpc.com',
            batch_size=100,
            block_interval=10  # Sample every 10th block for speed
        )

        # Test with yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        print(f"Scraping Ethereum from {yesterday} to {today} (every 10th block)")

        df = scraper.scrape_by_date_range(yesterday, today)

        if len(df) > 0:
            print(f"✓ Found {len(df)} EOA-to-EOA transactions!")
            filename = f'ethereum_date_{yesterday}_to_{today}.csv'
            save_to_csv(df, filename)
            print_transaction_summary(df, 'ethereum')
        else:
            print("No EOA-to-EOA transactions found in date range")

    except Exception as e:
        print(f"Date range test failed: {str(e)}")

def create_all_transaction_scraper():
    """Create a version that captures ALL types of transactions, not just EOA-to-EOA."""
    print("\n=== Creating All-Transaction Scraper ===")

    try:
        scraper = BlockchainScraper(
            network_name='scroll',
            rpc_url='https://rpc.scroll.io'
        )

        current_block = scraper.w3.eth.block_number
        start_block = current_block - 5

        all_transactions = []

        for block_num in range(start_block, current_block + 1):
            transactions, block_timestamp = scraper.get_block_transactions(block_num)

            for tx in transactions:
                if not tx.to:  # Skip contract creation
                    continue

                try:
                    receipt = scraper.w3.eth.get_transaction_receipt(tx.hash)
                    if receipt.status != 1:  # Skip failed transactions
                        continue

                    from_is_contract = scraper.is_contract(tx['from'])
                    to_is_contract = scraper.is_contract(tx.to)

                    # Determine transaction type
                    if not from_is_contract and not to_is_contract:
                        tx_type = "EOA-to-EOA"
                    elif not from_is_contract and to_is_contract:
                        tx_type = "EOA-to-Contract"
                    elif from_is_contract and not to_is_contract:
                        tx_type = "Contract-to-EOA"
                    else:
                        tx_type = "Contract-to-Contract"

                    gas_price = tx.gasPrice
                    gas_used = receipt.gasUsed
                    fee = scraper.w3.from_wei(gas_price * gas_used, 'ether')

                    tx_data = {
                        'hash': tx.hash.hex(),
                        'block_number': tx.blockNumber,
                        'from_address': tx['from'],
                        'to_address': tx.to,
                        'value_eth': float(scraper.w3.from_wei(tx.value, 'ether')),
                        'gas_price_gwei': float(scraper.w3.from_wei(gas_price, 'gwei')),
                        'gas_used': gas_used,
                        'fee_eth': float(fee),
                        'timestamp': datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                        'transaction_type': tx_type,
                        'network': 'scroll'
                    }

                    all_transactions.append(tx_data)

                except Exception as e:
                    continue

        if all_transactions:
            df = pd.DataFrame(all_transactions)
            filename = f'scroll_all_transactions_{start_block}_to_{current_block}.csv'
            save_to_csv(df, filename)

            print(f"✓ Found {len(df)} total transactions")

            # Show transaction type breakdown
            type_counts = df['transaction_type'].value_counts()
            print("\nTransaction type breakdown:")
            for tx_type, count in type_counts.items():
                percentage = (count / len(df)) * 100
                print(f"  {tx_type}: {count} ({percentage:.1f}%)")

            # Show EOA-to-EOA specifically
            eoa_to_eoa = df[df['transaction_type'] == 'EOA-to-EOA']
            if len(eoa_to_eoa) > 0:
                print(f"\n✓ Found {len(eoa_to_eoa)} EOA-to-EOA transactions!")
                print(eoa_to_eoa[['from_address', 'to_address', 'value_eth']].head())
            else:
                print("\n⚠ No EOA-to-EOA transactions found")
                print("This is normal for Scroll - most activity is through DeFi protocols")
        else:
            print("No transactions found")

    except Exception as e:
        print(f"All-transaction scraper failed: {str(e)}")

if __name__ == "__main__":
    test_ethereum_mainnet()
    test_with_date_range()
    create_all_transaction_scraper()
