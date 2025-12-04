import json
import pypdf
from typing import List, Dict, Any, Tuple

def read_document(filepath: str) -> str:
    """
    Reads text from a .txt or .pdf file.

    Args:
        filepath (str): The path to the document.

    Returns:
        str: The extracted text content of the document.
    """
    if filepath.lower().endswith('.pdf'):
        try:
            with open(filepath, 'rb') as f:
                reader = pypdf.PdfReader(f)
                text = "".join(page.extract_text() for page in reader.pages)
            return text
        except Exception as e:
            raise IOError(f"Error reading PDF file: {e}")
    elif filepath.lower().endswith('.txt'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Error reading text file: {e}")
    else:
        raise ValueError("Unsupported file type. Please provide a .txt or .pdf file.")

def extract_title_and_abstract(doc_text: str) -> Tuple[str, str]:
    """
    Extracts the title and abstract from the document text using heuristics.

    Args:
        doc_text (str): The full text of the document.

    Returns:
        Tuple[str, str]: A tuple containing the extracted title and abstract.
    """
    lines = [line.strip() for line in doc_text.split('\n') if line.strip()]
    
    # Heuristic for Title: Assume the first significant block of text before the abstract is the title.
    # This is a simple heuristic and might need refinement for different document structures.
    title = lines[0] if lines else ""
    
    # Heuristic for Abstract: Find the line that starts with "ABSTRACT" and capture text until the next common section.
    abstract = ""
    try:
        # Find the start of the abstract
        abstract_start_index = doc_text.upper().index("ABSTRACT")
        # Find the end of the abstract (e.g., start of "INDEX TERMS" or "I. INTRODUCTION")
        text_after_abstract = doc_text[abstract_start_index:]
        end_markers = ["INDEX TERMS", "I. INTRODUCTION"]
        end_index = min([text_after_abstract.upper().find(marker) for marker in end_markers if text_after_abstract.upper().find(marker) != -1] or [len(text_after_abstract)])
        abstract = text_after_abstract[len("ABSTRACT"):end_index].strip()
    except ValueError:
        abstract = "" # Could not find the abstract
    return title, abstract

def save_results_to_json(papers: List[Dict[str, Any]], output_path: str = "similar_papers.json"):
    """
    Saves the list of similar papers to a JSON file.

    Args:
        papers (List[Dict[str, Any]]): A list of dictionaries, each representing a similar paper.
        output_path (str): The path for the output JSON file.
    """
    results = []
    for item in papers:
        paper = item['paper']
        results.append({
            "arxiv_id": paper.entry_id.split('/')[-1],
            "title": paper.title,
            "abstract": paper.summary.replace("\n", " "),
            "authors": [author.name for author in paper.authors],
            "submitted_date": paper.published.isoformat(),
            "pdf_url": paper.pdf_url,
            "similarity_score": item['similarity_score']
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Results saved to {output_path}")