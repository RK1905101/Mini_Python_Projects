from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    Fore = Style = type('', (), {'GREEN':'','RED':'','YELLOW':'','CYAN':'','RESET_ALL':''})()

# Transaction history
history = []

# Popular currency exchange rates (sample, can be updated)
exchange_rates = {
    'USD': {'INR': 83.5, 'EUR': 0.93, 'GBP': 0.82, 'JPY': 144.2},
    'INR': {'USD': 0.012, 'EUR': 0.011, 'GBP': 0.0098, 'JPY': 1.73},
    'EUR': {'USD': 1.07, 'INR': 90.0, 'GBP': 0.88, 'JPY': 155.0}
}

def convert_currency(amount, rate):
    return amount * rate

def show_history():
    if not history:
        print(f"{Fore.YELLOW}📜 No conversions yet.")
    else:
        print(f"\n{Fore.CYAN}📜 Conversion History:")
        for idx, record in enumerate(history, 1):
            print(f"{idx}. {record}")
        print(f"\n🔢 Total Conversions: {len(history)}\n")

def main():
    print(f"{Fore.GREEN}💸 Welcome to the Advanced Currency Converter 💸")
    name = input("Enter your name: ").strip()
    print(f"Hi {name}! Let's get started.\n")

    while True:
        print(f"{Fore.CYAN}Menu Options:")
        print("1. Convert currency")
        print("2. Show conversion history")
        print("3. Clear history")
        print("4. Exit")
        choice = input("Choose option (1-4): ").strip()

        if choice == "1":
            source = input("Enter source currency code (e.g., USD, INR, EUR): ").upper()
            target = input("Enter target currency code (e.g., USD, INR, EUR): ").upper()

            try:
                amount = float(input(f"Enter amount in {source}: "))
                # Use pre-filled rate if available, else ask user
                if source in exchange_rates and target in exchange_rates[source]:
                    rate = exchange_rates[source][target]
                    print(f"{Fore.YELLOW}Using pre-filled exchange rate: 1 {source} = {rate} {target}")
                else:
                    rate = float(input(f"Enter exchange rate ({target} per 1 {source}): "))

                converted = convert_currency(amount, rate)
                timestamp = datetime.now().strftime("%H:%M:%S")
                record = f"{amount:.2f} {source} → {converted:.2f} {target} at {timestamp}"
                history.append(record)
                print(f"{Fore.GREEN}✅ {record}\n")

            except ValueError:
                print(f"{Fore.RED}❌ Invalid input! Please enter numeric values.\n")

        elif choice == "2":
            show_history()

        elif choice == "3":
            history.clear()
            print(f"{Fore.YELLOW}🗑️ Conversion history cleared.\n")

        elif choice == "4":
            print(f"{Fore.GREEN}🎉 Thank you for using the Advanced Currency Converter, {name}!")
            show_history()
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice! Please select 1-4.\n")

if __name__ == "__main__":
    main()
