#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import datetime
from django.core.management import call_command


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escola.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        try:
            import django

            django.setup()

            data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

            os.makedirs('backups', exist_ok=True)

            backup_nome = os.path.join(
                'backups',
                f"backup_{data}.json"
            )

            with open(backup_nome, "w", encoding="utf-8") as f:
                call_command(
                    'dumpdata',
                    indent=2,
                    stdout=f
                )

            print(f"💾 Backup automático criado: {backup_nome}")

        except Exception as e:
            print(f"⚠️ Erro ao criar backup automático: {e}")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()