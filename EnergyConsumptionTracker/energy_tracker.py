import json
import os
from datetime import date, datetime, timedelta
from collections import defaultdict

DATA_FILE = "data/energy_data.json"
ELECTRICITY_RATE = 8.5  # ₹ per kWh (default)

# Common appliance presets (in watts)
APPLIANCE_PRESETS = {
    "LED Bulb": 10,
    "CFL Bulb": 15,
    "Incandescent Bulb": 60,
    "Ceiling Fan": 75,
    "Table Fan": 50,
    "Air Conditioner (1.5 Ton)": 1500,
    "Refrigerator": 150,
    "TV (LED)": 100,
    "Washing Machine": 500,
    "Microwave": 1000,
    "Water Heater": 2000,
    "Laptop": 50,
    "Desktop Computer": 200,
    "Iron": 1000,
    "Water Pump": 750,
}


# ---------------- Utility Functions ---------------- #

def load_data():
    """Load energy usage data from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except json.JSONDecodeError:
        print("⚠️ Data file is corrupted or empty. Starting fresh.")
        return {}


def save_data(data):
    """Save energy usage data to JSON file."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def validate_input(appliance, power_watts, hours_used):
    """Validate input parameters."""
    if not appliance or not appliance.strip():
        raise ValueError("Appliance name cannot be empty")
    if power_watts <= 0:
        raise ValueError("Power consumption must be positive")
    if hours_used <= 0:
        raise ValueError("Hours used must be positive")
    if hours_used > 24:
        raise ValueError("Hours used cannot exceed 24 hours per day")
    return True


# ---------------- Core Logic ---------------- #

def add_usage(appliance, hours, power, rate):
    """
    Record usage of an appliance.

    Args:
        appliance (str): Appliance name
        hours (float): Duration used in hours
        power (float): Power consumption in watts
        rate (float): Electricity rate in ₹ per kWh

    Returns:
        dict: Summary info (energy, cost, total_today)
    """
    validate_input(appliance, power, hours)
    
    data = load_data()
    today = str(date.today())

    # Calculate energy and cost
    energy_kwh = (power * hours) / 1000
    cost = energy_kwh * rate

    # Append to today's data
    if today not in data:
        data[today] = []

    data[today].append({
        "appliance": appliance,
        "power": power,
        "hours": hours,
        "rate": rate,
        "energy_kwh": round(energy_kwh, 3),
        "cost": round(cost, 2),
        "timestamp": datetime.now().isoformat()
    })

    save_data(data)

    # Compute today's total energy and cost
    total_energy_today = sum(entry["energy_kwh"] for entry in data[today])
    total_cost_today = sum(entry["cost"] for entry in data[today])

    print(f"\n✅ Recorded: {appliance} used for {hours:.2f}h "
          f"({energy_kwh:.3f} kWh, ₹{cost:.2f})")
    print(f"📅 Today's Total: {total_energy_today:.3f} kWh | ₹{total_cost_today:.2f}")

    return {
        "appliance": appliance,
        "energy_kwh": energy_kwh,
        "cost": cost,
        "total_today": {
            "energy": total_energy_today,
            "cost": total_cost_today
        }
    }


def get_summary(days=None):
    """
    Generate a summary of recorded data.

    Args:
        days (int, optional): Number of days to include (None for all)

    Returns:
        dict: Total energy (kWh) and total cost (₹)
    """
    data = load_data()
    total_energy = 0
    total_cost = 0
    
    # Filter by date if days specified
    if days:
        cutoff_date = date.today() - timedelta(days=days-1)
        filtered_data = {
            d: entries for d, entries in data.items()
            if datetime.strptime(d, "%Y-%m-%d").date() >= cutoff_date
        }
    else:
        filtered_data = data

    for entries in filtered_data.values():
        total_energy += sum(e["energy_kwh"] for e in entries)
        total_cost += sum(e["cost"] for e in entries)

    return {
        "total_energy": round(total_energy, 3),
        "total_cost": round(total_cost, 2),
        "days": len(filtered_data)
    }


def get_daily_report(target_date=None):
    """
    Get detailed report for a specific day.

    Args:
        target_date (str, optional): Date in YYYY-MM-DD format (default: today)

    Returns:
        dict: Daily usage breakdown
    """
    data = load_data()
    if target_date is None:
        target_date = str(date.today())
    
    if target_date not in data:
        return {"date": target_date, "entries": [], "total_energy": 0, "total_cost": 0}
    
    entries = data[target_date]
    total_energy = sum(e["energy_kwh"] for e in entries)
    total_cost = sum(e["cost"] for e in entries)
    
    # Group by appliance
    by_appliance = defaultdict(lambda: {"energy": 0, "cost": 0, "count": 0})
    for entry in entries:
        app = entry["appliance"]
        by_appliance[app]["energy"] += entry["energy_kwh"]
        by_appliance[app]["cost"] += entry["cost"]
        by_appliance[app]["count"] += 1
    
    return {
        "date": target_date,
        "entries": entries,
        "total_energy": round(total_energy, 3),
        "total_cost": round(total_cost, 2),
        "by_appliance": dict(by_appliance)
    }


def get_appliance_analysis():
    """
    Analyze usage patterns by appliance across all data.

    Returns:
        dict: Appliance-wise breakdown
    """
    data = load_data()
    by_appliance = defaultdict(lambda: {
        "total_energy": 0,
        "total_cost": 0,
        "usage_count": 0,
        "total_hours": 0
    })
    
    for entries in data.values():
        for entry in entries:
            app = entry["appliance"]
            by_appliance[app]["total_energy"] += entry["energy_kwh"]
            by_appliance[app]["total_cost"] += entry["cost"]
            by_appliance[app]["usage_count"] += 1
            by_appliance[app]["total_hours"] += entry["hours"]
    
    # Sort by total cost
    sorted_appliances = sorted(
        by_appliance.items(),
        key=lambda x: x[1]["total_cost"],
        reverse=True
    )
    
    return dict(sorted_appliances)


def delete_entry(target_date, index):
    """
    Delete a specific entry from a date.

    Args:
        target_date (str): Date in YYYY-MM-DD format
        index (int): Index of entry to delete

    Returns:
        bool: True if successful, False otherwise
    """
    data = load_data()
    
    if target_date not in data:
        print(f"❌ No data found for {target_date}")
        return False
    
    if index < 0 or index >= len(data[target_date]):
        print(f"❌ Invalid index {index}")
        return False
    
    deleted = data[target_date].pop(index)
    
    # Remove date if no entries left
    if not data[target_date]:
        del data[target_date]
    
    save_data(data)
    print(f"✅ Deleted: {deleted['appliance']} entry from {target_date}")
    return True


def get_weekly_data():
    """
    Get data for the last 7 days.

    Returns:
        dict: Date-wise energy and cost for last 7 days
    """
    data = load_data()
    weekly_data = {}
    
    for i in range(7):
        target_date = str(date.today() - timedelta(days=i))
        if target_date in data:
            entries = data[target_date]
            weekly_data[target_date] = {
                "energy": round(sum(e["energy_kwh"] for e in entries), 3),
                "cost": round(sum(e["cost"] for e in entries), 2)
            }
        else:
            weekly_data[target_date] = {"energy": 0, "cost": 0}
    
    return dict(sorted(weekly_data.items()))


def show_presets():
    """Display available appliance presets."""
    print("\n🔌 Available Appliance Presets:")
    print("=" * 50)
    for appliance, watts in sorted(APPLIANCE_PRESETS.items()):
        print(f"  {appliance:<30} {watts:>5}W")
    print("=" * 50)