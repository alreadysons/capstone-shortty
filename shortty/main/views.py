from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Message, Category
import hashlib
import datetime

# 메인 페이지 뷰
def main_view(request):
    return render(request, 'main/main.html')  # 경로 수정이 필요할 수 있습니다.

# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:main')  # 로그인 성공 시 메인 페이지로 이동
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원 가입 후 자동 로그인
            return redirect('main:main')  # 성공적인 가입 후 메인 페이지로 리다이렉션
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

# 익명 로그인 뷰
def anonymous_login_view(request):
    ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    raw_id = f'{ip_address}-{now}'
    hashed_id = hashlib.sha256(raw_id.encode()).hexdigest()[:8]
    request.session['anonymous_id'] = f'익명{hashed_id}'
    return redirect('main:main')

# 채팅 페이지 뷰
def chatPage(request, *args, **kwargs):
    messages = Message.objects.all().order_by('timestamp')[50:]  # 최근 50개 메시지만 표시
    categories = Category.objects.all().order_by('name')
    context = {
        'username': request.session.get('anonymous_id', 'Guest') if not request.user.is_authenticated else request.user.username,
        'messages': messages,
        'categories': categories
    }
    return render(request, "main/chat.html", context)

# 카테고리 별 채팅 페이지 뷰
def category_chat_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    messages = Message.objects.filter(category=category).order_by('timestamp')
    return render(request, 'main/category_chat.html', {'category': category, 'messages': messages})
