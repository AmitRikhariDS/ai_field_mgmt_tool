# api/utils.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)

    # Company Info
    c.drawString(50, 800, "GlobalXperts Technology Pvt. Ltd.")
    c.drawString(50, 785, "113, Centrum Plaza, Golf Course Road")
    c.drawString(50, 770, "Sector 53, Gurugram, Haryana 122002, India")

    # Client & Invoice Info
    c.drawString(50, 740, f"Invoice Number: {invoice.invoice_number}")
    c.drawString(50, 725, f"Date: {invoice.date}")
    c.drawString(50, 710, f"Client: {invoice.client.name}")
    c.drawString(50, 695, f"Engineer: {invoice.engineer.name}")

    # Job & Charges
    c.drawString(50, 665, f"Job: {invoice.job.title if invoice.job else 'N/A'}")
    c.drawString(50, 650, f"Hours Worked: {invoice.hours_worked}")
    c.drawString(50, 635, f"Rate per Hour: ₹{invoice.per_hour_charge}")
    c.drawString(50, 620, f"Total Amount: ₹{invoice.total_amount}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
