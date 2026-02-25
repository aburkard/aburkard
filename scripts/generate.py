import glob
import hashlib
import io
import json
import os

from PIL import Image

REPO = "aburkard/aburkard"
GRID_SIZE = 256
CELL_SIZE = 2

COLORS = {
    "black": "\u2b1b",
    "white": "\u2b1c",
    "red": "\U0001f7e5",
    "blue": "\U0001f7e6",
    "green": "\U0001f7e9",
    "yellow": "\U0001f7e8",
    "purple": "\U0001f7ea",
    "orange": "\U0001f7e7",
}

HEX_COLORS = {
    "black": "#000000",
    "white": "#e0e0e0",
    "red": "#e74c3c",
    "blue": "#3498db",
    "green": "#2ecc71",
    "yellow": "#f1c40f",
    "purple": "#9b59b6",
    "orange": "#e67e22",
}


def load_grid():
    with open("grid.json") as f:
        return json.load(f)


def grid_to_png(grid):
    """Render the grid as a PNG image bytes."""
    size = GRID_SIZE * CELL_SIZE
    img = Image.new("RGB", (size, size))
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            hex_color = HEX_COLORS.get(color, HEX_COLORS["white"])
            r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
            for dy in range(CELL_SIZE):
                for dx in range(CELL_SIZE):
                    img.putpixel((x * CELL_SIZE + dx, y * CELL_SIZE + dy), (r, g, b))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_readme(png_filename):
    palette_items = []
    for name, emoji in COLORS.items():
        url = f"https://github.com/{REPO}/issues/new?title=place+0+0+{name}&body=%3C%21--+Change+the+coordinates+in+the+title+to+place+your+pixel.+Format%3A+place+x+y+{name}+--%3E"
        palette_items.append(f"[{emoji}]({url})")
    palette = " ".join(palette_items)

    custom_url = f"https://github.com/{REPO}/issues/new?title=&body=%3C%21--+Type+your+request+as+the+issue+title%2C+then+submit.%0A%0AExamples%3A%0A-+Draw+a+castle+with+a+moat%0A-+Add+a+forest+of+trees+across+the+bottom%0A-+Write+%22hello+world%22+in+blue%0A-+Fill+the+sky+with+stars+--%3E"

    return f"""## r/place

Pick a color to place a pixel, or [draw something]({custom_url}) with AI.

{palette}

<picture><img src="{png_filename}" alt="canvas" width="512"></picture>
"""


def main():
    grid = load_grid()

    # Delete old canvas files
    for old in glob.glob("canvas-*.svg") + glob.glob("canvas-*.png"):
        os.remove(old)
    if os.path.exists("canvas.svg"):
        os.remove("canvas.svg")

    png_bytes = grid_to_png(grid)
    content_hash = hashlib.md5(png_bytes).hexdigest()[:8]
    png_filename = f"canvas-{content_hash}.png"

    with open(png_filename, "wb") as f:
        f.write(png_bytes)

    with open("README.md", "w") as f:
        f.write(generate_readme(png_filename))


if __name__ == "__main__":
    main()
