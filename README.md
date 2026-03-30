# ollama-tool-bench

A lightweight agentic framework for testing how well local Ollama models handle tool calling. Run it against any model before you build your project — find out fast which ones actually follow tool schemas, which ones hallucinate, and which ones fall apart.

---

## Why this exists

Not all Ollama models are created equal when it comes to tool use. Some call tools reliably, some ignore them, some hallucinate results. This repo gives you a ready-made agent with a real tool suite so you can benchmark any model in minutes instead of finding out mid-project.

---

## Quickstart

**Requirements:** Python 3.10+, [Ollama](https://ollama.com) running locally

```bash
git clone https://github.com/your-username/ollama-tool-bench
cd ollama-tool-bench
pip install -r requirements.txt
ollama pull llama3.2:3b   # or any model you want to test
python agent.py
```

To test a single prompt without entering the chat loop:

```bash
python agent.py "what time is it?"
python agent.py "what is the square root of 1764?"
```

---

## Switching models

Change the `MODEL` variable at the top of `agent.py`:

```python
MODEL = "llama3.2:3b"       # default
MODEL = "mistral"
MODEL = "qwen2.5:7b"
MODEL = "llama3.1:8b"
```

Then run the same test prompts across models to compare behavior.

---

## Tools included

| Tool | What it tests |
|---|---|
| `get_time(format)` | Basic tool dispatch with an enum parameter |
| `calculate(expression)` | Math — models should never guess this |
| `web_search(query, num_results)` | Live search via DuckDuckGo |
| `http_get(url)` | Direct URL fetch |
| `read_file(path)` | File system read |
| `list_files(directory, pattern)` | Glob-based file discovery |
| `search_content(directory, query, file_pattern)` | Regex search across files |
| `write_file(path, content)` | File creation/overwrite *(confirmation required)* |
| `edit_file(path, old_text, new_text)` | In-place find & replace *(confirmation required)* |
| `delete_file(path)` | File deletion *(confirmation required)* |
| `run_command(command)` | Shell execution *(confirmation required)* |
| `get_clipboard()` | Read system clipboard |
| `set_clipboard(text)` | Write to system clipboard |
| `save_note(key, value)` | Persist a note across sessions |
| `get_note(key)` | Retrieve a saved note |

---

## Test prompts

Use these to quickly evaluate a model. Paste results in an issue or PR to share findings with the community.

```
what time is it?
what is today's date?
what is 847 divided by 13?
what is the square root of 1764?
what is pi times 5 squared?
search the web for the latest ollama release
fetch https://httpbin.org/json and tell me what you see
read the file ./agent.py
list all python files in ./tools
search ./ for the word "import"
create a file at ./test.txt with the content "hello from Lumi"
edit ./test.txt and replace "hello from Lumi" with "hello world"
copy the text "tool bench" to my clipboard
remember that my favorite language is Python
what's my favorite language?
run the command "echo hello world"
delete the file ./test.txt
```

---

## Adding a new tool

Drop a `.py` file into the `tools/` directory. It gets auto-registered on the next run — no changes to `agent.py` or `registry.py` needed.

```python
# tools/my_tool.py
from registry import tool

@tool(
    name="my_tool",
    description="Describe clearly when the model should call this.",
    parameters={
        "input": {
            "type": "string",
            "description": "What this parameter does.",
        }
    },
)
def my_tool(input: str) -> str:
    return f"Result: {input}"
```

---

## How it works

- Uses **Ollama's native tool-calling API** (`tools=` parameter in `ollama.chat`) — no text parsing or prompt hacks
- Tools are registered via a `@tool` decorator and passed as JSON schemas directly to the model
- After tool results are collected, a second call with `tools=[]` forces the model to produce a text answer rather than looping

---

## Dependencies

```
ollama
requests
beautifulsoup4
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Contributing

Tested a model and want to share results? Open an issue or PR with:
- Model name and version
- Which tools passed / failed
- Any interesting behavior worth noting

Community results help everyone pick the right model for their use case.

---

## License

MIT
