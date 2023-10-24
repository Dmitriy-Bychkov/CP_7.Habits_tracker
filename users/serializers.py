from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели пользователей """

    class Meta:
        model = User
        fields = ["id", "email", "telegram_user_name"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """ Сериализотор для создания пользователя """

    # Доп. атрибут для подтверждения пароля пользователя
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'telegram_user_name', 'password', 'password2']

    def save(self, *args, **kwargs):
        """ Переопределяем стандартный метод сохранения модели """

        user = User(
            email=self.validated_data['email'],
            telegram_user_name=self.validated_data['telegram_user_name'],
            is_superuser=False,
            is_staff=False,
            is_active=True
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароли не совпадают"})
        user.set_password(password)
        user.save()
        return user
