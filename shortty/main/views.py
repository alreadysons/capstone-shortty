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

import random
from django.shortcuts import redirect

import hashlib
import datetime
from django.shortcuts import redirect

def anonymous_login_view(request):
    # IP 주소 얻기
    ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')  
    # 현재 시각을 문자열로 변환
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # IP 주소와 현재 시각을 결합
    raw_id = f'{ip_address}-{now}'
    # 해시 함수를 사용하여 ID 생성
    hashed_id = hashlib.sha256(raw_id.encode()).hexdigest()[:8]  # 해시 후 첫 8자리만 사용
    # 세션에 저장
    request.session['anonymous_id'] = f'익명{hashed_id}'
    return redirect('main:main')  # 리다이렉션
