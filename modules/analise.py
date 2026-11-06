from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.db import connect


def carregar_historico(db_path=None) -> pd.DataFrame:
    with connect(db_path) as conn:
        df = pd.read_sql_query(
            """
            SELECT h.id, h.id_questao, h.resposta_usuario, h.correta, h.tempo_segundos,
                   h.data_hora, h.sessao_id, h.modo,
                   q.disciplina, q.topico, q.subtopico, q.peso, q.ano, q.dificuldade,
                   q.tempo_medio_esperado
            FROM historico h
            JOIN questoes q ON q.id = h.id_questao
            ORDER BY h.data_hora DESC
            """,
            conn,
        )
    return df


def resumo_geral(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "respostas": 0,
            "pct_acerto": 0.0,
            "tempo_medio": 0.0,
            "sessoes": 0,
        }
    return {
        "respostas": int(len(df)),
        "pct_acerto": round(100 * float(df["correta"].mean()), 1),
        "tempo_medio": round(float(df["tempo_segundos"].mean()), 1),
        "sessoes": int(df["sessao_id"].nunique()),
    }


def por_disciplina(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["disciplina", "acertos", "total", "pct_acerto", "tempo_medio"])
    g = (
        df.groupby("disciplina", as_index=False)
        .agg(
            acertos=("correta", "sum"),
            total=("correta", "count"),
            tempo_medio=("tempo_segundos", "mean"),
        )
    )
    g["pct_acerto"] = (100 * g["acertos"] / g["total"]).round(1)
    g["tempo_medio"] = g["tempo_medio"].round(1)
    return g.sort_values("pct_acerto")


def por_topico(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=["disciplina", "topico", "acertos", "total", "pct_acerto", "tempo_medio", "score_critico"]
        )
    g = (
        df.groupby(["disciplina", "topico"], as_index=False)
        .agg(
            acertos=("correta", "sum"),
            total=("correta", "count"),
            tempo_medio=("tempo_segundos", "mean"),
            tempo_esperado=("tempo_medio_esperado", "mean"),
        )
    )
    g["pct_acerto"] = (100 * g["acertos"] / g["total"]).round(1)
    g["tempo_medio"] = g["tempo_medio"].round(1)
    # gargalo: baixo acerto + tempo alto relativo
    tempo_rel = (g["tempo_medio"] / g["tempo_esperado"].clip(lower=1)).clip(upper=3)
    g["score_critico"] = ((100 - g["pct_acerto"]) * 0.7 + (tempo_rel * 30) * 0.3).round(1)
    return g.sort_values("score_critico", ascending=False)


def top_criticos(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return por_topico(df).head(n)


def _style_fig(fig, template: str = "plotly_white", colors: dict | None = None):
    c = colors or {}
    fig.update_layout(
        template=template,
        paper_bgcolor=c.get("paper", "rgba(0,0,0,0)"),
        plot_bgcolor=c.get("plot", "rgba(0,0,0,0)"),
        font=dict(color=c.get("font", "#152033"), family="Instrument Sans, Segoe UI, sans-serif"),
        margin=dict(l=40, r=24, t=56, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    if c.get("grid"):
        fig.update_xaxes(gridcolor=c["grid"], zerolinecolor=c["grid"])
        fig.update_yaxes(gridcolor=c["grid"], zerolinecolor=c["grid"])
    return fig


def fig_radar_disciplinas(df: pd.DataFrame, template: str = "plotly_white", colors: dict | None = None):
    g = por_disciplina(df)
    if g.empty:
        fig = go.Figure()
        fig.update_layout(title="Sem dados ainda")
        return _style_fig(fig, template, colors)
    accent = (colors or {}).get("accent", "#c4a35a")
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=g["pct_acerto"],
            theta=g["disciplina"],
            fill="toself",
            name="% acerto",
            line=dict(color=accent),
            fillcolor="rgba(196,163,90,0.25)",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=(g["tempo_medio"] / g["tempo_medio"].max() * 100).round(1)
            if g["tempo_medio"].max()
            else g["tempo_medio"],
            theta=g["disciplina"],
            fill="toself",
            name="tempo relativo",
            line=dict(color="#6e90a8"),
            fillcolor="rgba(110,144,168,0.18)",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=(colors or {}).get("grid")),
            angularaxis=dict(gridcolor=(colors or {}).get("grid")),
        ),
        title="Mapa de desempenho por disciplina",
    )
    return _style_fig(fig, template, colors)


def fig_heatmap_topicos(df: pd.DataFrame, template: str = "plotly_white", colors: dict | None = None):
    g = por_topico(df)
    if g.empty:
        fig = go.Figure()
        fig.update_layout(title="Sem dados ainda")
        return _style_fig(fig, template, colors)
    pivot = g.pivot_table(index="disciplina", columns="topico", values="pct_acerto", aggfunc="mean")
    fig = px.imshow(
        pivot,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        labels=dict(color="% acerto"),
        title="Heatmap de acerto por disciplina × tópico",
    )
    return _style_fig(fig, template, colors)


def fig_tempo_vs_acerto(df: pd.DataFrame, template: str = "plotly_white", colors: dict | None = None):
    g = por_topico(df)
    if g.empty:
        fig = go.Figure()
        fig.update_layout(title="Sem dados ainda")
        return _style_fig(fig, template, colors)
    fig = px.scatter(
        g,
        x="tempo_medio",
        y="pct_acerto",
        size="total",
        color="score_critico",
        hover_data=["disciplina", "topico"],
        color_continuous_scale="YlOrRd",
        title="Gargalos: tempo médio × % acerto",
        labels={"tempo_medio": "Tempo médio (s)", "pct_acerto": "% acerto"},
    )
    return _style_fig(fig, template, colors)
