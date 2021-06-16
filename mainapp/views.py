from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .forms import RegisterForm
from .models import Messengers
import json
from django.utils.safestring import mark_safe
from .consumers import ChatConsumer


class RegisterView(View):
    """Вносим в БД пользователя"""

    def get(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        context = {'form': form}
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            form = form.save(commit=False)
            if "telegram" in request.POST:
                messenger = Messengers.objects.get(pk=1)
            elif "viber" in request.POST:
                messenger = Messengers.objects.get(pk=2)
            elif "messenger" in request.POST:
                messenger = Messengers.objects.get(pk=3)
            form.messenger = messenger
            form.save()
            form = RegisterForm()
        return render(request, 'index.html', {'form': form})



def admin_chat(request):
    """Отправляю ссвлку на чат и последнее сообщение"""
    # rooms = ChatConsumer.rooms
    room_names = {}
    # for room in rooms:
    #     room_names[room] = rooms[room]["log"]
    context = {'rooms': room_names}
    return render(request, 'adminchat.html', context)
