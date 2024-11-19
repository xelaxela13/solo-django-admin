#!/bin/sh
aerich init -t database.TORTOISE_ORM
aerich upgrade
python -m solo_django_admin.manage collectstatic -c --settings=django_settings --no-input
python -m solo_django_admin.manage migrate --settings=django_settings
fastapi dev --host 0.0.0.0 --port 8000