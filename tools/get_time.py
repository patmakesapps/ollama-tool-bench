# tools/get_time.py
# Returns the current date and/or time.
# Great for testing — the model can't know this on its own,
# so if it answers correctly it MUST have called the tool.

from registry import tool
from datetime import datetime


@tool(
    name="get_time",
    description=(
        "Returns the current local date and time. "
        "Use this when the user asks what time it is, what today's date is, "
        "or anything that requires knowing the current moment."
    ),
    parameters={
        "format": {
            "type": "string",
            "enum": ["time", "date", "datetime"],
            "description": (
                "What to return: 'time' for current time only, "
                "'date' for today's date only, "
                "'datetime' for both date and time."
            ),
        }
    },
)
def get_time(format: str = "datetime") -> str:
    now = datetime.now()

    if format == "time":
        return now.strftime("Current time: %I:%M %p")
    elif format == "date":
        return now.strftime("Today's date: %A, %B %d, %Y")
    else:  # datetime or anything else
        return now.strftime("Current date and time: %A, %B %d, %Y at %I:%M %p")