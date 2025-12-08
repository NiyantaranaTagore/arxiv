# pipeline/arxiv_fetcher.py

import arxiv
import os
from typing import List
import logging

def search_arxiv_papers(query: str, max_results: int) -> List[arxiv.Result]:
    """
    Searches arXiv for a given query and returns the result objects containing
    metadata like title and abstract.

    Args:
        query (str): The search query (e.g., a paper title).
        max_results (int): The maximum number of papers to download.

    Returns:
        A list of arxiv.Result objects.
    """
    print(f"\nSearching arXiv for query: '{query}'...")
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = list(search.results())
    print(f"Found {len(results)} relevant papers on arXiv.")
    return results