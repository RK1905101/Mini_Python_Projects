"""
Configuration script for blockchain scraper.
This script helps users set up their environment and validate their configuration.
"""

import os
import sys
from datetime import datetime, timedelta
import argparse

def create_env_file():
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return

    if not os.path.exists('.env-example'):
        print("✗ .env-example file not found")
        return

    # Copy .env-example to .env
    with open('.env-example', 'r') as example_file:
        content = example_file.read()

    with open('.env', 'w') as env_file:
        env_file.write(content)

    print("✓ Created .env file from .env-example")
    print("  Please edit .env file to configure your settings")

def validate_rpc_connection(network_name, rpc_url):
    """Validate RPC connection to a blockchain network."""
    try:
        from web3 import Web3
        try:
            from web3.middleware.geth_poa import geth_poa_middleware
        except ImportError:
            try:
                from web3.middleware import ExtraDataToPOAMiddleware
                geth_poa_middleware = ExtraDataToPOAMiddleware
            except ImportError:
                geth_poa_middleware = None

        w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Add PoA middleware for networks that require it
        if network_name.lower() in ['scroll', 'polygon', 'bsc', 'avalanche'] and geth_poa_middleware:
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if w3.is_connected():
            latest_block = w3.eth.block_number
            chain_id = w3.eth.chain_id
            print(f"✓ Connected to {network_name}")
            print(f"  Chain ID: {chain_id}")
            print(f"  Latest block: {latest_block}")
            return True
        else:
            print(f"✗ Failed to connect to {network_name} at {rpc_url}")
            return False

    except ImportError:
        print("✗ web3 library not installed. Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Connection error for {network_name}: {str(e)}")
        return False

def validate_date_range(start_date, end_date):
    """Validate date range format and logic."""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        if start >= end:
            print(f"✗ Start date ({start_date}) must be before end date ({end_date})")
            return False

        if end > datetime.now():
            print(f"⚠ End date ({end_date}) is in the future")

        days_diff = (end - start).days
        if days_diff > 365:
            print(f"⚠ Date range is {days_diff} days. Large ranges may take a long time to process")

        print(f"✓ Date range valid: {start_date} to {end_date} ({days_diff} days)")
        return True

    except ValueError:
        print(f"✗ Invalid date format. Use YYYY-MM-DD format")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        ('web3', 'web3'),
        ('pandas', 'pandas'),
        ('python-dotenv', 'dotenv'),
        ('requests', 'requests')
    ]

    missing_packages = []

    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name}")
            missing_packages.append(package_name)

    if missing_packages:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    return True

def validate_configuration():
    """Validate the current configuration."""
    print("=== Validating Configuration ===")

    # Check dependencies
    print("\nChecking dependencies:")
    if not check_dependencies():
        return False

    # Check .env file
    print("\nChecking configuration file:")
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        create_env_file()
        return False

    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()

        network_name = os.getenv('NETWORK_NAME', 'ethereum')
        rpc_url = os.getenv('RPC_URL')
        start_date = os.getenv('START_DATE')
        end_date = os.getenv('END_DATE')
        batch_size = os.getenv('BATCH_SIZE', '500')
        block_interval = os.getenv('BLOCK_INTERVAL', '1')

        print(f"✓ Loaded configuration from .env")
        print(f"  Network: {network_name}")
        print(f"  RPC URL: {rpc_url}")
        print(f"  Date range: {start_date} to {end_date}")
        print(f"  Batch size: {batch_size}")
        print(f"  Block interval: {block_interval}")

    except ImportError:
        print("✗ python-dotenv not installed")
        return False
    except Exception as e:
        print(f"✗ Error loading .env file: {str(e)}")
        return False

    # Validate date range
    print("\nValidating date range:")
    if not start_date or not end_date:
        print("✗ START_DATE and END_DATE must be set in .env file")
        return False

    if not validate_date_range(start_date, end_date):
        return False

    # Test RPC connection
    print(f"\nTesting RPC connection:")
    if not rpc_url:
        print("✗ RPC_URL not set in .env file")
        return False

    if not validate_rpc_connection(network_name, rpc_url):
        return False

    print("\n✓ All validations passed!")
    return True

