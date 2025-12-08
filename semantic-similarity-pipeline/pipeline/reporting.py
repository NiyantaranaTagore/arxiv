# pipeline/reporting.py

from fpdf import FPDF
from typing import List, Dict, Any
import datetime
import os
import colorsys

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Semantic Similarity Report', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 5, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_report(config: Dict[str, Any], source_doc: Dict[str, Any], findings: List[Dict[str, Any]]):
    """
    Generates a PDF report with highlighted similar sentences.
    
    Args:
        config (Dict[str, Any]): The configuration dictionary.
        source_doc (Dict[str, Any]): The processed source document.
        findings (List[Dict[str, Any]]): The list of similarity findings.
    """
    pdf = PDFReport()
    pdf.add_page()
    
    # --- Font Setup (Portable) ---
    # Using font files included with the project makes it more portable
    # and avoids system dependency issues.
    times_path = 'assets/fonts/Times New Roman.ttf'
    times_bold_path = 'assets/fonts/Times New Roman Bold.ttf'

    if not os.path.exists(times_path):
        raise FileNotFoundError(f"Font file not found at {times_path}. "
                                "Please ensure the font file is in the assets/fonts directory.")
    if not os.path.exists(times_bold_path):
        raise FileNotFoundError(f"Font file not found at {times_bold_path}. "
                                "Please ensure the font file is in the assets/fonts directory.")

    # Set uni=True to enable Unicode support for the TTF fonts.
    pdf.add_font('TimesNewRoman', '', times_path, uni=True)
    pdf.add_font('TimesNewRoman', 'B', times_bold_path, uni=True)
    
    # Create a unique list of source documents from the findings
    unique_sources = list({finding['source_paper_path']: finding for finding in findings}.values())

    # --- Define Colors ---
    # Dynamically generate a list of distinct colors based on the number of unique sources.
    # This ensures each source has a unique color.
    num_colors = len(unique_sources)
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        # Use high lightness and saturation to get pleasant pastel colors for highlighting.
        rgb_float = colorsys.hls_to_rgb(hue, 0.9, 0.95)
        colors.append(tuple(int(c * 255) for c in rgb_float))

    # Map each unique source path to a color and a reference number
    source_map = {source['source_paper_path']: colors[i] for i, source in enumerate(unique_sources)}
    source_number_map = {source['source_paper_path']: i + 1 for i, source in enumerate(unique_sources)}

    # Find the maximum similarity score for each source paper
    max_similarity_per_source = {}
    for finding in findings:
        path = finding['source_paper_path']
        score = finding['similarity_score']
        max_similarity_per_source[path] = max(max_similarity_per_source.get(path, 0), score)

    # --- Report Title ---
    pdf.set_font("TimesNewRoman", 'B', config['font_size_title'])
    pdf.multi_cell(0, 10, source_doc['title'])
    pdf.ln(5)

    # --- Abstract with Highlighting ---
    pdf.set_font("TimesNewRoman", '', config['font_size_abstract'])
    
    # Group findings by source sentence
    findings_by_sentence = {}
    for find in findings:
        sentence = find['source_sentence']
        if sentence not in findings_by_sentence:
            findings_by_sentence[sentence] = []
        findings_by_sentence[sentence].append(find)

    # Write abstract sentence by sentence, highlighting if necessary
    for sentence in source_doc['sentences']:
        if sentence in findings_by_sentence:
            best_finding = max(findings_by_sentence[sentence], key=lambda x: x['similarity_score'])
            color = source_map[best_finding['source_paper_path']]
            pdf.set_fill_color(color[0], color[1], color[2])
            source_num = source_number_map[best_finding['source_paper_path']]
            
            text_to_write = f"{sentence} [{source_num}]"
            pdf.multi_cell(0, 5, text_to_write, fill=True)
        else:
            pdf.multi_cell(0, 5, sentence)
        pdf.ln(1) # Add a little space between sentences
        
    pdf.ln(10)

    # --- Sources Section ---
    pdf.set_font("TimesNewRoman", 'B', 12)
    pdf.cell(0, 10, "Sources of Similar Content", 0, 1)
    
    pdf.set_font("TimesNewRoman", '', config['font_size_sources'])
    for i, source in enumerate(unique_sources):
        path = source['source_paper_path']
        title = source['source_paper_title']
        color = source_map[path]
        source_num = i + 1
        max_score = max_similarity_per_source.get(path, 0)

        pdf.set_fill_color(color[0], color[1], color[2])
        pdf.cell(5, 5, '', 1, 0, 'L', fill=True)
        pdf.multi_cell(0, 5, f" [{source_num}] [Similarity: {max_score:.0%}] {title}\n      (Source: {path})", border=0, align='L')
        pdf.ln(2)

    # --- Save the PDF ---
    output_filename = os.path.join(config['output_dir'], "similarity_report.pdf")
    os.makedirs(config['output_dir'], exist_ok=True)
    pdf.output(output_filename)
    print(f"Report successfully generated at: {output_filename}")
