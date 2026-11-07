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
PORT = int(os.environ.get("TRT4_PORT", "8600"))
HOST = "127.0.0.1"
PID_FILE = ROOT / "data" / "streamlit.pid"


def _ensure_path() -> None:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    os.chdir(ROOT)


def _porta_livre(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((HOST, port)) != 0


def _salvar_pid(pid: int) -> None:
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(pid), encoding="utf-8")


def _encerrar(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


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
            _salvar_pid(proc.pid)
            webbrowser.open(url)
            return 0
        if proc.poll() is not None:
            print(f"Falha ao iniciar Streamlit. Veja {log}", file=sys.stderr)
            return 1

    # timeout: nao deixar processo órfão sem porta
    _encerrar(proc)
    print(f"Timeout ao iniciar Streamlit na porta {port}. Veja {log}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
