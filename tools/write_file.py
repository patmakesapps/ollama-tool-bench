# tools/write_file.py
from registry import tool
from pathlib import Path


@tool(
    name="write_file",
    description=(
        "Creates a new file or overwrites an existing file with the given content. "
        "Always requires user confirmation before writing."
    ),
    parameters={
        "path": {
            "type": "string",
            "description": "The path of the file to create or overwrite.",
        },
        "content": {
            "type": "string",
            "description": "The full content to write to the file.",
        },
    },
)
def write_file(path: str, content: str) -> str:
    action = "Overwrite" if Path(path).exists() else "Create"
    confirm = input(f"\n[Confirmation] {action} file '{path}'? [y/N] ").strip().lower()
    if confirm != "y":
        return f"[Cancelled] File '{path}' was not written."

    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content, encoding="utf-8")
        return f"[Success] File '{path}' written ({len(content)} characters)."
    except Exception as e:
        return f"[Error] Could not write '{path}': {e}"
