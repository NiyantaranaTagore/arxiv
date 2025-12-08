# pipeline/similarity_analyzer.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any

class SimilarityAnalyzer:
    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the SimilarityAnalyzer with a specified model.
        
        Args:
            config (Dict[str, Any]): The configuration dictionary.
        """
        self.model = SentenceTransformer(config['embedding_model'])
        self.threshold = config['similarity_threshold']

    def find_similar_sentences(self, source_doc: Dict[str, Any], corpus_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Finds sentences in the source document that are similar to sentences in the corpus.
        
        Args:
            source_doc (Dict[str, Any]): The processed source document.
            corpus_docs (List[Dict[str, Any]]): A list of corpus documents to compare against.

        Returns:
            A list of findings, where each finding details a similarity match.
        """
        source_sentences = source_doc['sentences']
        source_embeddings = self.model.encode(source_sentences)
        
        findings = []
        
        for i, doc in enumerate(corpus_docs):
            print(f"Analyzing against corpus document: {doc['title']}")
            corpus_sentences = doc['sentences']
            if not corpus_sentences:
                continue

            corpus_embeddings = self.model.encode(corpus_sentences)
            
            # Calculate cosine similarity
            sim_matrix = cosine_similarity(source_embeddings, corpus_embeddings)
            
            # Find matches above the threshold
            matches = np.where(sim_matrix >= self.threshold)
            
            for src_idx, corp_idx in zip(*matches):
                similarity_score = sim_matrix[src_idx, corp_idx]
                
                findings.append({
                    "source_sentence": source_sentences[src_idx],
                    "similar_sentence": corpus_sentences[corp_idx],
                    "similarity_score": float(similarity_score),
                    "source_paper_title": doc['title'],
                    "source_paper_path": doc['path']
                })
                
        return findings
