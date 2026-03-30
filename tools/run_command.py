# tools/run_command.py
from registry import tool
import subprocess


@tool(
    name="run_command",
    description=(
        "Runs a shell command and returns its output. "
        "Use this to execute scripts, run tests, check system info, or verify code output. "
        "Always requires user confirmation before running."
    ),
    parameters={
        "command": {
            "type": "string",
            "description": "The shell command to run, e.g. 'python main.py' or 'git status'.",
        }
    },
)
def run_command(command: str) -> str:
    print(f"\n[Confirmation] Run command: {command}")
    confirm = input("[y/N] ").strip().lower()
    if confirm != "y":
        return "[Cancelled] Command was not run."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip()
        errors = result.stderr.strip()

        parts = []
        if output:
            parts.append(f"stdout:\n{output}")
        if errors:
            parts.append(f"stderr:\n{errors}")
        if result.returncode != 0:
            parts.append(f"exit code: {result.returncode}")

        return "\n\n".join(parts) if parts else "[No output]"
    except subprocess.TimeoutExpired:
        return "[Error] Command timed out after 30 seconds."
    except Exception as e:
        return f"[Error] Failed to run command: {e}"
