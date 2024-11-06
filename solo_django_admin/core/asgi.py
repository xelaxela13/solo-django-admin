import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'solo_django_admin.core.settings')
application = get_asgi_application()
