# ⚡ Energy Consumption Tracker

A comprehensive Python-based application to track, analyze, and visualize household energy consumption. Monitor your appliance usage, identify energy-hungry devices, and make informed decisions to reduce your electricity bills.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔌 Core Functionality
- **Track Appliance Usage** - Record energy consumption with timestamp tracking
- **Appliance Presets** - 15+ common appliances with pre-configured power ratings
- **Custom Electricity Rates** - Support for different electricity pricing
- **Data Persistence** - JSON-based storage for reliable data management

### 📊 Analytics & Reports
- **Summary Statistics** - All-time, weekly, and monthly consumption overview
- **Daily Reports** - Detailed breakdown of daily energy usage
- **Appliance Analysis** - Identify top energy consumers
- **Cost Tracking** - Monitor electricity costs in real-time

### 📈 Visualizations
- **Weekly/Monthly Charts** - Dual-axis graphs showing energy and cost trends
- **Appliance Breakdown** - Pie charts for consumption distribution
- **Hourly Patterns** - Bar charts revealing peak usage hours
- **Comprehensive Reports** - Generate all visualizations at once

### 🛠️ Management Tools
- **Edit Capabilities** - Delete incorrect entries
- **Data Validation** - Input validation to prevent errors
- **Preset Library** - Quick access to common appliance specifications

## 🖼️ Screenshots

```
⚡  ENERGY CONSUMPTION TRACKER
==================================================

📋 Main Menu
========================================
1️⃣   Add Appliance Usage
2️⃣   View Summary Statistics
3️⃣   View Detailed Report (CLI)
4️⃣   View Appliance Analysis
5️⃣   Generate Visual Reports
6️⃣   Delete Usage Entry
7️⃣   View Appliance Presets
8️⃣   Exit
========================================
```

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/energy-tracker.git
cd energy-tracker
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
matplotlib>=3.5.0
```

### Step 3: Create Data Directory

```bash
mkdir data
```

## 💻 Usage

### Starting the Application

```bash
python main.py
```

### Quick Start Guide

#### 1. Add Your First Entry

```
Choose option 1: Add Appliance Usage
Select from presets or enter custom appliance
Enter usage hours (e.g., 2.5)
Enter electricity rate (default: ₹8.5/kWh)
```

#### 2. View Statistics

```
Choose option 2: View Summary Statistics
See all-time, weekly, and monthly summaries
Track average daily consumption
```

#### 3. Generate Reports

```
Choose option 5: Generate Visual Reports
Select report type:
  - Weekly/Monthly trends
  - Appliance breakdown
  - Hourly usage patterns
```

## 📁 Project Structure

```
energy-tracker/
│
├── main.py                 # Main application entry point
├── energy_tracker.py       # Core tracking logic
├── report_generator.py     # Visualization and reporting
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
│
├── data/                  # Data storage directory
│   ├── energy_data.json   # Usage data (auto-generated)
│   ├── energy_report.png  # Generated charts
│   ├── appliance_report.png
│   └── hourly_report.png
│
└── .gitignore            # Git ignore file
```

## ⚙️ Configuration

### Electricity Rate

Default rate: **₹8.5 per kWh**

To change the default rate, edit `energy_tracker.py`:

```python
ELECTRICITY_RATE = 8.5  # Change this value
```

### Appliance Presets

Add custom presets in `energy_tracker.py`:

```python
APPLIANCE_PRESETS = {
    "Your Appliance": 150,  # Power in watts
    # Add more...
}
```

### Data Storage

Data is stored in `data/energy_data.json` with the following structure:

```json
{
  "2025-10-16": [
    {
      "appliance": "Ceiling Fan",
      "power": 75,
      "hours": 8.0,
      "rate": 8.5,
      "energy_kwh": 0.6,
      "cost": 5.1,
      "timestamp": "2025-10-16T14:30:00"
    }
  ]
}
```

## 📖 Examples

### Example 1: Track Daily Fan Usage

```python
# Add 8 hours of ceiling fan usage
Appliance: Ceiling Fan
Hours: 8
Power: 75W
Rate: ₹8.5/kWh

Result: 0.6 kWh, ₹5.10
```

### Example 2: Analyze AC Consumption

```python
# Track air conditioner for 6 hours
Appliance: Air Conditioner (1.5 Ton)
Hours: 6
Power: 1500W
Rate: ₹8.5/kWh

Result: 9.0 kWh, ₹76.50
```

### Example 3: Monthly Cost Analysis

```
View Summary Statistics → Last 30 Days
Total Energy: 245.50 kWh
Total Cost: ₹2,086.75
Average per Day: 8.18 kWh
```

## 🔍 Key Functions

### energy_tracker.py

- `add_usage(appliance, hours, power, rate)` - Record energy usage
- `get_summary(days=None)` - Get consumption summary
- `get_daily_report(target_date=None)` - Detailed daily breakdown
- `get_appliance_analysis()` - Appliance-wise statistics
- `delete_entry(target_date, index)` - Remove incorrect entries

### report_generator.py

- `generate_report(days=7)` - Create energy/cost charts
- `generate_appliance_report()` - Pie chart of appliances
- `generate_hourly_usage_report()` - Hourly usage patterns
- `generate_comprehensive_report()` - All reports at once

## 💡 Tips for Effective Tracking

1. **Record Daily** - Track usage every day for accurate patterns
2. **Use Presets** - Save time with pre-configured appliances
3. **Check Peak Hours** - Identify when you consume most energy
4. **Monitor Top Consumers** - Focus on high-consumption appliances
5. **Set Goals** - Use weekly summaries to track improvements

## 🐛 Troubleshooting

### Issue: "No energy usage data found"

**Solution:** Add at least one usage entry before generating reports.

### Issue: Charts not displaying

**Solution:** Ensure matplotlib is installed:
```bash
pip install matplotlib --upgrade
```

### Issue: Data file corrupted

**Solution:** Delete `data/energy_data.json` and start fresh (backup first!).

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions

- [ ] CSV export functionality
- [ ] Monthly budget alerts
- [ ] Cost prediction models
- [ ] Mobile app integration
- [ ] Database support (SQLite)
- [ ] Multi-user support
- [ ] Web dashboard interface

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aritra Ghosh**
- GitHub: [@aritracodes-69](https://github.com/aritracodes-69)
- Email: aritraghosh.zen23@gmail.com

## 🙏 Acknowledgments

- Thanks to the Python community
- Matplotlib for excellent visualization tools
- All contributors and users

## 📞 Support

For support, please:
- Open an issue on GitHub
- Email: aritraghosh.zen23@gmail.com

---

<div align="center">

**⚡ Save Energy, Save Money, Save the Planet! 🌍**

Made with ❤️ and Python

[⬆ Back to Top](#-energy-consumption-tracker)

</div>