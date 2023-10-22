import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings
from users.models import User
from habits.models import Habit
from users.services import tg_get_updates, tg_send_message


class HabitTestCase(APITestCase):
    """ Тестирование CRUD модели привычек - Habit """

    def setUp(self):
        """ Основные тестовые настройки для временной БД, создание экземпляров моделеи """

        self.user = User.objects.create(
            email='user@test.ru',
            telegram_user_name='user',
            password='1234',
            is_staff=False,
            is_active=True
        )
        self.token = f'Bearer {AccessToken.for_user(self.user)}'

        self.habit = Habit.objects.create(
            place='at home',
            time='06:00:00',
            action='wake up early',
            is_pleasant=False,
            link_pleasant=None,
            frequency='Daily',
            award='eat a candy',
            duration=30,
            is_public=True,
            last_reminder_time=None,
            owner=self.user
        )

    def test_create_habit(self):
        """ Тестирование создания привычки """

        expected_data = {
            "place": "in the office",
            "time": "15:20",
            "action": "time to relax",
            "is_pleasant": False,
            "link_pleasant": '',
            "frequency": "Tuesday",
            "award": "eat a mango",
            "duration": 120,
            "is_public": False,
            "last_reminder_time": '',
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_view_habits_list(self):
        """ Тестирование вывода списка привычек """

        response = self.client.get(
            reverse('habits:habit_list'),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.pk,
                        "place": self.habit.place,
                        "time": self.habit.time,
                        "action": self.habit.action,
                        "is_pleasant": self.habit.is_pleasant,
                        "link_pleasant": self.habit.link_pleasant,
                        "frequency": self.habit.frequency,
                        "award": self.habit.award,
                        "duration": self.habit.duration,
                        "is_public": self.habit.is_public,
                        "last_reminder_time": self.habit.last_reminder_time,
                        "owner": self.user.pk
                    }]}
        )

    def test_view_habit_detail(self):
        """ Тестирование вывода отдельной привычки """

        response = self.client.get(
            reverse('habits:habit_detail', kwargs={'pk': self.habit.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk,
                "place": self.habit.place,
                "time": self.habit.time,
                "action": self.habit.action,
                "is_pleasant": self.habit.is_pleasant,
                "link_pleasant": self.habit.link_pleasant,
                "frequency": self.habit.frequency,
                "award": self.habit.award,
                "duration": self.habit.duration,
                "is_public": self.habit.is_public,
                "last_reminder_time": self.habit.last_reminder_time,
                "owner": self.user.pk
            }
        )

    def test_update_habit(self):
        """ Тестирование изменения привычки """

        expected_data = {
            'place': 'outside',
            'action': 'walking',
            'duration': 45,
            'award': 'watching TV-series',
            'is_public': True
        }

        response = self.client.put(
            reverse('habits:habit_update', kwargs={'pk': self.habit.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk,
                "place": 'outside',
                "time": self.habit.time,
                "action": 'walking',
                "is_pleasant": self.habit.is_pleasant,
                "link_pleasant": self.habit.link_pleasant,
                "frequency": self.habit.frequency,
                "award": 'watching TV-series',
                "duration": 45,
                "is_public": self.habit.is_public,
                "last_reminder_time": self.habit.last_reminder_time,
                "owner": self.user.pk
            }
        )

    def test_delete_habit(self):
        """ Тестирование удаления привычки """

        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': self.habit.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Habit.objects.all()),
            []
        )

    def test_view_habits_public_list(self):
        """ Тестирование вывода списка публичных привычек """

        response = self.client.get(
            reverse('habits:public_habit_list'),
            HTTP_AUTHORIZATION=self.token

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{
                "id": self.habit.pk,
                "place": self.habit.place,
                "time": self.habit.time,
                "action": self.habit.action,
                "is_pleasant": self.habit.is_pleasant,
                "link_pleasant": self.habit.link_pleasant,
                "frequency": self.habit.frequency,
                "award": self.habit.award,
                "duration": self.habit.duration,
                "is_public": self.habit.is_public,
                "last_reminder_time": self.habit.last_reminder_time,
                "owner": self.user.pk
            }]
        )


class TelegramServiceTests(TestCase):
    """ Тестирование сервисных функций - подключение к телеграмм по АПИ """

    @patch('requests.get')
    def test_tg_get_updates(self, mock_get):
        """ Тестирование получения обновлений от телеграм """

        # Устанавливаем ожидаемый ответ от API Telegram
        expected_response = {
            'ok': True,
            'result': [
                {'update_id': 1, 'message': {'text': 'Hello', 'chat': {'id': 123}}}
            ]
        }
        mock_get.return_value.json.return_value = expected_response

        # Вызываем функцию tg_get_updates
        response = tg_get_updates(offset=0)

        # Проверяем, что функция отправила GET-запрос к правильному URL
        mock_get.assert_called_once_with(
            f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getUpdates',
            params={'offset': 0}
        )

        # Проверяем, что функция вернула ожидаемый результат
        self.assertEqual(response, expected_response)

    @patch('requests.get')
    def test_tg_send_message(self, mock_get):
        """ Тестирование отправки сообщения боту """

        # Вызываем функцию tg_send_message
        tg_send_message(chat_id=123, text='Hello')

        # Проверяем, что функция отправила GET-запрос к правильному URL с правильными параметрами
        mock_get.assert_called_once_with(
            f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
            params={'chat_id': 123, 'text': 'Hello'}
        )


class CreateUserCommandTest(TestCase):
    """ Тестирование команды на создание пользователя в системе """

    def test_create_user_command(self):
        # Предварительно удаляем существующих пользователей, чтобы убедиться, что команда создает нового пользователя
        User.objects.all().delete()

        # Вызываем команду создания пользователя
        out = StringIO()
        call_command('csu', stdout=out)

        # Проверяем, что команда не выдала ошибок
        self.assertEqual(out.getvalue(), '')

        # Проверяем, что пользователь был создан
        user = User.objects.first()
        self.assertIsNotNone(user)

        # Проверяем значения полей пользователя
        self.assertEqual(user.email, 'admin@habits-tracker.com')
        self.assertEqual(user.first_name, 'Admin')
        self.assertEqual(user.last_name, 'Dmitriy')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(os.getenv('SUPERUSER_PASSWORD')))
