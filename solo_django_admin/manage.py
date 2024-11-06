#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import dotenv

dotenv.load_dotenv()

ENV_PREFIX = os.getenv('ENV_PREFIX', 'DJANGO_ADMIN')


def main():
    """Run administrative tasks."""
    os.environ.setdefault(f'DJANGO_SETTINGS_MODULE',
                          os.getenv(f"{ENV_PREFIX}_DJANGO_SETTINGS_MODULE",
                                    'core.settings'))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()