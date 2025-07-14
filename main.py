from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from typing import Optional
from io import BytesIO
import os

app = FastAPI(title="APTA Certificate Generator", version="1.0.0")

class APTACertificateData(BaseModel):
    reference_no: Optional[str] = ""
    issued_in: Optional[str] = ""
    consigned_from: Optional[str] = ""
    consigned_to: Optional[str] = ""
    transport_route: Optional[str] = ""
    official_use: Optional[str] = ""
    tariff_item_number: Optional[str] = ""
    package_marks_numbers: Optional[str] = ""
    package_description: Optional[str] = ""
    origin_criterion: Optional[str] = ""
    gross_weight_or_quantity: Optional[str] = ""
    invoice_number_date: Optional[str] = ""
    declaration_country: Optional[str] = ""
    importing_country: Optional[str] = ""
    declaration_place_date: Optional[str] = ""
    declaration_signature: Optional[str] = ""
    certification_place_date: Optional[str] = ""
    certification_signature_stamp: Optional[str] = ""

@app.post("/generate-apta-certificate-pdf/")
def generate_apta_pdf(data: APTACertificateData):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        def draw_image(filename):
            path = os.path.join(os.path.dirname(__file__), "static", filename)
            if os.path.exists(path):
                c.drawImage(ImageReader(path), 0, 0, width=width, height=height)

        def draw_grid():
            c.setStrokeColorRGB(0.85, 0.85, 0.85)
            c.setFont("Helvetica", 4)
            for x in range(0, int(width), 20):
                c.line(x, 0, x, height)
                c.drawString(x + 1, 5, str(x))
            for y in range(0, int(height), 20):
                c.line(0, y, width, y)
                c.drawString(2, y + 1, str(y))

        def draw_value(value, x, y):
            c.setFont("Helvetica", 9.2)
            for i, line in enumerate(value.splitlines()):
                c.drawString(x, y - (i * 10), line)

        # === Page 1 ===
        draw_image("1.jpg")
        draw_grid()

        draw_value(data.reference_no, 320, 780)
        draw_value(data.issued_in, 380, 700)
        draw_value(data.consigned_from, 70, 745)
        draw_value(data.consigned_to, 70, 640)
        draw_value(data.transport_route, 70, 555)
        draw_value(data.official_use, 325, 660)
        draw_value(data.tariff_item_number, 70, 445)
        draw_value(data.package_marks_numbers, 140, 445)
        draw_value(data.package_description, 200, 445)
        draw_value(data.origin_criterion, 380, 445)
        draw_value(data.gross_weight_or_quantity, 450, 445)
        draw_value(data.invoice_number_date, 520, 445)

        # (Optional: Add declaration and certification blocks later)
        c.showPage()
        c.save()
        buffer.seek(0)

        return Response(
            content=buffer.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=apta_certificate.pdf"}
        )

    except Exception as e:
        print("⚠️ PDF generation failed:", str(e))
        raise HTTPException(status_code=500, detail="PDF generation failed")
