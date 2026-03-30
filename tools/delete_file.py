# tools/delete_file.py
from registry import tool
from pathlib import Path


@tool(
    name="delete_file",
    description=(
        "Deletes a file from the filesystem. "
        "Always requires user confirmation before deleting."
    ),
    parameters={
        "path": {
            "type": "string",
            "description": "The path to the file to delete.",
        }
    },
)
def delete_file(path: str) -> str:
    if not Path(path).exists():
        return f"[Error] File not found: '{path}'"

    print(f"\n[Confirmation] Permanently delete '{path}'?")
    confirm = input("[y/N] ").strip().lower()
    if confirm != "y":
        return f"[Cancelled] '{path}' was not deleted."

    try:
        Path(path).unlink()
        return f"[Success] Deleted '{path}'."
    except Exception as e:
        return f"[Error] Could not delete '{path}': {e}"
