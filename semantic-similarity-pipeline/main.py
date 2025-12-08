# main.py

from pipeline.data_loader import load_config, load_source_document
from pipeline.arxiv_fetcher import search_arxiv_papers
from utils.text_utils import split_into_sentences
from pipeline.similarity_analyzer import SimilarityAnalyzer
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
    source_doc = load_source_document(config['input_doc_path'])

    # 3. Build Corpus: Either from arXiv or a local directory
    if config.get('use_arxiv_corpus', False):
        arxiv_results = search_arxiv_papers(
            query=source_doc['title'],
            max_results=config['max_arxiv_results']
        )
        # Process arXiv results in-memory
        corpus_docs = []
        for result in arxiv_results:
            # Exclude the source paper itself if it's found on arXiv
            if result.get_short_id() not in source_doc['path']:
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
        corpus_paths = [p for p in corpus_paths if os.path.abspath(p) != os.path.abspath(source_doc['path'])]
        corpus_docs = [load_source_document(p) for p in corpus_paths]

    # 4. Analyze for Similarity
    analyzer = SimilarityAnalyzer(config)
    findings = analyzer.find_similar_sentences(source_doc, corpus_docs)

    # 5. Generate Report
    if findings:
        generate_report(config, source_doc, findings)
    else:
        print("No significant similarities found based on the configured threshold.")

if __name__ == "__main__":
    # You would need to create a dummy 'source_paper.pdf' in 'data/input/'
    # or update the path in 'configs/config.yaml'.
    # For this example to run, ensure the input file exists.
    if not os.path.exists('data/input/2502.02587v1.pdf'):
        print("Error: 'data/input/2502.02587v1.pdf' not found.")
        print("Please add a PDF file to that location or update 'configs/config.yaml'.")
    else:
        run_pipeline()
