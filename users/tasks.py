from celery import shared_task

from users.models import User
from users.services import tg_get_updates, tg_send_message


@shared_task(name="get_tg_chat_id")
def get_tg_chat_id():
    """
    Задача на получение и обработку обновлений из Telegram,
    связывания chat_id пользователя с его профилем в базе данных и отправки
    приветственного сообщения пользователю, когда он отправляет "/start" в чат.
    """

    # Получаем данные об обновлениях из Telegram
    tg_data = tg_get_updates()
    # Получаем пользователей у которых поле chat_id не задано
    users = User.objects.filter(chat_id=None)

    # Если данные tg_data содержат успешный ответ (ok=True) и список результатов (result) не пустой,
    # выполняется цикл для каждого сообщения в tg_data['result'].
    if tg_data['ok'] and tg_data['result'] != []:
        for data_dict in tg_data['result']:
            if data_dict['message']['text'] == "/start":
                for user in users:
                    # Проверка на совпадение имени-username в Телеграмм с имененм в модели пользователя
                    if user.telegram_user_name.lower() == data_dict['message']['from']['username'].lower():
                        # Если проверка совпадения прошла, тогда вытаскиваем chat_id из данных и присваеваем его пользователю
                        chat_id = data_dict['message']['from']['id']
                        user.chat_id = chat_id
                        user.save()

                        # Выполненние функции с message['update_id'] для удаления обработанного обновления.
                        tg_get_updates(data_dict['update_id'])

                        # Отправляется сообщение пользователю с приветственным текстом
                        text = f'Добро пожаловать!\nСюда будут приходить напоминания о ваших привычках!'
                        tg_send_message(user.chat_id, text)

            # Выполненние функции с message['update_id'] для удаления обработанного обновления.
            tg_get_updates(data_dict['update_id'])
