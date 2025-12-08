# ArXiv Abstract Crawler

This project provides a Python script to crawl [arXiv.org](https://arxiv.org) for research papers that are similar to a given paper. It constructs a targeted search query using the paper's title, abstract, and a list of keywords to find relevant articles.

## Features

*   **Targeted Search**: Builds a powerful query to search for an exact title match or for papers with abstracts containing specific keywords.
*   **Relevance Sorting**: Fetches papers sorted by relevance to the query.
*   **Configurable**: Allows setting a maximum number of results to retrieve.
*   **API Compliance**: Respects arXiv API guidelines by including a delay between requests.

## Project Structure

```
├── arxiv_crawler.py
├── similar_papers.json
└── README.md
```

*   `main.py`: The main entry point for the script.
*   `arxiv_crawler.py`: The main Python script containing the crawling logic.
*   `keyword_extractor.py`: Extracts keywords from the document text.
*   `similarity_analyzer.py`: Analyzes and ranks papers based on similarity.
*   `utils.py`: Contains helper functions for reading documents and saving results.
*   `similar_papers.json`: An example JSON file showing the output of a search for similar papers.
*   `README.md`: This documentation file.

## Installation

1.  Clone this repository to your local machine.
2.  Make sure you have Python 3.6+ installed.
3.  Install the required Python packages. The primary dependency is the `arxiv` library.
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main function `crawl_arxiv` is located in `arxiv_crawler.py`. You can import and use this function in your own scripts.

### Function Signature

```python
def crawl_arxiv(title: str, abstract: str, keywords: List[str], max_results: int = 20) -> List[Dict[str, Any]]:
```

### Parameters

*   `title` (str): The title of the paper to search for.
*   `abstract` (str): The abstract of the paper.
*   `keywords` (List[str]): A list of keywords extracted from the paper.
*   `max_results` (int): The maximum number of papers to fetch. Defaults to `20`.

### Example

Here is an example of how to use the `crawl_arxiv` function:

```python
from utils import read_document, extract_title_and_abstract
from keyword_extractor import extract_keywords_from_text
from arxiv_crawler import crawl_arxiv

if __name__ == "__main__":
    doc_text = read_document("2512.04062v1.pdf")
    title, abstract = extract_title_and_abstract(doc_text)
    keywords = extract_keywords_from_text(doc_text, top_n=5)
    # Crawl for similar papers
    similar_papers = crawl_arxiv(title=paper_title, abstract=paper_abstract, keywords=paper_keywords, max_results=10)

    # Print the titles of the found papers
    for paper in similar_papers:
        print(f"- {paper.title}")
```