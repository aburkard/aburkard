import json
import os
import sys

GRID_SIZE = 32
VALID_COLORS = ["white", "black", "red", "blue", "green", "yellow", "purple", "orange"]


def place_single(grid, title):
    """Handle 'place x y color' format."""
    parts = title.strip().split()
    if len(parts) != 4 or parts[0] != "place":
        return None

    _, x_str, y_str, color = parts
    try:
        x, y = int(x_str), int(y_str)
    except ValueError:
        return None

    if color not in VALID_COLORS or not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
        return None

    grid[y][x] = color
    return f"Placed {color} at ({x}, {y})"


def place_with_llm(grid, prompt):
    """Handle natural language requests via Gemini."""
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set, skipping LLM request")
        sys.exit(0)

    client = genai.Client(api_key=api_key)

    grid_str = json.dumps(grid)
    system_prompt = f"""You are a pixel art assistant for a 32x32 grid. The grid is a JSON array of rows, where each cell is a color string.

Available colors: {', '.join(VALID_COLORS)}

The user will ask you to draw or modify something on the canvas. Return ONLY a valid JSON array representing the updated 32x32 grid. No explanation, no markdown, no code fences — just the JSON array.

Keep existing pixel art intact unless the user explicitly asks to change or remove it. Be creative but keep drawings simple and recognizable at 32x32 pixel resolution.

Current grid:
{grid_str}"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=system_prompt + "\n\nUser request: " + prompt,
    )

    text = response.text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[: text.rfind("```")]
        text = text.strip()

    new_grid = json.loads(text)

    # Validate
    if len(new_grid) != GRID_SIZE:
        raise ValueError(f"Expected {GRID_SIZE} rows, got {len(new_grid)}")
    for row in new_grid:
        if len(row) != GRID_SIZE:
            raise ValueError(f"Expected {GRID_SIZE} cols, got {len(row)}")
        for cell in row:
            if cell not in VALID_COLORS:
                raise ValueError(f"Invalid color: {cell}")

    return new_grid


def main():
    title = os.environ.get("ISSUE_TITLE", "")

    with open("grid.json") as f:
        grid = json.load(f)

    # Try single pixel placement first
    result = place_single(grid, title)
    if result:
        with open("grid.json", "w") as f:
            json.dump(grid, f)
        print(result)
    else:
        # Natural language request
        try:
            new_grid = place_with_llm(grid, title)
            with open("grid.json", "w") as f:
                json.dump(new_grid, f)
            print(f"LLM updated grid for: {title}")
        except Exception as e:
            print(f"LLM request failed: {e}")
            sys.exit(1)

    # Regenerate all files
    sys.path.insert(0, os.path.dirname(__file__))
    from generate import main as generate_main
    generate_main()


if __name__ == "__main__":
    main()
