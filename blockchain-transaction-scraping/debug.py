"""
Debug script to analyze transaction patterns and understand why no EOA-to-EOA transactions are found.
"""

from src.blockchain_scraper import BlockchainScraper
import pandas as pd

def debug_transactions():
    print("=== Debug: Analyzing Transaction Types ===")

    scraper = BlockchainScraper(
        network_name='scroll',
        rpc_url='https://rpc.scroll.io'
    )

    # Get current block and analyze last 5 blocks
    current_block = scraper.w3.eth.block_number
    start_block = current_block - 5
    end_block = current_block

    print(f"Analyzing blocks {start_block} to {end_block}")

    total_transactions = 0
    eoa_to_eoa = 0
    eoa_to_contract = 0
    contract_to_eoa = 0
    contract_to_contract = 0
    failed_transactions = 0

    for block_num in range(start_block, end_block + 1):
        try:
            transactions, block_timestamp = scraper.get_block_transactions(block_num)
            print(f"\nBlock {block_num}: {len(transactions)} transactions")

            for tx in transactions:
                if not tx.to:
                    continue

                total_transactions += 1

                # Check transaction receipt for status
                try:
                    receipt = scraper.w3.eth.get_transaction_receipt(tx.hash)
                    if receipt.status != 1:
                        failed_transactions += 1
                        continue
                except:
                    continue

                # Check address types
                from_is_contract = scraper.is_contract(tx['from'])
                to_is_contract = scraper.is_contract(tx.to)

                if not from_is_contract and not to_is_contract:
                    eoa_to_eoa += 1
                    print(f"  ✓ EOA-to-EOA: {tx.hash.hex()[:10]}... Value: {scraper.w3.from_wei(tx.value, 'ether')} ETH")
                elif not from_is_contract and to_is_contract:
                    eoa_to_contract += 1
                elif from_is_contract and not to_is_contract:
                    contract_to_eoa += 1
                else:
                    contract_to_contract += 1

        except Exception as e:
            print(f"Error processing block {block_num}: {str(e)}")

    print(f"\n=== Transaction Analysis Summary ===")
    print(f"Total successful transactions: {total_transactions}")
    print(f"Failed transactions: {failed_transactions}")
    print(f"EOA-to-EOA: {eoa_to_eoa} ({eoa_to_eoa/max(total_transactions, 1)*100:.1f}%)")
    print(f"EOA-to-Contract: {eoa_to_contract} ({eoa_to_contract/max(total_transactions, 1)*100:.1f}%)")
    print(f"Contract-to-EOA: {contract_to_eoa} ({contract_to_eoa/max(total_transactions, 1)*100:.1f}%)")
    print(f"Contract-to-Contract: {contract_to_contract} ({contract_to_contract/max(total_transactions, 1)*100:.1f}%)")

def test_with_larger_range():
    """Test with a larger block range to find EOA-to-EOA transactions."""
    print("\n=== Testing with Larger Block Range ===")

    scraper = BlockchainScraper(
        network_name='scroll',
        rpc_url='https://rpc.scroll.io',
        batch_size=50,
        block_interval=1
    )

    # Test with last 100 blocks
    current_block = scraper.w3.eth.block_number
    start_block = current_block - 100
    end_block = current_block

    print(f"Scraping 100 blocks: {start_block} to {end_block}")

    df = scraper.scrape_by_block_range(start_block, end_block)

    if len(df) > 0:
        print(f"Found {len(df)} EOA-to-EOA transactions in 100 blocks!")

        # Show sample transactions
        print("\nSample transactions:")
        print(df[['hash', 'from_address', 'to_address', 'value_eth', 'block_number']].head())

        # Save results
        filename = f'debug_scroll_100blocks_{start_block}_to_{end_block}.csv'
        from src.utils import save_to_csv
        save_to_csv(df, filename)

    else:
        print("Still no EOA-to-EOA transactions found in 100 blocks")
        print("This might indicate:")
        print("1. Scroll network has very few direct transfers")
        print("2. Most activity goes through smart contracts")
        print("3. Need to try different networks or larger ranges")

def test_different_networks():
    """Test different networks to compare EOA-to-EOA activity."""
    print("\n=== Testing Different Networks ===")

    networks = [
        ('ethereum', 'https://eth.llamarpc.com'),
        ('polygon', 'https://polygon-rpc.com'),
        ('arbitrum', 'https://arb1.arbitrum.io/rpc')
    ]

    for network_name, rpc_url in networks:
        try:
            print(f"\nTesting {network_name}...")
            scraper = BlockchainScraper(
                network_name=network_name,
                rpc_url=rpc_url,
                batch_size=10
            )

            # Test with last 20 blocks
            current_block = scraper.w3.eth.block_number
            start_block = current_block - 20
            end_block = current_block

            df = scraper.scrape_by_block_range(start_block, end_block)

            print(f"  {network_name}: {len(df)} EOA-to-EOA transactions in 20 blocks")

        except Exception as e:
            print(f"  {network_name}: Error - {str(e)}")

if __name__ == "__main__":
    try:
        debug_transactions()
        test_with_larger_range()
        test_different_networks()

    except Exception as e:
        print(f"Debug failed: {str(e)}")
