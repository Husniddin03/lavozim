from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


def register_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Bu telefon raqami allaqachon ro\'yxatdan o\'tgan')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=phone,
            phone_number=phone,
            full_name=full_name,
            password=password,
            role='employee'
        )
        login(request, user)
        messages.success(request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
        return redirect('profile')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, username=phone, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz!')
            return redirect('profile')
        else:
            messages.error(request, 'Telefon raqami yoki parol noto\'g\'ri')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
