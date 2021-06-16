from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterView.as_view(), name='homepage'),
    path('chat/<str:room_name>/', views.index, name='userchat'),
    path('chat/', views.admin_chat, name='adminchat')
]
