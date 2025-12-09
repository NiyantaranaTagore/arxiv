# utils/text_utils.py

import fitz  # PyMuPDF
import nltk
from typing import List, Tuple

def download_nltk_data():
    """Downloads the necessary NLTK data."""
    try:
        nltk.data.find('tokenizers/punkt')
    except nltk.downloader.DownloadError:
        print("Downloading NLTK 'punkt' model...")
        nltk.download('punkt')

def extract_text_from_pdf(pdf_path: str) -> Tuple[str, str]:
    """
    Extracts the title and abstract from the first page of a PDF.
    This function assumes a standard academic paper format.
    
    Args:
        pdf_path (str): The path to the input PDF file.

    Returns:
        A tuple containing the title and the abstract.
    """
    doc = fitz.open(pdf_path)
    first_page_text = doc[0].get_text("text")
    
    # These are heuristic rules and might need adjustment for different paper formats.
    lines = first_page_text.split('\n')
    title = lines[0].strip()
    
    abstract_start_index = -1
    for i, line in enumerate(lines):
        if "abstract" in line.lower():
            abstract_start_index = i
            break
            
    if abstract_start_index == -1:
        raise ValueError("Could not find 'Abstract' on the first page.")

    abstract_lines = lines[abstract_start_index + 1:]
    abstract = " ".join(line.strip() for line in abstract_lines if line.strip()).replace("Abstract", "").strip()
    
    doc.close()
    return title, abstract

def split_into_sentences(text: str) -> List[str]:
    """
    Splits a block of text into a list of sentences.
    
    Args:
        text (str): The text to split.

    Returns:
        A list of sentences.
    """
    download_nltk_data()
    return nltk.sent_tokenize(text)

