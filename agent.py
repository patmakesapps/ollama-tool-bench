# agent.py
# The agentic loop. Run this file to talk to your tool-enabled model.
#
# Usage:
#   python agent.py
#   python agent.py "What is 847 divided by 13?"   single prompt mode

import json
import sys

import ollama

# Importing tools triggers __init__.py which auto-registers everything
import tools
from registry import call_tool, get_schemas, list_tools

MODEL = "llama3.2:3b"

SYSTEM_PROMPT = (
    "You are Lumi, a helpful assistant. "
    "Use your tools when the user's question genuinely requires it. "
    "Do not call tools during casual conversation. "
    "After calling web_search specifically, write a concise summary of the findings, "
    "then list each source as a numbered reference with its URL. "
    "For all other tools, just answer directly using the result — no fake sources or URLs."
)


def run_agent(user_prompt: str, verbose: bool = True) -> str:
    """
    Agentic loop using Ollama's native tool-calling API.
    The model returns structured tool_calls; no text parsing needed.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    max_iterations = 10

    for _ in range(max_iterations):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=get_schemas(),
        )

        msg = response["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls") or []

        if not tool_calls:
            # No tool call — this is the final answer
            content = msg.get("content", "").strip()
            if verbose:
                print(f"\n[assistant] {content}\n")
            return content

        # Execute every tool the model requested
        tool_results = []
        for tc in tool_calls:
            fn_name = tc["function"]["name"]
            fn_args = tc["function"].get("arguments", {})

            if verbose:
                print(f"\n[tool call] {fn_name}({fn_args})")

            result = call_tool(fn_name, fn_args)

            if verbose:
                print(f"[tool result] {result}")

            messages.append({"role": "tool", "content": result})
            tool_results.append(f"{fn_name}: {result}")

        # Force a final text answer — no tools available, explicit context provided
        results_block = "\n".join(tool_results)
        final_response = ollama.chat(
            model=MODEL,
            messages=messages + [{
                "role": "user",
                "content": (
                    f"Tool results:\n{results_block}\n\n"
                    f"Answer concisely: {user_prompt}"
                ),
            }],
            tools=[],  # No tools — must produce text
        )
        content = final_response["message"].get("content", "").strip()
        if verbose:
            print(f"\n[assistant] {content}\n")
        return content

    return "[Error] Agent hit max iterations without a final response."


def chat_loop():
    """Interactive multi-turn chat loop."""
    print(f"\n Agent ready. Model: {MODEL}")
    list_tools()
    print("Type your message and press Enter. Ctrl+C to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            run_agent(user_input)
        except KeyboardInterrupt:
            print("\nBye.")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        run_agent(prompt)
    else:
        chat_loop()