def interactive_setup():
    print("=== Blockchain Scraper Setup Wizard ===")

    # Network selection
    networks = {
        '1': ('ethereum', 'https://eth.llamarpc.com'),
        '2': ('scroll', 'https://rpc.scroll.io'),
        '3': ('polygon', 'https://polygon-rpc.com'),
        '4': ('arbitrum', 'https://arb1.arbitrum.io/rpc'),
        '5': ('optimism', 'https://mainnet.optimism.io'),
        '6': ('bsc', 'https://bsc-dataseed1.binance.org'),
        '7': ('avalanche', 'https://api.avax.network/ext/bc/C/rpc'),
        '8': ('base', 'https://mainnet.base.org'),
        '9': ('custom', None)
    }

    print("\nSelect blockchain network:")
    for key, (name, rpc) in networks.items():
        print(f"{key}. {name.capitalize()}")

    choice = input("Enter choice (1-9): ").strip()

    if choice not in networks:
        print("Invalid choice")
        return

    network_name, rpc_url = networks[choice]

    if choice == '9':  # Custom
        network_name = input("Enter network name: ").strip()
        rpc_url = input("Enter RPC URL: ").strip()

    print(f"\nDate range configuration:")
    default_start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    default_end = datetime.now().strftime('%Y-%m-%d')

    start_date = input(f"Start date (YYYY-MM-DD) [{default_start}]: ").strip() or default_start
    end_date = input(f"End date (YYYY-MM-DD) [{default_end}]: ").strip() or default_end

    if not validate_date_range(start_date, end_date):
        return

    batch_size = input("Batch size [500]: ").strip() or "500"
    block_interval = input("Block interval [1]: ").strip() or "1"

    env_content = f"""# Blockchain Network Configuration
NETWORK_NAME={network_name}
RPC_URL={rpc_url}

# Date Range Configuration (YYYY-MM-DD format)
START_DATE={start_date}
END_DATE={end_date}

# Block Configuration
BATCH_SIZE={batch_size}
BLOCK_INTERVAL={block_interval}
MAX_BLOCKS_PER_REQUEST=100

# Output Configuration
OUTPUT_DIR=output
TEMP_DIR=temp_data

# API Rate Limiting
REQUEST_DELAY=0.1
MAX_RETRIES=3
"""

    with open('.env', 'w') as f:
        f.write(env_content)

    print(f"\n✓ Configuration saved to .env")

    # Test connection
    print(f"\nTesting connection...")
    if validate_rpc_connection(network_name, rpc_url):
        print(f"\n✓ Setup complete! You can now run the scraper with:")
        print(f"python main.py")
    else:
        print(f"\n⚠ Setup complete but connection test failed.")
        print(f"Please check your RPC URL and network settings.")

def main():
    parser = argparse.ArgumentParser(description='Blockchain Scraper Configuration')
    parser.add_argument('--validate', action='store_true', help='Validate current configuration')
    parser.add_argument('--setup', action='store_true', help='Run interactive setup wizard')
    parser.add_argument('--create-env', action='store_true', help='Create .env file from template')

    args = parser.parse_args()

    if args.validate:
        validate_configuration()
    elif args.setup:
        interactive_setup()
    elif args.create_env:
        create_env_file()
    else:
        print("Blockchain Scraper Configuration Tool")
        print("\nOptions:")
        print("  --validate    Validate current configuration")
        print("  --setup       Run interactive setup wizard")
        print("  --create-env  Create .env file from template")
        print("\nExample usage:")
        print("  python configure.py --setup")
        print("  python configure.py --validate")

if __name__ == "__main__":
    main()
