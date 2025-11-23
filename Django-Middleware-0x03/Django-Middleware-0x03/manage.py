#!/usr/bin/env python
<<<<<<< HEAD
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
=======
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middleware_project.settings')
>>>>>>> 68e6749 (Initial upload with middleware and settings adjustments)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
<<<<<<< HEAD
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

=======
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


>>>>>>> 68e6749 (Initial upload with middleware and settings adjustments)
if __name__ == '__main__':
    main()
