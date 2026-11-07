"""Sobe o túnel Cloudflare para o Simulador TRT4 e mostra o link público."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8501
CANDIDATOS = [
    Path(r"C:\Program Files (x86)\cloudflared\cloudflared.exe"),
    Path(r"C:\Program Files\cloudflared\cloudflared.exe"),
    Path.home() / "AppData/Local/Microsoft/WinGet/Links/cloudflared.exe",
]
URL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")


def achar_cloudflared() -> Path | None:
    for c in CANDIDATOS:
        if c.exists():
            return c
    return None


def main() -> int:
    cf = achar_cloudflared()
    if not cf:
        print("cloudflared nao encontrado. Rode: winget install Cloudflare.cloudflared", file=sys.stderr)
        return 1

    print(f"Abrindo tunel para http://localhost:{PORT} ...")
    print("Deixe esta janela aberta enquanto quiser acesso externo.")
    print("Pressione Ctrl+C para encerrar o tunel.\n")

    proc = subprocess.Popen(
        [str(cf), "tunnel", "--url", f"http://localhost:{PORT}", "--no-autoupdate"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=str(ROOT),
    )
    url = None
    try:
        assert proc.stdout is not None
        for linha in proc.stdout:
            print(linha, end="")
            if not url:
                m = URL_RE.search(linha)
                if m:
                    url = m.group(0)
                    print("\n" + "=" * 60)
                    print(f"  LINK PUBLICO: {url}")
                    print("=" * 60 + "\n")
    except KeyboardInterrupt:
        print("\nEncerrando tunel...")
    finally:
        proc.terminate()
    return 0 if url else 1


if __name__ == "__main__":
    raise SystemExit(main())
