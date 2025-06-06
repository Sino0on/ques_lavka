"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
from decouple import config
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!epamr8=185!uyy!^fvv_+cv1*$o1m#y2(53h379g&#4qdqg#r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(',')

ALLOWED_HOSTS = ['*']


# Application definition


PROJECT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DJANGO_APPS = [
    'authentication',
    'product',
    'mysite'
]

THIRD_PARTY_APPS = [
    "rest_framework",
    # "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    'ckeditor',
]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *PROJECT_APPS]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', cast=int),
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = "authentication.User"

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Bishkek"

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework.authentication.TokenAuthentication",
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ],
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
#     "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
#     "DEFAULT_RENDERER_CLASSES": [
#         "rest_framework.renderers.JSONRenderer",
#     ],
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.MultiPartParser',
#         'rest_framework.parsers.FormParser'
#     ),
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "TEST_REQUEST_DEFAULT_FORMAT": "json",
#     "DEFAULT_THROTTLE_RATES": {
#         "auth": '3/min',
#     }
# }
#
# if DEBUG:
#     REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append("rest_framework.authentication.BasicAuthentication")

# OpenAPI settings
#
# SPECTACULAR_SETTINGS = {
#     "TITLE": "Ques-Lavka OpenAPI",
#     "DESCRIPTION": "Описание нашего API в разработке...",
#     'COMPONENT_SPLIT_REQUEST': True,
#     "VERSION": "1.0.0",
#     "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
#     "SERVE_PERMISSIONS": ("rest_framework.permissions.IsAdminUser", ),
#     "SERVE_AUTHENTICATION": ('rest_framework.authentication.SessionAuthentication',
#                              'rest_framework.authentication.BasicAuthentication'),
#     "PREPROCESSING_HOOKS": ("openapi.preprocessors.get_urls_preprocessor",),
#     "SWAGGER_UI_SETTINGS": {
#         "docExpansion": "none",  # 'none' | 'list' | 'full'
#     },
#     "ENUM_NAME_OVERRIDES": {
#         "RatingsEnum": "apps.autoanswers.models.RatingChoices",
#         "CountMonthsEnum": "api.billing.serializers.PeriodChoices",
#     },
#     "SERVE_PERMISSIONS": ("rest_framework.permissions.AllowAny",)
# }
#
#
# SIMPLE_JWT = {
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
#     "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "UPDATE_LAST_LOGIN": True,
#     "ROTATE_REFRESH_TOKENS": True,
# }

# Email settings
EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
