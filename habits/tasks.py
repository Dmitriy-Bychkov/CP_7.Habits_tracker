from datetime import datetime, timedelta
from habits.models import Habit
from users.services import tg_send_message
from celery import shared_task


# @shared_task(name="send_habits")
# def send_habits():
#     """
#     Задача для асинхронной отправки в телеграмм напоминания о выполнении действия,
#     чтобы стать в будущем полезной прывычкой
#     """
#
#     current_time = datetime.now()
#     today = datetime.today().strftime('%A')
#     for habit in Habit.objects.filter(is_pleasant=False):
#         if habit.frequency == "Daily" or habit.frequency == today:
#             if habit.time.strftime("%H:%M") == current_time.strftime("%H:%M"):
#                 chat_id = habit.owner.chat_id
#                 if habit.award:
#                     users_award = habit.award
#                     message = (
#                         f"Напоминание от трекера привычек!\nДействие: {habit.action}\nМесто: {habit.place}"
#                         f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {users_award}")
#                     tg_send_message(chat_id, message)
#                 else:
#                     users_award = habit.link_pleasant
#                     message = (f"Напоминание от трекера привычек!\nДействие: {habit.action}\nМесто: {habit.place}"
#                                f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {users_award}")
#                     tg_send_message(chat_id, message)
#
#
# @shared_task(name="send_habits_test")
# def send_habits_test():
#     """
#     Задача для асинхронной отправки в телеграмм напоминания о выполнении действия,
#     чтобы стать в будущем полезной прывычкой
#     """
#
#     for habit in Habit.objects.filter(is_pleasant=False):
#
#         chat_id = habit.owner.chat_id
#         if habit.award:
#             users_award = habit.award
#         else:
#             users_award = habit.link_pleasant
#
#         message = (f"Напоминание от трекера полезных привычек.\nДействие: {habit.action}\nМесто: {habit.place}"
#                    f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {users_award}")
#         tg_send_message(chat_id, message)

@shared_task(name="send_habits")
def send_habits():
    """
    Задача для асинхронной отправки в телеграмм напоминания о выполнении действия,
    чтобы стать в будущем полезной привычкой
    """
    current_time = datetime.now().time()
    today = datetime.today().strftime('%A')
    for habit in Habit.objects.filter(is_pleasant=False):
        if habit.frequency == "Daily" or habit.frequency == today.lower():
            habit_time = habit.time
            if is_time_matches(current_time, habit_time):
                chat_id = habit.owner.chat_id
                last_reminder_time = habit.last_reminder_time
                if last_reminder_time is None or (current_time - last_reminder_time) >= timedelta(days=1):
                    if habit.award:
                        users_award = habit.award
                        message = (
                            f"Напоминание от трекера привычек!\nДействие: {habit.action}\nМесто: {habit.place}"
                            f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {users_award}")
                        tg_send_message(chat_id, message)
                    else:
                        users_award = habit.link_pleasant
                        message = (f"Напоминание от трекера привычек!\nДействие: {habit.action}\nМесто: {habit.place}"
                                   f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {users_award}")
                        tg_send_message(chat_id, message)
                    # Обновляем время последней отправки напоминания
                    habit.last_reminder_time = current_time
                    habit.save()


def is_time_matches(current_time, habit_time):
    """
    Проверяет, соответствует ли текущее время указанному времени выполнения привычки
    """
    return current_time == habit_time
