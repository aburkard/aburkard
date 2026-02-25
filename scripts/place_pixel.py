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
    system_prompt = f"""You are a pixel art assistant. The canvas is EXACTLY 32 rows and 32 columns. Each row MUST have exactly 32 elements. The output MUST be a JSON array with exactly 32 arrays, each with exactly 32 color strings.

Available colors: {', '.join(VALID_COLORS)}

Return ONLY the JSON array. No explanation, no markdown, no code fences.

Keep existing pixel art intact unless the user explicitly asks to change or remove it.

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

    # Fix up dimensions if slightly off
    # Trim or pad rows
    while len(new_grid) > GRID_SIZE:
        new_grid.pop()
    while len(new_grid) < GRID_SIZE:
        new_grid.append(["white"] * GRID_SIZE)
    # Trim or pad columns
    for i, row in enumerate(new_grid):
        if len(row) > GRID_SIZE:
            new_grid[i] = row[:GRID_SIZE]
        while len(new_grid[i]) < GRID_SIZE:
            new_grid[i].append("white")

    # Validate colors, replace invalid ones with white
    for y, row in enumerate(new_grid):
        for x, cell in enumerate(row):
            if cell not in VALID_COLORS:
                new_grid[y][x] = "white"

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
