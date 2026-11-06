from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from modules.db import connect


GERAIS = {
    "Língua Portuguesa",
    "Matemática e Raciocínio Lógico",
    "Noções de Legislação",
    "Noções de Direitos Humanos",
    "Noções de Informática",
}


@dataclass
class QuestaoSessao:
    id: int
    enunciado: str
    alternativas: dict[str, str]
    gabarito: str
    disciplina: str
    topico: str
    peso: int
    tempo_medio_esperado: int
    ano: int | None
    banca: str
    prova_ref: str | None
    resposta: str | None = None
    tempo_segundos: float = 0.0
    marcada_revisao: bool = False


@dataclass
class SessaoSimulado:
    sessao_id: str
    modo: str
    questoes: list[QuestaoSessao]
    indice: int = 0
    inicio_questao_ts: float | None = None
    finalizada: bool = False
    metadados: dict[str, Any] = field(default_factory=dict)


def _rows_to_questoes(rows) -> list[QuestaoSessao]:
    out: list[QuestaoSessao] = []
    for r in rows:
        out.append(
            QuestaoSessao(
                id=r["id"],
                enunciado=r["enunciado"],
                alternativas={
                    "A": r["alt_a"],
                    "B": r["alt_b"],
                    "C": r["alt_c"],
                    "D": r["alt_d"],
                    "E": r["alt_e"],
                },
                gabarito=r["gabarito"],
                disciplina=r["disciplina"],
                topico=r["topico"],
                peso=int(r["peso"]),
                tempo_medio_esperado=int(r["tempo_medio_esperado"] or 90),
                ano=r["ano"],
                banca=r["banca"] or "FCC",
                prova_ref=r["prova_ref"],
            )
        )
    return out


def listar_anos(db_path=None) -> list[int]:
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT DISTINCT ano FROM questoes WHERE ano IS NOT NULL ORDER BY ano DESC"
        ).fetchall()
    return [int(r["ano"]) for r in rows]


def listar_disciplinas(db_path=None) -> list[str]:
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT DISTINCT disciplina FROM questoes ORDER BY disciplina"
        ).fetchall()
    return [r["disciplina"] for r in rows]


def _amostrar(conn, where: str, params: tuple, n: int) -> list:
    rows = conn.execute(f"SELECT * FROM questoes WHERE {where}", params).fetchall()
    if len(rows) <= n:
        return list(rows)
    return random.sample(list(rows), n)


def _completar(conn, atuais: list, where: str, params: tuple, n: int, excluir: set | None = None) -> list:
    """Completa a lista até n itens sem descartar os já obtidos."""
    out = list(atuais)
    ids = {r["id"] for r in out} | set(excluir or ())
    if len(out) >= n:
        return out[:n]
    candidatos = _amostrar(conn, where, params, n + len(ids) + 10)
    for row in candidatos:
        if row["id"] in ids:
            continue
        out.append(row)
        ids.add(row["id"])
        if len(out) >= n:
            break
    return out


def criar_sessao(
    modo: str = "completo",
    *,
    disciplina: str | None = None,
    ano: int | None = None,
    db_path=None,
    seed: int | None = None,
) -> SessaoSimulado:
    if seed is not None:
        random.seed(seed)
    sessao_id = str(uuid.uuid4())
    with connect(db_path) as conn:
        if modo == "completo":
            gerais = _amostrar(conn, "peso = 1", (), 30)
            if len(gerais) < 30:
                gerais = _completar(conn, gerais, "1=1", (), 30)
            especificas = _amostrar(conn, "peso = 2", (), 30)
            if len(especificas) < 30:
                especificas = _completar(conn, especificas, "peso = 2", (), 30)
            if len(especificas) < 30:
                ids_gerais = {r["id"] for r in gerais}
                especificas = _completar(conn, especificas, "1=1", (), 30, excluir=ids_gerais)
            rows = list(gerais) + list(especificas)
            random.shuffle(rows)
        elif modo == "disciplina":
            if not disciplina:
                raise ValueError("disciplina obrigatória")
            rows = _amostrar(conn, "disciplina = ?", (disciplina,), 20)
        elif modo == "prova_antiga":
            if not ano:
                raise ValueError("ano obrigatório")
            gerais = _amostrar(conn, "ano = ? AND peso = 1", (ano,), 30)
            especificas = _amostrar(conn, "ano = ? AND peso = 2", (ano,), 30)
            if len(gerais) + len(especificas) < 10:
                rows = _amostrar(conn, "ano = ?", (ano,), 60)
            else:
                rows = list(gerais) + list(especificas)
                random.shuffle(rows)
        elif modo == "erros":
            rows = conn.execute(
                """
                SELECT q.* FROM questoes q
                JOIN historico h ON h.id_questao = q.id
                WHERE h.correta = 0
                GROUP BY q.id
                ORDER BY COUNT(*) DESC, MAX(h.data_hora) DESC
                LIMIT 30
                """
            ).fetchall()
            if not rows:
                rows = _amostrar(conn, "1=1", (), 15)
        elif modo == "revisao":
            rows = _amostrar(conn, "1=1", (), 15)
        else:
            raise ValueError(f"modo desconhecido: {modo}")

    questoes = _rows_to_questoes(rows)
    return SessaoSimulado(sessao_id=sessao_id, modo=modo, questoes=questoes)


