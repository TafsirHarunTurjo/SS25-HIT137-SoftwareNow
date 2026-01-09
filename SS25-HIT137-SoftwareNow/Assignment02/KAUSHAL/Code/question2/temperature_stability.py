def temperature_stability(data, base_dir, month_cols):
    # Calculate standard deviation per station across all months


    station_std = data.groupby('STATION_NAME')[month_cols].agg("std")  # std for each month per station
    station_std = station_std.mean(axis=1)  # mean across months → one number per station

    # Find most stable and most variable stations
    min_std = station_std.min()  # smallest std → most stable
    max_std = station_std.max()  # largest std → most variable

    most_stable_stations = station_std[station_std == min_std]
    most_variable_stations = station_std[station_std == max_std]

    # Prepare output lines
    output_lines = []

    # Most Stable
    for station, std in most_stable_stations.items():
        output_lines.append(f"Most Stable: Station {station}: StdDev {std:.2f}°C")

    # Most Variable
    for station, std in most_variable_stations.items():
        output_lines.append(f"Most Variable: Station {station}: StdDev {std:.2f}°C")

    # Save to file
    output_file = base_dir / "temperature_stability_stations.txt"
    with open(output_file, "w", encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + "\n")
    
    print(f"Temperature stability file is successfully saved to {output_file}")


