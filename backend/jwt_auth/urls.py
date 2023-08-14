from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    UserAPIView,
    UserAPICreateView,
    UserAPIUpdateView,
    UserAPIDeleteView,
    LoginOTPView,
    ValidateOTPView,
)

urlpatterns = [
    path("user/<int:pk>", UserAPIView.as_view()),
    path("user/update/<int:pk>", UserAPIUpdateView.as_view()),
    path("user/delete/<int:pk>", UserAPIDeleteView.as_view()),
    path("user/create/", UserAPICreateView.as_view()),
    path('login/', LoginOTPView.as_view()),
    path('validate/', ValidateOTPView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]