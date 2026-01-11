# question3.py
# HIT137 Group Assignment 2 - Question 3
#
# Turtle recursive pattern:
# For each edge:
# 1) Divide into 3 equal parts
# 2) Replace the middle part by two sides of an inward equilateral triangle
# 3) Recursively apply based on depth

import turtle


def draw_recursive_edge(length: float, depth: int) -> None:
    """
    Draw one edge using recursion.

    Base case:
      depth == 0 -> draw a straight line

    Recursive case:
      length is split into 3 parts. The middle third is replaced with two
      sides of an equilateral triangle pointing inward.
    """
    if depth == 0:
        turtle.forward(length)
        return

    segment = length / 3.0

    # First segment
    draw_recursive_edge(segment, depth - 1)

    # Turn to make inward triangle "notch"
    turtle.right(60)
    draw_recursive_edge(segment, depth - 1)

    turtle.left(120)
    draw_recursive_edge(segment, depth - 1)

    turtle.right(60)
    draw_recursive_edge(segment, depth - 1)


def draw_polygon(sides: int, length: float, depth: int) -> None:
    """Draw a polygon where each side is drawn using draw_recursive_edge."""
    angle = 360.0 / sides
    for _ in range(sides):
        draw_recursive_edge(length, depth)
        turtle.left(angle)


def main() -> None:
    # Speed up drawing for deeper recursion
    turtle.speed(0)
    turtle.hideturtle()

    try:
        sides = int(input("Enter the number of sides: ").strip())
        length = float(input("Enter the side length: ").strip())
        depth = int(input("Enter the recursion depth: ").strip())
    except ValueError:
        print("ERROR: Invalid input. Please enter integers for sides/depth and a number for length.")
        return

    if sides < 3:
        print("ERROR: Number of sides must be 3 or more.")
        return
    if length <= 0:
        print("ERROR: Side length must be greater than 0.")
        return
    if depth < 0:
        print("ERROR: Recursion depth must be 0 or more.")
        return

    # Position turtle to make drawing more visible
    turtle.penup()
    turtle.goto(-length / 2, 0)
    turtle.pendown()

    draw_polygon(sides, length, depth)

    turtle.done()


if __name__ == "__main__":
    main()
