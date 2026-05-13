from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.backup_service import create_sqlite_backup, is_sqlite_mode


class Command(BaseCommand):
    help = "Cria backup do banco SQLite em backups/ com retenção configurável."

    def handle(self, *args, **options):
        if not settings.DATAGREEN_DESKTOP or not is_sqlite_mode():
            raise CommandError("backup_sqlite só pode ser usado no modo desktop com SQLite.")
        backup_file = create_sqlite_backup()
        self.stdout.write(self.style.SUCCESS(f"Backup criado com sucesso: {backup_file}"))
