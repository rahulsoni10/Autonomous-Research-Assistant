from newspaper import Article
from serpapi import GoogleSearch
import os
import pdfplumber
from pathlib import Path



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
            "hl": "en",
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
        if url.endswith(".pdf"):
            try:
                all_text += download_and_extract_pdf(url) + "\n"
            except:
                pass
        else:
            try:
                all_text += fetch_article_text(url) + "\n"
            except:
                pass
    return all_text


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a local PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def download_and_extract_pdf(pdf_url: str, save_path="data/raw/temp.pdf") -> str:
    """Download PDF from a URL and extract text."""
    import requests
    r = requests.get(pdf_url)
    Path(save_path).write_bytes(r.content)
    return extract_text_from_pdf(save_path)

# from dotenv import load_dotenv  

# load_dotenv()  #  to load variables from .env

# if __name__ == "__main__":
#     topic = input("Enter a topic: ")
#     data = collect_data(topic)
#     print(data)


