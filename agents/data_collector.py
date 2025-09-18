from newspaper import Article
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv  # <-- ADD THIS LINE

load_dotenv()  # <-- AND ADD THIS LINE to load variables from .env

# Function to fetch and parse article text
def fetch_article_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return ""

# Function to search Google using SerpAPI
def search_google(query: str, max_results=5):
    try:
        # The script will now correctly find the API key
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            print("Error: SERPAPI_API_KEY not found. Make sure it's in your .env file.")
            return []
            
        params = {
            "q": query,
            "api_key": api_key,
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Good practice to check for an error message in the response
        if "error" in results:
            print(f"SerpAPI Error: {results['error']}")
            return []

        urls = [result["link"] for result in results.get("organic_results", [])]
        return urls[:max_results]
    except Exception as e:
        print(f"Error searching Google for '{query}': {e}")
        return []

# Function to collect data from multiple articles
def collect_data(topic: str):
    urls = search_google(topic)
    if not urls:
        print("No URLs found.")
        return ""
    
    all_text = ""
    for url in urls:
        text = fetch_article_text(url)
        if text:
            all_text += text + "\n"
    return all_text


