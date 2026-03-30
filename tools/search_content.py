# tools/search_content.py
from registry import tool
from pathlib import Path
import re


@tool(
    name="search_content",
    description=(
        "Searches for a text string or regex pattern inside files in a directory. "
        "Use this to find where something is defined or used in a codebase."
    ),
    parameters={
        "directory": {
            "type": "string",
            "description": "The directory to search in.",
        },
        "query": {
            "type": "string",
            "description": "The text string or regex pattern to search for.",
        },
        "file_pattern": {
            "type": "string",
            "description": "Glob pattern to limit which files are searched, e.g. '*.py'. Defaults to all files.",
        },
    },
)
def search_content(directory: str, query: str, file_pattern: str = "**/*") -> str:
    base = Path(directory)
    if not base.exists():
        return f"[Error] Directory not found: '{directory}'"

    try:
        pattern = re.compile(query, re.IGNORECASE)
    except re.error as e:
        return f"[Error] Invalid regex pattern: {e}"

    matches = []
    for filepath in sorted(base.glob(file_pattern)):
        if not filepath.is_file():
            continue
        try:
            lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            if pattern.search(line):
                matches.append(f"{filepath}:{i}: {line.strip()}")

    if not matches:
        return f"No matches found for '{query}' in '{directory}' ({file_pattern})."

    return f"{len(matches)} match(es):\n" + "\n".join(matches)
