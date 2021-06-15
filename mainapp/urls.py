from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.RegisterView.as_view(), name='userchat'),
    path('chat/', views.admin_chat, name='adminchat')
]
