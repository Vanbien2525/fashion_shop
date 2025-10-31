from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import RegisterForm
from django.contrib import messages
from django.http import HttpResponse

from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .pdf_generator.generate_pdf import generate_user_pdf


def register(request):
    if request.method == 'POST':
        # ✅ Sửa chỗ này: thêm request.FILES
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Đăng ký thành công!")
            # ✅ Sửa chỗ này: dùng name của URL chứ không phải file
            return redirect('accounts:login')
        else:
            print(form.errors)
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:index')  # ✅ chuyển đến index.html
        else:
            return render(request, 'accounts/login.html', {'error': 'Sai tên đăng nhập hoặc mật khẩu.'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:base')  # ✅ quay về trang ngoài


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def export_pdf_view(request):
    """
    Xuất hồ sơ người dùng ra file PDF để tải về.
    """
    buffer = generate_user_pdf(request.user)
    filename = f"profile_{request.user.username}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)

