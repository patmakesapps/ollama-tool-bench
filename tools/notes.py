# tools/notes.py
# Persists key/value notes to a local JSON file so Lumi can remember things across sessions.
from registry import tool
from pathlib import Path
import json

_NOTES_FILE = Path(__file__).parent.parent / "notes.json"


def _load() -> dict:
    if _NOTES_FILE.exists():
        try:
            return json.loads(_NOTES_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save(data: dict) -> None:
    _NOTES_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


@tool(
    name="save_note",
    description=(
        "WRITE tool: saves a new note to persistent storage. "
        "Use this whenever the user says 'remember', 'save', 'note that', or 'don't forget'. "
        "Requires both a key and a value. Notes persist across conversations."
    ),
    parameters={
        "key": {
            "type": "string",
            "description": "A short label for the note, e.g. 'project_name' or 'user_preference'.",
        },
        "value": {
            "type": "string",
            "description": "The content to remember.",
        },
    },
)
def save_note(key: str, value: str) -> str:
    data = _load()
    data[key] = value
    _save(data)
    return f"[Success] Saved note '{key}'."


@tool(
    name="get_note",
    description=(
        "READ tool: retrieves a previously saved note from persistent storage. "
        "Use this when the user asks what you remember, or references something saved before. "
        "Do NOT use this to save new information — use save_note for that."
    ),
    parameters={
        "key": {
            "type": "string",
            "description": "The key of the note to retrieve. Pass '*' to list all saved notes.",
        }
    },
)
def get_note(key: str) -> str:
    data = _load()
    if key == "*":
        if not data:
            return "[No notes saved yet]"
        return "\n".join(f"{k}: {v}" for k, v in data.items())
    if key not in data:
        return f"[Not found] No note saved under '{key}'."
    return f"{key}: {data[key]}"
