import glob
import hashlib
import json
import os

REPO = "aburkard/aburkard"
GRID_SIZE = 32
CELL_SIZE = 15
GRID_PAD = 1

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


def emoji_for(color):
    return COLORS.get(color, COLORS["white"])


def generate_svg(grid):
    total = CELL_SIZE * GRID_SIZE + GRID_PAD * (GRID_SIZE + 1)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{total}" viewBox="0 0 {total} {total}">',
        f'<rect width="{total}" height="{total}" fill="#c0c0c0"/>',
    ]
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            px = GRID_PAD + x * (CELL_SIZE + GRID_PAD)
            py = GRID_PAD + y * (CELL_SIZE + GRID_PAD)
            fill = HEX_COLORS.get(cell, HEX_COLORS["white"])
            lines.append(f'<rect x="{px}" y="{py}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{fill}"/>')
    lines.append("</svg>")
    return "\n".join(lines)


def generate_clickable_grid(grid, color):
    rows = []
    for y, row in enumerate(grid):
        cells = []
        for x, cell in enumerate(row):
            emoji = emoji_for(cell)
            url = f"https://github.com/{REPO}/issues/new?title=place+{x}+{y}+{color}&body=%3C%21--+Click+%22Submit+new+issue%22+to+place+your+pixel.+--%3E"
            cells.append(f'<td><a href="{url}">{emoji}</a></td>')
        rows.append(f'<tr>{"".join(cells)}</tr>')
    return f'<table>{"".join(rows)}</table>'


def generate_readme(grid, svg_filename):
    palette_items = []
    for name, emoji in COLORS.items():
        palette_items.append(f"[{emoji}](colors/{name}.md)")
    palette = " ".join(palette_items)

    custom_url = f"https://github.com/{REPO}/issues/new?title=&body=%3C%21--+Type+your+request+as+the+issue+title%2C+then+submit.%0A%0AExamples%3A%0A-+Add+a+blue+ghost+next+to+the+red+one%0A-+Draw+a+small+green+tree+in+the+top+right%0A-+Write+%22hello%22+in+orange%0A-+Clear+the+bottom+row+--%3E"

    return f"""## r/place

Pick a color to place a pixel, or [draw something]({custom_url}) with AI.

{palette}

<img src="{svg_filename}" alt="canvas" width="512">
"""


def generate_color_page(grid, color_name, color_emoji):
    clickable = generate_clickable_grid(grid, color_name)
    return f"""Placing {color_emoji} — click a cell, then submit the issue.

[back to canvas](../README.md)

{clickable}
"""


def main():
    grid = load_grid()

    # Delete old canvas-*.svg files
    for old in glob.glob("canvas-*.svg"):
        os.remove(old)
    # Also remove legacy canvas.svg
    if os.path.exists("canvas.svg"):
        os.remove("canvas.svg")

    svg_content = generate_svg(grid)
    content_hash = hashlib.md5(svg_content.encode()).hexdigest()[:8]
    svg_filename = f"canvas-{content_hash}.svg"

    with open(svg_filename, "w") as f:
        f.write(svg_content)

    with open("README.md", "w") as f:
        f.write(generate_readme(grid, svg_filename))

    os.makedirs("colors", exist_ok=True)
    for name, emoji in COLORS.items():
        with open(f"colors/{name}.md", "w") as f:
            f.write(generate_color_page(grid, name, emoji))


if __name__ == "__main__":
    main()
