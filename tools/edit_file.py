# tools/edit_file.py
from registry import tool
from pathlib import Path


@tool(
    name="edit_file",
    description=(
        "Finds and replaces a specific string inside a file. "
        "Always requires user confirmation before making changes."
    ),
    parameters={
        "path": {
            "type": "string",
            "description": "The path to the file to edit.",
        },
        "old_text": {
            "type": "string",
            "description": "The exact text to find and replace.",
        },
        "new_text": {
            "type": "string",
            "description": "The text to replace it with.",
        },
    },
)
def edit_file(path: str, old_text: str, new_text: str) -> str:
    try:
        original = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[Error] File not found: '{path}'"
    except Exception as e:
        return f"[Error] Could not read '{path}': {e}"

    if old_text not in original:
        return f"[Error] Text not found in '{path}':\n{old_text}"

    count = original.count(old_text)
    print(f"\n[Confirmation] Edit '{path}': replace {count} occurrence(s) of:")
    print(f"  OLD: {old_text[:120]}")
    print(f"  NEW: {new_text[:120]}")
    confirm = input("[y/N] ").strip().lower()
    if confirm != "y":
        return f"[Cancelled] '{path}' was not modified."

    updated = original.replace(old_text, new_text)
    try:
        Path(path).write_text(updated, encoding="utf-8")
        return f"[Success] Replaced {count} occurrence(s) in '{path}'."
    except Exception as e:
        return f"[Error] Could not write '{path}': {e}"
