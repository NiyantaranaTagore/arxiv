from keybert import KeyBERT
from typing import List

def extract_keywords_from_text(text: str, top_n: int = 10) -> List[str]:
    """
    Extracts key phrases from the given text using the KeyBERT model.

    Args:
        text (str): The input text from the document.
        top_n (int): The number of top keywords to extract.

    Returns:
        List[str]: A list of the most relevant keywords.
    """
    # KeyBERT uses sentence-transformers to find the most representative keywords
    kw_model = KeyBERT()
    # We look for keyphrases of 1 or 2 words, ignoring common English stop words.
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    
    # Return only the keyword text, not the similarity score
    return [keyword for keyword, _ in keywords]