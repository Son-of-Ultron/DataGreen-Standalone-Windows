import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.backup_service import create_sqlite_backup, is_sqlite_mode, sqlite_db_path


class Command(BaseCommand):
    help = "Restaura backup SQLite informado, criando backup de segurança antes da restauração."

    def add_arguments(self, parser):
        parser.add_argument("backup_file", type=str, help="Caminho para o arquivo .sqlite3 de backup.")

    def handle(self, *args, **options):
        if not settings.DATAGREEN_DESKTOP or not is_sqlite_mode():
            raise CommandError("restore_sqlite só pode ser usado no modo desktop com SQLite.")

        source = Path(options["backup_file"]).expanduser().resolve()
        if not source.exists() or not source.is_file():
            raise CommandError(f"Arquivo de backup não encontrado: {source}")

        self.stdout.write("Criando backup de segurança do banco atual...")
        current_backup = create_sqlite_backup(prefix="datagreen_pre_restore")
        self.stdout.write(self.style.SUCCESS(f"Backup pré-restauração criado: {current_backup}"))

        target_db = sqlite_db_path()
        self.stdout.write(f"Restaurando banco a partir de: {source}")
        shutil.copy2(source, target_db)
        self.stdout.write(self.style.SUCCESS("Restauração concluída com sucesso."))
