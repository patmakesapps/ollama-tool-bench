# tools/clipboard.py
from registry import tool
import subprocess
import sys


def _read_clipboard() -> str:
    if sys.platform == "win32":
        result = subprocess.run(
            ["powershell", "-command", "Get-Clipboard"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    elif sys.platform == "darwin":
        result = subprocess.run(["pbpaste"], capture_output=True, text=True)
        return result.stdout.strip()
    else:
        result = subprocess.run(["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True)
        return result.stdout.strip()


def _write_clipboard(text: str) -> None:
    if sys.platform == "win32":
        subprocess.run(
            ["powershell", "-command", f"Set-Clipboard -Value '{text}'"],
            capture_output=True
        )
    elif sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=text.encode(), capture_output=True)
    else:
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), capture_output=True)


@tool(
    name="get_clipboard",
    description="Returns the current text content of the system clipboard.",
    parameters={
        "dummy": {
            "type": "string",
            "description": "Unused. Pass an empty string.",
        }
    },
)
def get_clipboard(dummy: str = "") -> str:
    try:
        text = _read_clipboard()
        return text if text else "[Clipboard is empty]"
    except Exception as e:
        return f"[Error] Could not read clipboard: {e}"


@tool(
    name="set_clipboard",
    description="Writes text to the system clipboard so the user can paste it.",
    parameters={
        "text": {
            "type": "string",
            "description": "The text to copy to the clipboard.",
        }
    },
)
def set_clipboard(text: str) -> str:
    try:
        _write_clipboard(text)
        return f"[Success] Copied to clipboard: {text[:80]}{'...' if len(text) > 80 else ''}"
    except Exception as e:
        return f"[Error] Could not write to clipboard: {e}"
