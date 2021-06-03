from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .forms import RegisterForm
import json
from django.utils.safestring import mark_safe


class RegisterView(View):
    """Вносим в БД пользователя"""

    def get(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            form.save()
            return render(request, 'register.html', {'form': form})
        return HttpResponse('Error')


def index(request, room_name):
    """Страница чата"""
    """Комната для чата в форме http://127.0.0.1:8000/chat/s/"""
    context = {'room_name_json': mark_safe(json.dumps(room_name))}
    return render(request, 'userchat.html', context)