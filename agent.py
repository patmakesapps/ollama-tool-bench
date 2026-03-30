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

SYSTEM_PROMPT = """You are Lumi, a helpful assistant with access to tools.

IMPORTANT RULES — follow these exactly:
- If the user asks for the current time or date, you MUST call get_time.
- If the user asks to search the web or needs current news/info, you MUST call web_search.
- If the user gives a specific URL to fetch, you MUST call http_get. Never use run_command or web_search for this.
- If the user asks a math question or calculation, you MUST call calculate.
- If the user asks to read/view/show a file, you MUST call read_file.
- If the user asks to list files or explore a directory, you MUST call list_files.
- If the user asks to search inside files or a codebase, you MUST call search_content.
- If the user asks to create or write a file, you MUST call write_file.
- If the user asks to edit/change/modify a file, you MUST call edit_file.
- If the user asks to delete/remove a file, you MUST call delete_file.
- If the user asks to run a terminal/shell command, you MUST call run_command.
- If the user asks what is on their clipboard, you MUST call get_clipboard.
- If the user asks to copy text to their clipboard, you MUST call set_clipboard.
- If the user says remember/save/note/don't forget something, you MUST call save_note.
- If the user asks what you remember or for your notes, you MUST call get_note.
- For greetings, casual chat, opinions, or general knowledge, call no_action with your response.

RESPONSE RULES:
- After web_search, summarize findings and list each source with its URL.
- For all other tools, answer directly using the result. Do not invent fake URLs or sources.
- Never guess the time, date, or math results — always use the tool.
"""


def run_agent(user_prompt: str, verbose: bool = True) -> str:
    """
    Agentic loop with a no_action escape hatch.
    Tools are always available, including a 'no_action' tool the model picks
    when it can answer on its own — preventing it from misusing real tools.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    max_iterations = 5

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
            content = msg.get("content", "").strip()
            if verbose:
                print(f"\n[assistant] {content}\n")
            return content

        # Check for no_action — model is answering directly
        first_call = tool_calls[0]
        if first_call["function"]["name"] == "no_action":
            content = first_call["function"].get("arguments", {}).get("message", "")
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
                    f"The tools returned:\n{results_block}\n\n"
                    f"Reply to the user using ONLY the information above. "
                    f"Do not say you have no information. Do not make anything up. "
                    f"User asked: {user_prompt}"
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
    tool_count = len(get_schemas())
    print(f"\n Agent ready. Model: {MODEL} | {tool_count} tools loaded")
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
