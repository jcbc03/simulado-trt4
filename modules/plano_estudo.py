from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from modules.analise import por_topico, resumo_geral, top_criticos
from modules.db import connect


TRILHAS = {
    "básico": "Fundamentos e legislação literal; 40–60 min/dia; foco em definição e princípios.",
    "intermediário": "Casos típicos FCC; 60–90 min/dia; misturar teoria + 15–20 questões.",
    "avançado": "Simulados cronometrados e revisão espaçada; 90–120 min/dia; erro zero em básicos.",
}


def _nivel(pct: float) -> str:
    if pct >= 75:
        return "avançado"
    if pct >= 50:
        return "intermediário"
    return "básico"


def gerar_plano(df: pd.DataFrame, dias: int = 14, questoes_por_dia: int = 20) -> dict[str, Any]:
    resumo = resumo_geral(df)
    criticos = top_criticos(df, 10)
    nivel = _nivel(float(resumo["pct_acerto"]))

    if criticos.empty:
        foco = [
            {"disciplina": "Língua Portuguesa", "topico": "Interpretação de texto", "motivo": "alta frequência FCC"},
            {"disciplina": "Matemática e Raciocínio Lógico", "topico": "Lógica proposicional", "motivo": "peso em gerais"},
            {"disciplina": "Direito do Trabalho", "topico": "Jornada", "motivo": "específico de alto peso"},
        ]
        trilhas = [{"topico": f["topico"], "disciplina": f["disciplina"], "trilha": "básico", "motivo": f["motivo"]} for f in foco]
    else:
        trilhas = []
        for _, row in criticos.iterrows():
            trilha = "básico" if row["pct_acerto"] < 50 else ("intermediário" if row["pct_acerto"] < 75 else "avançado")
            trilhas.append(
                {
                    "disciplina": row["disciplina"],
                    "topico": row["topico"],
                    "trilha": trilha,
                    "pct_acerto": float(row["pct_acerto"]),
                    "tempo_medio": float(row["tempo_medio"]),
                    "score_critico": float(row["score_critico"]),
                    "motivo": "baixo acerto + tempo elevado" if row["score_critico"] >= 40 else "desempenho irregular",
                }
            )

    calendario = []
    inicio = date.today()
    foco_ciclo = trilhas[:6] or [{"disciplina": "Geral", "topico": "Revisão ampla", "trilha": nivel}]
    for i in range(dias):
        dia = inicio + timedelta(days=i)
        item = foco_ciclo[i % len(foco_ciclo)]
        # revisão espaçada: dias 3,7,14 revisitam o 1º crítico
        revisao = None
        if i in (2, 6, 13) and trilhas:
            revisao = trilhas[0]
        calendario.append(
            {
                "data": dia.isoformat(),
                "questoes_sugeridas": questoes_por_dia,
                "foco_disciplina": item["disciplina"],
                "foco_topico": item["topico"],
                "trilha": item.get("trilha", nivel),
                "atividade": TRILHAS.get(item.get("trilha", nivel), TRILHAS["básico"]),
                "revisao_espacada": (
                    f"{revisao['disciplina']} / {revisao['topico']}" if revisao else None
                ),
            }
        )

    return {
        "nivel_geral": nivel,
        "resumo": resumo,
        "prioridades": trilhas[:10],
        "calendario": calendario,
        "orientacao": (
            "Priorize tópicos com baixo acerto e alto tempo. "
            "No simulado completo, gerais peso 1 e específicas peso 2."
        ),
    }


def sugerir_questoes(disciplina: str | None = None, topico: str | None = None, n: int = 10, db_path=None) -> list[dict]:
    clauses = ["1=1"]
    params: list[Any] = []
    if disciplina:
        clauses.append("disciplina = ?")
        params.append(disciplina)
    if topico:
        clauses.append("topico = ?")
        params.append(topico)
    sql = f"""
        SELECT id, enunciado, disciplina, topico, dificuldade, ano, peso
        FROM questoes
        WHERE {' AND '.join(clauses)}
        ORDER BY RANDOM()
        LIMIT ?
    """
    params.append(n)
    with connect(db_path) as conn:
        rows = conn.execute(sql, tuple(params)).fetchall()
    return [dict(r) for r in rows]


def plano_para_dataframe(plano: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    pri = pd.DataFrame(plano["prioridades"])
    cal = pd.DataFrame(plano["calendario"])
    return pri, cal
