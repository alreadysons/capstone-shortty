from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  

# Create your views here.
def main_view(request):
    return render(request, 'main/main.html')  # 경로 수정이 필요할 수 있습니다.

def login_view(request):  # 로그인
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:main')  # 로그인 성공 시 main으로 이동
            else:
                messages.error(request, "Invalid username or password.")  
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form}) 

def signup_view(request): # 회원가입
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원 가입 후 자동 로그인
            return redirect('main:main')  # 성공적인 가입 후 리다이렉션
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})