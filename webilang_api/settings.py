import os
from pathlib import Path
import settings
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-ofa%tpy60+)w4bz_ldq)3*x-wwig)=mp$k8(l^w!cl0z_3pw29'

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'user.User'
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'info@webilang.com'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SERIALIZER = 'json'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'log_formatter':{
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'django_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'log_formatter'
        },
        'users_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'users.log',
            'formatter': 'log_formatter'
        },

    },
    'loggers': {
        'django': { # <-- must have one django
            'handlers': ['django_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'user': {
            'handlers': ['users_log'],
            'level': 'INFO',
            'propagate': True,
        },

    },
}

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_cleanup',

    'djoser',
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',

    'user',
    'data',
    'group',
    'lesson',
    'chat',
]

ASGI_APPLICATION = "webilang_api.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user.middleware.Process500'
]

ROOT_URLCONF = 'webilang_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webilang_api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = f'/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),

}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user_create': 'user.serializers.UserCreateSerializer',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'