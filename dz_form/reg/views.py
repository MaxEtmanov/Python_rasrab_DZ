from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, MessageForm
from .models import Message

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логиним
            messages.success(request, 'Регистрация прошла успешно. Вы вошли в систему.')
            # перенаправляем на отправку сообщений
            return redirect('reg:send_message')
    else:
        form = RegistrationForm()
    return render(request, 'reg/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Успешно вошли в систему.')
                # перенаправляем на отправку сообщений
                return redirect('reg:send_message')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'reg/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('reg:login')


def send_message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение успешно отправлено.')
            return redirect('reg:send_message')
    else:
        form = MessageForm()
    return render(request, 'reg/send_message.html', {'form': form})


@login_required
def home_view(request):
    # Показываем сообщения, привязанные к email пользователя
    user_messages = Message.objects.filter(email=request.user.email) if request.user.email else []
    return render(request, 'reg/home.html', {'user_messages': user_messages})