"""
Daily Energy Consumption Tracker
Track household appliance usage and calculate energy consumption and costs.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


class EnergyTracker:
    """Main class for tracking energy consumption of household appliances."""
    
    # Available household appliances with typical wattage (in watts)
    DEFAULT_APPLIANCES = {
        "Refrigerator": 150,
        "Microwave": 1200,
        "Lamp": 60,
        "Hair Dryer": 1500,
        "Radio": 10,
        "TV": 120,
        "Computer": 200,
        "Ceiling Fan": 75,
        "Air Conditioner": 1500,
        "Heater": 1500,
        "Treadmill": 700,
        "Stove/Oven": 3000,
    }
    
    def __init__(self, electricity_rate: float = 0.12):
        """
        Initialize the energy tracker.
        
        Args:
            electricity_rate: Cost per kWh (default: $0.12)
        """
        self.electricity_rate = electricity_rate
        self.appliances: Dict[str, float] = self.DEFAULT_APPLIANCES.copy()
        self.daily_usage: Dict[str, float] = {}  # appliance: hours per day
        self.data_file = "energy_data.json"
    
    def remove_appliance(self, name: str) -> None:
        """Remove an appliance from daily tracking."""
        if not self.daily_usage:
            print("[WARNING] No appliances have been added to tracking yet.")
            return
            
        if name in self.daily_usage:
            del self.daily_usage[name]
            print(f"[OK] Removed '{name}' from tracking.")
        else:
            print(f"[ERROR] Appliance '{name}' is not currently being tracked.")
    
    def set_appliance_usage(self, name: str, hours_per_day: float) -> None:
        """Set daily usage hours for an appliance."""
        if name in self.appliances:
            self.daily_usage[name] = hours_per_day
            print(f"[OK] Set '{name}' usage to {hours_per_day} hours/day.")
        else:
            print(f"[ERROR] Appliance '{name}' not found.")
    
    def calculate_daily_consumption(self, appliance: str = None) -> float:
        """
        Calculate daily energy consumption in kWh.
        
        Args:
            appliance: Specific appliance name, or None for total
            
        Returns:
            Energy consumption in kWh
        """
        if appliance:
            if appliance in self.daily_usage:
                wattage = self.appliances[appliance]
                hours = self.daily_usage[appliance]
                return (wattage * hours) / 1000  # Convert Wh to kWh
            return 0.0
        
        # Calculate total for all appliances
        total_kwh = 0.0
        for app, hours in self.daily_usage.items():
            wattage = self.appliances[app]
            total_kwh += (wattage * hours) / 1000
        return total_kwh
    
    def calculate_weekly_consumption(self, appliance: str = None) -> float:
        """Calculate weekly energy consumption in kWh."""
        return self.calculate_daily_consumption(appliance) * 7
    
    def calculate_daily_cost(self, appliance: str = None) -> float:
        """Calculate daily electricity cost."""
        return self.calculate_daily_consumption(appliance) * self.electricity_rate
    
    def calculate_weekly_cost(self, appliance: str = None) -> float:
        """Calculate weekly electricity cost."""
        return self.calculate_weekly_consumption(appliance) * self.electricity_rate
    
    def calculate_monthly_cost(self, appliance: str = None) -> float:
        """Calculate estimated monthly electricity cost."""
        return self.calculate_daily_consumption(appliance) * 30 * self.electricity_rate
    
    def get_consumption_breakdown(self) -> List[Tuple[str, float, float, float]]:
        """
        Get detailed consumption breakdown for all appliances.
        
        Returns:
            List of tuples: (appliance, daily_kWh, weekly_kWh, daily_cost)
        """
        breakdown = []
        for appliance in self.daily_usage:
            daily_kwh = self.calculate_daily_consumption(appliance)
            weekly_kwh = self.calculate_weekly_consumption(appliance)
            daily_cost = self.calculate_daily_cost(appliance)
            breakdown.append((appliance, daily_kwh, weekly_kwh, daily_cost))
        
        # Sort by daily consumption (highest first)
        breakdown.sort(key=lambda x: x[1], reverse=True)
        return breakdown
    
    def display_summary(self) -> None:
        """Display a comprehensive summary of energy consumption."""
        if not self.daily_usage:
            print("\n[WARNING] No appliance usage data entered yet.")
            return
        
        print("\n" + "="*80)
        print("ENERGY CONSUMPTION SUMMARY".center(80))
        print("="*80)
        print(f"Electricity Rate: ${self.electricity_rate:.3f} per kWh")
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # Detailed breakdown
        breakdown = self.get_consumption_breakdown()
        print("\nDETAILED BREAKDOWN BY APPLIANCE:")
        print("-"*80)
        print(f"{'Appliance':<30} {'Daily (kWh)':<15} {'Weekly (kWh)':<15} {'Daily Cost':<15}")
        print("-"*80)
        
        for appliance, daily_kwh, weekly_kwh, daily_cost in breakdown:
            print(f"{appliance:<30} {daily_kwh:>10.3f}     {weekly_kwh:>10.3f}      ${daily_cost:>10.2f}")
        
        print("-"*80)
        
        # Totals
        total_daily_kwh = self.calculate_daily_consumption()
        total_weekly_kwh = self.calculate_weekly_consumption()
        total_daily_cost = self.calculate_daily_cost()
        total_weekly_cost = self.calculate_weekly_cost()
        total_monthly_cost = self.calculate_monthly_cost()
        
        print(f"\n{'TOTAL':<30} {total_daily_kwh:>10.3f}     {total_weekly_kwh:>10.3f}      ${total_daily_cost:>10.2f}")
        print("="*80)
        
        print(f"\nCOST SUMMARY:")
        print(f"   Daily Cost:    ${total_daily_cost:.2f}")
        print(f"   Weekly Cost:   ${total_weekly_cost:.2f}")
        print(f"   Monthly Cost:  ${total_monthly_cost:.2f} (estimated)")
        print(f"   Yearly Cost:   ${total_daily_cost * 365:.2f} (estimated)")
        
        # Find top consumer
        if breakdown:
            top_consumer = breakdown[0]
            percentage = (top_consumer[1] / total_daily_kwh) * 100
            print(f"\n>> Top Energy Consumer: {top_consumer[0]}")
            print(f"   Consumes {top_consumer[1]:.3f} kWh/day ({percentage:.1f}% of total)")
        
        print("="*80 + "\n")
    
    def save_data(self) -> None:
        """Save current data to JSON file."""
        data = {
            "electricity_rate": self.electricity_rate,
            "appliances": self.appliances,
            "daily_usage": self.daily_usage,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Data saved to {self.data_file}")
    
    def load_data(self) -> bool:
        """Load data from JSON file."""
        if not os.path.exists(self.data_file):
            return False
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.electricity_rate = data.get("electricity_rate", self.electricity_rate)
            self.appliances = data.get("appliances", self.appliances)
            self.daily_usage = data.get("daily_usage", {})
            print(f"[OK] Data loaded from {self.data_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Error loading data: {e}")
            return False


def display_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("DAILY ENERGY CONSUMPTION TRACKER".center(60))
    print("="*60)
    print("1. View available appliances")
    print("2. Remove appliance from tracking")
    print("3. Add/Update appliance usage")
    print("4. View consumption summary")
    print("5. Set electricity rate")
    print("6. Save data")
    print("7. Load data")
    print("8. Quick setup (guided entry)")
    print("0. Exit")
    print("="*60)


def quick_setup(tracker: EnergyTracker) -> None:
    """Guided setup for entering appliance usage."""
    print("\n" + "="*60)
    print("QUICK SETUP - Enter your appliance usage".center(60))
    print("="*60)
    print("Select appliances you use and enter their daily usage hours.")
    print("Press Enter without a number to skip an appliance.\n")
    
    # Display all available appliances
    print("Available Appliances:")
    print("-" * 60)
    
    for appliance in sorted(tracker.appliances.keys()):
        wattage = tracker.appliances[appliance]
        usage = input(f"  {appliance} ({wattage}W) - Hours per day: ").strip()
        if usage:
            try:
                hours = float(usage)
                if 0 <= hours <= 24:
                    tracker.set_appliance_usage(appliance, hours)
                else:
                    print("    [WARNING] Hours must be between 0 and 24. Skipped.")
            except ValueError:
                print("    [WARNING] Invalid input. Skipped.")
    
    print("\n[OK] Quick setup completed!")


def main():
    """Main application loop."""
    tracker = EnergyTracker()
    
    # Try to load existing data
    if os.path.exists(tracker.data_file):
        print("\n[INFO] Found existing data file.")
        choice = input("Load previous data? (y/n): ").strip().lower()
        if choice == 'y':
            tracker.load_data()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (0-8): ").strip()
        
        if choice == '1':
            # View available appliances
            print("\n" + "="*60)
            print("AVAILABLE APPLIANCES".center(60))
            print("="*60)
            
            if not tracker.daily_usage:
                print("\n[INFO] No appliances have been added to tracking yet.")
                print("Use option 3 or 8 to add appliances.\n")
            else:
                print(f"\n{'Appliance':<25} {'Power (Watts)':<15} {'Status':<20}")
                print("-"*60)
                
            for appliance, wattage in sorted(tracker.appliances.items()):
                usage = tracker.daily_usage.get(appliance, 0)
                if usage > 0:
                    status = f"Tracking ({usage}h/day)"
                    print(f"{appliance:<25} {wattage:<10}W     {status}")
                else:
                    print(f"{appliance:<25} {wattage:<10}W     Not tracked")
            print("="*60)
        
        elif choice == '2':
            # Remove appliance
            print("\n--- Remove Appliance from Tracking ---")
            if not tracker.daily_usage:
                print("[WARNING] No appliances are currently being tracked.")
            else:
                print("\nCurrently tracked appliances:")
                for i, appliance in enumerate(sorted(tracker.daily_usage.keys()), 1):
                    hours = tracker.daily_usage[appliance]
                    print(f"  {i}. {appliance} ({hours}h/day)")
                
                name = input("\nEnter appliance name to remove: ").strip()
                if name:
                    tracker.remove_appliance(name)
        
        elif choice == '3':
            # Set appliance daily usage
            print("\n--- Add/Update Appliance Usage ---")
            print("\nAvailable appliances:")
            for i, appliance in enumerate(sorted(tracker.appliances.keys()), 1):
                wattage = tracker.appliances[appliance]
                status = ""
                if appliance in tracker.daily_usage:
                    status = f" [Currently: {tracker.daily_usage[appliance]}h/day]"
                print(f"  {i}. {appliance} ({wattage}W){status}")
            
            name = input("\nEnter appliance name: ").strip()
            if name in tracker.appliances:
                try:
                    hours = float(input("Hours used per day: ").strip())
                    if 0 <= hours <= 24:
                        tracker.set_appliance_usage(name, hours)
                    else:
                        print("[ERROR] Hours must be between 0 and 24.")
                except ValueError:
                    print("[ERROR] Invalid hours value.")
            else:
                print(f"[ERROR] Appliance '{name}' not found. Please select from the list above.")
        
        elif choice == '4':
            # View consumption summary
            tracker.display_summary()
        
        elif choice == '5':
            # Set electricity rate
            print("\n--- Set Electricity Rate ---")
            print(f"Current rate: ${tracker.electricity_rate:.3f} per kWh")
            try:
                rate = float(input("Enter new rate ($/kWh): ").strip())
                if rate > 0:
                    tracker.electricity_rate = rate
                    print(f"[OK] Electricity rate set to ${rate:.3f} per kWh")
                else:
                    print("[ERROR] Rate must be positive.")
            except ValueError:
                print("[ERROR] Invalid rate value.")
        
        elif choice == '6':
            # Save data
            tracker.save_data()
        
        elif choice == '7':
            # Load data
            tracker.load_data()
        
        elif choice == '8':
            # Quick setup
            quick_setup(tracker)
        
        elif choice == '0':
            # Exit
            print("\n--- Exit ---")
            save = input("Save data before exiting? (y/n): ").strip().lower()
            if save == 'y':
                tracker.save_data()
            print("\nThank you for using Energy Consumption Tracker!")
            print("Stay energy conscious!\n")
            break
        
        else:
            print("\n[ERROR] Invalid choice. Please select 0-8.")


if __name__ == "__main__":
    main()

