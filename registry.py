# registry.py
# The heart of the tool system. This module does three things:
#   1. Stores all registered tools in a dict (TOOLS)
#   2. Provides a @tool decorator to register functions
#   3. Exposes helpers to get schemas and dispatch calls

TOOLS = {}
# Structure: { "tool_name": { "fn": <callable>, "schema": <dict> } }


def tool(name: str, description: str, parameters: dict):
    """
    Decorator factory that registers a Python function as a callable tool.

    Args:
        name        : The name the model will use to call this tool.
        description : Plain English description — the MODEL reads this to
                      decide WHEN to call the tool. Write it clearly.
        parameters  : Dict of parameter_name -> JSON Schema property dict.
                      Example:
                        {
                            "expression": {
                                "type": "string",
                                "description": "A math expression like '2 + 2'"
                            }
                        }

    Usage:
        @tool(
            name="my_tool",
            description="Does something useful",
            parameters={"input": {"type": "string", "description": "..."}}
        )
        def my_tool(input: str):
            return f"You said: {input}"
    """
    def decorator(fn):
        TOOLS[name] = {
            "fn": fn,
            # This is the exact schema format Ollama expects
            "schema": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": parameters,
                        # All parameters are required by default.
                        # You can customize this per tool if needed.
                        "required": list(parameters.keys()),
                    },
                },
            },
        }
        return fn  # Return the original function unchanged so it's still callable directly
    return decorator


def get_schemas() -> list:
    """
    Returns a list of all registered tool schemas.
    This is what you pass to ollama.chat(tools=...).
    """
    return [entry["schema"] for entry in TOOLS.values()]


def call_tool(name: str, args: dict) -> str:
    """
    Looks up a tool by name and calls it with the provided arguments.

    This is the dispatcher — when the model says "call calculate with
    expression='2+2'", your agent calls this function.

    Args:
        name : Tool name (must match a registered @tool name)
        args : Dict of arguments from the model's tool_call response

    Returns:
        String result to feed back to the model as a tool message.
    """
    if name not in TOOLS:
        return f"[Error] Unknown tool: '{name}'. Available: {list(TOOLS.keys())}"

    try:
        result = TOOLS[name]["fn"](**args)
        return str(result)
    except Exception as e:
        return f"[Error] Tool '{name}' raised an exception: {e}"


def list_tools() -> None:
    """Prints a summary of all registered tools. Useful for debugging."""
    if not TOOLS:
        print("No tools registered.")
        return
    print(f"\n{len(TOOLS)} tool(s) registered:")
    for name, entry in TOOLS.items():
        desc = entry["schema"]["function"]["description"]
        params = list(entry["schema"]["function"]["parameters"]["properties"].keys())
        print(f"  • {name}({', '.join(params)}) — {desc}")
    print()