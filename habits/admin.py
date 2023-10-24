from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Представление раздела - "Привычки" в админке"""

    list_display = ('owner', 'place', 'action',)
    search_fields = ('owner', 'place', 'action',)
