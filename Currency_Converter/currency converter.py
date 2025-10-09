import argparse
from decimal import Decimal, ROUND_HALF_UP

# Exchange rates (1 USD = X currency)
FALLBACK_RATES_USD = {
    "USD": 1.0,
    "EUR": 0.92,
    "INR": 83.50,
    "GBP": 0.79,
    "JPY": 158.20,
    "AUD": 1.53,
    "CAD": 1.36,
    "SGD": 1.26,
    "CHF": 0.87,
    "CNY": 6.88,
    "NZD": 1.69,
}

SUPPORTED = sorted(FALLBACK_RATES_USD.keys())

def format_amount(amount: Decimal, places: int = 2) -> str:
    q = Decimal(10) ** -places
    rounded = amount.quantize(q, rounding=ROUND_HALF_UP)
    return f"{rounded:,.{places}f}"

def convert_offline(amount: float, frm: str, to: str) -> float:
    frm = frm.upper()
    to = to.upper()
    if frm not in FALLBACK_RATES_USD or to not in FALLBACK_RATES_USD:
        raise ValueError("Currency not supported in fallback table.")
    rate_from = FALLBACK_RATES_USD[frm]
    rate_to = FALLBACK_RATES_USD[to]
    amount_usd = amount / rate_from
    result = amount_usd * rate_to
    return result

def list_supported():
    print("Supported currencies (offline):")
    print(", ".join(SUPPORTED))

def do_convert(amount: float, frm: str, to: str, places: int):
    try:
        converted = convert_offline(amount, frm, to)
    except ValueError as e:
        print(e)
        list_supported()
        return
    amt_dec = Decimal(str(amount))
    res_dec = Decimal(str(converted))
    print(f"{format_amount(amt_dec, places)} {frm.upper()} = {format_amount(res_dec, places)} {to.upper()}")
    print("(offline rates from built-in table)")

def main():
    parser = argparse.ArgumentParser(description="Offline Currency Converter (no API)")
    parser.add_argument("amount", nargs="?", type=float, help="Amount to convert")
    parser.add_argument("from_currency", nargs="?", type=str, help="From currency code (e.g. USD)")
    parser.add_argument("to_currency", nargs="?", type=str, help="To currency code (e.g. INR)")
    parser.add_argument("--list", action="store_true", help="List supported currencies")
    parser.add_argument("--places", type=int, default=2, help="Decimal places in output (default: 2)")
    args = parser.parse_args()

    if args.list:
        list_supported()
        return

    if args.amount is None or args.from_currency is None or args.to_currency is None:
        print("Offline Currency Converter — Interactive Mode")
        print("Type 'list' to see supported currencies, or 'quit' to exit.\n")
        while True:
            try:
                s = input("Enter amount (e.g. 100) or 'quit': ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not s:
                continue
            if s.lower() in ("quit", "exit"):
                return
            if s.lower() == "list":
                list_supported()
                continue
            try:
                amount = float(s)
            except ValueError:
                print("Invalid amount. Try again.")
                continue

            frm = input("From currency (e.g. USD): ").strip().upper()
            if not frm:
                print("Empty currency code. Try again.")
                continue
            if frm.lower() == "list":
                list_supported()
                continue

            to = input("To currency (e.g. INR): ").strip().upper()
            if not to:
                print("Empty currency code. Try again.")
                continue
            if to.lower() == "list":
                list_supported()
                continue

            do_convert(amount, frm, to, args.places)
            print()
    else:
        do_convert(args.amount, args.from_currency, args.to_currency, args.places)

if __name__ == "__main__":
    main()
