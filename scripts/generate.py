import json
import os

REPO = "aburkard/aburkard"
GRID_SIZE = 16
CELL_SIZE = 30
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
    lines = []
    for y, row in enumerate(grid):
        cells = []
        for x, cell in enumerate(row):
            emoji = emoji_for(cell)
            url = f"https://github.com/{REPO}/issues/new?title=place+{x}+{y}+{color}"
            cells.append(f"[{emoji}]({url})")
        lines.append("".join(cells))
    return "\n\n".join(lines)


def generate_readme(grid, svg_content):
    palette_items = []
    for name, emoji in COLORS.items():
        palette_items.append(f"[{emoji}](colors/{name}.md)")
    palette = " ".join(palette_items)

    return f"""# place

Pick a color, then click a cell.

{palette}

<a href="https://github.com/{REPO}"><img src="https://raw.githubusercontent.com/{REPO}/main/canvas.svg" alt="canvas" width="496"></a>
"""


def generate_color_page(grid, color_name, color_emoji):
    clickable = generate_clickable_grid(grid, color_name)
    return f"""# Placing: {color_emoji}

[back to canvas](../README.md)

{clickable}
"""


def main():
    grid = load_grid()

    svg_content = generate_svg(grid)
    with open("canvas.svg", "w") as f:
        f.write(svg_content)

    with open("README.md", "w") as f:
        f.write(generate_readme(grid, svg_content))

    os.makedirs("colors", exist_ok=True)
    for name, emoji in COLORS.items():
        with open(f"colors/{name}.md", "w") as f:
            f.write(generate_color_page(grid, name, emoji))


if __name__ == "__main__":
    main()
