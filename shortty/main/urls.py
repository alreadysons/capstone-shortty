from django.urls import path
from .views import main_view, login_view , signup_view,anonymous_login_view

app_name = "main"
urlpatterns = [
    path('main/', main_view, name='main'),
    path('', login_view, name='login'),  # 로그인 뷰 
    path('signup/', signup_view, name='signup'), #회원가입 뷰
    path('anonymous/', anonymous_login_view, name='anonymous_login'), # 익명 접속 뷰
]
