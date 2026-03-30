# tools/read_file.py
from registry import tool


@tool(
    name="read_file",
    description=(
        "Reads and returns the contents of a file. "
        "Use this when the user wants to see or understand the contents of a file."
    ),
    parameters={
        "path": {
            "type": "string",
            "description": "The absolute or relative path to the file to read.",
        }
    },
)
def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            contents = f.read()
        if not contents:
            return f"[Info] File '{path}' exists but is empty."
        return contents
    except FileNotFoundError:
        return f"[Error] File not found: '{path}'"
    except Exception as e:
        return f"[Error] Could not read '{path}': {e}"
