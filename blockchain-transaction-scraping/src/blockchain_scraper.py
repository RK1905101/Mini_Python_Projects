from web3 import Web3
try:
    from web3.middleware.geth_poa import geth_poa_middleware
except ImportError:
    try:
        from web3.middleware import ExtraDataToPOAMiddleware
        geth_poa_middleware = ExtraDataToPOAMiddleware
    except ImportError:
        geth_poa_middleware = None
from web3.exceptions import ContractLogicError
from datetime import datetime, timezone
import pandas as pd
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class BlockchainScraper:
    def __init__(self,
                 network_name=None,
                 rpc_url=None,
                 batch_size=None,
                 block_interval=None,
                 temp_dir=None,
                 request_delay=None,
                 max_retries=None):

        # Load configuration from environment variables or use provided values
        self.network_name = network_name or os.getenv('NETWORK_NAME', 'ethereum')
        self.rpc_url = rpc_url or os.getenv('RPC_URL', 'https://eth.llamarpc.com')
        self.batch_size = int(batch_size or os.getenv('BATCH_SIZE', '500'))
        self.block_interval = int(block_interval or os.getenv('BLOCK_INTERVAL', '1'))
        self.temp_dir = temp_dir or os.getenv('TEMP_DIR', 'temp_data')
        self.request_delay = float(request_delay or os.getenv('REQUEST_DELAY', '0.1'))
        self.max_retries = int(max_retries or os.getenv('MAX_RETRIES', '3'))

        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        # Add PoA middleware for networks that require it
        if self.network_name.lower() in ['scroll', 'polygon', 'bsc', 'avalanche'] and geth_poa_middleware:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.w3.is_connected():
            raise Exception(f"Cannot connect to {self.network_name} network at {self.rpc_url}")

        print(f"Successfully connected to {self.network_name} network")
        print(f"Latest block: {self.w3.eth.block_number}")

        # Cache for address types to avoid repeated contract calls
        self.address_type_cache = {}

    def get_block_by_timestamp(self, target_timestamp):
        left = 1
        right = self.w3.eth.block_number
        closest_block = None
        smallest_diff = float('inf')

        max_iterations = 1000
        iterations = 0

        print(f"Searching for block closest to timestamp {target_timestamp}")

        while left <= right and iterations < max_iterations:
            mid = (left + right) // 2
            try:
                block = self.w3.eth.get_block(mid)
                block_time = block.timestamp
                time_diff = abs(block_time - target_timestamp)

                if time_diff < smallest_diff:
                    smallest_diff = time_diff
                    closest_block = mid

                if block_time == target_timestamp:
                    return mid
                elif block_time < target_timestamp:
                    left = mid + 1
                else:
                    right = mid - 1
                iterations += 1

            except Exception as e:
                print(f"Error reading block {mid}: {str(e)}")
                # Continue with binary search logic
                if left == mid and right == mid:
                    return closest_block
                if block_time < target_timestamp:
                    left = mid + 1
                else:
                    right = mid - 1
                iterations += 1

        print(f"Found closest block: {closest_block} (difference: {smallest_diff} seconds)")
        return closest_block

    def get_block_transactions(self, block_number):
        retries = 0
        while retries < self.max_retries:
            try:
                block = self.w3.eth.get_block(block_number, full_transactions=True)
                return block.transactions, block.timestamp
            except Exception as e:
                retries += 1
                if retries >= self.max_retries:
                    print(f"Error getting transactions for block {block_number} after {self.max_retries} retries: {str(e)}")
                    return [], None
                time.sleep(self.request_delay * retries)  # Exponential backoff

        return [], None

    def is_contract(self, address):
        if not address:
            return False

        if address in self.address_type_cache:
            return self.address_type_cache[address]

        try:
            code = self.w3.eth.get_code(Web3.to_checksum_address(address))
            is_contract_bool = len(code) > 0
            self.address_type_cache[address] = is_contract_bool
            return is_contract_bool
        except Exception as e:
            self.address_type_cache[address] = False
            return False

    def get_native_currency_symbol(self):
        currency_map = {
            'ethereum': 'ETH',
            'scroll': 'ETH',
            'polygon': 'MATIC',
            'arbitrum': 'ETH',
            'optimism': 'ETH',
            'bsc': 'BNB',
            'avalanche': 'AVAX',
            'base': 'ETH'
        }
        return currency_map.get(self.network_name.lower(), 'ETH')

    def get_transaction_details(self, tx, block_timestamp):
        if tx.blockHash is None:
            return None

        # Filter for EOA-to-EOA transactions only
        if tx.to is None or self.is_contract(tx['from']) or self.is_contract(tx['to']):
            return None

        try:
            receipt = self.w3.eth.get_transaction_receipt(tx.hash)

            # Only include successful transactions
            if receipt.status != 1:
                return None

            gas_price = tx.gasPrice
            gas_used = receipt.gasUsed
            fee = self.w3.from_wei(gas_price * gas_used, 'ether')
            currency_symbol = self.get_native_currency_symbol()

            tx_details = {
                'hash': tx.hash.hex(),
                'block_number': tx.blockNumber,
                'from_address': tx['from'],
                'to_address': tx.to,
                f'value_{currency_symbol.lower()}': float(self.w3.from_wei(tx.value, 'ether')),
                'gas_price_gwei': float(self.w3.from_wei(gas_price, 'gwei')),
                'gas_used': gas_used,
                f'fee_{currency_symbol.lower()}': float(fee),
                'timestamp': datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                'network': self.network_name,
                'status': receipt.status,
                'is_eoa_to_eoa': True
            }

            return tx_details
        except Exception as e:
            print(f"Error processing transaction {tx.hash.hex()}: {str(e)}")
            return None

    def scrape_by_date_range(self, start_date_str=None, end_date_str=None, batch_size=None):
        # Use provided values or environment variables
        start_date_str = start_date_str or os.getenv('START_DATE', '2024-01-01')
        end_date_str = end_date_str or os.getenv('END_DATE', '2024-01-31')
        batch_size = batch_size or self.batch_size

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)

        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        print(f"Scraping {self.network_name} network from {start_date_str} to {end_date_str}")

        start_block = self.get_block_by_timestamp(start_timestamp)
        end_block = self.get_block_by_timestamp(end_timestamp)

        if not start_block or not end_block:
            raise Exception("Cannot determine block range for the given date range")

        print(f"Scanning blocks from {start_block} to {end_block} (interval: {self.block_interval})")

        transactions_data = []
        current_block = start_block
        batch_id = 0
        total_blocks = (end_block - start_block) // self.block_interval + 1
        processed_blocks = 0

        while current_block <= end_block:
            try:
                progress = (processed_blocks / total_blocks) * 100
                print(f"Processing block {current_block} ({progress:.1f}% complete, {len(transactions_data)} EOA-to-EOA transactions collected)")

                transactions, block_timestamp = self.get_block_transactions(current_block)

                # Skip block if timestamp is not relevant
                if not block_timestamp or not (start_timestamp <= block_timestamp <= end_timestamp):
                    current_block += self.block_interval
                    processed_blocks += 1
                    continue

                for tx in transactions:
                    tx_details = self.get_transaction_details(tx, block_timestamp)
                    if tx_details:
                        transactions_data.append(tx_details)

                # Save batch if it reaches the specified size
                if len(transactions_data) >= batch_size:
                    temp_df = pd.DataFrame(transactions_data)
                    temp_filename = os.path.join(self.temp_dir, f'{self.network_name}_eoa_to_eoa_temp_batch_{batch_id}.csv')
                    temp_df.to_csv(temp_filename, index=False)
                    print(f"Saved EOA-to-EOA batch to {temp_filename}")
                    transactions_data = []
                    batch_id += 1

                time.sleep(self.request_delay)
                current_block += self.block_interval
                processed_blocks += 1

            except Exception as e:
                print(f"Error on block {current_block}: {str(e)}. Continuing to next block...")
                time.sleep(self.request_delay * 2)
                current_block += self.block_interval
                processed_blocks += 1
                continue

        # Save remaining transactions
        if transactions_data:
            final_temp_df = pd.DataFrame(transactions_data)
            temp_filename = os.path.join(self.temp_dir, f'{self.network_name}_eoa_to_eoa_temp_final_batch_{batch_id}.csv')
            final_temp_df.to_csv(temp_filename, index=False)
            print(f"Saved final EOA-to-EOA batch to {temp_filename}")

        # Combine all temporary files
        all_temp_files = [
            os.path.join(self.temp_dir, f)
            for f in os.listdir(self.temp_dir)
            if f.startswith(f'{self.network_name}_eoa_to_eoa_temp_') and f.endswith('.csv')
        ]

        if not all_temp_files:
            print("No temporary EOA-to-EOA files found to combine.")
            self._cleanup_temp_dir()
            return pd.DataFrame()

        print(f"Combining {len(all_temp_files)} temporary files...")
        combined_df = pd.concat([pd.read_csv(f) for f in all_temp_files], ignore_index=True)

        # Clean up temporary files
        for f in all_temp_files:
            try:
                os.remove(f)
            except OSError as e:
                print(f"Error deleting temporary file {f}: {e}")

        self._cleanup_temp_dir()

        print(f"Successfully scraped {len(combined_df)} EOA-to-EOA transactions")
        return combined_df

    def scrape_by_block_range(self, start_block, end_block, batch_size=None):
        batch_size = batch_size or self.batch_size

        print(f"Scraping {self.network_name} network from block {start_block} to {end_block}")
        print(f"Block interval: {self.block_interval}")

        transactions_data = []
        current_block = start_block
        batch_id = 0
        total_blocks = (end_block - start_block) // self.block_interval + 1
        processed_blocks = 0

        while current_block <= end_block:
            try:
                progress = (processed_blocks / total_blocks) * 100
                print(f"Processing block {current_block} ({progress:.1f}% complete, {len(transactions_data)} EOA-to-EOA transactions collected)")

                transactions, block_timestamp = self.get_block_transactions(current_block)

                if not block_timestamp:
                    current_block += self.block_interval
                    processed_blocks += 1
                    continue

                for tx in transactions:
                    tx_details = self.get_transaction_details(tx, block_timestamp)
                    if tx_details:
                        transactions_data.append(tx_details)

                # Save batch if it reaches the specified size
                if len(transactions_data) >= batch_size:
                    temp_df = pd.DataFrame(transactions_data)
                    temp_filename = os.path.join(self.temp_dir, f'{self.network_name}_eoa_to_eoa_temp_batch_{batch_id}.csv')
                    temp_df.to_csv(temp_filename, index=False)
                    print(f"Saved EOA-to-EOA batch to {temp_filename}")
                    transactions_data = []
                    batch_id += 1

                time.sleep(self.request_delay)
                current_block += self.block_interval
                processed_blocks += 1

            except Exception as e:
                print(f"Error on block {current_block}: {str(e)}. Continuing to next block...")
                time.sleep(self.request_delay * 2)
                current_block += self.block_interval
                processed_blocks += 1
                continue

        # Save remaining transactions
        if transactions_data:
            final_temp_df = pd.DataFrame(transactions_data)
            temp_filename = os.path.join(self.temp_dir, f'{self.network_name}_eoa_to_eoa_temp_final_batch_{batch_id}.csv')
            final_temp_df.to_csv(temp_filename, index=False)
            print(f"Saved final EOA-to-EOA batch to {temp_filename}")

        # Combine all temporary files
        all_temp_files = [
            os.path.join(self.temp_dir, f)
            for f in os.listdir(self.temp_dir)
            if f.startswith(f'{self.network_name}_eoa_to_eoa_temp_') and f.endswith('.csv')
        ]

        if not all_temp_files:
            print("No temporary EOA-to-EOA files found to combine.")
            self._cleanup_temp_dir()
            return pd.DataFrame()

        print(f"Combining {len(all_temp_files)} temporary files...")
        combined_df = pd.concat([pd.read_csv(f) for f in all_temp_files], ignore_index=True)

        # Clean up temporary files
        for f in all_temp_files:
            try:
                os.remove(f)
            except OSError as e:
                print(f"Error deleting temporary file {f}: {e}")

        self._cleanup_temp_dir()

        print(f"Successfully scraped {len(combined_df)} EOA-to-EOA transactions")
        return combined_df

    def _cleanup_temp_dir(self):
        if os.path.exists(self.temp_dir) and not os.listdir(self.temp_dir):
            try:
                os.rmdir(self.temp_dir)
            except OSError as e:
                print(f"Error removing temp directory {self.temp_dir}: {e}")

    def get_network_info(self):
        try:
            latest_block = self.w3.eth.block_number
            chain_id = self.w3.eth.chain_id

            return {
                'network_name': self.network_name,
                'rpc_url': self.rpc_url,
                'chain_id': chain_id,
                'latest_block': latest_block,
                'native_currency': self.get_native_currency_symbol(),
                'is_connected': self.w3.is_connected()
            }
        except Exception as e:
            return {
                'network_name': self.network_name,
                'rpc_url': self.rpc_url,
                'error': str(e),
                'is_connected': False
            }
