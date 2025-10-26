import sys
from energy_tracker import (
    add_usage, 
    load_data, 
    get_summary, 
    get_daily_report,
    get_appliance_analysis,
    delete_entry,
    show_presets,
    APPLIANCE_PRESETS
)
from report_generator import (
    generate_report,
    generate_appliance_report,
    generate_hourly_usage_report,
    generate_comprehensive_report
)


def show_detailed_report():
    """Display detailed CLI report of all energy usage."""
    data = load_data()
    if not data:
        print("\n📊 No energy usage data found.")
        return

    print("\n🔋 Detailed Energy Consumption Report")
    print("=" * 70)
    total_energy = 0
    total_cost = 0

    for date, records in sorted(data.items(), reverse=True):
        print(f"\n📅 Date: {date}")
        print("-" * 70)
        for idx, record in enumerate(records):
            appliance = record["appliance"]
            hours = record["hours"]
            power = record["power"]
            rate = record["rate"]
            energy_kwh = record.get("energy_kwh", (power * hours) / 1000)
            cost = record.get("cost", energy_kwh * rate)

            total_energy += energy_kwh
            total_cost += cost

            print(
                f"  [{idx}] {appliance:<18} | {hours:>5.1f}h | {power:>6.0f}W | "
                f"{energy_kwh:>6.2f} kWh | ₹{cost:>7.2f}"
            )

    print("\n" + "=" * 70)
    print(f"⚡ Total Energy Consumed: {total_energy:.2f} kWh")
    print(f"💰 Total Cost: ₹{total_cost:.2f}")
    print("=" * 70)


def show_summary_stats():
    """Display summary statistics."""
    print("\n📈 Energy Consumption Summary")
    print("=" * 50)
    
    # Overall summary
    overall = get_summary()
    print(f"\n🌍 All-Time Statistics:")
    print(f"  Total Energy: {overall['total_energy']:.2f} kWh")
    print(f"  Total Cost: ₹{overall['total_cost']:.2f}")
    print(f"  Days Tracked: {overall['days']}")
    
    if overall['days'] > 0:
        print(f"  Avg per Day: {overall['total_energy']/overall['days']:.2f} kWh")
    
    # Last 7 days
    week = get_summary(days=7)
    print(f"\n📅 Last 7 Days:")
    print(f"  Total Energy: {week['total_energy']:.2f} kWh")
    print(f"  Total Cost: ₹{week['total_cost']:.2f}")
    print(f"  Days with Data: {week['days']}")
    
    if week['days'] > 0:
        print(f"  Avg per Day: {week['total_energy']/week['days']:.2f} kWh")
    
    # Last 30 days
    month = get_summary(days=30)
    print(f"\n📆 Last 30 Days:")
    print(f"  Total Energy: {month['total_energy']:.2f} kWh")
    print(f"  Total Cost: ₹{month['total_cost']:.2f}")
    print(f"  Days with Data: {month['days']}")
    
    if month['days'] > 0:
        print(f"  Avg per Day: {month['total_energy']/month['days']:.2f} kWh")
    
    print("=" * 50)


def show_appliance_stats():
    """Display appliance-wise statistics."""
    analysis = get_appliance_analysis()
    
    if not analysis:
        print("\n⚠️  No appliance data available.")
        return
    
    print("\n🔌 Appliance-Wise Energy Analysis")
    print("=" * 80)
    print(f"{'Appliance':<20} {'Energy (kWh)':<15} {'Cost (₹)':<12} {'Uses':<8} {'Hours'}")
    print("-" * 80)
    
    for appliance, stats in list(analysis.items())[:10]:  # Top 10
        print(
            f"{appliance:<20} {stats['total_energy']:>12.2f}   "
            f"₹{stats['total_cost']:>9.2f}   {stats['usage_count']:>5}   "
            f"{stats['total_hours']:>6.1f}h"
        )
    
    print("=" * 80)


