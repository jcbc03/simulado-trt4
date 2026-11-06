"""Abre o Simulador TRT4 sem interação: sobe Streamlit e abre o navegador."""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(os.environ.get("TRT4_PORT", "8501"))
HOST = "127.0.0.1"


def _ensure_path() -> None:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    os.chdir(ROOT)


def _porta_livre(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((HOST, port)) != 0


def _bootstrap_db() -> None:
    from modules.db import count_questoes, init_db
    from modules.importar_questoes import importar_padrao

    init_db()
    if count_questoes() == 0:
        json_path = ROOT / "data" / "questoes_iniciais.json"
        if not json_path.exists():
            from scripts.gerar_questoes import main as gerar

            gerar()
        importar_padrao(regenerar_json=False)


def _streamlit_cmd(port: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT / "app.py"),
        "--server.headless=true",
        f"--server.port={port}",
        f"--server.address={HOST}",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
    ]


def main() -> int:
    _ensure_path()
    _bootstrap_db()

    port = PORT
    if not _porta_livre(port):
        # já rodando: só abre o browser
        webbrowser.open(f"http://{HOST}:{port}")
        return 0

    creation = 0
    if sys.platform == "win32":
        creation = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    log = ROOT / "data" / "launcher.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as log_f:
        proc = subprocess.Popen(
            _streamlit_cmd(port),
            cwd=str(ROOT),
            stdout=log_f,
            stderr=subprocess.STDOUT,
            creationflags=creation if sys.platform == "win32" else 0,
            close_fds=True,
        )

    url = f"http://{HOST}:{port}"
    for _ in range(60):
        time.sleep(0.5)
        if not _porta_livre(port):
            webbrowser.open(url)
            return 0
        if proc.poll() is not None:
            print(f"Falha ao iniciar Streamlit. Veja {log}", file=sys.stderr)
            return 1

    webbrowser.open(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
