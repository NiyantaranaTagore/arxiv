# main.py

from pipeline.data_loader import load_config, load_source_document
from pipeline.arxiv_fetcher import search_arxiv_papers
from utils.text_utils import extract_text_from_pdf, split_into_sentences
from pipeline.similarity_analyzer import SimilarityAnalyzer # Updated import
from pipeline.reporting import generate_report
import glob
import os

def run_pipeline():
    """
    Executes the full semantic similarity pipeline.
    """
    # 1. Load Configuration
    config = load_config('configs/config.yaml')

    # 2. Load and Process Source Document
    source_doc_title, source_doc_abstract = extract_text_from_pdf(config['input_doc_path'])
    source_sentences = split_into_sentences(source_doc_abstract)

    # 3. Build Corpus: Either from arXiv or a local directory
    if config.get('use_arxiv_corpus', False):
        arxiv_results = search_arxiv_papers( # This function is now correctly defined in arxiv_fetcher
            query=source_doc_title,
            max_results=config['max_arxiv_results']
        )
        # Process arXiv results in-memory
        corpus_docs = []
        for result in arxiv_results:
            # Exclude the source paper itself if it's found on arXiv
            if result.get_short_id() not in config['input_doc_path']:
                corpus_docs.append({
                    "title": result.title,
                    "abstract": result.summary,
                    "sentences": split_into_sentences(result.summary),
                    "path": result.pdf_url # Use the URL as a unique identifier
                })
    else:
        print("\nUsing local corpus directory.")
        corpus_dir = config.get('corpus_dir', 'data/corpus/')
        corpus_paths = glob.glob(os.path.join(corpus_dir, "*.pdf"))
        corpus_paths = [p for p in corpus_paths if os.path.abspath(p) != os.path.abspath(config['input_doc_path'])]
        corpus_docs = [load_source_document(p) for p in corpus_paths]

    source_doc_processed = {
        "title": source_doc_title,
        "abstract": source_doc_abstract,
        "sentences": source_sentences,
        "path": config['input_doc_path']
    }

    # 4. Analyze for Similarity
    analyzer = SimilarityAnalyzer(config)
    findings = analyzer.find_similar_sentences(source_doc_processed, corpus_docs)

    # 5. Generate Report
    if findings:
        generate_report(config, source_doc_processed, findings)
    else:
        print("No significant similarities found based on the configured threshold.")

if __name__ == "__main__":
    config = load_config('configs/config.yaml')
    if not os.path.exists(config['input_doc_path']):
        print(f"Error: Input file not found at '{config['input_doc_path']}'.")
        print("Please add a PDF file to that location or update 'configs/config.yaml'.")
    else:
        run_pipeline()
