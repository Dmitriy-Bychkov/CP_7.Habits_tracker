import requests
from django.conf import settings


def tg_get_updates(offset=None):
    """
    Отправляем GET-запрос к API Telegram с использованием метода getUpdates,
    чтобы получить список обновлений чата.
    Принимает необязательный параметр offset, который указывает на идентификатор обновления,
    начиная с которого нужно получить последующие обновления.
    Если offset не указан, будут получены все доступные обновления.
    """

    params = {}
    if offset is not None:
        params = {'offset': offset}
    response = requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getUpdates', params=params)
    return response.json()


def tg_send_message(chat_id, text):
    """
    Отправляет GET-запрос к API Telegram с использованием метода sendMessage,
    чтобы отправить текстовое сообщение в указанный чат.
    Принимает два параметра:
    chat_id, который указывает идентификатор чата пользователя, в который нужно отправить сообщение, и
    text, который содержит текст сообщения.
    """

    params = {'chat_id': chat_id, 'text': text}
    requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
