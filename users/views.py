from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer
from users.permissions import IsOwnerOrReadOnly


class UserRegistrationView(generics.CreateAPIView):
    """ Generic - класс для создания (регистрации) нового пользователя """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    """ Generic - класс для вывода списка пользователей """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    """ Generic - класс для детального просмотра пользователя """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateView(generics.UpdateAPIView):
    """ Generic - класс для обновления (редактирования) пользователя """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserDeleteView(generics.DestroyAPIView):
    """ Generic - класс для удаления пользователя """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]
