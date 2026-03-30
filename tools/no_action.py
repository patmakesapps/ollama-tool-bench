# tools/no_action.py
from registry import tool


@tool(
    name="no_action",
    description=(
        "Call this tool when you can answer the user directly without any other tool. "
        "Use this for greetings, casual conversation, general knowledge questions, "
        "opinions, or anything you already know the answer to. "
        "Pass your full response as the message parameter."
    ),
    parameters={
        "message": {
            "type": "string",
            "description": "Your response to the user.",
        }
    },
)
def no_action(message: str) -> str:
    return message
