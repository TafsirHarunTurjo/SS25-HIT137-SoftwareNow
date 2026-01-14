def temperature_stability(data, base_dir, month_cols):
    """
    Rule:
        - Most stable temperature have smallest standard deviation
        - Most variable temperatures  have largest standard deviation
    Task:
        - Find which station(s) have the most stable temperatures (smallest standard deviation)
          and which have the most variable temperatures (largest standard deviation). Save the
          results to "temperature_stability_stations.txt"
    Parameters(3):
        - data, that combine all csv files (using append and concat)
        - base_dir to get the base file path
        - month_cols to get months (Jan-Dec)
    Output format:
        - "Most Stable: Station XYZ: StdDev 2.3°C"
        - "Most Variable: Station DEF: StdDev 12.8°C"
        - If multiple stations tie, list all of them
    """

    # std for each month per station
    station_std = data.groupby('STATION_NAME')[month_cols].agg("std")

    # mean across months → one number per station  
    station_std = station_std.mean(axis=1)  

    # get most stable and most variable stations
    min_std = station_std.min()  
    max_std = station_std.max()  

    most_stable_stations = station_std[station_std == min_std]
    most_variable_stations = station_std[station_std == max_std]

    # prepare output lines
    output_lines = []

    # most Stable
    for station, std in most_stable_stations.items():
        output_lines.append(f"Most Stable: Station {station}: StdDev {std:.2f}°C")

    # most Variable
    for station, std in most_variable_stations.items():
        output_lines.append(f"Most Variable: Station {station}: StdDev {std:.2f}°C")

    # save to file
    output_file = base_dir / "temperature_stability_stations.txt"
    with open(output_file, "w", encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + "\n")
    
    print(f"Temperature stability file is successfully saved to {output_file}")


