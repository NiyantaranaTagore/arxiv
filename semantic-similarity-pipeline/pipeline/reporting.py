# pipeline/reporting.py

from fpdf import FPDF
from typing import List, Dict, Any
import datetime
import os

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
    
    # --- Define Colors ---
    colors = [
        (255, 192, 203),  # Pink
        (173, 216, 230),  # Light Blue
        (144, 238, 144),  # Light Green
        (255, 255, 224),  # Light Yellow
        (221, 160, 221),  # Plum
    ]
    # Create a unique list of source documents from the findings
    unique_sources = {finding['source_paper_path']: finding for finding in findings}.values()
    # Map each unique source path to a color
    source_map = {source['source_paper_path']: colors[i % len(colors)] for i, source in enumerate(unique_sources)}

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
            
            text_to_write = f"{sentence} [Similarity: {best_finding['similarity_score']:.0%}]"
            pdf.multi_cell(0, 5, text_to_write, fill=True)
        else:
            pdf.multi_cell(0, 5, sentence)
        pdf.ln(1) # Add a little space between sentences
        
    pdf.ln(10)

    # --- Sources Section ---
    pdf.set_font("TimesNewRoman", 'B', 12)
    pdf.cell(0, 10, "Sources of Similar Content", 0, 1)
    
    pdf.set_font("TimesNewRoman", '', config['font_size_sources'])
    for source in unique_sources:
        path = source['source_paper_path']
        title = source['source_paper_title']
        color = source_map[path]
        pdf.set_fill_color(color[0], color[1], color[2])
        pdf.cell(10, 5, '', 1, 0, 'L', fill=True)
        pdf.multi_cell(0, 5, f" {title}\n   (Source: {path})", border=0, align='L')
        pdf.ln(2)

    # --- Save the PDF ---
    output_filename = os.path.join(config['output_dir'], "similarity_report.pdf")
    os.makedirs(config['output_dir'], exist_ok=True)
    pdf.output(output_filename)
    print(f"Report successfully generated at: {output_filename}")
