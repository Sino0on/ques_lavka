from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from authentication.views import (UserRegisterApiView, UserActivateApiView, SendSMSAgainApiView,
                                      GetMeApiView, EmailCheckView, PasswordCheckView, CustomTokenObtainView,
                                      ResetPasswordApiView, ResetPasswordConfirmApiView, CodeResetPasswordApiView)

urlpatterns = [
    path("token/", CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("users/me/", GetMeApiView.as_view()),
    path("users/check-email/", EmailCheckView.as_view()),
    path("users/check-passwords/", PasswordCheckView.as_view()),

    path("users/register/", UserRegisterApiView.as_view()),
    # path("users/register/activation/<str:code>/", UserActivateApiView.as_view()),
    # path("users/register/send-sms-again/", SendSMSAgainApiView.as_view()),

    path("users/reset/password/", ResetPasswordApiView.as_view()),
    path("users/reset/code/confirm/", CodeResetPasswordApiView.as_view()),
    path("users/reset/password/confirm/", ResetPasswordConfirmApiView.as_view())
]