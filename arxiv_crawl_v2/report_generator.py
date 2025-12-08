import fitz  # PyMuPDF
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Ensure sentence tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

def get_color_palette(num_colors: int):
    """Generates a palette of visually distinct colors."""
    colors = [
        (1, 0.8, 0.8),  # Light Red
        (0.8, 1, 0.8),  # Light Green
        (0.8, 0.8, 1),  # Light Blue
        (1, 1, 0.8),    # Light Yellow
        (1, 0.8, 1),    # Light Magenta
        (0.8, 1, 1),    # Light Cyan
        (1, 0.9, 0.8),  # Light Orange
        (0.9, 0.8, 1),  # Light Purple
        (0.8, 0.9, 0.9),# Light Teal
        (0.9, 0.9, 0.8),# Light Olive
    ]
    # Repeat colors if more are needed
    return [colors[i % len(colors)] for i in range(num_colors)]

def generate_pdf_report(
    original_title: str,
    original_abstract: str,
    similar_papers: List[Dict[str, Any]],
    output_pdf_path: str,
    model_name: str
):
    """
    Generates a PDF report with highlighted sentences and a list of sources.
    """
    print(f"Generating PDF report at {output_pdf_path}...")
    model = SentenceTransformer(model_name)

    # Create a new PDF
    doc = fitz.open()
    page = doc.new_page()

    # --- 1. Add Original Title and Abstract to PDF ---
    page.insert_text((72, 72), f"Original Paper Title: {original_title}", fontsize=14, fontname="helvetica-bold")
    
    # Split abstract into sentences for highlighting
    original_abstract_sentences = nltk.sent_tokenize(original_abstract)
    if not original_abstract_sentences:
        page.insert_text((72, 100), "Original abstract not found or empty.", fontsize=11)
        y_pos = 120
    else:
        original_abstract_embeddings = model.encode(original_abstract_sentences)
        y_pos = 100
        page.insert_text((72, y_pos), "Original Abstract:", fontsize=12, fontname="helvetica-bold")
        y_pos += 20

        # --- 2. Find and Highlight Similar Sentences ---
        colors = get_color_palette(len(similar_papers))
        
        for sent_idx, (sentence, sent_embedding) in enumerate(zip(original_abstract_sentences, original_abstract_embeddings)):
            max_sim = 0
            best_paper_idx = -1

            for paper_idx, paper_item in enumerate(similar_papers):
                similar_paper_abstract = paper_item['paper'].summary
                similar_paper_sentences = nltk.sent_tokenize(similar_paper_abstract)
                if not similar_paper_sentences:
                    continue
                
                similar_paper_embeddings = model.encode(similar_paper_sentences)
                similarities = cosine_similarity(sent_embedding.reshape(1, -1), similar_paper_embeddings)[0]
                current_max_sim = np.max(similarities)

                if current_max_sim > max_sim:
                    max_sim = current_max_sim
                    best_paper_idx = paper_idx

            # Insert the sentence text into the PDF first
            # We use a TextWriter to handle wrapping long sentences
            text_rect = fitz.Rect(72, y_pos, page.rect.width - 72, y_pos + 100)
            res = page.insert_textbox(text_rect, f"{sentence} ", fontsize=11, fontname="helvetica")
            y_pos += res + 5 # Move y_pos down by the height of the inserted text

            # Highlight sentence if similarity is high enough
            if max_sim > 0.65 and best_paper_idx != -1:
                text_instances = page.search_for(sentence)
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=colors[best_paper_idx])
                    # Add a popup annotation with the similarity score
                    info_text = f"Source: Paper #{best_paper_idx + 1}\nSimilarity: {max_sim:.2%}"
                    info_annot = page.add_text_annot(inst.tl, info_text, icon="Note")
                    highlight.update()

    # --- 3. Add Sources List ---
    y_pos += 30
    page.insert_text((72, y_pos), "Similar Papers Found on ArXiv:", fontsize=12, fontname="helvetica-bold")
    y_pos += 20

    for i, item in enumerate(similar_papers):
        paper = item['paper']
        score = item['similarity_score']
        color = colors[i]
        
        # Draw a colored rectangle next to the source
        rect = fitz.Rect(72, y_pos - 2, 82, y_pos + 10)
        page.draw_rect(rect, color=color, fill=color)
        
        page.insert_text((90, y_pos + 8), f"{i+1}. [{paper.title}]({paper.pdf_url}) - Score: {score:.2%}", fontsize=10)
        y_pos += 20

    doc.save(output_pdf_path, garbage=4, deflate=True, clean=True)
    print("PDF report generation complete.")