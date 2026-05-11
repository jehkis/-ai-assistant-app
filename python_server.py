from __future__ import annotations

import mimetypes
import os
from pathlib import Path

from flask import Flask, jsonify, request, send_file


ROOT_DIR = Path(__file__).resolve().parent


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        if key and key not in os.environ:
            os.environ[key] = value


def create_app() -> Flask:
    load_dotenv(ROOT_DIR / ".env")

    app = Flask(__name__, static_folder=None)

    @app.get("/api/health")
    def api_health():
        return jsonify({"ok": True, "mode": "local-demo"})

    @app.get("/")
    def root():
        return send_static_file("index.html")

    @app.get("/<path:relative_path>")
    def static_files(relative_path: str):
        return send_static_file(relative_path)

    return app


def send_static_file(relative_path: str):
    candidate = (ROOT_DIR / relative_path).resolve()

    if ROOT_DIR not in candidate.parents and candidate != ROOT_DIR:
        return ("Not found", 404)

    if not candidate.exists() or not candidate.is_file():
        return ("Not found", 404)

    mime_type, _ = mimetypes.guess_type(candidate.name)
    return send_file(candidate, mimetype=mime_type or "application/octet-stream", max_age=0)

if __name__ == "__main__":
    load_dotenv(ROOT_DIR / ".env")
    port = int(os.environ.get("PORT", "3000"))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
