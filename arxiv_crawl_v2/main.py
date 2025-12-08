import argparse
import yaml
from keyword_extractor import extract_keywords_from_text
from arxiv_crawler import crawl_arxiv
from similarity_analyzer import find_similar_papers
from local_llm_corrector import correct_text_with_local_llm
from utils import read_document, save_results_to_json, extract_title_and_abstract
from report_generator import generate_pdf_report

def main():
    """
    Main function to orchestrate document processing, keyword/title/abstract extraction,
    ArXiv crawling, and similarity analysis.
    """
    parser = argparse.ArgumentParser(description="Find papers on ArXiv similar to a given document.")
    parser.add_argument("config_path", type=str, help="Path to the configuration YAML file.")
    args = parser.parse_args()

    # Load configuration from YAML file
    with open(args.config_path, 'r') as f:
        config = yaml.safe_load(f)

    doc_path = config["document_path"]
    output_json_path = config["output_file"]
    num_keywords = config["num_keywords"]
    max_papers = config["max_papers"]
    min_similarity = config["min_similarity"]
    similarity_model = config["similarity_model"]
    llm_model = config.get("llm_model") # Use .get() for optional keys
    ollama_url = config.get("ollama_url")
    title_weight = config["title_weight"]
    abstract_weight = config["abstract_weight"]
    output_pdf_path = output_json_path.replace('.json', '_report.pdf')

    # 1. Read the input document
    print(f"Reading document: {doc_path}")
    doc_text = read_document(doc_path)

    # 2. Extract title and abstract from the document
    print("Extracting title and abstract...")
    title, abstract = extract_title_and_abstract(doc_text)
    
    # Optionally correct the extracted title using the local LLM
    if llm_model and ollama_url:
        print(f"Extracted Title (raw): {title}")
        title = correct_text_with_local_llm(title, llm_model, ollama_url)
        print(f"Corrected Title: {title}")
    else:
        print(f"Extracted Title: {title}")

    # 3. Extract keywords
    print("Extracting keywords...")
    keywords = extract_keywords_from_text(doc_text, top_n=num_keywords)
    print(f"Extracted keywords: {', '.join(keywords)}")

    # 4. Crawl ArXiv using the extracted title, abstract, and keywords
    crawled_papers = crawl_arxiv(title, abstract, keywords, max_results=max_papers)

    # 5. Find and rank similar papers using a weighted comparison of title and abstract
    similar_papers = find_similar_papers(title, abstract, crawled_papers, similarity_model, title_weight, abstract_weight)

    # 6. Save the results to a JSON file
    save_results_to_json(similar_papers, output_json_path, min_similarity)

    # 7. Generate the PDF report
    # Filter papers for the report based on the similarity threshold
    report_papers = [p for p in similar_papers if p['similarity_score'] >= min_similarity]
    if report_papers:
        generate_pdf_report(title, abstract, report_papers, output_pdf_path, similarity_model)
    else:
        print("No papers met the minimum similarity threshold for PDF report generation.")

if __name__ == "__main__":
    main()