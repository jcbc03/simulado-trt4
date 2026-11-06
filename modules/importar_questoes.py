from __future__ import annotations

import json
from pathlib import Path

from modules.db import DB_PATH, DATA, connect, init_db

JSON_PADRAO = DATA / "questoes_iniciais.json"

TOPICOS_PADRAO = [
    ("Língua Portuguesa", None, 1.2),
    ("Matemática e Raciocínio Lógico", None, 1.1),
    ("Noções de Legislação", None, 1.0),
    ("Noções de Direitos Humanos", None, 0.9),
    ("Noções de Informática", None, 1.0),
    ("Direito do Trabalho", None, 2.0),
    ("Direito Processual do Trabalho", None, 2.0),
    ("Direito Administrativo", None, 1.8),
    ("Direito Constitucional", None, 1.8),
]


def _upsert_topicos(conn) -> None:
    for nome, pai, peso in TOPICOS_PADRAO:
        conn.execute(
            "INSERT OR IGNORE INTO topicos (nome, pai, peso_edital) VALUES (?, ?, ?)",
            (nome, pai, peso),
        )
    for row in conn.execute("SELECT DISTINCT disciplina, topico FROM questoes"):
        conn.execute(
            "INSERT OR IGNORE INTO topicos (nome, pai, peso_edital) VALUES (?, ?, ?)",
            (row["topico"], row["disciplina"], 1.0),
        )


def importar_json(json_path: Path, db_path: Path | None = None, limpar: bool = False) -> int:
    path = db_path or DB_PATH
    init_db(path)
    itens = json.loads(json_path.read_text(encoding="utf-8"))
    with connect(path) as conn:
        if limpar:
            conn.execute("DELETE FROM historico")
            conn.execute("DELETE FROM questoes")
        sql = """
            INSERT INTO questoes (
                enunciado, alt_a, alt_b, alt_c, alt_d, alt_e, gabarito,
                disciplina, topico, subtopico, dificuldade, ano, banca,
                tempo_medio_esperado, peso, prova_ref, cargo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for item in itens:
            conn.execute(
                sql,
                (
                    item["enunciado"],
                    item["alt_a"],
                    item["alt_b"],
                    item["alt_c"],
                    item["alt_d"],
                    item["alt_e"],
                    item["gabarito"].upper(),
                    item["disciplina"],
                    item["topico"],
                    item.get("subtopico") or item["topico"],
                    int(item.get("dificuldade", 2)),
                    int(item.get("ano") or 0) or None,
                    item.get("banca", "FCC"),
                    int(item.get("tempo_medio_esperado", 90)),
                    int(item.get("peso", 1)),
                    item.get("prova_ref"),
                    item.get("cargo"),
                ),
            )
        _upsert_topicos(conn)
        conn.commit()
        return int(conn.execute("SELECT COUNT(*) AS c FROM questoes").fetchone()["c"])


def importar_padrao(db_path: Path | None = None, regenerar_json: bool = False) -> int:
    if regenerar_json or not JSON_PADRAO.exists():
        from scripts.gerar_questoes import main as gerar

        gerar()
    return importar_json(JSON_PADRAO, db_path=db_path, limpar=True)


if __name__ == "__main__":
    n = importar_padrao(regenerar_json=True)
    print(f"Banco pronto com {n} questões em {DB_PATH}")
