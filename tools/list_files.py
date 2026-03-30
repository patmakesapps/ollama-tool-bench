# tools/list_files.py
from registry import tool
from pathlib import Path


@tool(
    name="list_files",
    description=(
        "Lists files in a directory matching an optional glob pattern. "
        "Use this to explore a codebase, find files by extension, or locate files by name."
    ),
    parameters={
        "directory": {
            "type": "string",
            "description": "The directory to search in. Use '.' for the current directory.",
        },
        "pattern": {
            "type": "string",
            "description": (
                "Glob pattern to filter results, e.g. '*.py', '**/*.js', 'main*'. "
                "Use '**/*' to list all files recursively."
            ),
        },
    },
)
def list_files(directory: str, pattern: str = "**/*") -> str:
    base = Path(directory)
    if not base.exists():
        return f"[Error] Directory not found: '{directory}'"
    if not base.is_dir():
        return f"[Error] '{directory}' is not a directory."

    matches = sorted(base.glob(pattern))
    files = [str(p) for p in matches if p.is_file()]

    if not files:
        return f"No files found in '{directory}' matching '{pattern}'."

    return f"{len(files)} file(s) found:\n" + "\n".join(files)
