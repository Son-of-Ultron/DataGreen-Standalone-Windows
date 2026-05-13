import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings


def is_sqlite_mode() -> bool:
    engine = settings.DATABASES["default"]["ENGINE"]
    return engine.endswith("sqlite3")


def sqlite_db_path() -> Path:
    return Path(settings.DATABASES["default"]["NAME"]).resolve()


def ensure_backup_dir() -> Path:
    backup_dir = Path(settings.SQLITE_BACKUP_DIR).resolve()
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir


def create_sqlite_backup(prefix: str = "datagreen_backup") -> Path:
    source = sqlite_db_path()
    if not source.exists():
        raise FileNotFoundError(f"Banco SQLite não encontrado em: {source}")

    backup_dir = ensure_backup_dir()
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    target = backup_dir / f"{prefix}_{stamp}.sqlite3"
    shutil.copy2(source, target)
    apply_backup_retention(backup_dir=backup_dir)
    return target


def apply_backup_retention(backup_dir: Path | None = None) -> None:
    base = backup_dir or ensure_backup_dir()
    keep = max(1, int(settings.SQLITE_BACKUP_RETENTION))
    backups = sorted(base.glob("*.sqlite3"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old_file in backups[keep:]:
        old_file.unlink(missing_ok=True)
