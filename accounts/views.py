from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import FileResponse

from .forms import RegisterForm
from .models import UserImage
from .pdf_generator.generate_pdf import generate_user_pdf


def register(request):
    """
    Đăng ký tài khoản người dùng mới kèm tối đa 5 ảnh đại diện.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined_custom = timezone.now()
            user.save()

            # ✅ Lưu tối đa 5 ảnh upload
            images = request.FILES.getlist('images')
            for img in images[:5]:
                UserImage.objects.create(user=user, image=img)

            messages.success(request, "🎉 Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.")
            return redirect('accounts:login')
        else:
            print("❌ Form errors:", form.errors)
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Xử lý đăng nhập người dùng.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Xin chào {user.username} 👋")
            return redirect('core:index')
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    Đăng xuất người dùng và quay về trang chính.
    """
    logout(request)
    messages.info(request, "Bạn đã đăng xuất.")
    return redirect('core:base')


@login_required
def profile_view(request):
    user_images = request.user.images.all()  # 👈 thêm dòng này
    return render(request, 'accounts/profile.html', {
        'user_images': user_images,           # 👈 và thêm dòng này vào context
    })


@login_required
def export_pdf_view(request):
    """
    Xuất hồ sơ người dùng ra file PDF để tải về.
    """
    buffer = generate_user_pdf(request.user)
    filename = f"profile_{request.user.username}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)
