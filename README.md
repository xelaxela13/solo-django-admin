# solo-django-admin
## Django admin for non Django ORM

For now support only Tortoise ORM 

https://github.com/tortoise/tortoise-orm 

### Install
```
pip install solo-django-admin
```
### Config
1. Create settings.py file and redefine DATABASES if needed because by default db engine is 'django.db.backends.sqlite3'
```
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
INSTALLED_APPS.append('YOR_APP_NAME')
```
2. Create .env and/or set environments variables if needed, all values are optional
```
ENV_PREFIX=DJANGO_ADMIN  # by default
DJANGO_ADMIN_DEBUG=True  # default False
DJANGO_ADMIN_DJANGO_SETTINGS_MODULE=path_to_settings_file
DJANGO_ADMIN_DB_USER=postgres
DJANGO_ADMIN_DB_NAME=postgres
DJANGO_ADMIN_DB_HOST=localhost
DJANGO_ADMIN_DB_PASSWORD=postgres
DJANGO_ADMIN_DB_PORT=5432
DJANGO_ADMIN_STATIC_URL=/django-admin-static/  # by default
DJANGO_ADMIN_STATIC_ROOT=path_to_static_files
DJANGO_ADMIN_MEDIA_URL=/django-admin-media/  # by default
DJANGO_ADMIN_MEDIA_ROOT=path_to_media_files
DJANGO_ADMIN_ALLOWED_HOSTS=* # by default (example: https://site.com,localhost)
```
3. Collect static
```
python -m solo_django_admin.manage collectstatic --settings=path_to_settings
```
4. Migrate database

Attention! the following tables will be created in the database, they are necessary for the operation of the Django admin panel
```
auth_group
auth_group_permissions
auth_permission
auth_user
auth_user_groups
auth_user_user_permissions
django_admin_log
django_content_type
django_migrations
django_session
```
5. Create superuser
```
python -m solo_django_admin.manage createsuperuser
```
6. Start app

Adding models to the admin panel is no different from Django, but adding models is a little different

create your own app, for example `mappers`
```
python -m solo_django_admin.manage startapp mappers
```
add the same models as in your application on fastapi

`models.py`
```
from solo_django_admin.models import MapperModel
from path_to_fastapi_model import Account as FastAPIAccount

class Account(MapperModel):
    fast_api_model = FastAPIAccount
```
`admin.py`
```
from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ...
```
### Don`t forget add your app to settings 
INSTALLED_APPS.append('mappers')

---
How to use FK, ManyToMany, OneToOne etc. fields see examples

---
### Example how to connect with FastAPI

```
import os

from fastapi import FastAPI

from solo_django_admin.core.asgi import application
from solo_django_admin.core.settings import BASE_DIR

from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from path_to_your_lifespan import lifespan


def create_app():
    app_ = FastAPI(lifespan=lifespan)
    app_.mount(
        "/django-admin-static",
        StaticFiles(
            directory=os.path.join(BASE_DIR, "django_admin_static_files")),
        name="static",
    )
    app_.mount("/admin", application)

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    # YOUR SETTINGS HERE
    return app_


app = create_app()

if __name__ == '__main__':
    ...
```