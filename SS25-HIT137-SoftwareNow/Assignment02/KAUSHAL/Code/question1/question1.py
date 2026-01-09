from encryption import *
from decryption import *
from verification import *
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    while True:
        shift1_raw = input("Enter the first shift value: ")
        shift2_raw = input("Enter the second shift value: ")

        try:
            shift1_value = int(shift1_raw)
            shift2_value = int(shift2_raw)

            if shift1_value > 0 and shift2_value > 0:
                break  # valid input, exit loop
            else:
                print("Both numbers must be positive integers. Try again.\n")
        except ValueError:
            print("Invalid input. Please enter numbers only.\n")

    # Call the functions after valid input
    encryption(shift1_value, shift2_value, base_dir)
    decryption(shift1_value, shift2_value, base_dir)
    raw_file = base_dir/"raw_text.txt"
    decrypted_file = base_dir/"decrypted_text.txt"
    verification(raw_file, decrypted_file)

if __name__ == "__main__":
    main()
    

    


