# Universal Blockchain Transaction Scraper

A flexible and configurable blockchain transaction scraper that works with multiple EVM-compatible networks. This tool specializes in extracting EOA-to-EOA (Externally Owned Account) transactions for sybil detection and analysis.

## Features

- **Multi-Network Support**: Works with Ethereum, Scroll, Polygon, Arbitrum, Optimism, BSC, Avalanche, Base, and custom networks
- **Flexible Date/Block Ranges**: Scrape by date range or specific block numbers
- **Configurable Block Intervals**: Skip blocks to speed up scraping or sample data
- **Environment-Based Configuration**: Easy setup using `.env` files
- **Batch Processing**: Efficient handling of large datasets with configurable batch sizes
- **Comprehensive Analysis**: Built-in transaction summaries and statistics
- **Resume Capability**: Temporary file system for handling interruptions
- **Command Line Interface**: Full CLI support with various options

## ⚠️ Important: VPS Recommendation for Large Data

**For small-scale testing** (< 1000 blocks): Use your local machine
**For large-scale scraping** (> 10,000 blocks, multiple days/months): **Use a VPS**

Large blockchain data scraping can take hours to days and requires stable internet connection. A VPS ensures:
- ✅ Uninterrupted 24/7 processing
- ✅ Better network stability
- ✅ Higher performance and resources
- ✅ Cost-effective for long-running tasks
- ✅ Ability to use your local computer for other work

