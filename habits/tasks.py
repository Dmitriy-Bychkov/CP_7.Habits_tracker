from datetime import timedelta
from django.utils import timezone
from habits.models import Habit
from users.services import tg_send_message
from celery import shared_task


@shared_task(name="send_habits_task")
def Re():
    """
    Задача для асинхронной отправки в телеграмм напоминания о выполнении действия,
    чтобы стать в будущем полезной привычкой
    """

    # получить текущее дату и время
    current_dt = timezone.now()
    # print(f'Текущее время: {current_dt}')

    for habit in Habit.objects.filter(is_pleasant=False):
        # print(f'Время следующей отправки: {habit.reminder_datetime()}')

        # текущее дата и время >= даты и времени привычки
        is_reminder_time = current_dt >= habit.reminder_datetime()
        # print(f'текущее дата и время >= даты и времени привычки?: {is_reminder_time}')

        # дата и время последнего уведомления < даты и времени напоминания
        is_last_notify = True
        if habit.last_reminder_time:
            is_last_notify = habit.last_reminder_time < habit.reminder_datetime()
        # print(f'дата и время последнего уведомления < даты и времени напоминания?: {is_last_notify}')

        # текущее дата и время - дата и время напоминания = меньше часа
        is_right_time = (current_dt - timedelta(hours=1)) < habit.reminder_datetime()
        # print(f'текущее дата и время - дата и время напоминания = меньше часа?: {is_right_time}')

        if all([is_reminder_time, is_last_notify, is_right_time]):
            # отправить уведомление
            if habit.award:
                # print('1) Привычка, Вознаграждение, Связанная привычка')
                # print(habit, habit.award, habit.link_pleasant.action)
                message = (
                    f"Напоминание от трекера привычек!\nДействие: {habit.action}\nМесто: {habit.place}"
                    f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {habit.award}")
                tg_send_message(habit.owner.chat_id, message)
            else:
                # print('2) Привычка, Вознаграждение, Связанная привычка')
                # print(habit, habit.award, habit.link_pleasant.action)
                message = (f"Напоминание от трекера привычек!\nДействие: {habit.action}\nМесто: {habit.place}"
                           f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {habit.link_pleasant.action}")
                tg_send_message(habit.owner.chat_id, message)

            # Обновляем время последней отправки напоминания
            habit.last_reminder_time = current_dt
            habit.save()
