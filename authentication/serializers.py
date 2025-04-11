from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _("Неправильный логин или пароль")
    }


class PasswordCheckSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate_password2(self, password2):
        if self.initial_data.get("password1") != password2:
            raise serializers.ValidationError(_("Пароли не совпадают."))

        return password2

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password1 = serializers.CharField()
    email = serializers.EmailField()

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1

    def validate_email(self, email):
        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError(
                _("Пользователь с такой почтой уже зарегистрирован.")
            )
        return email

    def validate_phone(self, phone):
        if User.objects.filter(phone=phone, is_active=True).exists():
            raise serializers.ValidationError(
                _("Пользователь с таким номером телефона уже зарегистрирован.")
            )
        return phone

    class Meta:
        model = User
        fields = ("phone", "password1", 'email', 'first_name', 'last_name')


class ActivateUserSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Проверка введенного email в базе данных.
        """
        try:

            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Почты не существует!"))
        return value


class CodeResetPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    email = serializers.EmailField()

    def validate_code(self, value):
        """
        Проверять код на шестизначность чисел
        """
        if len(str(value)) != 6 or value < 0:
            raise serializers.ValidationError(_('Код должен быть шестизначным!'))
        return value


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, new_password):
        if not validate_password(new_password):
            return new_password

class UserGetSerializer(serializers.ModelSerializer):
    # user_cabinet = CabinetSerializer(source='cabinet')

    class Meta:
        model = User
        # include = ('user_cabinet',)
        exclude = (
            "last_login",
            "date_joined",
            "patronymic",
            "password",
            "last_sms_date",
            "is_superuser",
            "is_staff",
            "is_active",
            "username",
            "groups",
            "user_permissions",
            "code",
        )
