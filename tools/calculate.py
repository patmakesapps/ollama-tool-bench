# tools/calculate.py
from registry import tool
import math
import operator


# Safe namespace — only math functions, no builtins that could be abused
_SAFE_GLOBALS = {
    "__builtins__": {},
    "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
    "pow": pow, "divmod": divmod,
    "math": math,
    "sqrt": math.sqrt, "floor": math.floor, "ceil": math.ceil,
    "log": math.log, "log2": math.log2, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "pi": math.pi, "e": math.e, "inf": math.inf,
}


@tool(
    name="calculate",
    description=(
        "Evaluates a mathematical expression and returns the result. "
        "Use this for any arithmetic, algebra, or math the user asks about. "
        "Supports standard operators, math functions (sqrt, log, sin, etc.), pi, and e."
    ),
    parameters={
        "expression": {
            "type": "string",
            "description": "A math expression to evaluate, e.g. '2 ** 32', 'sqrt(144)', 'pi * 5**2'.",
        }
    },
)
def calculate(expression: str) -> str:
    try:
        result = eval(expression, _SAFE_GLOBALS, {})
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "[Error] Division by zero."
    except Exception as e:
        return f"[Error] Could not evaluate '{expression}': {e}"
