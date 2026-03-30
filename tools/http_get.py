# tools/http_get.py
from registry import tool
import requests


@tool(
    name="http_get",
    description=(
        "Fetches the response body from a URL via HTTP GET. "
        "Use this to call APIs, fetch raw JSON, or retrieve web content directly by URL. "
        "Prefer web_search when you don't have a specific URL."
    ),
    parameters={
        "url": {
            "type": "string",
            "description": "The full URL to fetch, e.g. 'https://api.github.com/repos/ollama/ollama'.",
        }
    },
)
def http_get(url: str) -> str:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        content_type = response.headers.get("Content-Type", "")
        text = response.text.strip()

        if len(text) > 4000:
            text = text[:4000] + "\n... [truncated]"

        return f"Status: {response.status_code}\nContent-Type: {content_type}\n\n{text}"
    except requests.exceptions.Timeout:
        return "[Error] Request timed out."
    except requests.exceptions.ConnectionError:
        return "[Error] Could not connect to the URL."
    except Exception as e:
        return f"[Error] HTTP GET failed: {e}"
