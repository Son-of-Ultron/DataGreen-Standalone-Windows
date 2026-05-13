import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound


def _web_root() -> Path:
    return Path(settings.DATAGREEN_WEB_DIST).resolve()


def serve_desktop_spa(request, path: str = ""):
    """Serve arquivos do build Vite (dist/public) ou index.html para rotas do SPA."""
    base = _web_root()
    if not base.is_dir():
        return HttpResponseNotFound("Build do site não encontrado. Rode o build do frontend (pnpm build).")

    path = path.strip("/")
    if path:
        candidate = (base / path).resolve()
        if not str(candidate).startswith(str(base)):
            candidate = base / "index.html"
        elif not candidate.is_file():
            candidate = base / "index.html"
    else:
        candidate = base / "index.html"

    if not candidate.is_file():
        return HttpResponseNotFound()

    content_type, _ = mimetypes.guess_type(str(candidate))
    return FileResponse(candidate.open("rb"), content_type=content_type or "application/octet-stream")
