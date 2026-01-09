# Calculate seasonal averages (all stations, all years)
# avg of (avg Dec, avg Jan, avg Feb) -> double mean()
def seasional_average(data, base_dir):
    seasonal_averages = {
        "Summer (Dec-Feb)": data[['December', 'January', 'February']].mean().mean(),
        "Autumn (Mar-May)": data[['March', 'April', 'May']].mean().mean(),
        "Winter (Jun-Aug)": data[['June', 'July', 'August']].mean().mean(),
        "Spring (Sep-Nov)": data[['September', 'October', 'November']].mean().mean()
    }


    # Output file path
    output_file = base_dir / "average_temp.txt"

    # Save results
    with open(output_file, "w", encoding = 'utf-8') as f:
        f.write("Average Seasonal Temperature (All Stations, All Years)\n")
        for season, avg in seasonal_averages.items():
            f.write(f"{season}: {avg:.1f}°C\n")

    print(f"Seasional average file successfully saved to {output_file}")
