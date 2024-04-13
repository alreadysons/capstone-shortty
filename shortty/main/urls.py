from django.urls import path
from .views import main_view, login_view , signup_view

app_name = "main"
urlpatterns = [
    path('main/', main_view, name='main'),
    path('', login_view, name='login'),  # 로그인 뷰 
        path('signup/', signup_view, name='signup'),
]
