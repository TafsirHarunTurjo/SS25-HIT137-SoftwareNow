def temperature_range(data, base_dir, month_cols):
    # Columns for months

    station_stats = data.groupby('STATION_NAME')[month_cols].agg(['max','min'])

    station_stats['range'] = station_stats.xs('max', axis=1, level=1).max(axis=1) - \
                station_stats.xs('min', axis=1, level=1).min(axis=1)
    
    # Find the largest range
    max_range = station_stats['range'].max()
    # Get all stations with this max range (handles ties)
    largest_range_stations = station_stats[station_stats['range'] == max_range]

    # Prepare output lines
    output_lines = []
    for station in largest_range_stations.index:
        max_temp = largest_range_stations.xs('max', axis=1, level=1).loc[station].max()
        min_temp = largest_range_stations.xs('min', axis=1, level=1).loc[station].min()
        range_temp = max_temp - min_temp
        output_lines.append(f"Station {station}: Range {range_temp:.2f}°C (Max: {max_temp:.2f}°C, Min: {min_temp:.2f}°C)")

    # Save results to a text file
    output_file = base_dir / "largest_temp_range_station.txt"
    with open(output_file, "w", encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"largest_temp_range_station.txt created successfully with {len(output_lines)} station(s).")
