import argparse
import logging
from keyword_extractor import extract_keywords_from_text
from arxiv_crawler import crawl_arxiv
from similarity_analyzer import find_similar_papers
from utils import read_document, save_results_to_json, extract_title_and_abstract

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    """
    Main function to orchestrate document processing, keyword/title/abstract extraction,
    ArXiv crawling, and similarity analysis.
    """
    parser = argparse.ArgumentParser(
        description="Find papers on ArXiv similar to a given document."
    )
    parser.add_argument(
        "document_path",
        type=str,
        help="Path to the input document (.txt or .pdf)."
    )
    parser.add_argument(
        "--num_keywords",
        type=int,
        default=5,
        help="Number of keywords to extract from the document."
    )
    parser.add_argument(
        "--max_papers",
        type=int,
        default=200,
        help="Maximum number of papers to fetch from ArXiv."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="similar_papers.json",
        help="Path to the output JSON file."
    )
    args = parser.parse_args()

    # 1. Read the input document
    logging.info(f"Reading document: {args.document_path}")
    doc_text = read_document(args.document_path)

    # 2. Extract title and abstract from the document
    logging.info("Extracting title and abstract...")
    title, abstract = extract_title_and_abstract(doc_text)
    logging.info(f"Extracted Title: {title}")
    logging.info(f"Extracted Abstract: {abstract[:100]}...")
    
    # 3. Extract keywords
    logging.info("Extracting keywords...")
    keywords = extract_keywords_from_text(doc_text, top_n=args.num_keywords)
    logging.info(f"Extracted keywords: {', '.join(keywords)}")

    # 4. Crawl ArXiv using the extracted title, abstract, and keywords
    logging.info("Crawling ArXiv for similar papers...")
    crawled_papers = crawl_arxiv(title, abstract, keywords, max_results=args.max_papers)

    # 5. Find and rank similar papers based on the original document's full text
    logging.info("Analyzing similarity with crawled papers...")
    similar_papers = find_similar_papers(doc_text, crawled_papers)

    # 6. Save the results to a JSON file
    logging.info(f"Saving results to {args.output_file}")
    save_results_to_json(similar_papers, args.output_file)

if __name__ == "__main__":
    main()