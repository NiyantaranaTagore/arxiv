# In the file responsible for fetching data from arXiv (e.g., pipeline/corpus.py)

import arxiv
import re
import math
from typing import Dict, Any

# ... other imports

def fetch_arxiv_corpus(config: Dict[str, Any], source_doc: Dict[str, Any]) -> None:
    """
    Fetches relevant papers from arXiv based on the source document's title.
    """
    # --- START of Suggested Changes ---

    # 1. Clean the title to create a robust search query.
    # Remove newlines, extra whitespace, and prepare for arXiv query format.
    cleaned_title = re.sub(r'\s+', ' ', source_doc['title']).strip()
    
    # 2. Format the query for the arXiv API.
    # Use ti:"..." to search specifically in the title field. This is much more reliable.
    # Escape quotes within the title to prevent breaking the query.
    escaped_title = cleaned_title.replace('"', '\\"')
    search_query = f'ti:"{escaped_title}"'

    print(f"Searching arXiv with formatted query: {search_query}...")

    # 3. Handle the max_results=-1 case to fetch all results.
    max_results = float('inf') if config['max_arxiv_results'] == -1 else config['max_arxiv_results']

    # --- END of Suggested Changes ---

    # Execute the search with the new, robust query
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    client = arxiv.Client()
    results = list(client.results(search)) # Use list() to get all results for 'inf'

    print(f"Found {len(results)} relevant paper(s) on arXiv.")

    # ... rest of the function to process and save the results ...
