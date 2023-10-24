from django.contrib.auth.models import AbstractUser
from django.db import models

from habits.models import NULLABLE


class User(AbstractUser):
    """ Модель для пользователей сервиса """

    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    chat_id = models.IntegerField(unique=True, verbose_name='tg chat id', **NULLABLE)
    telegram_user_name = models.CharField(max_length=150, unique=True, verbose_name='tg username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        """ Представление написания заголовков в админке """

        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
