def currency_converter(amount, rate):
    return amount * rate

def main():
    print("💰 Welcome to Currency Converter 💰\n")
    
    try:
        source_currency = input("Enter source currency (e.g., USD, INR, EUR): ").upper()
        target_currency = input("Enter target currency (e.g., USD, INR, EUR): ").upper()
        amount = float(input(f"Enter amount in {source_currency}: "))
        rate = float(input(f"Enter how much 1 {source_currency} is worth in {target_currency}: "))
        
        converted_amount = currency_converter(amount, rate)
        print(f"\n✅ {amount:.2f} {source_currency} = {converted_amount:.2f} {target_currency}")
        
    except ValueError:
        print("❌ Invalid input. Please enter numeric values only.")

if __name__ == "__main__":
    main()
