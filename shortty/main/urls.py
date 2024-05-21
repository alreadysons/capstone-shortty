from django.urls import path
from .views import main_view, login_view , signup_view,anonymous_login_view , chatPage , category_chat_view,logout_view,create_category_view

app_name = "main"
urlpatterns = [
    path('main/', main_view, name='main'),
    path('', login_view, name='login'),  # 로그인 뷰 
    path('signup/', signup_view, name='signup'), #회원가입 뷰
    path('logout/', logout_view, name='logout'),
    path('anonymous/', anonymous_login_view, name='anonymous_login'), # 익명 접속 뷰
    path("chat/",chatPage, name="chat"),
    path('chat/<int:category_id>/', category_chat_view, name='category_chat'),
    path('create/',create_category_view,name='create_category')
]
