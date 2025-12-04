import arxiv
import time
from typing import List, Dict, Any, Set

def crawl_arxiv_by_keywords(keywords: List[str], max_results_per_keyword: int = 10) -> List[Dict[str, Any]]:
    """
    Crawls ArXiv for papers matching a list of keywords and returns their metadata.

    Args:
        keywords (List[str]): A list of keywords to search for.
        max_results_per_keyword (int): The maximum number of papers to fetch for each keyword.

    Returns:
        List[Dict[str, Any]]: A list of unique papers found.
    """
    print(f"Crawling ArXiv for keywords: {', '.join(keywords)}...")
    
    all_papers = []
    seen_ids: Set[str] = set()

    for keyword in keywords:
        search = arxiv.Search(
            query=keyword,
            max_results=max_results_per_keyword,
            sort_by=arxiv.SortCriterion.Relevance
        )

        for result in search.results():
            arxiv_id = result.entry_id.split('/')[-1]
            if arxiv_id not in seen_ids:
                all_papers.append(result)
                seen_ids.add(arxiv_id)
        
        # ArXiv API guidelines recommend a 3-second delay between requests
        time.sleep(3)

    print(f"Found {len(all_papers)} unique papers from ArXiv.")
    return all_papers