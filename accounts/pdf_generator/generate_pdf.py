from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from django.utils import timezone
from django.conf import settings
import os


def generate_user_pdf(user):
    """
    Tạo file PDF chứa thông tin người dùng và ảnh đại diện (nếu có).
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # === 1️⃣ Đăng ký font Unicode có hỗ trợ tiếng Việt ===
    font_path = os.path.join(settings.BASE_DIR, 'accounts', 'pdf_generator', 'fonts', 'DejaVuSans.ttf')
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found at {font_path}")
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    # === 2️⃣ Dùng đúng font này khi vẽ text ===
    p.setFont("DejaVuSans", 20)
    p.drawCentredString(width / 2, height - 3 * cm, "THÔNG TIN CÁ NHÂN")

    p.setFont("DejaVuSans", 12)
    y = height - 5 * cm
    p.drawString(3 * cm, y, f"Tên tài khoản: {user.username}")
    y -= 1 * cm
    p.drawString(3 * cm, y, f"Email: {user.email or 'Không có'}")
    y -= 1 * cm
    p.drawString(3 * cm, y, f"Số điện thoại: {getattr(user, 'phone_number', 'Không có')}")

    # === 3️⃣ Hiển thị ngày đăng ký đúng giờ Việt Nam ===
    local_time = timezone.localtime(user.date_joined)
    formatted_date = local_time.strftime('%d/%m/%Y %H:%M')
    y -= 1 * cm
    p.drawString(3 * cm, y, f"Ngày đăng ký: {formatted_date}")

    # === 4️⃣ Thêm ảnh đại diện ===
    y -= 2 * cm
    p.setFont("DejaVuSans", 12)
    p.drawString(3 * cm, y, "Ảnh:")

    avatar_path = None
    if getattr(user, "avatar", None) and user.avatar:
        avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar.name)
    else:
        avatar_path = os.path.join(settings.STATIC_ROOT, "core/images/default-avatar.png")

    if os.path.exists(avatar_path):
        try:
            p.drawImage(avatar_path, 3 * cm, y - 8 * cm, width=6 * cm, height=6 * cm, preserveAspectRatio=True)
        except Exception as e:
            p.drawString(3 * cm, y - 1 * cm, f"(Không thể hiển thị ảnh: {e})")
    else:
        p.drawString(3 * cm, y - 1 * cm, "(Không tìm thấy ảnh)")

    # === 5️⃣ Kết thúc ===
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
