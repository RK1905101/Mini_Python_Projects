import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

DATA_FILE = "data/energy_data.json"
CHART_FILE = "data/energy_report.png"


def load_energy_data():
    """Load energy data from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except json.JSONDecodeError:
        return {}


def generate_report(days=7):
    """
    Generate a visual report of energy consumption.
    
    Args:
        days (int): Number of days to include in report (default: 7)
    """
    os.makedirs("data", exist_ok=True)
    data = load_energy_data()
    
    if not data:
        print("⚠️  No energy usage data found.")
        return

    # Prepare date range
    today = datetime.now().date()
    date_range = [(today - timedelta(days=i)).isoformat() for i in range(days-1, -1, -1)]
    
    daily_energy = []
    daily_cost = []
    date_labels = []

    print(f"\n📊 Energy Consumption Report (Last {days} Days)")
    print("=" * 60)
    
    total_energy_period = 0
    total_cost_period = 0
    
    for day in date_range:
        entries = data.get(day, [])
        day_energy = sum(e["energy_kwh"] for e in entries)
        day_cost = sum(e["cost"] for e in entries)
        
        daily_energy.append(day_energy)
        daily_cost.append(day_cost)
        date_labels.append(datetime.fromisoformat(day).strftime("%m/%d"))
        
        total_energy_period += day_energy
        total_cost_period += day_cost
        
        print(f"{day}: {day_energy:>6.2f} kWh | ₹{day_cost:>7.2f}")
    
    print("=" * 60)
    print(f"📈 Period Total: {total_energy_period:.2f} kWh | ₹{total_cost_period:.2f}")
    
    if days >= 7:
        avg_daily = total_energy_period / days
        print(f"📊 Daily Average: {avg_daily:.2f} kWh | ₹{total_cost_period/days:.2f}")
    
    print("=" * 60)

    # Generate dual-axis chart (Energy + Cost)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Energy plot (left y-axis)
    color1 = '#2E86AB'
    ax1.set_xlabel('Date', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Energy (kWh)', color=color1, fontsize=11, fontweight='bold')
    line1 = ax1.plot(date_labels, daily_energy, marker='o', linestyle='-', 
                     linewidth=2.5, color=color1, label='Energy (kWh)', markersize=7)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Cost plot (right y-axis)
    ax2 = ax1.twinx()
    color2 = '#A23B72'
    ax2.set_ylabel('Cost (₹)', color=color2, fontsize=11, fontweight='bold')
    line2 = ax2.plot(date_labels, daily_cost, marker='s', linestyle='--', 
                     linewidth=2.5, color=color2, label='Cost (₹)', markersize=7)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Title and legend
    plt.title(f'Energy Consumption & Cost - Last {days} Days', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=10)
    
    # Rotate x-axis labels
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    fig.tight_layout()
    plt.savefig(CHART_FILE, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Report chart saved to: {CHART_FILE}\n")


def generate_appliance_report():
    """Generate a pie chart showing energy consumption by appliance."""
    data = load_energy_data()
    
    if not data:
        print("⚠️  No energy usage data found.")
        return
    
    # Aggregate by appliance
    appliance_totals = {}
    
    for entries in data.values():
        for entry in entries:
            app = entry["appliance"]
            energy = entry["energy_kwh"]
            
            if app in appliance_totals:
                appliance_totals[app] += energy
            else:
                appliance_totals[app] = energy
    
    if not appliance_totals:
        print("⚠️  No appliance data to generate report.")
        return
    
    # Sort and get top appliances
    sorted_appliances = sorted(appliance_totals.items(), 
                               key=lambda x: x[1], reverse=True)
    
    # Take top 8, combine rest as "Others"
    if len(sorted_appliances) > 8:
        top_8 = sorted_appliances[:8]
        others_total = sum(energy for _, energy in sorted_appliances[8:])
        appliances = [app for app, _ in top_8] + ["Others"]
        energies = [energy for _, energy in top_8] + [others_total]
    else:
        appliances = [app for app, _ in sorted_appliances]
        energies = [energy for _, energy in sorted_appliances]
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = plt.cm.Set3(range(len(appliances)))
    wedges, texts, autotexts = ax.pie(
        energies, 
        labels=appliances, 
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 10, 'fontweight': 'bold'}
    )
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
    
    ax.set_title('Energy Consumption by Appliance', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    appliance_chart = "data/appliance_report.png"
    plt.savefig(appliance_chart, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✅ Appliance report saved to: {appliance_chart}")
    
    # Print summary
    print("\n🔌 Top Energy Consumers:")
    print("=" * 50)
    for i, (app, energy) in enumerate(sorted_appliances[:5], 1):
        percentage = (energy / sum(appliance_totals.values())) * 100
        print(f"{i}. {app:<20} {energy:>7.2f} kWh ({percentage:>5.1f}%)")
    print("=" * 50 + "\n")


def generate_hourly_usage_report():
    """Generate a bar chart showing usage patterns by hour of day."""
    data = load_energy_data()
    
    if not data:
        print("⚠️  No energy usage data found.")
        return
    
    hourly_usage = [0] * 24
    
    for entries in data.values():
        for entry in entries:
            # Check if timestamp exists
            if "timestamp" in entry:
                timestamp = datetime.fromisoformat(entry["timestamp"])
                hour = timestamp.hour
                hourly_usage[hour] += entry["energy_kwh"]
    
    # Check if we have any hourly data
    if sum(hourly_usage) == 0:
        print("⚠️  No timestamp data available for hourly analysis.")
        return
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(14, 6))
    
    hours = [f"{h:02d}:00" for h in range(24)]
    bars = ax.bar(hours, hourly_usage, color='#06A77D', alpha=0.8, edgecolor='black')
    
    # Highlight peak hours
    max_usage = max(hourly_usage)
    for i, bar in enumerate(bars):
        if hourly_usage[i] == max_usage and max_usage > 0:
            bar.set_color('#D00000')
    
    ax.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax.set_ylabel('Energy (kWh)', fontsize=11, fontweight='bold')
    ax.set_title('Energy Consumption by Hour of Day', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    hourly_chart = "data/hourly_report.png"
    plt.savefig(hourly_chart, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✅ Hourly usage report saved to: {hourly_chart}\n")


def generate_comprehensive_report():
    """Generate all available reports."""
    print("\n🔋 Generating Comprehensive Energy Reports...")
    print("=" * 60)
    
    generate_report(days=7)
    generate_appliance_report()
    generate_hourly_usage_report()
    
    print("=" * 60)
    print("✅ All reports generated successfully!")
    print("=" * 60 + "\n")