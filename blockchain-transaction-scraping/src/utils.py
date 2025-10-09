import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def save_to_csv(df, filename, output_dir=None):
    if output_dir is None:
        output_dir = os.getenv('OUTPUT_DIR', 'output')

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
    return filepath

def generate_filename(network_name, start_date, end_date, file_type='csv'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'{network_name}_eoa_to_eoa_transactions_{start_date}_to_{end_date}_{timestamp}.{file_type}'

def print_transaction_summary(df, network_name):
    if len(df) == 0:
        print(f"No EOA-to-EOA transactions found for {network_name}")
        return

    print(f"\n=== {network_name.upper()} EOA-to-EOA Transaction Summary ===")
    print(f"Total transactions: {len(df)}")

    currency_cols = [col for col in df.columns if col.startswith('value_')]
    fee_cols = [col for col in df.columns if col.startswith('fee_')]

    if currency_cols:
        currency_col = currency_cols[0]
        currency_symbol = currency_col.split('_')[1].upper()
        total_value = df[currency_col].sum()
        print(f"Total {currency_symbol} transferred: {total_value:.6f} {currency_symbol}")

        print(f"Average {currency_symbol} per transaction: {df[currency_col].mean():.6f} {currency_symbol}")
        print(f"Median {currency_symbol} per transaction: {df[currency_col].median():.6f} {currency_symbol}")

    if fee_cols:
        fee_col = fee_cols[0]
        currency_symbol = fee_col.split('_')[1].upper()
        total_fees = df[fee_col].sum()
        print(f"Total fees paid: {total_fees:.6f} {currency_symbol}")
        print(f"Average fee per transaction: {df[fee_col].mean():.6f} {currency_symbol}")

    if 'gas_price_gwei' in df.columns:
        print(f"Average gas price: {df['gas_price_gwei'].mean():.2f} Gwei")
        print(f"Median gas price: {df['gas_price_gwei'].median():.2f} Gwei")

    if 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_transactions = df.groupby('date').size()
        print(f"\nDaily transaction distribution:")
        for date, count in daily_transactions.items():
            print(f"  {date}: {count} transactions")

        print(f"\nDate range: {daily_transactions.index.min()} to {daily_transactions.index.max()}")
        print(f"Average transactions per day: {daily_transactions.mean():.1f}")

    # Address analysis
    unique_from = df['from_address'].nunique()
    unique_to = df['to_address'].nunique()
    unique_addresses = pd.concat([df['from_address'], df['to_address']]).nunique()

    print(f"\nAddress statistics:")
    print(f"Unique sender addresses: {unique_from}")
    print(f"Unique recipient addresses: {unique_to}")
    print(f"Total unique addresses: {unique_addresses}")

def validate_date_format(date_string):

    # Validate date string format (YYYY-MM-DD).

    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_network_config(network_name):
    # Get configuration for common blockchain networks.

    networks = {
        'ethereum': {
            'name': 'Ethereum Mainnet',
            'rpc_url': 'https://eth.llamarpc.com',
            'chain_id': 1,
            'currency': 'ETH',
            'requires_poa': False
        },
        'scroll': {
            'name': 'Scroll',
            'rpc_url': 'https://rpc.scroll.io',
            'chain_id': 534352,
            'currency': 'ETH',
            'requires_poa': True
        },
        'polygon': {
            'name': 'Polygon',
            'rpc_url': 'https://polygon-rpc.com',
            'chain_id': 137,
            'currency': 'MATIC',
            'requires_poa': True
        },
        'arbitrum': {
            'name': 'Arbitrum One',
            'rpc_url': 'https://arb1.arbitrum.io/rpc',
            'chain_id': 42161,
            'currency': 'ETH',
            'requires_poa': False
        },
        'optimism': {
            'name': 'Optimism',
            'rpc_url': 'https://mainnet.optimism.io',
            'chain_id': 10,
            'currency': 'ETH',
            'requires_poa': False
        },
        'bsc': {
            'name': 'Binance Smart Chain',
            'rpc_url': 'https://bsc-dataseed1.binance.org',
            'chain_id': 56,
            'currency': 'BNB',
            'requires_poa': True
        },
        'avalanche': {
            'name': 'Avalanche C-Chain',
            'rpc_url': 'https://api.avax.network/ext/bc/C/rpc',
            'chain_id': 43114,
            'currency': 'AVAX',
            'requires_poa': True
        },
        'base': {
            'name': 'Base',
            'rpc_url': 'https://mainnet.base.org',
            'chain_id': 8453,
            'currency': 'ETH',
            'requires_poa': False
        }
    }

    return networks.get(network_name.lower(), {
        'name': network_name,
        'rpc_url': None,
        'chain_id': None,
        'currency': 'ETH',
        'requires_poa': False
    })
