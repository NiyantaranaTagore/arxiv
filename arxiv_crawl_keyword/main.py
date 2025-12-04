import argparse
from keyword_extractor import extract_keywords_from_text
from arxiv_crawler import crawl_arxiv_by_keywords
from similarity_analyzer import find_similar_papers
from utils import read_document, save_results_to_json

def main():
    """
    Main function to orchestrate the document processing, keyword extraction,
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
        default=10,
        help="Max number of papers to fetch from ArXiv per keyword."
    )
    parser.add_argument(
        "--top_n_similar",
        type=int,
        default=5,
        help="Number of most similar papers to return in the output."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="similar_papers.json",
        help="Path to the output JSON file."
    )
    args = parser.parse_args()

    # 1. Read the input document
    print(f"Reading document: {args.document_path}")
    doc_text = read_document(args.document_path)

    # 2. Extract keywords
    print("Extracting keywords...")
    keywords = extract_keywords_from_text(doc_text, top_n=args.num_keywords)
    print(f"Extracted keywords: {', '.join(keywords)}")
    
    # User confirmation could be added here if this were an interactive script.
    # For a non-interactive script, we proceed with the extracted keywords.

    # 3. Crawl ArXiv using the keywords
    crawled_papers = crawl_arxiv_by_keywords(keywords, max_results_per_keyword=args.max_papers)

    # 4. Find and rank similar papers
    similar_papers = find_similar_papers(doc_text, crawled_papers, top_n=args.top_n_similar)

    # 5. Save the results to a JSON file
    save_results_to_json(similar_papers, args.output_file)

if __name__ == "__main__":
    main()