See the [VPS Deployment Guide](#vps-deployment-for-large-scale-scraping) below for detailed setup instructions.

## Supported Networks

| Network | Chain ID | Native Currency | Default RPC |
|---------|----------|-----------------|-------------|
| Ethereum | 1 | ETH | https://eth.llamarpc.com |
| Scroll | 534352 | ETH | https://rpc.scroll.io |
| Polygon | 137 | MATIC | https://polygon-rpc.com |
| Arbitrum | 42161 | ETH | https://arb1.arbitrum.io/rpc |
| Optimism | 10 | ETH | https://mainnet.optimism.io |
| BSC | 56 | BNB | https://bsc-dataseed1.binance.org |
| Avalanche | 43114 | AVAX | https://api.avax.network/ext/bc/C/rpc |
| Base | 8453 | ETH | https://mainnet.base.org |

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd blockchain-transaction-scraping
   ```

2. **Install dependencies**:
    ```bash
   python -m venv venv
   ```
   ```bash
   venv\Scripts\activate
   ```
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**:
   ```bash
   # Option 1: Interactive setup (recommended)
   python configure.py --setup

   # Option 2: Manual setup
   python configure.py --create-env
   # Then edit .env file manually
   ```

## Quick Start Guide

### 🔥 Local Machine (Testing & Small Data)

**Perfect for**: Learning, testing, small samples (< 1000 blocks)

```bash
# 1. Quick test (recommended first step)
python demo.py

# 2. Small sample (1 day, every 10th block)
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-02 --block-interval 10

# 3. Specific block range (fast)
python main.py --network scroll --start-block 22881000 --end-block 22881500
```

### 🚀 VPS Deployment (Production & Large Data)

**Perfect for**: Research, analysis, large datasets (> 10,000 blocks)

```bash
# VPS Setup (Ubuntu)
sudo apt update && sudo apt install python3 python3-pip python3-venv git screen -y
git clone <repository-url>
cd blockchain-transaction-scraping
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Large-scale scraping (in screen session)
screen -S scraper
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-31
# Detach with Ctrl+A, D
```

### 📊 When to Use What?

| Data Size | Time Estimate | Recommendation | Example Command |
|-----------|---------------|----------------|-----------------|
| 10-100 blocks | Minutes | Local | `python demo.py` |
| 1-7 days sampled | 10-30 min | Local | `--block-interval 10` |
| 1 month full | 2-8 hours | VPS | `--start-date 2024-01-01 --end-date 2024-01-31` |
| 3+ months | 8+ hours | VPS | Multiple monthly runs |
| Full year | 1-3 days | VPS | Background processing |

## Configuration

### Environment Variables

Create a `.env` file (or copy from `.env-example`) with the following variables:

```env
# Blockchain Network Configuration
NETWORK_NAME=ethereum
RPC_URL=https://eth.llamarpc.com

# Date Range Configuration (YYYY-MM-DD format)
START_DATE=2024-01-01
END_DATE=2024-01-31

# Block Configuration
BATCH_SIZE=500
BLOCK_INTERVAL=1
MAX_BLOCKS_PER_REQUEST=100

# Output Configuration
OUTPUT_DIR=output
TEMP_DIR=temp_data

# API Rate Limiting
REQUEST_DELAY=0.1
MAX_RETRIES=3
```

### Configuration Options

- **NETWORK_NAME**: Blockchain network identifier
- **RPC_URL**: RPC endpoint for blockchain connection
- **START_DATE/END_DATE**: Date range for scraping (YYYY-MM-DD format)
- **BATCH_SIZE**: Number of transactions to process before saving to temp file
- **BLOCK_INTERVAL**: Skip blocks (1 = every block, 2 = every other block, etc.)
- **REQUEST_DELAY**: Delay between API requests (seconds)
- **MAX_RETRIES**: Maximum retry attempts for failed requests

## Usage

### Basic Usage

```bash
# Use configuration from .env file
python main.py

# Scrape specific network
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-31

# Scrape by block range
python main.py --network scroll --start-block 1000000 --end-block 1100000

# Show network information
python main.py --network polygon --info
```

### Advanced Usage

```bash
# Custom RPC endpoint
python main.py --network ethereum --rpc-url https://mainnet.infura.io/v3/YOUR_KEY

# Large batch size for faster processing
python main.py --batch-size 1000

# Sample every 10th block
python main.py --block-interval 10

# Show available networks
python main.py --help-networks
```

### Configuration Management

```bash
# Validate current configuration
python configure.py --validate

# Interactive setup wizard
python configure.py --setup

# Create .env from template
python configure.py --create-env
```

## Output

### CSV Output

The scraper generates CSV files with the following columns:

- `hash`: Transaction hash
- `block_number`: Block number
- `from_address`: Sender address
- `to_address`: Recipient address
- `value_[currency]`: Transfer amount in native currency
- `gas_price_gwei`: Gas price in Gwei
- `gas_used`: Gas consumed
- `fee_[currency]`: Transaction fee in native currency
- `timestamp`: Transaction timestamp
- `network`: Blockchain network name
- `status`: Transaction status (1 = success)
- `is_eoa_to_eoa`: Always true (filter flag)

### Analysis Summary

The tool provides comprehensive analysis including:

- Total transactions and volume
- Fee statistics
- Gas price analysis
- Daily transaction distribution
- Address activity patterns
- Top active addresses

## Examples

### Example 1: Scrape Ethereum for January 2024

```bash
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-31
```

### Example 2: Sample Polygon Every 5 Blocks

```bash
python main.py --network polygon --start-date 2024-01-01 --end-date 2024-01-07 --block-interval 5
```

### Example 3: Scrape Specific Block Range on Arbitrum

```bash
python main.py --network arbitrum --start-block 150000000 --end-block 150010000
```

### Example 4: Custom Network Configuration

```bash
python main.py --network custom --rpc-url https://rpc.custom-network.com --start-date 2024-01-01 --end-date 2024-01-02
```

### Example 5: VPS Large-Scale Scraping

**For local testing (small data)**:
```bash
# Quick test - 10 blocks only
python demo.py

# Small sample - 1 week with sampling
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-07 --block-interval 10
```

**For VPS deployment (large data)**:
```bash
# Full month scraping (recommended for VPS)
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-31

# Multiple networks in parallel (VPS only)
screen -S eth-scraper
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-12-31
# Detach with Ctrl+A, D

screen -S polygon-scraper
python main.py --network polygon --start-date 2024-01-01 --end-date 2024-12-31
# Detach with Ctrl+A, D

# Monitor progress
screen -list                    # List all sessions
screen -r eth-scraper          # Reattach to ethereum scraper
tail -f output/*.csv           # Watch output files
```

**VPS batch processing example**:
```bash
# Create batch script for year-long scraping
cat > scrape_year.sh << 'EOF'
#!/bin/bash
networks=("ethereum" "polygon" "arbitrum" "optimism")
for network in "${networks[@]}"; do
    echo "Starting $network scraping..."
    python main.py --network $network --start-date 2024-01-01 --end-date 2024-12-31
    echo "$network scraping completed"
done
EOF

chmod +x scrape_year.sh
nohup ./scrape_year.sh > batch_scraping.log 2>&1 &
```

## Project Structure

```
├── main.py                 # Main application entry point
├── configure.py           # Configuration and setup tool
├── .env-example          # Environment variables template
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── src/
│   ├── __init__.py
│   ├── blockchain_scraper.py     # Main scraper class
│   ├── utils.py                  # Utility functions
├── output/              # Generated CSV files (created automatically)
└── temp_data/          # Temporary files during processing (created automatically)
```

## Error Handling

The scraper includes robust error handling:

- **Connection Issues**: Automatic retry with exponential backoff
- **Rate Limiting**: Configurable delays between requests
- **Block Processing**: Continues on individual block failures
- **Data Validation**: Filters invalid transactions
- **Memory Management**: Batch processing to handle large datasets

## Performance Tips

1. **Optimize Block Interval**: Use `--block-interval 5` or higher for sampling
2. **Increase Batch Size**: Use `--batch-size 1000` for better performance
3. **Use Faster RPC**: Configure premium RPC endpoints for better speed
4. **Smaller Date Ranges**: Process smaller chunks for faster results
5. **Monitor Resources**: Large ranges may require significant time and storage

## VPS Deployment for Large-Scale Scraping

For scraping large amounts of blockchain data (thousands of blocks or long date ranges), it's highly recommended to use a VPS (Virtual Private Server) instead of running on your local machine. Here's why and how:

### Why Use VPS for Large Scraping?

1. **Uninterrupted Processing**: VPS runs 24/7 without local computer shutdowns
2. **Better Network Stability**: Dedicated server connection with minimal interruptions
3. **Higher Performance**: More CPU cores and RAM for faster processing
4. **Background Processing**: Can run scraping while using your local computer for other tasks
5. **Cost Effective**: Often cheaper than running local machine for days/weeks
6. **Scalability**: Can easily upgrade resources when needed

### Recommended VPS Specifications

For blockchain scraping, consider these minimum specifications:

**Small Scale (1-30 days, 1 network)**:
- 2 CPU cores
- 4GB RAM
- 50GB SSD storage
- Ubuntu 20.04 LTS

**Medium Scale (1-3 months, multiple networks)**:
- 4 CPU cores
- 8GB RAM
- 100GB SSD storage
- Ubuntu 20.04 LTS

**Large Scale (6+ months, multiple networks)**:
- 8 CPU cores
- 16GB RAM
- 200GB SSD storage
- Ubuntu 20.04 LTS

### VPS Setup Guide

#### 1. Choose VPS Provider
Popular options for blockchain scraping:
- **DigitalOcean**: Starting from $6/month, good performance
- **Vultr**: Starting from $5/month, multiple locations
- **Linode**: Starting from $5/month, reliable network
- **AWS EC2**: Pay-as-you-go, highly scalable
- **Google Cloud**: Free tier available, powerful instances

#### 2. VPS Initial Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install python3 python3-pip python3-venv git -y

# Clone repository
git clone <your-repository-url>
cd blockchain-transaction-scraping

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure for Long-Running Tasks
```bash
# Install screen for background processing
sudo apt install screen -y

# Create a screen session
screen -S blockchain-scraper

# Configure environment
python configure.py --setup

# Edit .env for your target data
nano .env
```

#### 4. Optimize Configuration for VPS
```env
# VPS-optimized settings in .env
BATCH_SIZE=2000              # Larger batches for better performance
BLOCK_INTERVAL=1             # Adjust based on your needs
REQUEST_DELAY=0.05           # Faster requests (be careful with rate limits)
MAX_RETRIES=5                # More retries for stability
```

#### 5. Run Large Scraping Tasks
```bash
# For very large date ranges, split into chunks
python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-01-31
python main.py --network ethereum --start-date 2024-02-01 --end-date 2024-02-29
# ... continue for other months

# Or use nohup for background processing
nohup python main.py --network ethereum --start-date 2024-01-01 --end-date 2024-12-31 > scraping.log 2>&1 &
```

### VPS Best Practices

1. **Monitor Resources**: Use `htop`, `free -h`, `df -h` to monitor CPU, RAM, and disk usage
2. **Use Screen/Tmux**: Always run long tasks in screen sessions to prevent disconnection issues
3. **Regular Backups**: Backup your data and configuration files regularly
4. **Set Up Monitoring**: Configure alerts for when scraping completes or fails
5. **Optimize Network**: Choose VPS location close to your RPC endpoints for better latency
6. **Cost Management**: Stop VPS when not needed, use spot instances if available

### Sample VPS Commands
```bash
# Check system resources
htop                    # CPU and RAM usage
df -h                   # Disk usage
free -h                 # Memory usage

# Screen session management
screen -S scraper       # Create new session
screen -r scraper       # Reattach to session
Ctrl+A, D              # Detach from session
screen -list           # List all sessions

# Monitor scraping progress
tail -f scraping.log    # Watch log file in real-time
ls -la output/         # Check generated files
du -sh output/         # Check output directory size
```

### Cost Estimation

**Example costs for 1 year of Ethereum data scraping**:
- Small VPS (4GB RAM): ~$50-70/month
- Medium VPS (8GB RAM): ~$80-120/month
- Storage: ~$10-20/month for 200GB
- **Total**: $60-140/month depending on configuration

**Compared to local costs**:
- Electricity for running PC 24/7: ~$30-50/month
- Wear and tear on local hardware
- Internet stability issues
- Cannot use computer for other tasks

### When NOT to Use VPS

Use local machine if:
- Scraping small amounts of data (<1000 blocks)
- Testing and development
- One-time quick analysis
- Budget constraints
- Learning and experimenting

## Performance & Time Estimates

### Processing Speed Factors

The scraping speed depends on several factors:
- **Network Activity**: Busier networks = more transactions to process
- **Block Interval**: Sampling every 5th block = 5x faster
- **RPC Speed**: Premium endpoints are significantly faster
- **System Resources**: More CPU/RAM = faster processing
- **Batch Size**: Larger batches = better efficiency

### Time Estimates (Approximate)

**Local Machine** (4GB RAM, regular RPC):
| Data Range | Block Interval | Est. Time | EOA Transactions* |
|------------|----------------|-----------|-------------------|
| 10 blocks | 1 | 30 seconds | 1-5 |
| 100 blocks | 1 | 3-5 minutes | 10-50 |
| 1 day (7,200 blocks) | 1 | 2-4 hours | 500-2,000 |
| 1 day | 10 | 15-30 minutes | 50-200 |
| 1 week | 10 | 2-4 hours | 350-1,400 |
| 1 month | 1 | 8-24 hours | 15,000-60,000 |

**VPS** (8GB RAM, fast RPC):
| Data Range | Block Interval | Est. Time | EOA Transactions* |
|------------|----------------|-----------|-------------------|
| 1 day | 1 | 30-60 minutes | 500-2,000 |
| 1 week | 1 | 3-6 hours | 3,500-14,000 |
| 1 month | 1 | 12-24 hours | 15,000-60,000 |
| 3 months | 1 | 2-4 days | 45,000-180,000 |
| 1 year | 1 | 1-2 weeks | 180,000-720,000 |

*EOA transaction counts vary significantly by network and time period

### Storage Requirements

| Data Range | CSV Size | Temp Files | Total Storage |
|------------|----------|------------|---------------|
| 1 day | 50-200 KB | 10-50 KB | ~500 KB |
| 1 week | 350KB-1.4MB | 70-300 KB | ~3 MB |
| 1 month | 1.5-6 MB | 300KB-1.2MB | ~15 MB |
| 3 months | 4.5-18 MB | 1-4 MB | ~45 MB |
| 1 year | 18-72 MB | 4-15 MB | ~180 MB |

### Network Comparison (Activity Level)

**High Activity** (More EOA transactions):
- Ethereum: Highest volume, most EOA-to-EOA transactions
- BSC: High volume, many simple transfers
- Polygon: High volume, lower gas fees encourage transfers

**Medium Activity**:
- Arbitrum: Growing ecosystem, moderate EOA activity
- Avalanche: Decent volume, mixed transaction types
- Base: Newer network, increasing adoption

**Lower Activity** (Fewer EOA transactions):
- Scroll: Newer L2, growing but smaller volume
- Optimism: More contract interactions than simple transfers

### Optimization Tips by Scale

**Small Scale (Local)**:
```bash
# Quick sampling for analysis
--block-interval 20        # Sample every 20th block
--batch-size 100          # Smaller batches for responsiveness
```

**Medium Scale (Local/Small VPS)**:
```bash
# Balanced speed and completeness
--block-interval 5         # Sample every 5th block
--batch-size 500          # Default batch size
```

**Large Scale (VPS)**:
```bash
# Maximum throughput
--block-interval 1         # Every block for completeness
--batch-size 2000         # Large batches for efficiency
REQUEST_DELAY=0.05        # Faster requests (in .env)
```

## Troubleshooting

### Common Issues

1. **Connection Failed**:
   - Check RPC URL and network connectivity
   - Try alternative RPC endpoints
   - Verify network name matches configuration

2. **Rate Limited**:
   - Increase `REQUEST_DELAY` in .env
   - Use premium RPC endpoints
   - Reduce `BATCH_SIZE`

3. **Out of Memory**:
   - Reduce `BATCH_SIZE`
   - Process smaller date ranges
   - Increase system memory

4. **No Transactions Found**:
   - Verify date range is valid
   - Check if network was active during the period
   - Try different block ranges

### Debug Commands

```bash
# Test network connection
python configure.py --validate

# Show network information
python main.py --network ethereum --info

# Check available networks
python main.py --help-networks
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes. Always respect the terms of service of RPC providers and be mindful of rate limits. The accuracy of data depends on the reliability of the RPC endpoints used.