def _count(conn) -> int:
    return int(conn.execute("SELECT COUNT(*) AS c FROM questoes").fetchone()["c"])


def questao_atual(sessao: SessaoSimulado) -> QuestaoSessao | None:
    if not sessao.questoes or sessao.indice >= len(sessao.questoes):
        return None
    return sessao.questoes[sessao.indice]


def registrar_tempo(sessao: SessaoSimulado, segundos: float) -> None:
    q = questao_atual(sessao)
    if q is None:
        return
    q.tempo_segundos += max(0.0, float(segundos))


def responder(sessao: SessaoSimulado, alternativa: str | None) -> None:
    q = questao_atual(sessao)
    if q is None:
        return
    # defensivo: widget pode devolver None ou valor não-string
    if isinstance(alternativa, str) and alternativa.strip():
        q.resposta = alternativa.strip().upper()


def marcar_revisao(sessao: SessaoSimulado, valor: bool = True) -> None:
    q = questao_atual(sessao)
    if q is None:
        return
    q.marcada_revisao = bool(valor)


def navegar(sessao: SessaoSimulado, destino: int) -> None:
    if 0 <= destino < len(sessao.questoes):
        sessao.indice = destino


def proxima(sessao: SessaoSimulado) -> None:
    if sessao.indice < len(sessao.questoes) - 1:
        sessao.indice += 1


def anterior(sessao: SessaoSimulado) -> None:
    if sessao.indice > 0:
        sessao.indice -= 1


def finalizar(sessao: SessaoSimulado, db_path=None) -> dict[str, Any]:
    agora = datetime.now(timezone.utc).isoformat()
    acertos = 0
    pontos = 0.0
    pontos_max = 0.0
    tempo_total = 0.0
    detalhe = []

    with connect(db_path) as conn:
        for q in sessao.questoes:
            correta = 1 if q.resposta and q.resposta == q.gabarito else 0
            if correta:
                acertos += 1
                pontos += q.peso
            pontos_max += q.peso
            tempo_total += q.tempo_segundos
            conn.execute(
                """
                INSERT INTO historico (
                    id_questao, resposta_usuario, correta, tempo_segundos,
                    data_hora, sessao_id, modo
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    q.id,
                    q.resposta,
                    correta,
                    round(q.tempo_segundos, 2),
                    agora,
                    sessao.sessao_id,
                    sessao.modo,
                ),
            )
            detalhe.append(
                {
                    "id": q.id,
                    "disciplina": q.disciplina,
                    "topico": q.topico,
                    "resposta": q.resposta,
                    "gabarito": q.gabarito,
                    "correta": bool(correta),
                    "tempo": q.tempo_segundos,
                    "peso": q.peso,
                    "marcada_revisao": q.marcada_revisao,
                }
            )
        conn.commit()

    sessao.finalizada = True
    total = len(sessao.questoes)
    return {
        "sessao_id": sessao.sessao_id,
        "modo": sessao.modo,
        "total": total,
        "acertos": acertos,
        "pct_acerto": round(100 * acertos / total, 1) if total else 0.0,
        "pontos": pontos,
        "pontos_max": pontos_max,
        "pct_pontos": round(100 * pontos / pontos_max, 1) if pontos_max > 0 else 0.0,
        "tem_peso": pontos_max > 0,
        "respondidas": sum(1 for q in sessao.questoes if q.resposta),
        "tempo_total": round(tempo_total, 1),
        "tempo_medio": round(tempo_total / total, 1) if total else 0.0,
        "detalhe": detalhe,
    }
