"""
DataGreen — launcher Windows com bandeja do sistema.
Duplo clique no atalho: sobe o servidor (se preciso), abre o navegador.
Ícone perto do relógio: Abrir / Encerrar (para o servidor de verdade).
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

PORT = os.environ.get("DATAGREEN_PORT", "8765")
HOME_URL = f"http://127.0.0.1:{PORT}/"
MUTEX_NAME = "DataGreenDesktopSingleInstance"


def _app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


APP_ROOT = _app_root()
BACKEND_DIR = APP_ROOT / "backend"


def _desktop_env() -> dict:
    env = os.environ.copy()
    env["DATAGREEN_DESKTOP"] = "1"
    env["USE_SQLITE"] = "1"
    env["DATAGREEN_PORT"] = PORT
    env.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    web_alt = APP_ROOT / "web"
    if web_alt.is_dir():
        env["DATAGREEN_WEB_DIST"] = str(web_alt.resolve())
    return env


def _no_window_flags() -> int:
    if sys.platform == "win32":
        return int(getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000))
    return 0


def _run_manage(*args: str) -> int:
    return subprocess.run(
        [sys.executable, str(BACKEND_DIR / "manage.py"), *args],
        cwd=str(BACKEND_DIR),
        env=_desktop_env(),
        check=False,
        creationflags=_no_window_flags(),
    ).returncode


def _server_responds() -> bool:
    try:
        urlopen(HOME_URL + "api/auth/csrf/", timeout=2)
        return True
    except (URLError, OSError):
        return False


def _wait_server(seconds: int = 45) -> bool:
    for _ in range(seconds * 2):
        if _server_responds():
            return True
        time.sleep(0.5)
    return False


def _open_browser() -> None:
    webbrowser.open(HOME_URL)


def _try_mutex_second_instance() -> bool:
    """Retorna True se já existe outra instância (apenas abre o navegador e sai)."""
    if sys.platform != "win32":
        return False
    import ctypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.SetLastError(0)
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    kernel32.CreateMutexW(None, True, MUTEX_NAME)
    return kernel32.GetLastError() == 183  # ERROR_ALREADY_EXISTS


_server_proc: subprocess.Popen | None = None


def _start_server() -> None:
    global _server_proc
    _server_proc = subprocess.Popen(
        [
            sys.executable,
            str(BACKEND_DIR / "manage.py"),
            "runserver",
            f"127.0.0.1:{PORT}",
            "--noreload",
        ],
        cwd=str(BACKEND_DIR),
        env=_desktop_env(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=_no_window_flags(),
    )


def _stop_server() -> None:
    global _server_proc
    if _server_proc is None:
        return
    if _server_proc.poll() is None:
        _server_proc.terminate()
        try:
            _server_proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            _server_proc.kill()
    _server_proc = None


def _first_run_setup() -> None:
    _run_manage("migrate", "--noinput")
    _run_manage("seed_if_empty")


def main() -> None:
    if not BACKEND_DIR.is_dir():
        print(f"Pasta backend não encontrada em {BACKEND_DIR}", file=sys.stderr)
        sys.exit(1)

    if _try_mutex_second_instance():
        if _server_responds():
            _open_browser()
        else:
            print("DataGreen já está aberto na bandeja — use Encerrar antes de iniciar de novo.", file=sys.stderr)
        return

    _first_run_setup()

    if not _server_responds():
        _start_server()
        if not _wait_server():
            print("O servidor não respondeu a tempo. Veja se a porta está livre.", file=sys.stderr)
            sys.exit(1)

    _open_browser()

    try:
        import pystray
        from PIL import Image
    except ImportError:
        print(
            "Instale dependências do ícone: pip install pystray pillow",
            file=sys.stderr,
        )
        print(f"O servidor continua em {HOME_URL} — feche a janela do terminal ou mate o processo Python.", file=sys.stderr)
        try:
            input("Pressione Enter para encerrar o servidor...")
        except EOFError:
            pass
        _stop_server()
        return

    image = Image.new("RGB", (64, 64), color="#1f4a33")

    def on_open(icon, _item) -> None:
        _open_browser()

    def on_quit(icon, _item) -> None:
        _stop_server()
        icon.stop()

    menu = pystray.Menu(
        pystray.MenuItem("Abrir no navegador", on_open),
        pystray.MenuItem("Encerrar DataGreen", on_quit),
    )
    icon = pystray.Icon(
        "datagreen",
        image,
        "DataGreen — clique direito para menu",
        menu,
    )
    icon.run()


if __name__ == "__main__":
    main()
