from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config import settings
from users.forms import UserRegisterForm
from users.models import User
from django.http import HttpResponse
import random
import string


def generate_random_password(length=8):
    # Генерация случайного пароля из цифр и букв
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Поиск пользователя по email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Пользователь с таким email не найден.")

        # Генерация нового пароля
        new_password = generate_random_password()

        # Захешировать новый пароль и обновить пароль пользователя
        user.password = make_password(new_password)
        user.save()

        # Отправка нового пароля на email
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль: {new_password}'
        recipient_list = [email]

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )

        return HttpResponse("Новый пароль отправлен на вашу электронную почту.")

    return render(request, 'users/password_request.html')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()

        # Отправка электронного письма
        subject = 'Добро пожаловать на наш сайт!'
        message = f'Привет! Спасибо за регистрацию на нашем сайте.'
        recipient_list = [user.email]

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )

        return super().form_valid(form)

