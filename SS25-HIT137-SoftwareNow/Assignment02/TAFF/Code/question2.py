# question2.py
# HIT137 Group Assignment 2 - Question 2
#
# This program reads ALL yearly CSV files from the "temperatures" folder and calculates:
# 1) Seasonal average temperature across all stations and years (Australian seasons)
# 2) Station(s) with largest temperature range (max - min across all years/months)
# 3) Most stable and most variable stations using standard deviation

from pathlib import Path
import csv
import math
import statistics
from typing import Dict, List, Tuple


MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Australian seasons (per assignment):
SEASON_BY_MONTH = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring"
}


def is_missing(value: str) -> bool:
    """
    Missing values may be '', 'NaN', or actual blank.
    We'll treat anything that cannot convert to float as missing too.
    """
    if value is None:
        return True
    v = value.strip()
    return v == "" or v.lower() == "nan"


def to_float_or_none(value: str):
    """Convert a string to float, return None if missing/invalid."""
    if is_missing(value):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def read_all_temperatures(folder: Path) -> Tuple[
    Dict[str, List[float]],  # station -> list of all temps across all months/years
    Dict[str, List[float]]   # season  -> list of temps across all stations/years
]:
    """
    Reads all CSVs in folder, extracting station temps and season temps.

    CSV columns expected (based on your provided files):
      STATION_NAME, STN_ID, LAT, LON, January..December
    """
    station_temps: Dict[str, List[float]] = {}
    season_temps: Dict[str, List[float]] = {"Summer": [], "Autumn": [], "Winter": [], "Spring": []}

    csv_files = sorted(folder.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder}")

    for file_path in csv_files:
        with file_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            # Basic safety: ensure month columns exist
            for m in MONTHS:
                if m not in reader.fieldnames:
                    raise ValueError(f"Missing expected month column '{m}' in file: {file_path.name}")

            # Station identity: use STN_ID if present; otherwise fallback to STATION_NAME
            has_id = "STN_ID" in reader.fieldnames
            has_name = "STATION_NAME" in reader.fieldnames

            for row in reader:
                if has_id and row.get("STN_ID") is not None:
                    station_key = row["STN_ID"].strip()
                elif has_name and row.get("STATION_NAME") is not None:
                    station_key = row["STATION_NAME"].strip()
                else:
                    # If neither exists, skip (should not happen with your dataset)
                    continue

                if station_key not in station_temps:
                    station_temps[station_key] = []

                # Collect temperatures month by month
                for month in MONTHS:
                    temp = to_float_or_none(row.get(month, ""))
                    if temp is None:
                        continue  # ignore missing values

                    station_temps[station_key].append(temp)

                    season = SEASON_BY_MONTH[month]
                    season_temps[season].append(temp)

    return station_temps, season_temps


def write_seasonal_averages(season_temps: Dict[str, List[float]], out_file: Path) -> None:
    """
    Writes seasonal average temperatures to average_temp.txt
    Format example:
      Summer: 28.50°C
    """
    lines = []
    for season in ["Summer", "Autumn", "Winter", "Spring"]:
        temps = season_temps.get(season, [])
        if temps:
            avg = sum(temps) / len(temps)
            lines.append(f"{season}: {avg:.2f}°C")
        else:
            lines.append(f"{season}: No data")

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_largest_range_station(station_temps: Dict[str, List[float]], out_file: Path) -> None:
    """
    Finds station(s) with largest temperature range (max - min).
    Handles ties by listing all tied stations.
    """
    best_range = -math.inf
    best_stations = []

    for station, temps in station_temps.items():
        if not temps:
            continue
        rng = max(temps) - min(temps)

        if rng > best_range:
            best_range = rng
            best_stations = [station]
        elif rng == best_range:
            best_stations.append(station)

    if best_range == -math.inf:
        out_file.write_text("No valid temperature data found.\n", encoding="utf-8")
        return

    lines = [
        f"Largest Temperature Range: {best_range:.2f}°C",
        "Station(s):"
    ]
    for st in best_stations:
        lines.append(f"- {st}")

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def safe_std_dev(values: List[float]) -> float:
    """
    Standard deviation with safe handling:
    - If 0 or 1 values, std dev = 0.0
    - Using population std dev (pstdev) because we treat the available dataset as the full set given.
    """
    if len(values) <= 1:
        return 0.0
    return statistics.pstdev(values)


def write_stability(station_temps: Dict[str, List[float]], out_file: Path) -> None:
    """
    Finds:
    - Most stable station(s): smallest std dev
    - Most variable station(s): largest std dev
    Handles ties.
    """
    stdev_by_station: Dict[str, float] = {}

    for station, temps in station_temps.items():
        if not temps:
            continue
        stdev_by_station[station] = safe_std_dev(temps)

    if not stdev_by_station:
        out_file.write_text("No valid temperature data found.\n", encoding="utf-8")
        return

    min_sd = min(stdev_by_station.values())
    max_sd = max(stdev_by_station.values())

    most_stable = [s for s, sd in stdev_by_station.items() if sd == min_sd]
    most_variable = [s for s, sd in stdev_by_station.items() if sd == max_sd]

    lines = [
        f"Most Stable Station(s) (Lowest Std Dev = {min_sd:.2f}):"
    ]
    for s in most_stable:
        lines.append(f"- {s}")

    lines.append("")  # blank line

    lines.append(
        f"Most Variable Station(s) (Highest Std Dev = {max_sd:.2f}):"
    )
    for s in most_variable:
        lines.append(f"- {s}")

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    temps_dir = base_dir / "temperatures"

    avg_out = base_dir / "average_temp.txt"
    range_out = base_dir / "largest_temp_range_station.txt"
    stability_out = base_dir / "temperature_stability_stations.txt"

    if not temps_dir.exists():
        print(f"ERROR: Folder not found: {temps_dir}")
        print("Create a folder named 'temperatures' and put all yearly CSV files inside it.")
        return

    try:
        station_temps, season_temps = read_all_temperatures(temps_dir)
    except Exception as e:
        print(f"ERROR while reading temperature data: {e}")
        return

    # Write outputs required by the assignment
    write_seasonal_averages(season_temps, avg_out)
    write_largest_range_station(station_temps, range_out)
    write_stability(station_temps, stability_out)

    # Console summary (useful for marking/debugging)
    total_stations = len(station_temps)
    total_files = len(list(temps_dir.glob("*.csv")))
    print("Q2 Completed ✅")
    print(f"- CSV files processed: {total_files}")
    print(f"- Stations found: {total_stations}")
    print(f"- Output written: {avg_out.name}, {range_out.name}, {stability_out.name}")


if __name__ == "__main__":
    main()
