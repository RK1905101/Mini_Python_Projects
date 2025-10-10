import pandas as pd

# Load CSV
data = pd.read_csv("data.csv")

history = []

print("👋 Welcome to Weather Data Analysis 🌤")

while True:
    print("\nAvailable locations:", ", ".join(data['Location'].unique()))
    location = input("Enter location from above: ").title()

    # Filter location
    loc_data = data[data['Location'] == location]

    if loc_data.empty:
        print("❌ Location not found!")
    else:
        print(f"\n🌤 Weather Data Preview for {location}:")
        print(loc_data.to_string(index=False))  # tabular output

        avg_temp = loc_data['Temperature'].mean()
        total_rain = loc_data['Rainfall'].sum()

        print(f"\n🌡 Average Temperature: {avg_temp:.2f}°C")
        print(f"🌧 Total Rainfall: {total_rain} mm")

        history.append(location)

    cont = input("\nDo you want to check another location? (yes/no): ").lower()
    if cont != 'yes':
        break

print("\n👋 Goodbye! Here's your query history:")
for i, loc in enumerate(history, 1):
    print(f"{i}. {loc}")
