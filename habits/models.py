from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """ Модель привычки - поля в базе данных """

    class Frequency(models.TextChoices):
        """ Класс частотности у привычки """

        daily = 'Daily'
        monday = 'Monday'
        tuesday = 'Tuesday'
        wednesday = 'Wednesday'
        thursday = 'Thursday'
        friday = 'Friday'
        saturday = 'Saturday'
        sunday = 'Sunday'

    place = models.CharField(max_length=100, verbose_name='место выполнения задачи')
    time = models.TimeField(default='12:00', verbose_name='время начала выполнения задачи')
    action = models.CharField(max_length=100, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    link_pleasant = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='связанная привычка', **NULLABLE)
    frequency = models.CharField(choices=Frequency.choices, default=Frequency.daily, verbose_name='периодичность')
    award = models.CharField(max_length=100, verbose_name='вознаграждение', **NULLABLE)
    duration = models.IntegerField(verbose_name='продолжительность выполнения', **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name='признак публичной привычки')
    last_reminder_time = models.DateTimeField(verbose_name='время последней отправки', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец привычки',
                              **NULLABLE)

    def __str__(self):
        return f'{self.owner} - {self.action}'

    class Meta:
        """ Представление написания заголовков для привычки в админке """

        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
