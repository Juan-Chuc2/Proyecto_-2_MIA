import os
from datetime import datetime
from reportlab.pdfgen import canvas
from src.Repositorio.contactos import obtener_todos_contactos


def generar_pdf():
    contactos = obtener_todos_contactos()

    os.makedirs("exportaciones", exist_ok=True)

    pdf = canvas.Canvas("exportaciones/Contactos.pdf", pagesize=(595, 842))

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, 800, "REPORTE DE CONTACTOS")

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, 775, f"Fecha: {fecha}")

    y = 740

    for contacto in contactos:
        if y < 130:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = 790

        pdf.drawString(50, y, f"ID: {contacto.id}")
        pdf.drawString(50, y - 20, f"Nombre: {contacto.nombre}")
        pdf.drawString(50, y - 40, f"Telefono: {contacto.telefono}")
        pdf.drawString(50, y - 60, f"Correo: {contacto.correo}")
        pdf.drawString(50, y - 80, f"Ciudad: {contacto.ciudad}")

        y -= 120

    pdf.save()

    return True