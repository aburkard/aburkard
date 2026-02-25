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
    system_prompt = f"""You are a pixel art assistant for a 32x32 grid (x: 0-31, y: 0-31). x is the column (left to right), y is the row (top to bottom).

Available colors: {', '.join(VALID_COLORS)}

The user will request a drawing or modification. You must:

1. REFUSE any request that is offensive, hateful, violent, sexual, or inappropriate. If the request is inappropriate, return exactly: {{"refused": true}}
2. Otherwise, return ONLY a JSON array of pixel changes: [[x, y, "color"], ...]
   - Only include pixels that need to change.
   - Do NOT output the full grid.
   - No explanation, no markdown, no code fences. Just the JSON array.

Keep existing art intact unless the user asks to change or remove it. Be creative but keep drawings simple and recognizable at 32x32 resolution.

Current grid:
{grid_str}"""

    import time

    models = ["gemini-3-flash-preview", "gemini-2.5-flash"]
    response = None
    for model in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=system_prompt + "\n\nUser request: " + prompt,
                )
                break
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    print(f"{model} attempt {attempt + 1} failed: {e}")
                    time.sleep(2 ** attempt)
                else:
                    raise
        if response:
            break

    if not response:
        raise RuntimeError("All models unavailable after retries")

    text = response.text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[: text.rfind("```")]
        text = text.strip()

    parsed = json.loads(text)

    # Check if refused
    if isinstance(parsed, dict) and parsed.get("refused"):
        raise ValueError("Request was refused as inappropriate")

    # Validate and apply changes
    if not isinstance(parsed, list):
        raise ValueError(f"Expected a JSON array, got {type(parsed).__name__}")

    changes = 0
    for item in parsed:
        if not isinstance(item, list) or len(item) != 3:
            continue
        x, y, color = item
        if not isinstance(x, int) or not isinstance(y, int):
            continue
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            continue
        if color not in VALID_COLORS:
            continue
        grid[y][x] = color
        changes += 1

    if changes == 0:
        raise ValueError("No valid pixel changes in LLM response")

    return changes


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
            changes = place_with_llm(grid, title)
            with open("grid.json", "w") as f:
                json.dump(grid, f)
            print(f"LLM applied {changes} pixel changes for: {title}")
        except Exception as e:
            print(f"LLM request failed: {e}")
            sys.exit(1)

    # Regenerate all files
    sys.path.insert(0, os.path.dirname(__file__))
    from generate import main as generate_main
    generate_main()


if __name__ == "__main__":
    main()
