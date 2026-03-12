import json
from pathlib import Path


def save_response_to_json(response, file_path: str) -> None:
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        pass


def extract_tile_grid_to_file(source_path: str, output_path: str, ) -> None:
    try:
        source = Path(source_path)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with source.open("r", encoding="utf-8") as f:
            data = json.load(f)

        widget_states = data.get("widgetStates", {})

        tile_value = None

        for key, value in widget_states.items():
            if key.startswith("tileGrid"):
                tile_value = value
                break

        if tile_value is None:
            raise ValueError("tileGrid* not found")

        if isinstance(tile_value, str):
            try:
                tile_value = json.loads(tile_value)
            except json.JSONDecodeError:
                pass

        with output.open("w", encoding="utf-8") as f:
            json.dump(tile_value, f, ensure_ascii=False, indent=2)
    except:
        print("Failed to load tileGrid")
        pass

