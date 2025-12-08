# Semantic Similarity Pipeline

This project is a Python-based pipeline designed to analyze a given academic paper or document and identify semantic similarities within a corpus of other documents. It fetches relevant papers from arXiv, compares them sentence by sentence, and generates a clear, color-coded PDF report highlighting the sections with significant semantic overlap.

## Features

- **Semantic Analysis**: Utilizes state-of-the-art sentence-transformer models to understand the meaning behind sentences, not just keywords.
- **Dynamic Corpus Generation**: Automatically searches and downloads relevant papers from arXiv.org based on the source document's title.
- **Local Corpus Support**: Can also run comparisons against a local directory of PDF files.
- **Configurable Similarity Threshold**: Easily adjust the sensitivity of the similarity detection.
- **Detailed PDF Reporting**: Generates a PDF report where similar sentences in the source document are highlighted.
- **Clear Source Referencing**:
  - Each highlight is color-coded and annotated with a number `[#]` that links to a specific source document.
  - A "Sources" section lists all documents that contain similar content, along with their title and the highest similarity score found.
- **Highly Configurable**: All major parameters (file paths, model selection, thresholds, etc.) are managed in a simple `config.yaml` file.

## How It Works

The pipeline follows a high-level, four-step process:

1.  **Load & Parse**: The source document is loaded, and its text is extracted and split into sentences.
2.  **Fetch Corpus**: Relevant documents are either fetched from arXiv or loaded from a local directory.
3.  **Analyze & Compare**: Sentences are converted into numerical vectors (embeddings) and compared for semantic similarity.
4.  **Generate Report**: A PDF report is created, visually highlighting similar sentences and listing the sources.

*(See the **Detailed Workflow** section below for a more in-depth explanation.)*

## Project Structure

```
semantic-similarity-pipeline/
├── assets/
│   └── fonts/              # Stores .ttf font files for PDF reporting.
├── configs/
│   └── config.yaml         # Main configuration file for all parameters.
├── data/
│   ├── input/              # Place your source PDF document here.
│   ├── output/             # Generated PDF reports are saved here.
│   └── corpus/             # Directory for the local corpus of documents.
├── pipeline/
│   ├── corpus.py           # Handles fetching and processing of the document corpus.
│   ├── data_loader.py      # Loads the source document and configuration.
│   ├── reporting.py        # Generates the final PDF report.
│   └── similarity.py       # Core logic for embedding and similarity calculation.
├── utils/
│   └── text_utils.py       # Utility functions for text extraction and processing.
├── main.py                 # The main entry point to run the pipeline.
├── requirements.txt        # A list of all Python dependencies.
└── README.md               # Project documentation.
```

The pipeline follows a four-step process:

1.  **Load & Parse**: The source document (`input_doc_path`) is loaded, and its text is extracted and split into sentences.
2.  **Fetch Corpus**: Based on the configuration (`use_arxiv_corpus`), the pipeline either:
    - Queries the arXiv API for relevant papers using the source document's title.
    - Scans the local `corpus_dir` for documents.
3.  **Analyze & Compare**:
    - All sentences from the source and corpus documents are converted into numerical vectors (embeddings) using a sentence-transformer model.
    - The pipeline then calculates the cosine similarity between sentences from the source document and sentences from the corpus.
4.  **Generate Report**: If any sentence pairs exceed the `similarity_threshold`, a PDF report is generated in the `output_dir`. The report visually highlights the similar sentences and lists the corresponding sources.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd semantic-similarity-pipeline
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    The `requirements.txt` file lists all necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Font Files**:
    Ensure the specified TrueType font files (`Times New Roman.ttf` and `Times New Roman Bold.ttf`) are present in the `assets/fonts/` directory. The reporting module relies on these for PDF generation.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd semantic-similarity-pipeline
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    A `requirements.txt` file should be created to list all dependencies.
    ```bash
    pip install -r requirements.txt
    ```
    Your `requirements.txt` should look something like this:
    ```
    fpdf2
    sentence-transformers
    torch
    PyYAML
    arxiv
    PyMuPDF
    ```

## How to Run

1.  **Configure the Analysis**:
    Open `configs/config.yaml` and modify the parameters to suit your needs.

    ```yaml
    # Path to the input PDF document you want to analyze.
    input_doc_path: "data/input/my_paper.pdf"

    # Directory where the output PDF report will be saved.
    output_dir: "data/output/"

    # --- Corpus Source Configuration ---
    # Set to true to fetch the corpus dynamically from arXiv.org.
    use_arxiv_corpus: true

    # The maximum number of relevant papers to fetch from arXiv.
    # Set to -1 to fetch all available papers.
    max_arxiv_results: 100

    # The threshold for considering two sentences as similar (0.0 to 1.0).
    similarity_threshold: 0.75
    ```

2.  **Place Your Input File**:
    Make sure the document you want to analyze is placed in the path specified by `input_doc_path` (e.g., `data/input/my_paper.pdf`).

3.  **Execute the Pipeline**:
    Run the main script from the root directory of the project.
    ```bash
    python main.py
    ```

4.  **View the Report**:
    Once the analysis is complete, a message will be printed to the console with the location of the report. You can find the generated `similarity_report.pdf` in the directory specified by `output_dir`.

## Detailed Workflow

The pipeline's execution flow is orchestrated by `main.py` and is broken down as follows:

1.  **Initialization**: The `main.py` script starts by loading the configuration from `configs/config.yaml` using the `load_config` function in `pipeline/data_loader.py`.

2.  **Source Document Loading**: The primary document specified in `input_doc_path` is loaded. The `extract_text_from_pdf` and `split_into_sentences` utilities are used to parse its title and content into a structured format.

3.  **Corpus Acquisition (`pipeline/corpus.py`)**:
    - If `use_arxiv_corpus` is `true`, the pipeline constructs a formatted query from the source document's title and uses the `arxiv` library to find and download relevant papers.
    - If `false`, the pipeline scans the `corpus_dir` and processes all PDF files found locally.

4.  **Semantic Analysis (`pipeline/similarity.py`)**:
    - The sentence-transformer model specified by `embedding_model` is loaded.
    - All sentences from both the source document and the corpus documents are encoded into high-dimensional vectors (embeddings).
    - The cosine similarity is calculated between each source sentence embedding and all corpus sentence embeddings.

5.  **Filtering and Reporting (`pipeline/reporting.py`)**:
    - Any sentence pair with a similarity score exceeding the `similarity_threshold` is collected as a "finding."
    - If one or more findings exist, the `generate_report` function is triggered. It creates a new PDF, dynamically assigns colors to each source, highlights the relevant sentences with source numbers, and compiles a final list of sources with their maximum similarity scores.