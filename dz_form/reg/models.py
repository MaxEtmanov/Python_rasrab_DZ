from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Введите корректный номер телефона. Примеры: +71234567890 или 71234567890'
)

class CustomUser(AbstractUser):
    """
    Расширённая пользовательская модель.
    Добавлены: phone_number и bio.
    Наследуемся от AbstractUser — сохраняются username/email/password и т.д.
    """
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[phone_validator],
        help_text='Номер телефона в международном формате, необязательно.'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=1000,
        help_text='Короткая информация о пользователе (необязательно).'
    )

    def __str__(self):
        return self.get_username()

class Message(models.Model):
    name = models.CharField('Имя', max_length=150)
    email = models.EmailField('Email')
    text = models.TextField('Сообщение', max_length=500)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    def __str__(self):
        return f'{self.name} <{self.email}> — {self.created_at:%Y-%m-%d %H:%M}'