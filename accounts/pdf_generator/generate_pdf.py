from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
import os

def generate_users_pdf():
    pdf_dir = "media/exports"
    os.makedirs(pdf_dir, exist_ok=True)
    file_path = os.path.join(pdf_dir, "users_list.pdf")

    c = canvas.Canvas(file_path, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(200, 800, "Danh sách người dùng")

    y = 760
    users = User.objects.all()
    for user in users:
        c.drawString(100, y, f"- {user.username} ({user.email})")
        y -= 20
        if y < 100:
            c.showPage()
            y = 800

    c.save()
    return file_path
