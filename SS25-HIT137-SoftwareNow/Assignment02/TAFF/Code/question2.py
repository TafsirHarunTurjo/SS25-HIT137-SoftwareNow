# question2.py
# HIT137 Group Assignment 2 - Question 2
#
# This program reads ALL yearly CSV files from the "temperatures" folder and calculates:
# 1) Seasonal average temperature across all stations and years (Australian seasons)
# 2) Station(s) with largest temperature range (max - min across all years/months)
# 3) Most stable and most variable stations using standard deviation
#
# Outputs (as required):
# - average_temp.txt
# - largest_temp_range_station.txt
# - temperature_stability_stations.txt

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

SEASONS_IN_ORDER = ["Summer", "Autumn", "Winter", "Spring"]

# Float tolerance for tie checks
EPS = 1e-9


def is_missing(value: str) -> bool:
    """
    Missing values may be '', 'NaN', or actual blank.
    We'll treat anything that cannot convert to float as missing too.
    """
    if value is None:
        return True
    v = str(value).strip()
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
    Dict[str, List[float]],   # station_key -> list of all temps across all months/years
    Dict[str, List[float]],   # season      -> list of temps across all stations/years
    Dict[str, str]            # station_key -> display label (e.g., "STATION_NAME (STN_ID)")
]:
    """
    Reads all CSVs in folder, extracting station temps and season temps.

    CSV columns expected (based on your provided files):
      STATION_NAME, STN_ID, LAT, LON, January..December
    """
    station_temps: Dict[str, List[float]] = {}
    season_temps: Dict[str, List[float]] = {s: [] for s in SEASONS_IN_ORDER}
    station_label: Dict[str, str] = {}

    csv_files = sorted(folder.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder}")

    for file_path in csv_files:
        with file_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                continue

            # Ensure month columns exist
            for m in MONTHS:
                if m not in reader.fieldnames:
                    raise ValueError(f"Missing expected month column '{m}' in file: {file_path.name}")

            has_id = "STN_ID" in reader.fieldnames
            has_name = "STATION_NAME" in reader.fieldnames

            for row in reader:
                stn_id = (row.get("STN_ID") or "").strip() if has_id else ""
                stn_name = (row.get("STATION_NAME") or "").strip() if has_name else ""

                # Choose a stable key:
                # Prefer STN_ID if present, otherwise STATION_NAME
                if stn_id:
                    station_key = stn_id
                elif stn_name:
                    station_key = stn_name
                else:
                    continue  # no usable station identifier

                # Build a nice display label for outputs
                if station_key not in station_label:
                    if stn_name and stn_id:
                        station_label[station_key] = f"{stn_name} ({stn_id})"
                    elif stn_name:
                        station_label[station_key] = stn_name
                    else:
                        station_label[station_key] = station_key

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

    return station_temps, season_temps, station_label


def write_seasonal_averages(season_temps: Dict[str, List[float]], out_file: Path) -> None:
    """
    Writes seasonal average temperatures to average_temp.txt
    Required output format example:
      Summer: 28.5°C
    """
    lines = []
    for season in SEASONS_IN_ORDER:
        temps = season_temps.get(season, [])
        if temps:
            avg = sum(temps) / len(temps)
            lines.append(f"{season}: {avg:.1f}°C")
        else:
            lines.append(f"{season}: N/A")

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_largest_range_station(
    station_temps: Dict[str, List[float]],
    station_label: Dict[str, str],
    out_file: Path
) -> None:
    """
    Finds station(s) with largest temperature range (max - min).
    Handles ties by listing all tied stations.

    Required output format example:
      Station ABC: Range 45.2°C (Max: 48.3°C, Min: 3.1°C)
    """
    best_range = -math.inf
    winners = []  # list of (station_key, range, max, min)

    for station, temps in station_temps.items():
        if not temps:
            continue
        mx = max(temps)
        mn = min(temps)
        rng = mx - mn

        if rng > best_range + EPS:
            best_range = rng
            winners = [(station, rng, mx, mn)]
        elif abs(rng - best_range) <= EPS:
            winners.append((station, rng, mx, mn))

    if best_range == -math.inf or not winners:
        out_file.write_text("No valid temperature data found.\n", encoding="utf-8")
        return

    lines = []
    for station, rng, mx, mn in sorted(winners, key=lambda x: station_label.get(x[0], x[0])):
        label = station_label.get(station, station)
        lines.append(f"{label}: Range {rng:.1f}°C (Max: {mx:.1f}°C, Min: {mn:.1f}°C)")

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def safe_std_dev(values: List[float]) -> float:
    """
    Standard deviation with safe handling:
    - If 0 or 1 values, std dev = 0.0
    - Using population std dev (pstdev) since we're using the full provided dataset.
    """
    if len(values) <= 1:
        return 0.0
    return statistics.pstdev(values)


def write_stability(
    station_temps: Dict[str, List[float]],
    station_label: Dict[str, str],
    out_file: Path
) -> None:
    """
    Finds:
    - Most stable station(s): smallest std dev
    - Most variable station(s): largest std dev
    Handles ties.

    Required output format example:
      Most Stable: Station XYZ: StdDev 2.3°C
      Most Variable: Station DEF: StdDev 12.8°C
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

    most_stable = [s for s, sd in stdev_by_station.items() if abs(sd - min_sd) <= EPS]
    most_variable = [s for s, sd in stdev_by_station.items() if abs(sd - max_sd) <= EPS]

    lines = []

    # Most Stable lines (one per station, same prefix, per assignment style)
    for s in sorted(most_stable, key=lambda k: station_label.get(k, k)):
        label = station_label.get(s, s)
        lines.append(f"Most Stable: {label}: StdDev {stdev_by_station[s]:.1f}°C")

    # Most Variable lines
    for s in sorted(most_variable, key=lambda k: station_label.get(k, k)):
        label = station_label.get(s, s)
        lines.append(f"Most Variable: {label}: StdDev {stdev_by_station[s]:.1f}°C")

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
        station_temps, season_temps, station_label = read_all_temperatures(temps_dir)
    except Exception as e:
        print(f"ERROR while reading temperature data: {e}")
        return

    # Write outputs required by the assignment
    write_seasonal_averages(season_temps, avg_out)
    write_largest_range_station(station_temps, station_label, range_out)
    write_stability(station_temps, station_label, stability_out)

    # Console summary (useful for marking/debugging)
    total_stations = len(station_temps)
    total_files = len(list(temps_dir.glob("*.csv")))
    print("Q2 Completed ✅")
    print(f"- CSV files processed: {total_files}")
    print(f"- Stations found: {total_stations}")
    print(f"- Output written: {avg_out.name}, {range_out.name}, {stability_out.name}")


if __name__ == "__main__":
    main()