def add_usage_with_preset():
    """Add usage with option to use presets."""
    print("\n🔌 Add Appliance Usage")
    print("-" * 40)
    print("Choose an option:")
    print("  1. Use preset appliance")
    print("  2. Enter custom appliance")
    print("  3. View all presets")
    
    option = input("👉 Your choice (1-3): ").strip()
    
    if option == "3":
        show_presets()
        return add_usage_with_preset()
    
    appliance = ""
    power = 0
    
    if option == "1":
        print("\n📋 Common Appliances:")
        presets_list = list(APPLIANCE_PRESETS.items())
        for idx, (name, watts) in enumerate(presets_list[:15], 1):
            print(f"  {idx}. {name} ({watts}W)")
        
        try:
            preset_idx = int(input("\n👉 Select appliance number: ").strip())
            if 1 <= preset_idx <= len(presets_list):
                appliance, power = presets_list[preset_idx - 1]
                print(f"✅ Selected: {appliance} ({power}W)")
            else:
                print("❌ Invalid selection.")
                return
        except ValueError:
            print("❌ Invalid input.")
            return
    
    elif option == "2":
        appliance = input("🔌 Enter appliance name: ").strip()
        try:
            power = float(input("💡 Enter power rating (W): ").strip())
        except ValueError:
            print("❌ Invalid power rating.")
            return
    else:
        print("❌ Invalid option.")
        return
    
    try:
        hours = float(input("⏱️  Enter usage hours: ").strip())
        rate = float(input("💰 Enter electricity rate (₹/kWh) [default 8.5]: ").strip() or "8.5")
        
        add_usage(appliance, hours, power, rate)
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def delete_usage_entry():
    """Delete a specific usage entry."""
    data = load_data()
    if not data:
        print("\n⚠️  No data to delete.")
        return
    
    print("\n🗑️  Delete Usage Entry")
    print("=" * 50)
    
    # Show recent dates
    dates = sorted(data.keys(), reverse=True)[:10]
    print("\nRecent dates:")
    for idx, date in enumerate(dates, 1):
        entry_count = len(data[date])
        print(f"  {idx}. {date} ({entry_count} entries)")
    
    try:
        date_idx = int(input("\n👉 Select date number: ").strip())
        if 1 <= date_idx <= len(dates):
            target_date = dates[date_idx - 1]
            
            # Show entries for that date
            print(f"\nEntries for {target_date}:")
            for idx, entry in enumerate(data[target_date]):
                print(
                    f"  [{idx}] {entry['appliance']} - {entry['hours']}h - "
                    f"{entry['energy_kwh']:.2f} kWh"
                )
            
            entry_idx = int(input("\n👉 Select entry to delete: ").strip())
            delete_entry(target_date, entry_idx)
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Invalid input.")
    except Exception as e:
        print(f"❌ Error: {e}")


def reports_menu():
    """Sub-menu for different report types."""
    while True:
        print("\n📊 Reports & Analytics")
        print("=" * 40)
        print("1️⃣  Weekly Report (Chart)")
        print("2️⃣  Monthly Report (Chart)")
        print("3️⃣  Appliance Breakdown (Pie Chart)")
        print("4️⃣  Hourly Usage Pattern")
        print("5️⃣  Generate All Reports")
        print("6️⃣  Back to Main Menu")
        print("=" * 40)
        
        choice = input("👉 Enter your choice: ").strip()
        
        if choice == "1":
            generate_report(days=7)
        elif choice == "2":
            generate_report(days=30)
        elif choice == "3":
            generate_appliance_report()
        elif choice == "4":
            generate_hourly_usage_report()
        elif choice == "5":
            generate_comprehensive_report()
        elif choice == "6":
            break
        else:
            print("⚠️  Invalid option.")


def main():
    """Main application loop."""
    print("\n" + "=" * 50)
    print("⚡  ENERGY CONSUMPTION TRACKER")
    print("=" * 50)
    
    while True:
        try:
            print("\n📋 Main Menu")
            print("=" * 40)
            print("1️⃣   Add Appliance Usage")
            print("2️⃣   View Summary Statistics")
            print("3️⃣   View Detailed Report (CLI)")
            print("4️⃣   View Appliance Analysis")
            print("5️⃣   Generate Visual Reports")
            print("6️⃣   Delete Usage Entry")
            print("7️⃣   View Appliance Presets")
            print("8️⃣   Exit")
            print("=" * 40)

            choice = input("👉 Enter your choice: ").strip()

            if choice == "1":
                add_usage_with_preset()

            elif choice == "2":
                show_summary_stats()

            elif choice == "3":
                show_detailed_report()
            
            elif choice == "4":
                show_appliance_stats()

            elif choice == "5":
                reports_menu()
            
            elif choice == "6":
                delete_usage_entry()
            
            elif choice == "7":
                show_presets()

            elif choice == "8":
                print("\n👋 Thank you for using Energy Tracker!")
                print("💡 Remember: Every kWh saved makes a difference!")
                print("=" * 50 + "\n")
                sys.exit(0)

            else:
                print("⚠️  Invalid option. Please choose 1-8.")

        except KeyboardInterrupt:
            print("\n\n🛑 Keyboard interrupt detected.")
            print("👋 Exiting Energy Tracker...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            print("Please try again or contact support.")


if __name__ == "__main__":
    main()