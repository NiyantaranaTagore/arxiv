# pipeline/data_loader.py

import yaml
from typing import Dict, Any
from utils.text_utils import extract_text_from_pdf, split_into_sentences

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_source_document(doc_path: str) -> Dict[str, Any]:
    """
    Loads the source document and prepares it for analysis.
    
    Args:
        doc_path (str): Path to the source PDF.

    Returns:
        A dictionary with the paper's title, abstract, and sentences.
    """
    print(f"Loading and processing source document: {doc_path}")
    title, abstract = extract_text_from_pdf(doc_path)
    sentences = split_into_sentences(abstract)
    
    return {
        "title": title,
        "abstract": abstract,
        "sentences": sentences,
        "path": doc_path
    }
