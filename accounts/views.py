from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm
from .models import UserProfile
from .pdf_generator.generate_pdf import generate_users_pdf

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('accounts:login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:profile')
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu!")

    return render(request, 'accounts/login.html')


@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def export_users_pdf(request):
    pdf_path = generate_users_pdf()
    if pdf_path:
        return redirect('accounts:export_success')
    else:
        messages.error(request, "Lỗi khi xuất PDF!")
        return redirect('accounts:profile')


def export_success(request):
    return render(request, 'accounts/export_success.html')
