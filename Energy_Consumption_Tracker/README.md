# Daily Energy Consumption Tracker 🔌⚡

A comprehensive Python application to track household appliance usage and calculate daily/weekly energy consumption and estimated electricity costs.

## Features

✨ **Key Features:**
- 📊 Track energy consumption for 12 common household appliances
- 💰 Calculate daily, weekly, and monthly electricity costs
- 📈 Detailed consumption breakdown by appliance
- 💾 Save and load your data
- 🎯 Quick setup mode for easy data entry
- 📋 Identify top energy consumers
- ⚙️ Customizable electricity rates
- ✅ Simple and focused appliance list

## Installation

No external dependencies required! This project uses only Python standard library.

```bash
# Clone or download the project
cd Energy_Consumption_Tracker

# Run the application
python energy_tracker.py
```

**Requirements:**
- Python 3.6 or higher

## Usage

### Interactive Mode

Run the main application:

```bash
python energy_tracker.py
```

### Menu Options

1. **View available appliances** - See all appliances with their power ratings and tracking status
2. **Remove appliance from tracking** - Stop tracking a specific appliance
3. **Add/Update appliance usage** - Set or update hours of daily usage for any appliance
4. **View consumption summary** - See detailed energy and cost breakdown
5. **Set electricity rate** - Update your local electricity rate
6. **Save data** - Save your current data to file
7. **Load data** - Load previously saved data
8. **Quick setup** - Guided entry for all appliances
0. **Exit** - Exit the application

### Quick Setup Mode

The easiest way to get started:

1. Select option `9` from the main menu
2. Go through each appliance category
3. Enter daily usage hours (or press Enter to skip)
4. View your consumption summary

### Programmatic Usage

You can also use the `EnergyTracker` class in your own scripts:

```python
from energy_tracker import EnergyTracker

# Initialize tracker with your electricity rate
tracker = EnergyTracker(electricity_rate=0.15)  # $0.15 per kWh

# Set appliance usage
tracker.set_appliance_usage("Refrigerator", 24)  # 24 hours/day
tracker.set_appliance_usage("Air Conditioner (1.5 Ton)", 8)  # 8 hours/day
tracker.set_appliance_usage("Television (LED)", 5)  # 5 hours/day

# Calculate consumption
daily_kwh = tracker.calculate_daily_consumption()
daily_cost = tracker.calculate_daily_cost()

print(f"Daily consumption: {daily_kwh:.2f} kWh")
print(f"Daily cost: ${daily_cost:.2f}")

# Display full summary
tracker.display_summary()

# Save your data
tracker.save_data()
```

## Available Appliances

The tracker includes 12 common household appliances:

| Appliance       | Power Rating |
|-----------------|--------------|
| Refrigerator    | 150W         |
| Microwave       | 1200W        |
| Lamp            | 60W          |
| Hair Dryer      | 1500W        |
| Radio           | 10W          |
| TV              | 120W         |
| Computer        | 200W         |
| Ceiling Fan     | 75W          |
| Air Conditioner | 1500W        |
| Heater          | 1500W        |
| Treadmill       | 700W         |
| Stove/Oven      | 3000W        |

**Note:** You can only track appliances from this list. Custom appliances cannot be added.

## Example Output

```
================================================================================
                       ENERGY CONSUMPTION SUMMARY
================================================================================
Electricity Rate: $0.120 per kWh
Report Generated: 2025-10-11 14:30:00
================================================================================

DETAILED BREAKDOWN BY APPLIANCE:
--------------------------------------------------------------------------------
Appliance                      Daily (kWh)     Weekly (kWh)    Daily Cost     
--------------------------------------------------------------------------------
Refrigerator                         3.600          25.200      $       0.43
Air Conditioner (1.5 Ton)           12.000          84.000      $       1.44
Water Heater (Geyser)                2.000          14.000      $       0.24
Television (LED)                     0.500           3.500      $       0.06
LED Bulb (10W)                       0.050           0.350      $       0.01
--------------------------------------------------------------------------------

TOTAL                               18.150         127.050      $       2.18
================================================================================

📊 COST SUMMARY:
   Daily Cost:    $2.18
   Weekly Cost:   $15.26
   Monthly Cost:  $65.40 (estimated)
   Yearly Cost:   $795.70 (estimated)

🔥 Top Energy Consumer: Air Conditioner (1.5 Ton)
   Consumes 12.000 kWh/day (66.1% of total)
================================================================================
```

## Data Persistence

Your data is automatically saved to `energy_data.json` when you use the "Save data" option. The file includes:
- Your electricity rate
- Daily usage hours for each appliance
- Last update timestamp

## Customization

### Setting Your Electricity Rate

Default rate is $0.12/kWh. To change it:

1. Select option `5` from the main menu
2. Enter your local electricity rate in $/kWh

**How to find your rate:**
- Check your electricity bill
- Look for "per kWh" or "per unit" charge
- Typical rates range from $0.08 to $0.30 per kWh

## Tips for Accurate Tracking

1. **24-hour appliances**: Refrigerators, routers typically run 24/7
2. **Variable usage**: For appliances used multiple times, estimate total daily hours
3. **Seasonal changes**: Update AC/heating usage based on season
4. **Standby power**: Many devices consume power even when "off"
5. **Check your bills**: Compare calculated costs with actual bills to validate

## Understanding Energy Consumption

**kWh (Kilowatt-hour)**: Unit of energy consumption
- 1 kWh = Running a 1000W appliance for 1 hour
- Example: 100W bulb for 10 hours = 1 kWh

**Formula:**
```
Energy (kWh) = Power (Watts) × Time (Hours) ÷ 1000
Cost ($) = Energy (kWh) × Rate ($/kWh)
```

## Energy Saving Tips 💡

Based on your consumption summary:
- Focus on top energy consumers first
- Replace high-wattage bulbs with LEDs
- Use AC wisely (biggest consumer in most homes)
- Unplug chargers when not in use
- Use natural light during the day
- Regular appliance maintenance improves efficiency

## Contributing

Feel free to enhance this tracker with additional features:
- Graphs and visualizations
- Historical tracking
- Energy-saving recommendations
- Bill prediction accuracy
- Multi-user support
- Web interface

## License

MIT License - Feel free to use and modify!

## Author

Created as part of Mini Python Projects collection

## Support

For issues or questions:
1. Check that Python 3.6+ is installed
2. Ensure write permissions in the directory
3. Verify your electricity rate is correct
4. Contact for bugs or feature requests

---

**Stay energy conscious! 💚 Every kWh saved helps the planet! 🌍**

