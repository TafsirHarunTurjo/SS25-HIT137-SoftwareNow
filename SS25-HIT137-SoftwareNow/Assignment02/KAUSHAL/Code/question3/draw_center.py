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