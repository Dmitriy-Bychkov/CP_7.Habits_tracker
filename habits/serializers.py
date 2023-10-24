from rest_framework import serializers
from habits.models import Habit
from habits.validators import DurationValidator, AwardValidator, PleasantHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели привычки """

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [DurationValidator(field='duration'), AwardValidator(is_pleasant='is_pleasant', award='award',
                                                                          link_pleasant='link_pleasant'),
                      PleasantHabitValidator(field='link_pleasant')]
