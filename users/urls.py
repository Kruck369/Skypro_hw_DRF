from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('users/update/<int:pk>', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
