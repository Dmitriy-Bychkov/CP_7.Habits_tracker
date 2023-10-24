from django.contrib import admin
from users.models import User

# Регистрация пользователей в админке (появляется соответствующее меню)
admin.site.register(User)
