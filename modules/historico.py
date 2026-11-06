from __future__ import annotations

from pathlib import Path

import pandas as pd

from modules.db import connect
from modules.importar_questoes import importar_json


def limpar_historico(db_path: Path | None = None) -> int:
    with connect(db_path) as conn:
        n = int(conn.execute("SELECT COUNT(*) AS c FROM historico").fetchone()["c"])
        conn.execute("DELETE FROM historico")
        conn.commit()
    return n


def importar_upload(arquivo, db_path: Path | None = None) -> int:
    nome = (arquivo.name or "").lower()
    tmp = Path(__file__).resolve().parents[1] / "data" / "_upload_tmp"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if nome.endswith(".json"):
        path = tmp.with_suffix(".json")
        path.write_bytes(arquivo.getvalue())
        return importar_json(path, db_path=db_path, limpar=False)
    if nome.endswith((".xlsx", ".xls")):
        path = tmp.with_suffix(".xlsx")
        path.write_bytes(arquivo.getvalue())
        df = pd.read_excel(path)
        json_path = tmp.with_suffix(".json")
        df.to_json(json_path, orient="records", force_ascii=False)
        return importar_json(json_path, db_path=db_path, limpar=False)
    raise ValueError("Use arquivo .json ou .xlsx")


def format_tempo(segundos: float) -> str:
    s = max(0, int(segundos))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"
