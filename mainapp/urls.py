from django.urls import path
from .views import RegisterView, index

urlpatterns = [
    path('', RegisterView.as_view(), name='homepage'),
    path('chat/<str:room_name>/', index, name='userchat')
]
