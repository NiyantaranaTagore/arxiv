import arxiv
import time
from typing import List, Dict, Any, Set

def crawl_arxiv(title: str, abstract: str, keywords: List[str], max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Crawls ArXiv for papers using a combined query of title, abstract, and keywords.

    Args:
        title (str): The title of the paper to search for.
        abstract (str): The abstract of the paper.
        keywords (List[str]): A list of keywords from the paper.
        max_results (int): The maximum number of papers to fetch.

    Returns:
        List[Dict[str, Any]]: A list of unique papers found.
    """
    # Build a powerful query. Search the title for an exact match, and search the abstract
    # for the extracted keywords to find related papers.
    # The `ti:` prefix searches the title, `abs:` searches the abstract.
    keyword_query = " OR ".join([f'"{k}"' for k in keywords])
    query = f'(ti:"{title}") OR (abs:({keyword_query}))'
    
    print(f"Crawling ArXiv with query: {query}...")
    
    all_papers = []

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    for result in search.results():
        all_papers.append(result)
    
    # ArXiv API guidelines recommend a 3-second delay between requests
    time.sleep(3)

    print(f"Found {len(all_papers)} unique papers from ArXiv.")
    return all_papers