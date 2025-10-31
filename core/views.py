from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Trang mặc định: base.html
def base(request):
    # Nếu user đã login, chuyển thẳng sang index
    if request.user.is_authenticated:
       return redirect('core:index')
    return render(request, 'core/base.html')

# Trang index: chỉ cho user đã login
@login_required
def index(request):
    return render(request, 'core/index.html')
