"""
Question 3 — Recursive Turtle Geometric Pattern (Inward Indentation)

What it draws:
- Start with a regular polygon (n sides).
- For each edge, recursively replace the middle third with two sides of an equilateral
  triangle that points *inward* (relative to a counter-clockwise polygon).

How to run (Terminal / VS Code):
    python q3_recursive_turtle.py

Notes:
- A turtle window will open.
- Higher recursion depths grow very fast (depth 0–4 is usually reasonable).
- The code uses ONLY Python's standard library.
"""

import turtle
import math


def indent_edge(length, depth, pen):
    """Recursively draw one edge using the inward-indentation rule (Koch-like)."""
    if depth == 0:
        pen.forward(length)
        return

    third = length / 3.0

    indent_edge(third, depth - 1, pen)
    pen.left(60)
    indent_edge(third, depth - 1, pen)
    pen.right(120)
    indent_edge(third, depth - 1, pen)
    pen.left(60)
    indent_edge(third, depth - 1, pen)


class _SimPen:
    """Tiny turtle-like simulator used only to compute the drawing bounding box (for centering)."""

    def __init__(self, x=0.0, y=0.0, heading=0.0):
        self.x = x
        self.y = y
        self.heading = heading  # degrees, 0 = east
        self.minx = self.maxx = x
        self.miny = self.maxy = y

    def _update_bbox(self):
        self.minx = min(self.minx, self.x)
        self.maxx = max(self.maxx, self.x)
        self.miny = min(self.miny, self.y)
        self.maxy = max(self.maxy, self.y)

    def forward(self, dist):
        r = math.radians(self.heading)
        self.x += dist * math.cos(r)
        self.y += dist * math.sin(r)
        self._update_bbox()

    def left(self, ang):
        self.heading += ang

    def right(self, ang):
        self.heading -= ang


def _compute_center_offset(sides, side_length, depth):
    """Return (dx, dy) so the final drawing is centered at (0,0)."""
    sim = _SimPen(0.0, 0.0, 0.0)
    exterior_angle = 360.0 / sides

    for _ in range(sides):
        indent_edge(side_length, depth, sim)
        sim.left(exterior_angle)

    cx = (sim.minx + sim.maxx) / 2.0
    cy = (sim.miny + sim.maxy) / 2.0
    return -cx, -cy


def draw_pattern(sides, side_length, depth):
    """Draw the full recursive polygon pattern, centered on the screen."""
    screen = turtle.Screen()
    screen.title("Q3 — Recursive Inward-Indentation Polygon Pattern")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # Speed-up drawing
    screen.tracer(0, 0)

    # Centering fix
    dx, dy = _compute_center_offset(sides, side_length, depth)
    t.penup()
    t.goto(dx, dy)
    t.setheading(0)
    t.pendown()

    exterior_angle = 360.0 / sides

    # Draw counter-clockwise (left turns)
    for _ in range(sides):
        indent_edge(side_length, depth, t)
        t.left(exterior_angle)

    screen.update()
    turtle.done()


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
