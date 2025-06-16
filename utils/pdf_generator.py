"""
pdf_generator.py
Generates downloadable roadmaps or recruiting plans using BytesIO for Streamlit Cloud.
"""

from fpdf import FPDF
from io import BytesIO

def remove_non_latin1(text):
    return text.encode("latin-1", "replace").decode("latin-1")

def generate_pdf_from_chat(content, filename="recruiting_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your DIY Recruiting Plan", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)

    clean_content = remove_non_latin1(content)
    for line in clean_content.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Output PDF to bytes using Latin-1
    pdf_output = pdf.output(dest="S").encode("latin1")
    buffer = BytesIO(pdf_output)
    return buffer
