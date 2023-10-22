from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserRegistrationView, UserListView, UserDetailView, UserUpdateView, UserDeleteView

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name='user_registration'),
    path("list/", UserListView.as_view(), name='user_list'),
    path("detail/<int:pk>/", UserDetailView.as_view(), name='user_detail'),
    path("update/<int:pk>/", UserUpdateView.as_view(), name='user_update'),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name='user_delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]