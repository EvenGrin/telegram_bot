from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import User
from django.conf import settings
import requests

BOT_TOKEN = settings.BOT_TOKEN


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'bot/index.html')


def add_user(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        full_name = request.POST.get('full_name')
        if telegram_id and full_name:
            try:
                User.objects.create(telegram_id=telegram_id, full_name=full_name)
                return redirect('users_list')
            except:
                return render(request, 'bot/add_user.html', {'error': 'Пользователь с таким ID уже существует'})
        else:
            return render(request, 'bot/add_user.html', {'error': 'Введите Telegram ID и ФИО'})
    else:
        return render(request, 'bot/add_user.html')


def users_list(request):
    users = User.objects.all()
    return render(request, 'bot/users_list.html', {'users': users})


def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        code = request.POST.get('code')
        if code == '123':  # Замените на ваш секретный код
            users = User.objects.all()
            for user in users:
                send_telegram_message(user.telegram_id, message)
            return redirect('index')
        else:
            return render(request, 'bot/send_message.html', {'error': 'Неверный код'})
    else:
        return render(request, 'bot/send_message.html')


def send_telegram_message(chat_id, message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    print(response.json())
    return response.json()

