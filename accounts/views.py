from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   # <-- اضافه کن
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Profile

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ایجاد پروفایل بلافاصله بعد از ثبت نام
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'ثبت نام موفق! حالا وارد شوید.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    # اگر کاربر وارد شده، برگرد به صفحه اصلی
    if request.user.is_authenticated:
        return redirect('/')

    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')

    return render(request, 'accounts/login.html', {'next': next_url})

@login_required(login_url='login')
def profile(request):
    # اگر profile وجود نداشت بساز
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل شما آپدیت شد!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

def logout_view(request):
    logout(request)
    return redirect('/')