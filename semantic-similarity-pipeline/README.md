# Semantic Similarity Pipeline

This project provides a complete pipeline to analyze a source document and find semantically similar sentences within a corpus of other documents. The corpus can be a local collection of PDFs or can be dynamically fetched from [arXiv.org](https://arxiv.org) based on the source document's title.

The final output is a detailed PDF report that highlights the similar sentences found in the source document's abstract and provides citations for the source papers.

## Features

- **PDF Text Extraction**: Extracts title and abstract from PDF documents.
- **Dual Corpus Mode**:
  - **Local**: Compares against a local directory of PDF files.
  - **Dynamic (arXiv)**: Automatically searches and "crawls" relevant papers from arXiv.org based on the source document's title, using their abstracts for comparison without downloading the full PDFs.
- **Semantic Analysis**: Uses state-of-the-art `sentence-transformers` models to generate vector embeddings and calculate semantic similarity.
- **Configurable Pipeline**: All major parameters, including the embedding model, similarity threshold, and corpus mode, are configurable via a single `config.yaml` file.
- **PDF Report Generation**: Produces a clean, easy-to-read PDF report showing the source abstract with highlighted sentences, similarity scores, and a list of sources.

## How It Works

The pipeline is orchestrated by `main.py` and can be visualized with the following workflow.

### Detailed Workflow

```
[ Start ]
    |
    v
[ configs/config.yaml ] -> Read by main.py
    |
    +----------------------------------------------------------------+
    |                                                                |
    v                                                                v
[ data/input/source.pdf ]                                     [ Corpus Source Selection ]
    |                                                                | (Based on 'use_arxiv_corpus')
    | (load_source_document)                                         |
    v                                                                +------------+
[ Source Doc Object ]                                                |            |
  - title                                                            | (true)     | (false)
  - abstract                                                         v            v
  - sentences[]                                          [ arXiv API Query ]  [ data/corpus/*.pdf ]
    |                                                       (using source title)      |
    |                                                                |            | (load_source_document)
    |                                                                v            v
    |                                                      [ In-Memory Corpus Objects ]
    |                                                                |
    +--------------------------------->[ SimilarityAnalyzer ]<-------+
                                            |
                                            | (find_similar_sentences)
                                            v
                                      [ Findings[] ]
                               (List of similar sentence pairs)
                                            |
                                            v
                                      [ reporting.py ] -> Generates -> [ data/output/report.pdf ]
                                            |
                                            v
                                        [ End ]
```

The pipeline follows these main steps:

1.  **Load Configuration**: Reads settings from `configs/config.yaml`.
2.  **Load Source Document**: Extracts the title and abstract from the input PDF specified in the config.
3.  **Build Corpus**:
    - If `use_arxiv_corpus` is `true`, it queries the arXiv API using the source document's title and fetches the abstracts of the most relevant papers.
    - Otherwise, it loads all PDF documents from the local `corpus_dir`.
4.  **Analyze Similarity**:
    - It generates sentence embeddings for the source abstract and all corpus abstracts using the specified transformer model.
    - It calculates the cosine similarity between every sentence in the source document and every sentence in the corpus.
5.  **Generate Report**: If any sentences are found with a similarity score above the configured threshold, it generates a PDF report detailing the findings.

## Project Structure

```
semantic-similarity-pipeline/
├── assets/
│   └── fonts/              # Fonts for PDF report generation
├── configs/
│   └── config.yaml         # Main configuration file for the pipeline
├── data/
│   ├── input/              # Place your source PDF document here
│   ├── output/             # Generated PDF reports are saved here
│   └── corpus/             # (Optional) Local corpus of PDFs
├── pipeline/
│   ├── __init__.py
│   ├── arxiv_fetcher.py    # Handles searching and fetching data from arXiv
│   ├── data_loader.py      # Loads config and processes documents
│   ├── reporting.py        # Generates the final PDF report
│   └── similarity_analyzer.py # Core logic for semantic analysis
├── utils/
│   ├── __init__.py
│   └── text_utils.py       # Helper functions for text extraction and processing
├── main.py                 # Main entry point to run the pipeline
├── README.md               # This file
└── requirements.txt        # Project dependencies
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd semantic-similarity-pipeline
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Place your source document** inside the `data/input/` directory.

2.  **Configure the pipeline** by editing `configs/config.yaml`. Key options include:
    - `input_doc_path`: Path to your source document.
    - `use_arxiv_corpus`: Set to `true` to use arXiv or `false` to use the local `data/corpus/` directory.
    - `max_arxiv_results`: The number of papers to fetch from arXiv.
    - `similarity_threshold`: The minimum similarity score (0.0 to 1.0) to consider a match.

3.  **Run the pipeline:**
    ```bash
    python main.py
    ```

4.  **Check the output**: The generated report will be saved in the `data/output/` directory.

## Configuration Details

The `configs/config.yaml` file allows you to control the pipeline's behavior without changing the code.

| Parameter              | Description                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------- |
| `input_doc_path`       | Path to the source PDF you want to analyze.                                                             |
| `output_dir`           | Directory where the final PDF report will be saved.                                                     |
| `corpus_dir`           | Directory containing local PDFs to use as the corpus (if `use_arxiv_corpus` is `false`).                |
| `embedding_model`      | The `sentence-transformers` model to use. `all-MiniLM-L6-v2` is a good default.                         |
| `similarity_threshold` | The cutoff for similarity scores. A higher value means stricter matching.                               |
| `use_arxiv_corpus`     | If `true`, the pipeline will query arXiv. If `false`, it will use `corpus_dir`.                         |
| `max_arxiv_results`    | The maximum number of relevant papers to fetch from arXiv for comparison.                               |
| `font_size_title`      | Font size for the main title in the PDF report.                                                         |
| `font_size_abstract`   | Font size for the abstract text in the PDF report.                                                      |
| `font_size_sources`    | Font size for the sources section in the PDF report.                                                    |

---

This `README.md` provides a comprehensive guide for anyone looking to use or understand your project.