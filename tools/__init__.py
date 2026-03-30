# tools/__init__.py
# Auto-imports every .py file in this folder.
#
# This means you can drop a new tool file into tools/ and it gets
# registered automatically — no need to touch agent.py or registry.py.
#
# How it works:
#   1. Scans the tools/ directory for .py files (excluding __init__ itself)
#   2. Imports each one as a module
#   3. Since each file calls @tool(...) at import time, the tool gets
#      registered in registry.TOOLS automatically

import importlib
import os
from pathlib import Path

# Get the directory this file lives in
_tools_dir = Path(__file__).parent

for _path in _tools_dir.glob("*.py"):
    # Skip __init__.py itself
    if _path.stem == "__init__":
        continue

    # Import the module — e.g. "tools.calculate"
    _module_name = f"tools.{_path.stem}"
    importlib.import_module(_module_name)