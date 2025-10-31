"""Rendering utilities.

Provides two rendering backends:
- Turtle-based interactive renderer (opens a window)
- Pillow-based headless renderer that can export PNG files

The main script can choose which backend to use. Pillow is optional.
"""
from typing import List, Tuple, Optional

try:
    from PIL import Image, ImageDraw
except Exception:
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore

import turtle as t
import random


def draw_turtle_grid(rows: int, cols: int, dot_size: int, spacing: int, bg_color: str, palette: List[Tuple[int, int, int]]):
    """Open a Turtle window and draw the grid. This call blocks until the window is closed."""
    t.colormode(255)
    screen = t.Screen()
    screen.bgcolor(bg_color)

    rex = t.Turtle()
    rex.hideturtle()
    rex.penup()

    start_x = -((cols - 1) * spacing) / 2
    start_y = -((rows - 1) * spacing) / 2

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing
            y = start_y + row * spacing
            rex.goto(x, y)
            rex.dot(dot_size, random.choice(palette))

    screen.mainloop()


def render_png(path: str, rows: int, cols: int, dot_size: int, spacing: int, bg_color: str, palette: List[Tuple[int, int, int]], margin: Optional[int] = None):
    """Render the grid into a PNG file using Pillow.

    If Pillow is not installed, raise ImportError.
    """
    if Image is None or ImageDraw is None:
        raise ImportError('Pillow is required for PNG export. Install with: pip install pillow')

    # compute canvas size. margin makes circles fully visible on edges
    if margin is None:
        margin = int(dot_size * 1.5)

    width = spacing * (cols - 1) + margin * 2 + dot_size
    height = spacing * (rows - 1) + margin * 2 + dot_size

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    start_x = margin + dot_size // 2
    start_y = margin + dot_size // 2

    for r in range(rows):
        for c in range(cols):
            cx = start_x + c * spacing
            cy = start_y + r * spacing
            color = random.choice(palette)
            left = cx - dot_size // 2
            top = cy - dot_size // 2
            right = cx + dot_size // 2
            bottom = cy + dot_size // 2
            draw.ellipse([left, top, right, bottom], fill=tuple(color))

    img.save(path, format='PNG')
