# tools/web_search.py
from registry import tool
import requests
from bs4 import BeautifulSoup

@tool(
    name="web_search",
    description=(
        "Searches the web and returns the top results for a query. "
        "Use this when you need current information, news, facts, or "
        "anything you don't already know."
    ),
    parameters={
        "query": {
            "type": "string",
            "description": "The search query, e.g. 'latest Python release'"
        },
        "num_results": {
            "type": "integer",
            "description": "How many results to return. Default 3, max 8."
        }
    }
)
def web_search(query: str, num_results: int = 3) -> str:
    num_results = int(num_results)
    headers = {
        # Pretend to be a browser — DDG blocks default requests user-agent
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.post(
        "https://html.duckduckgo.com/html/",
        data={"q": query},
        headers=headers,
        timeout=10
    )

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.select(".result__body")[:num_results]:
        title_el = result.select_one(".result__title")
        snippet_el = result.select_one(".result__snippet")
        url_el = result.select_one(".result__url")

        title   = title_el.get_text(strip=True) if title_el else "No title"
        snippet = snippet_el.get_text(strip=True) if snippet_el else "No snippet"
        url     = url_el.get_text(strip=True) if url_el else "No URL"

        results.append(f"Title: {title}\nURL: {url}\nSummary: {snippet}")

    if not results:
        return "No results found."

    return "\n\n".join(results)
