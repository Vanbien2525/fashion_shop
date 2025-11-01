from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from django.utils import timezone
from django.conf import settings
from accounts.models import UserImage 
import os


def generate_user_pdf(user):
    """
    Tạo file PDF chứa thông tin người dùng và ảnh đã upload (nếu có).
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # === 1️⃣ Font Unicode tiếng Việt ===
    font_path = os.path.join(settings.BASE_DIR, 'accounts', 'pdf_generator', 'fonts', 'DejaVuSans.ttf')
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found at {font_path}")
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    # === 2️⃣ Tiêu đề ===
    p.setFont("DejaVuSans", 20)
    p.drawCentredString(width / 2, height - 3 * cm, "THÔNG TIN CÁ NHÂN")

    p.setFont("DejaVuSans", 12)
    y = height - 5 * cm
    p.drawString(3 * cm, y, f"Tên tài khoản: {user.username}")
    y -= 1 * cm
    p.drawString(3 * cm, y, f"Email: {user.email or 'Không có'}")
    y -= 1 * cm
    p.drawString(3 * cm, y, f"Số điện thoại: {getattr(user, 'phone_number', 'Không có')}")

    # === 3️⃣ Ngày đăng ký ===
    local_time = timezone.localtime(user.date_joined)
    formatted_date = local_time.strftime('%d/%m/%Y %H:%M')
    y -= 1 * cm
    p.drawString(3 * cm, y, f"Ngày đăng ký: {formatted_date}")

    # === 4️⃣ Hiển thị các ảnh đã upload ===
    y -= 2 * cm
    p.setFont("DejaVuSans", 12)
    p.drawString(3 * cm, y, "Ảnh đã tải lên:")

    # ✅ Dùng đúng related_name = 'images'
    if hasattr(user, "images") and user.images.exists():
        y -= 1 * cm
        for i, img_obj in enumerate(user.images.all()):
            img_path = os.path.join(settings.MEDIA_ROOT, img_obj.image.name)
            if os.path.exists(img_path):
                try:
                    # Nếu sắp hết trang → tạo trang mới
                    if y - 7 * cm < 2 * cm:
                        p.showPage()
                        p.setFont("DejaVuSans", 12)
                        y = height - 3 * cm  # reset vị trí đầu trang mới

                    p.drawImage(img_path, 3 * cm, y - 6 * cm, width=6 * cm, height=6 * cm, preserveAspectRatio=True)
                    y -= 7 * cm

                except Exception as e:
                    p.drawString(3 * cm, y, f"(Không thể hiển thị ảnh {i+1}: {e})")
                    y -= 1 * cm
            else:
                p.drawString(3 * cm, y, f"(Không tìm thấy ảnh {i+1})")
                y -= 1 * cm
    else:
        p.drawString(3 * cm, y - 1 * cm, "(Chưa có ảnh nào được tải lên)")

    # === 5️⃣ Kết thúc ===
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
