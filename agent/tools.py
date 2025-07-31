import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def search_tool(query):
    """Searches the web using DuckDuckGo and returns the results."""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()




@tool
def get_latest_politifact_claims(limit=5):
    """Fetches the latest fact-check claims related to politics from Politifact."""
    url = "https://www.politifact.com/factchecks/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.select('.m-statement__quote')[:limit]
    results = []

    for item in items:
        statement = item.get_text(strip=True)
        ruling_tag = item.find_parent().find_next_sibling('div', class_='m-statement__meter')
        rating = ruling_tag.img['alt'] if ruling_tag and ruling_tag.img else "Unknown"
        results.append((statement, rating))

    return results

# Example usage
# for statement, rating in get_latest_politifact_claims():
#     print(f"🔹 Claim: {statement}\n✅ Rating: {rating}\n")


@tool
def get_latest_snopes_claims(limit=5):
    """Fetches the latest fact-check claims from Snopes."""
    url = "https://www.snopes.com/fact-check/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.select("article")[:limit]
    results = []

    for article in articles:
        title_tag = article.select_one("h2.title")
        title = title_tag.text.strip() if title_tag else "No title"
        verdict = article.select_one(".claim-rating")
        verdict_text = verdict.text.strip() if verdict else "Unknown"
        results.append((title, verdict_text))

    return results

# Example usage
# for claim, verdict in get_latest_snopes_claims():
#     print(f"🔹 Claim: {claim}\n✅ Verdict: {verdict}\n")


# Modify get_retriever to accept collection name
@tool
def get_retriever(collection_name):
    """
    Retrieves a retriever for a specified vector store collection.
    """
    from langchain.vectorstores import Chroma
    from agent.yt_components.embedder import embedding_model1
    
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model1,
        collection_name=collection_name  # Use dynamic collection name
    )
    return db.as_retriever()