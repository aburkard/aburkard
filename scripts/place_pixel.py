import json
import os
import sys

GRID_SIZE = 16
VALID_COLORS = ["white", "black", "red", "blue", "green", "yellow", "purple", "orange"]


def main():
    title = os.environ.get("ISSUE_TITLE", "")
    parts = title.strip().split()

    if len(parts) != 4 or parts[0] != "place":
        print(f"Skipping invalid issue title: {title}")
        sys.exit(0)

    _, x_str, y_str, color = parts

    try:
        x, y = int(x_str), int(y_str)
    except ValueError:
        print(f"Skipping invalid coordinates: {x_str}, {y_str}")
        sys.exit(0)

    if color not in VALID_COLORS:
        print(f"Skipping invalid color: {color}")
        sys.exit(0)

    if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
        print(f"Skipping out-of-bounds: {x}, {y}")
        sys.exit(0)

    with open("grid.json") as f:
        grid = json.load(f)

    grid[y][x] = color

    with open("grid.json", "w") as f:
        json.dump(grid, f)

    # Regenerate all markdown files
    sys.path.insert(0, os.path.dirname(__file__))
    from generate import main as generate_main
    generate_main()

    print(f"Placed {color} at ({x}, {y})")


if __name__ == "__main__":
    main()
