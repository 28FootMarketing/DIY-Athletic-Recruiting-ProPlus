"""
pdf_generator.py
Generates downloadable roadmaps or recruiting plans using BytesIO for Streamlit Cloud.
"""

from fpdf import FPDF
from io import BytesIO

def generate_pdf_from_chat(content, filename="recruiting_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your DIY Recruiting Plan", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
