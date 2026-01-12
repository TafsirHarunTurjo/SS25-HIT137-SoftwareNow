# question3.py
# HIT137 Group Assignment 2 - Question 3
#
# Inward indentation fractal (Koch inward notch) on each polygon side.

import turtle


def draw_inward_edge(length: float, depth: int) -> None:
    """
    Draw one edge with inward indentation using recursion.

    Depth 0: straight line
    Depth >0: split into 3 parts; replace the middle third by two sides
              of an equilateral triangle pointing inward (a notch).
    """
    if depth == 0:
        turtle.forward(length)
        return

    seg = length / 3.0

    # 1st third
    draw_inward_edge(seg, depth - 1)

    # Inward notch (NOT the classic outward Koch bump)
    turtle.right(60)
    draw_inward_edge(seg, depth - 1)

    turtle.left(120)
    draw_inward_edge(seg, depth - 1)

    turtle.right(60)
    draw_inward_edge(seg, depth - 1)


def draw_polygon(sides: int, length: float, depth: int) -> None:
    """
    Draw polygon CLOCKWISE so the indentation consistently points inward.
    """
    angle = 360.0 / sides
    for _ in range(sides):
        draw_inward_edge(length, depth)
        turtle.right(angle)   # clockwise turn


def main() -> None:
    # Slow drawing (visible)
    # turtle.speed(3)       # 1 slowest, 10 fast, 0 instant
    # turtle.delay(15)      # delay between steps (ms)
    turtle.speed(10)       
    turtle.delay(5)
    turtle.pensize(2)
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

    # Center better (roughly)
    turtle.penup()
    turtle.goto(-length / 2, length / 3)
    turtle.pendown()

    draw_polygon(sides, length, depth)

    turtle.done()


if __name__ == "__main__":
    main()
