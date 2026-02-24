import json
import os

REPO = "aburkard/aburkard"
GRID_SIZE = 16

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


def load_grid():
    with open("grid.json") as f:
        return json.load(f)


def emoji_for(color):
    return COLORS.get(color, COLORS["white"])


def generate_display_grid(grid):
    lines = []
    for row in grid:
        lines.append("".join(emoji_for(cell) for cell in row))
    return "\n\n".join(lines)


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


def generate_readme(grid):
    display = generate_display_grid(grid)
    palette_items = []
    for name, emoji in COLORS.items():
        palette_items.append(f"[{emoji}](colors/{name}.md)")
    palette = " ".join(palette_items)

    return f"""# place

Pick a color, then click a cell.

{palette}

{display}
"""


def generate_color_page(grid, color_name, color_emoji):
    clickable = generate_clickable_grid(grid, color_name)
    return f"""# Placing: {color_emoji}

[back to canvas](../README.md)

{clickable}
"""


def main():
    grid = load_grid()

    with open("README.md", "w") as f:
        f.write(generate_readme(grid))

    os.makedirs("colors", exist_ok=True)
    for name, emoji in COLORS.items():
        with open(f"colors/{name}.md", "w") as f:
            f.write(generate_color_page(grid, name, emoji))


if __name__ == "__main__":
    main()
