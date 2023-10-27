from celery import shared_task

from users.models import User
from users.services import tg_get_updates, tg_send_message


@shared_task(name="get_tg_chat_id_task")
def get_tg_chat_id():
    """
    Задача на получение и обработку обновлений из Telegram,
    связывания chat_id пользователя с его профилем в базе данных и отправки
    приветственного сообщения пользователю, когда он отправляет "/start" в чат.
    """

    # Получаем данные об обновлениях из Telegram
    tg_data = tg_get_updates()

    # Если данные tg_data содержат успешный ответ (ok=True) и список результатов (result) не пустой
    # (тоесть пользователь ввел - /start),
    # выполняется цикл для каждого сообщения в tg_data['result'].
    if not tg_data['ok']:
        print("Ошибка получения обновлений")
        return

    for data_dict in tg_data['result']:
        username = data_dict["message"]["chat"]["username"]
        chat_id = data_dict['message']['chat']['id']

        if data_dict['message']['text'] == "/start":
            try:
                user = User.objects.get(telegram_user_name=username)
            except User.DoesNotExist:
                text = 'Давай досвидания! Тебя нет в нашей базе!'
                tg_send_message(chat_id, text)

                # Очищаем все обновления чата
                tg_get_updates(data_dict['update_id'] + 1)
                continue

            # Присваиваем пользователю его chat_id
            if not user.chat_id:
                user.chat_id = chat_id
                user.save()

            text = 'Добро пожаловать!\nСюда будут приходить напоминания о ваших привычках!'
            tg_send_message(chat_id, text)

            # Очищаем все обновления чата
            tg_get_updates(data_dict['update_id'] + 1)

        elif data_dict['message']['text'] == "/stop":
            try:
                user = User.objects.get(telegram_user_name=username)
            except User.DoesNotExist:
                text = 'Пользователь не найден!'
                tg_send_message(chat_id, text)

                # Очищаем все обновления чата
                tg_get_updates(data_dict['update_id'] + 1)
                continue

            text = 'Нам очень жаль, что вы решили отписаться от уведомлений:(\nРассылка остановлена!'
            tg_send_message(chat_id, text)
            user.chat_id = None
            user.save()

            # Очищаем все обновления чата
            tg_get_updates(data_dict['update_id'] + 1)
