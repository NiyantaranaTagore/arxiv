from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer

def find_similar_papers(
    original_title: str,
    original_abstract: str,
    crawled_papers: List[Any],
    model_name: str = 'all-MiniLM-L6-v2',
    title_weight: float = 0.3,
    abstract_weight: float = 0.7,
) -> List[Dict[str, Any]]:
    """
    Compares crawled papers to the original document's title and abstract,
    returning a ranked list based on a weighted similarity score.

    Args:
        original_title (str): The title of the source document.
        original_abstract (str): The abstract of the source document.
        crawled_papers (List[Any]): A list of paper objects from the arxiv library.
        model_name (str): The name of the sentence-transformer model to use.
        title_weight (float): The weight to give to title similarity.
        abstract_weight (float): The weight to give to abstract similarity.

    Returns:
        List[Dict[str, Any]]: A sorted list of the top N similar papers with their metadata.
    """
    if not crawled_papers:
        return []

    print(f"Loading similarity model: {model_name}...")
    model = SentenceTransformer(model_name)

    # Generate embeddings for the original document's title and abstract
    original_title_embedding = model.encode(original_title, convert_to_tensor=False).reshape(1, -1)
    original_abstract_embedding = model.encode(original_abstract, convert_to_tensor=False).reshape(1, -1)

    # Separate titles and abstracts from the crawled papers
    corpus_titles = [paper.title for paper in crawled_papers]
    corpus_abstracts = [paper.summary.replace('\n', ' ') for paper in crawled_papers]

    # Generate embeddings for the corpus titles and abstracts
    corpus_title_embeddings = model.encode(corpus_titles, convert_to_tensor=False)
    corpus_abstract_embeddings = model.encode(corpus_abstracts, convert_to_tensor=False)

    # Calculate cosine similarity between the original document and all crawled papers
    title_similarities = cosine_similarity(original_title_embedding, corpus_title_embeddings)[0]
    abstract_similarities = cosine_similarity(original_abstract_embedding, corpus_abstract_embeddings)[0]

    # Calculate a weighted combined similarity score.
    combined_similarities = (title_weight * title_similarities) + (abstract_weight * abstract_similarities)

    # Pair each paper with its similarity score
    scored_papers = []
    for i, paper in enumerate(crawled_papers):
        scored_papers.append({
            "paper": paper,
            "similarity_score": float(combined_similarities[i])
        })

    # Sort papers by similarity score in descending order
    scored_papers.sort(key=lambda x: x['similarity_score'], reverse=True)

    # Return all scored and sorted papers
    return scored_papers