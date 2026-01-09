import pandas as pd
from pathlib import Path
from seasional_average import *
from temperature_range import *
from temperature_stability import *

def main():
    # Get the directory where this script is located
    base_dir = Path(__file__).resolve().parent

    # Path to the temperatures folder
    temperature_dir = base_dir / "temperatures"

    # Read all CSV files dynamically
    csv_files = temperature_dir.glob("*.csv")

    # Combine all data
    all_data = []
    for file in csv_files:
        df = pd.read_csv(file)
        all_data.append(df)

    data = pd.concat(all_data, ignore_index=True)

    month_cols = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
    ]

    seasional_average(data,base_dir)
    temperature_range(data, base_dir,month_cols)
    temperature_stability(data, base_dir, month_cols)


if __name__ == "__main__":
    main()
