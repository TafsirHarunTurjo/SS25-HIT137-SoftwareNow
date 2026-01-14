"""
Question 3 — Recursive Turtle Geometric Pattern (Inward Indentation)

What it draws:
- Start with a regular polygon (n sides).
- For each edge, recursively replace the middle third with two sides of an equilateral
  triangle that points *inward* (relative to a counter-clockwise polygon).

How to run (Terminal / VS Code):
    python question3.py

Notes:
- A turtle window will open.
- Higher recursion depths grow very fast (depth 0–4 is usually reasonable).
- The code uses ONLY Python's standard library.
"""

from draw_center import *

def _read_int(prompt, min_value):
    while True:
        try:
            v = int(input(prompt).strip())
            if v < min_value:
                print(f"Please enter an integer >= {min_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")


def _read_float(prompt, min_value):
    while True:
        try:
            v = float(input(prompt).strip())
            if v <= min_value:
                print(f"Please enter a number > {min_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("Q3 — Recursive Turtle Pattern")
    sides = _read_int("Enter number of polygon sides (>=3): ", 3)
    side_length = _read_float("Enter side length in pixels (>0): ", 0.0)
    depth = _read_int("Enter recursion depth (>=0): ", 0)

    draw_pattern(sides, side_length, depth)


if __name__ == "__main__":
    main()
