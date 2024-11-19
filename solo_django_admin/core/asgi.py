import os

from django.core.asgi import get_asgi_application

import dotenv

dotenv.load_dotenv()

ENV_PREFIX = os.getenv('ENV_PREFIX', 'DJANGO_ADMIN')

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          os.getenv(f"{ENV_PREFIX}_DJANGO_SETTINGS_MODULE",
                                    'solo_django_admin.core.settings'))
application = get_asgi_application()
