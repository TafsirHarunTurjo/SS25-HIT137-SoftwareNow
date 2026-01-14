def seasional_average(data, base_dir):
    """
    Rule:
        - Use Australian seasons: Summer (Dec-Feb), Autumn (Mar-May), Winter (Jun-Aug), Spring (Sep-Nov)
    Task:
        - Calculate the average temperature for each season across ALL
          stations and ALL years. Save the results to "average_temp.txt".
    Parameters(2):
        - data, that combine all csv files (using append and concat)
        - base_dir to get the base file path
    Output format:
        - "Summer: 28.5°C"
    """
    # note: avg of (avg Dec, avg Jan, avg Feb) -> double mean()
    seasonal_averages = {
        "Summer": data[['December', 'January', 'February']].mean().mean(),
        "Autumn": data[['March', 'April', 'May']].mean().mean(),
        "Winter": data[['June', 'July', 'August']].mean().mean(),
        "Spring": data[['September', 'October', 'November']].mean().mean()
    }


    # output file path
    output_file = base_dir / "average_temp.txt"

    # save results
    with open(output_file, "w", encoding = 'utf-8') as f:
        f.write("Average Seasonal Temperature (All Stations, All Years)\n")
        for season, avg in seasonal_averages.items():
            f.write(f"{season}: {avg:.1f}°C\n")

    print(f"Seasional average file successfully saved to {output_file}")
