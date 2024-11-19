from solo_django_admin.core.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv(f'{ENV_PREFIX}_DB_NAME'),
        'USER': os.getenv(f'{ENV_PREFIX}_DB_USER'),
        'PASSWORD': os.getenv(f'{ENV_PREFIX}_DB_PASSWORD'),
        'HOST': os.getenv(f'{ENV_PREFIX}_DB_HOST'),
        'PORT': os.getenv(f'{ENV_PREFIX}_DB_PORT', default=5432)
    }
}
INSTALLED_APPS.append('django_app')
