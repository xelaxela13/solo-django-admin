import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PREFIX = os.getenv('ENV_PREFIX', 'DJANGO_ADMIN')

SECRET_KEY = 'django-insecure-_knbo^o96om89at7qx#+1ff^&a2-9$91p24djt2!nnzn64v*!6'

DEBUG = os.getenv(f'{ENV_PREFIX}_DEBUG', False)

ALLOWED_HOSTS = os.getenv(f'{ENV_PREFIX}_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'solo_django_admin.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

ASGI_APPLICATION = 'solo_django_admin.core.asgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = os.getenv(f'{ENV_PREFIX}_STATIC_URL', '/django-admin-static/')
STATIC_ROOT = os.getenv(f'{ENV_PREFIX}_STATIC_ROOT',
                        os.path.join(BASE_DIR, 'django_admin_static_files'))
MEDIA_URL = os.getenv(f'{ENV_PREFIX}_MEDIA_URL', '/django-admin-media/')
MEDIA_ROOT = os.getenv(f'{ENV_PREFIX}_MEDIA_ROOT',
                       os.path.join(BASE_DIR, 'django_admin_media_files'))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
