from fpdf import FPDF
import datetime

def generate_pdf_from_chat(content, filename="recruiting_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your DIY Recruiting Plan", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = filename.replace(" ", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.pdf"

    path = f"/mnt/data/{full_filename}"
    pdf.output(path)
    return path
