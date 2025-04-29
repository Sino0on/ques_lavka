import datetime
import random

from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from authentication.serializers import CodeResetPasswordSerializer, ResetPasswordConfirmSerializer, \
    UserRegisterSerializer, UserGetSerializer, ActivateUserSerializer, \
    EmailCheckSerializer, PasswordCheckSerializer, CustomTokenObtainSerializer, PasswordResetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_str as force_text
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from authentication.utils import send_sms_code, send_sms_code_for_reset
from django.utils.translation import gettext as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        refresh = super().get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data


@extend_schema_view(
    post=extend_schema(
        description=_('URL для проверки правильности пароли'),
        summary=_('Проверить пароли'),
    ),
)
class PasswordCheckView(APIView):
    serializer_class = PasswordCheckSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        description=_('URL для проверки существующего почты'),
        summary=_('Проверить почту'),
    ),
)
class EmailCheckView(APIView):
    serializer_class = EmailCheckSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = User.objects.filter(email=email)
            if user.exists():
                return Response({'email': _("Пользователь с такой почтой уже существует")},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'email': "OK"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterApiView(APIView):
    """Регистрация пользователя"""

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        phone = serializer.validated_data.get("phone")
        raw_password = serializer.validated_data.get("password1")
        email = serializer.validated_data.get("email")

        # code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])

        user = User.objects.filter(email=email)

        if user.exists():
            user = user.first()
            # user.code = urlsafe_base64_encode(force_bytes(code))
            # user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        else:
            user = User(
                phone=phone,
                # is_confirm=False,
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
                # code=urlsafe_base64_encode(force_bytes(code)),
                # last_sms_date=datetime.datetime.now(datetime.timezone.utc),
            )

        user.set_password(raw_password)
        user.save()
        # cabinet = Cabinet.objects.create(user=user)
        # send_sms_code(email, code)
        das = MyTokenObtainPairSerializer()
        tokens = das.get_token(user=user)
        data = {
            'user': UserGetSerializer(user).data,
            "tokens": tokens
        }
        return Response(data, status=status.HTTP_200_OK)


class UserActivateApiView(APIView):
    """Активация пользователя"""

    serializer_class = ActivateUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, code):

        serializer = ActivateUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")

        user = get_object_or_404(User, email=email)

        if not code == force_text(urlsafe_base64_decode(user.code)):
            return Response(
                {"detail": _("Вы ввели неверный код.")}, status=status.HTTP_404_NOT_FOUND
            )

        user.is_confirm = True

        user.save()

        return Response(
            {"detail": _("Пользователь был успешно активирован.")},
            status=status.HTTP_200_OK,
        )


class SendSMSAgainApiView(APIView):
    """Отправка SMS сообщения и обновление кода у user-а"""

    serializer_class = None
    permission_classes = (AllowAny,)

    @extend_schema(parameters=[
        OpenApiParameter(name="email", type=str, description='email'),
    ])
    def get(self, request):
        email = request.GET.get("email")

        if not email:
            return Response(
                {"detail": _("Необходимо указать ?email= в query параметре.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])

        user = get_object_or_404(User, email=email)
        user.code = urlsafe_base64_encode(force_bytes(code))
        user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        user.save()
        if user.is_confirm:
            send_sms_code_for_reset(email, code)
        else:
            send_sms_code(email, code)

        return Response(UserGetSerializer(user).data, status=status.HTTP_200_OK)


class GetMeApiView(APIView):
    """Позволяет пользователю получить информацию о себе"""
    serializer_class = UserGetSerializer

    def get(self, request):
        user = self.request.user

        return Response(
            {
                "user": UserGetSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordApiView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
                user.code = urlsafe_base64_encode(force_bytes(code))
                user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)

                user.save()
                if user.is_confirm:
                    send_sms_code_for_reset(email, code)
                else:
                    send_sms_code(email, code)

                return Response(UserGetSerializer(user).data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': _('Если аккаунт с такой почтой существует, на почту будет отправлен код')},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeResetPasswordApiView(APIView):
    """ Активация полученного кода"""
    serializer_class = CodeResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        code = serializer.validated_data.get("code")
        email = serializer.validated_data.get("email")
        encoded = urlsafe_base64_encode(force_bytes(code))
        print("code: ", encoded)
        print("email: ", email)

        user = User.objects.filter(email=email, code=encoded)
        print(user.exists())
        if not user.exists():
            return Response(
                {"detail": _("Вы ввели неверный код.")}, status=status.HTTP_404_NOT_FOUND
            )
        user = user.first()
        user.is_confirm = True
        user.save()

        token = MyTokenObtainPairSerializer()
        tokens = token.get_token(user=user)
        data = {
            "tokens": tokens,
            "message": _("Код активирован")
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmApiView(APIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            # Использование токена для идентификации пользователя
            user = request.user
            if not user:
                return Response({"detail": _("Неверный токен")}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": _("Пароль успешно изменен")}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)