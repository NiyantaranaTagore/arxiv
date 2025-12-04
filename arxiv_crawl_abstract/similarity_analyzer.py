from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any, Tuple

# Load a pre-trained model for creating sentence embeddings.
# 'all-MiniLM-L6-v2' is a great balance of speed and performance.
model = SentenceTransformer('all-MiniLM-L6-v2')

def find_similar_papers(
    original_text: str,
    crawled_papers: List[Any],
) -> List[Dict[str, Any]]:
    """
    Compares crawled papers to the original document text and returns the most similar ones.

    Args:
        original_text (str): The text of the input proposal document.
        crawled_papers (List[Any]): A list of paper objects from the arxiv library.

    Returns:
        List[Dict[str, Any]]: A sorted list of the top N similar papers with their metadata.
    """
    if not crawled_papers:
        return []

    # Generate an embedding for the original document
    original_embedding = model.encode(original_text, convert_to_tensor=False).reshape(1, -1)

    # Combine title and abstract for each crawled paper and generate embeddings
    corpus_texts = [f"{paper.title} {paper.summary.replace(' ', ' ')}" for paper in crawled_papers]
    corpus_embeddings = model.encode(corpus_texts, convert_to_tensor=False)

    # Calculate cosine similarity between the original document and all crawled papers
    similarities = cosine_similarity(original_embedding, corpus_embeddings)[0]

    # Pair each paper with its similarity score
    scored_papers = []
    for i, paper in enumerate(crawled_papers):
        scored_papers.append({
            "paper": paper,
            "similarity_score": float(similarities[i])
        })

    # Sort papers by similarity score in descending order
    scored_papers.sort(key=lambda x: x['similarity_score'], reverse=True)

    # Return all scored and sorted papers
    return scored_papers