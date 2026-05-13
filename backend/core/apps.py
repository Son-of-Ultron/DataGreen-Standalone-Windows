import os
import sys
from datetime import date

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "DataGreen"

    def ready(self) -> None:
        import core.signals  # noqa: F401

        if not self._should_run_auto_backup():
            return
        self._run_auto_backup_once_per_day()

    def _should_run_auto_backup(self) -> bool:
        if not settings.DATAGREEN_DESKTOP:
            return False
        if "runserver" not in sys.argv:
            return False
        # Em runserver com autoreload, executa apenas no processo principal.
        return os.environ.get("RUN_MAIN") == "true"

    def _run_auto_backup_once_per_day(self) -> None:
        from core.backup_service import create_sqlite_backup, ensure_backup_dir, is_sqlite_mode

        if not is_sqlite_mode():
            return
        marker = ensure_backup_dir() / ".last_auto_backup_date"
        today = date.today().isoformat()
        if marker.exists() and marker.read_text(encoding="utf-8").strip() == today:
            return
        try:
            create_sqlite_backup()
            marker.write_text(today, encoding="utf-8")
        except OSError:
            # Falha de backup automático não deve impedir a inicialização local.
            return
