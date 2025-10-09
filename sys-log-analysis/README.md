# System Log Analysis Tool

## Project Description

This is a mini project for analyzing system logs that extracts and analyzes error messages and user activities from system log files. The program consists of two main modules that work sequentially to generate analysis reports in CSV and HTML formats.

## Main Features

### 1. System Log Analysis (`main.py`)
- **Error Message Extraction**: Identifies and counts the frequency of each type of error message
- **User Activity Analysis**: Tracks INFO and ERROR activities for each user
- **Data Grouping**: Groups data based on error types and user activities
- **CSV Export**: Generates two CSV files for further analysis

### 2. CSV to HTML Conversion (`csv_to_html.py`)
- **Data Visualization**: Converts CSV files into neat HTML tables
- **Automatic Styling**: Applies CSS styling for professional appearance
- **Responsive**: HTML tables with alternating row colors for easy reading

## Types of Data That Can Be Analyzed

This program is designed to analyze **system log files** with standard format containing:

### Supported Log Format
```
Timestamp hostname service: LEVEL Message (username)
```

**Example:**
```
Jan 31 00:09:39 ubuntu.local ticky: INFO Created ticket [#4217] (mdouglas)
Jan 31 00:21:30 ubuntu.local ticky: ERROR The ticket was modified while updating (breee)
```

### Types of Messages Analyzed
- **INFO Messages**: Normal information messages (ticket creation, comments, ticket closure)
- **ERROR Messages**: System error messages classified into:
  - Timeout while retrieving information
  - Connection to DB failed
  - Tried to add information to closed ticket
  - Permission denied while closing ticket
  - The ticket was modified while updating
  - Ticket doesn't exist

### Data Output
1. **User Statistics** (`user_statistics.csv`):
   - Username
   - Number of INFO messages per user
   - Number of ERROR messages per user

2. **Error Messages** (`error_message.csv`):
   - Type of error message
   - Frequency of occurrence for each error

## Usage Instructions

### Prerequisites
- Python 3.x
- Standard Python modules: `os`, `re`, `sys`, `operator`, `csv`

### Step-by-Step Usage

#### 1. Data Preparation
```bash
# Ensure log file is located in data/ folder
data/syslog.log
```

#### 2. Running Log Analysis
```bash
python main.py
```

**Generated output:**
- `data/user_statistics.csv` - Activity statistics per user
- `data/error_message.csv` - Error message statistics

#### 3. Convert to HTML (Optional)
```bash
# For user statistics
python csv_to_html.py data/user_statistics.csv data/user_statistics.html

# For error statistics
python csv_to_html.py data/error_message.csv data/error_message.html
```

### Complete Usage Example
```bash
# 1. Analyze logs
python main.py

# 2. Create HTML reports
python csv_to_html.py data/user_statistics.csv reports/user_report.html
python csv_to_html.py data/error_message.csv reports/error_report.html
```

## File Structure

```
sys-log-analysis/
│
├── main.py                 # Main script for log analysis
├── csv_to_html.py         # CSV to HTML conversion script
├── README.md              # Project documentation
│
└── data/
    ├── syslog.log         # Input log file
    ├── user_statistics.csv # User statistics output
    ├── error_message.csv  # Error statistics output
    ├── user_statistics.html # User HTML report (optional)
    └── error_message.html # Error HTML report (optional)
```

## Main Function Explanations

### `main.py` - Main Functions:
- `search_file()`: Reads each log line and classifies INFO/ERROR
- `find_error()`: Extracts and counts types of error messages
- `add_user_list()`: Tracks activities per user
- `sort_list()`: Sorts data based on specific criteria
- `write_csv()`: Writes analysis results to CSV files

### `csv_to_html.py` - Main Functions:
- `process_csv()`: Reads and processes CSV files
- `data_to_html()`: Converts data to HTML format
- `write_html_file()`: Saves HTML files with CSS styling

## Sample Output

### User Statistics
| Username | INFO | ERROR |
|----------|------|-------|
| mdouglas | 2    | 2     |
| noel     | 4    | 2     |
| blossom  | 2    | 4     |

### Error Messages
| Error | Count |
|-------|-------|
| Timeout while retrieving information | 15 |
| Connection to DB failed | 13 |
| Tried to add information to closed ticket | 12 |

## Benefits and Use Cases

1. **System Monitoring**: Monitor system health based on error frequency
2. **User Analysis**: Identify users who frequently encounter problems
3. **Troubleshooting**: Help identify the most common system issues
4. **Reporting**: Create visual reports for stakeholders
5. **Audit Trail**: Track user activities in the system

## Development Notes

- Program uses regex pattern matching for data extraction
- Data is sorted based on frequency (errors) and alphabetically (users)
- HTML output uses embedded CSS styling
- Error handling available for files not found

## Contributing

For further development, consider adding:
- Support for other log formats
- Interactive web dashboard
- Time-series analysis
- Alerting system
- Export to other formats (JSON, XML)
