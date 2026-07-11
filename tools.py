from langchain.tools import tool
import os
from dotenv import load_dotenv
from tavily import TavilyClient  # FIX: package/module is "tavily", not "travily"
from rich import print
from bs4 import BeautifulSoup
import requests
load_dotenv()

# FIX: removed stray "TRAVILY_API_KEY" line (was just a bare name, did nothing / would error)
# FIX: env var name corrected to "TAVILY_API_KEY" (was "TRAVILY_API_KEY")
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """SEARCH WEB ON RECENT AND RELIABLE INFORMATION ON TOPIC"""
    # FIX: tavily.search() returns a dict, not a list directly -> grab ["results"]
    response = tavily.search(query=query, max_results=5)
    results = response["results"]

    out = []

    for r in results:
        out.append(
            # FIX: nested double quotes inside an f-string using double quotes was a syntax error
            # -> switched inner quotes to single quotes: r['title'], r['url'], r['content']
            # FIX: r[cotent] -> typo + missing quotes (cotent was undefined) -> r['content']
            f"Title: {r['title']}\n Url: {r['url']}\n Snippet: {r['content'][:300]}\n"
        )

    # FIX: return was indented inside the for-loop, so it exited after the first result
    # -> moved outside the loop to join all results
    return "\n-------\n".join(out)






@tool
def scrape_url(url: str) -> str:
    """SCRAPE AND RETURN CLEAN CONTENT FROM THE GIVEN URL"""  # FIX: typo "CONTNET" -> "CONTENT"
    try:
        # FIX: "request.get" -> "requests.get" (module name typo)
        # FIX: "header" -> "headers" (wrong kwarg name for requests)
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
 
        # FIX: variable was assigned as "Soup" (capital S) but used later as "soup" -> made consistent (lowercase)
        # FIX: "resp" was correct here, but earlier typo'd as "reps" when assigning the request -> fixed above
        # FIX: parser name "tml-parser" is invalid -> correct parser is "html.parser"
        soup = BeautifulSoup(resp.text, "html.parser")
 
        # FIX: "taf" (loop variable) vs "tag" (used in body) mismatch -> renamed consistently to "tag"
        # FIX: "scripts" -> "script" (correct HTML tag name has no "s")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
 
        # FIX: "strip =True" spacing was fine but ensured no other typos remain here
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception:
        # FIX: bare "except:" replaced with "except Exception:" (avoids catching system-exit/keyboard interrupt)
        return f"Could not scrape url: {url}"
