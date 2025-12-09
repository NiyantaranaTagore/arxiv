# pipeline/similarity_analyzer.py

from sentence_transformers import SentenceTransformer, models
from sentence_transformers.util import cos_sim
from tqdm import tqdm
import torch

class SimilarityAnalyzer:
    """
    Handles the loading of sentence embedding models and the calculation of semantic similarity.
    """
    def __init__(self, config):
        self.model_name = config['embedding_model']
        self.threshold = config['similarity_threshold']
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        self.model = self._load_model()

    def _load_model(self):
        """
        Loads the sentence-transformer model.
        This handles the specific case for contriever models to ensure the correct pooling is used.
        """
        print(f"Loading embedding model: {self.model_name}...")
        # The contriever model requires explicit pooling layer definition for optimal performance
        # when not loaded directly as a pre-saved SentenceTransformer object. We also
        # handle SimCSE models, which require CLS pooling.
        model_name_lower = self.model_name.lower()
        if 'contriever' in model_name_lower:
            word_embedding_model = models.Transformer(self.model_name)
            # Contriever uses mean pooling
            pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode='mean')
            model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device=self.device)
        elif 'simcse' in model_name_lower:
            word_embedding_model = models.Transformer(self.model_name)
            # SimCSE uses the embedding of the [CLS] token
            pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode='cls')
            model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device=self.device)
        else:
            # For standard sentence-transformer models, direct loading is fine.
            model = SentenceTransformer(self.model_name, device=self.device)
        print("Model loaded successfully.")
        return model

    def find_similar_sentences(self, source_doc, corpus_docs):
        """
        Finds sentences in the corpus that are similar to sentences in the source document.
        """
        print("Encoding sentences from the source document...")
        source_embeddings = self.model.encode(
            source_doc['sentences'], 
            convert_to_tensor=True, 
            device=self.device,
            show_progress_bar=True
        )

        findings = []
        print("\nAnalyzing corpus documents for similarity...")
        for corpus_doc in tqdm(corpus_docs, desc="Comparing Documents"):
            if not corpus_doc.get('sentences'):
                continue

            corpus_embeddings = self.model.encode(
                corpus_doc['sentences'], 
                convert_to_tensor=True, 
                device=self.device,
                show_progress_bar=False # Disable inner progress bar
            )

            # Calculate cosine similarity between all source and corpus sentences
            similarity_matrix = cos_sim(source_embeddings, corpus_embeddings)

            # Find pairs above the threshold
            for i in range(len(source_doc['sentences'])):
                for j in range(len(corpus_doc['sentences'])):
                    score = similarity_matrix[i][j].item()
                    if score >= self.threshold:
                        findings.append({
                            'source_sentence': source_doc['sentences'][i],
                            'similar_sentence': corpus_doc['sentences'][j],
                            'similarity_score': score,
                            'source_paper_title': corpus_doc['title'],
                            'source_paper_path': corpus_doc['path']
                        })
        
        # Sort findings by similarity score in descending order
        findings.sort(key=lambda x: x['similarity_score'], reverse=True)
        return findings