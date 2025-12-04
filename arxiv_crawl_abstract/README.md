# ArXiv Crawler and Similarity Analyzer

This project is a command-line tool that automates the process of finding relevant academic literature on ArXiv based on the content of a source document, such as a research proposal or an article. It uses a hybrid approach, combining title, abstract, and keyword analysis to perform a comprehensive search and deliver a complete, ranked list of similar papers.

## Features

- **Document Processing**: Reads text directly from both `.pdf` and `.txt` files.
- **Hybrid Content Analysis**: Automatically extracts the document's title and abstract using heuristics, and identifies the most relevant keywords using `KeyBERT`.
- **Advanced ArXiv Crawling**: Builds a powerful query using both the extracted title and keywords to ensure a broad yet relevant search on ArXiv.
- **Exhaustive Similarity Ranking**: Fetches a large set of papers and ranks all of them by semantic similarity to the original document. No relevant paper is left behind.
- **Structured Output**: Saves a complete, sorted list of all similar papers found, along with their metadata and similarity score, into a clean `json` file.

## Project Structure

```
arxiv_crawl_abstract/
├── main.py                # Main CLI entry point for the user
├── keyword_extractor.py   # Extracts keywords from the input document
├── arxiv_crawler.py       # Fetches papers from ArXiv using a hybrid query
├── similarity_analyzer.py # Ranks all fetched papers by similarity
├── utils.py               # Helper functions for file I/O and text extraction
├── requirements.txt       # Project dependencies
└── similar_papers.json    # Example output file
```

## Setup and Installation

1.  **Clone the repository** (or create the files as described in the project).

2.  **Create a Conda Environment (Recommended)**:
    It's best practice to create an isolated environment to manage dependencies.
    ```bash
    conda create --name arxiv_crawler python=3.9 -y
    conda activate arxiv_crawler
    ```

3.  **Install Dependencies**:
    Install all the required packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The tool is run from the command line. You need to provide the path to your source document.

### Command

```bash
python main.py [path_to_your_document] [options]
```

### Example

Let's say you have a proposal named `my_proposal.pdf`. To perform a comprehensive search, you would run:

```bash
python main.py my_proposal.pdf --num_keywords 5 --max_papers 200
```

This command will:
1.  Read and process `my_proposal.pdf`.
2.  Extract its title and abstract.
3.  Extract the top 5 keywords from its content.
4.  Crawl ArXiv for up to 200 papers using a combined query of the title and keywords.
5.  Analyze all crawled papers for similarity against the original document.
6.  Save the complete, ranked list of results to `similar_papers.json`.

### Example Output (`similar_papers.json`)

```json
[
    {
        "arxiv_id": "2502.02587v1",
        "title": "Spatio-temporal transformer to support automatic sign language translation",
        "abstract": "Sign Language Translation (SLT) systems support hearing-impaired people communication...",
        "authors": [
            "Christian Ruiz",
            "Fabio Martinez"
        ],
        "submitted_date": "2025-02-04T18:59:19+00:00",
        "pdf_url": "https://arxiv.org/pdf/2502.02587v1",
        "similarity_score": 0.9597
    },
    ...
]
```

## How It Works

1.  **`utils.py`**: The `read_document` function extracts raw text. The `extract_title_and_abstract` function then parses this text to find the document's title and abstract.
2.  **`keyword_extractor.py`**: The full document text is passed to `KeyBERT` to identify the most representative keywords.
3.  **`arxiv_crawler.py`**: A hybrid query is constructed (e.g., `(ti:"Document Title") OR (abs:("keyword1" OR "keyword2"))`). This query is used to fetch a comprehensive list of papers from ArXiv.
4.  **`similarity_analyzer.py`**:
    -   The full text from the original document is converted into a numerical vector (embedding).
    -   The title and abstract of each crawled paper are also converted into embeddings.
    -   `cosine_similarity` is used to calculate the similarity score between the original document and every crawled paper. The full, sorted list is returned.
5.  **`main.py`**: This script orchestrates the entire workflow, parsing command-line arguments and calling the other modules in sequence.

## Future Enhancements

- **More Robust Extraction**: Improve the title and abstract extraction in `utils.py` to handle a wider variety of PDF layouts.
- **Advanced Similarity Scoring**: Implement a weighted scoring system that gives more importance to title similarity or other metadata.
- **Web Interface**: Build a simple web UI using Streamlit or Flask to make the tool more accessible.