# ArXiv Crawler and Similarity Analyzer

This project is a command-line tool that automates the process of finding relevant academic literature on ArXiv based on the content of a source document, such as a research proposal or an article. It extracts keywords, crawls ArXiv for related papers, and then ranks them by semantic similarity to the original document.

## Features

- **Document Processing**: Reads text directly from both `.pdf` and `.txt` files.
- **Automatic Keyword Extraction**: Uses `KeyBERT` to identify the most relevant keywords and keyphrases from the source document.
- **Targeted ArXiv Crawling**: Fetches papers from ArXiv based on the extracted keywords, filtering by relevance.
- **Semantic Similarity Ranking**: Employs sentence embeddings (`sentence-transformers`) and cosine similarity to score and rank the crawled papers against the original document's text.
- **Structured Output**: Saves the top N most similar papers, along with their metadata (title, abstract, authors, etc.) and similarity score, into a clean `json` file.

## Project Structure

```
arxiv_crawler/
├── main.py                # Main CLI entry point for the user
├── keyword_extractor.py   # Extracts keywords from the input document
├── arxiv_crawler.py       # Fetches papers from ArXiv using keywords
├── similarity_analyzer.py # Ranks fetched papers by similarity
├── utils.py               # Helper functions for file I/O
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

Let's say you have a proposal named `my_proposal.pdf` in the project directory. To find the 5 most similar papers on ArXiv, you would run:

```bash
python main.py my_proposal.pdf --num_keywords 5 --max_papers 10 --top_n_similar 5
```

This command will:
1.  Read and process `my_proposal.pdf`.
2.  Extract the top 5 keywords.
3.  Crawl ArXiv for up to 10 papers for each keyword.
4.  Analyze the crawled papers and identify the 5 most similar ones.
5.  Save the results to `similar_papers.json`.

### Example Output (`similar_papers.json`)

```json
[
    {
        "arxiv_id": "2307.05440v1",
        "title": "ISLTranslate: Dataset for Translating Indian Sign Language",
        "abstract": "Sign languages are the primary means of communication for many hard-of-hearing people...",
        "authors": [
            "Abhinav Joshi",
            "Susmit Agrawal",
            "Ashutosh Modi"
        ],
        "submitted_date": "2023-07-11T17:06:52+00:00",
        "pdf_url": "https://arxiv.org/pdf/2307.05440v1",
        "similarity_score": 0.6995
    },
    ...
]
```

## How It Works

1.  **`utils.py`**: The `read_document` function uses `pypdf` to extract raw text from PDF files or reads it directly from `.txt` files.
2.  **`keyword_extractor.py`**: The extracted text is passed to `KeyBERT`, which uses sentence embeddings to find phrases that are most representative of the entire document.
3.  **`arxiv_crawler.py`**: The approved keywords are used to query the ArXiv API. The script fetches a list of relevant papers, ensuring no duplicates are collected.
4.  **`similarity_analyzer.py`**:
    -   The text from the original document is converted into a numerical vector (embedding).
    -   The title and abstract of each crawled paper are also converted into embeddings.
    -   `cosine_similarity` is used to calculate the similarity score between the original document's embedding and each of the crawled paper's embeddings.
5.  **`main.py`**: This script orchestrates the entire workflow, parsing command-line arguments and calling the other modules in sequence.

## Future Enhancements

- **Interactive Keyword Confirmation**: Add a step to allow the user to review, edit, or approve the automatically extracted keywords before crawling.
- **Advanced Similarity Scoring**: Implement a weighted scoring system that gives more importance to title similarity or other metadata.
- **Web Interface**: Build a simple web UI using Streamlit or Flask to make the tool more accessible to non-technical users.