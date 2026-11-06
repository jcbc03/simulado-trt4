from __future__ import annotations

import sys
import time
from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.analise import (
    carregar_historico,
    fig_heatmap_topicos,
    fig_radar_disciplinas,
    fig_tempo_vs_acerto,
    por_disciplina,
    resumo_geral,
    top_criticos,
)
from modules.db import DB_PATH, connect, count_questoes, init_db
from modules.historico import format_tempo, importar_upload, limpar_historico
from modules.importar_questoes import importar_padrao
from modules.plano_estudo import gerar_plano, plano_para_dataframe, sugerir_questoes
from modules.simulador import (
    anterior,
    criar_sessao,
    finalizar,
    listar_anos,
    listar_disciplinas,
    marcar_revisao,
    navegar,
    proxima,
    questao_atual,
    registrar_tempo,
    responder,
)

st.set_page_config(
    page_title="Simulador TRT4 FCC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

W = "stretch"


def bootstrap() -> None:
    init_db()
    if count_questoes() == 0:
        json_path = ROOT / "data" / "questoes_iniciais.json"
        if not json_path.exists():
            from scripts.gerar_questoes import main as gerar

            gerar()
        importar_padrao(regenerar_json=False)


def load_css() -> None:
    css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


THEMES = {
    "Claro": {
        "text": "#152033",
        "text_muted": "#5c6678",
        "surface": "#fffcf7",
        "border": "rgba(21, 32, 51, 0.10)",
        "border_strong": "rgba(21, 32, 51, 0.16)",
        "shadow": "0 8px 24px rgba(21, 32, 51, 0.06)",
        "app_bg": (
            "radial-gradient(900px 420px at 100% -5%, rgba(196,163,90,0.14), transparent 55%),"
            "linear-gradient(180deg, #f3efe7 0%, #ebe6dc 100%)"
        ),
        "sidebar_bg": "linear-gradient(180deg, #faf7f1 0%, #f0ebe2 100%)",
        "header_bg": "rgba(243, 239, 231, 0.78)",
        "hero_bg": (
            "radial-gradient(900px 360px at 8% -20%, rgba(196,163,90,0.35), transparent 55%),"
            "linear-gradient(135deg, #12253a 0%, #1a3550 48%, #234860 100%)"
        ),
        "hero_text": "#f7f3ea",
        "hero_sub": "rgba(247,243,234,0.88)",
        "hero_border": "rgba(18, 37, 58, 0.35)",
        "hero_shadow": "0 22px 48px rgba(18, 37, 58, 0.18)",
        "input_bg": "#fffcf7",
        "chart_surface": "#fffcf7",
        "progress_track": "#e6dfd2",
        "plotly": "plotly_white",
        "fig": {
            "paper": "#fffcf7",
            "plot": "#f3efe7",
            "font": "#152033",
            "grid": "rgba(21,32,51,0.10)",
            "accent": "#c4a35a",
        },
    },
    "Escuro": {
        "text": "#e8e3d9",
        "text_muted": "#98a1af",
        "surface": "#12171f",
        "border": "rgba(232, 227, 217, 0.08)",
        "border_strong": "rgba(232, 227, 217, 0.14)",
        "shadow": "0 10px 28px rgba(0, 0, 0, 0.32)",
        "app_bg": (
            "radial-gradient(1000px 480px at 0% -10%, rgba(196,163,90,0.08), transparent 45%),"
            "radial-gradient(800px 500px at 100% 110%, rgba(56,110,150,0.08), transparent 50%),"
            "linear-gradient(180deg, #07090c 0%, #0b0f14 55%, #0a1018 100%)"
        ),
        "sidebar_bg": "linear-gradient(180deg, #0a0d12 0%, #0d1219 100%)",
        "header_bg": "rgba(7, 9, 12, 0.78)",
        "hero_bg": (
            "radial-gradient(900px 380px at 12% -30%, rgba(196,163,90,0.20), transparent 50%),"
            "linear-gradient(145deg, #0a1018 0%, #101820 45%, #142030 100%)"
        ),
        "hero_text": "#f3eee4",
        "hero_sub": "rgba(232, 227, 217, 0.78)",
        "hero_border": "rgba(232, 227, 217, 0.08)",
        "hero_shadow": "0 24px 56px rgba(0, 0, 0, 0.45)",
        "input_bg": "#161c26",
        "chart_surface": "#12171f",
        "progress_track": "#1a222e",
        "plotly": "plotly_dark",
        "fig": {
            "paper": "#12171f",
            "plot": "#0b0f14",
            "font": "#e8e3d9",
            "grid": "rgba(232,227,217,0.10)",
            "accent": "#c4a35a",
        },
    },
}


def apply_theme(tema: str) -> None:
    t = THEMES[tema]
    st.session_state["plotly_template"] = t["plotly"]
    st.session_state["theme_colors"] = t["fig"]
    root = "".join(f"--{k.replace('_', '-')}: {v};" for k, v in t.items() if k != "fig")
    st.markdown(f"<style>:root{{{root}}}</style>", unsafe_allow_html=True)


def flush_tempo() -> None:
    sess = st.session_state.get("sessao")
    if not sess or sess.finalizada:
        return
    t0 = st.session_state.get("questao_t0")
    if t0 is None:
        return
    registrar_tempo(sess, time.time() - t0)
    st.session_state["questao_t0"] = time.time()


def start_timer() -> None:
    st.session_state["questao_t0"] = time.time()
    if "prova_t0" not in st.session_state or st.session_state.get("prova_t0") is None:
        st.session_state["prova_t0"] = time.time()


@st.fragment(run_every=timedelta(seconds=1))
def painel_cronometro() -> None:
    sess = st.session_state.get("sessao")
    if not sess or sess.finalizada:
        return
    q = questao_atual(sess)
    t0 = st.session_state.get("questao_t0")
    p0 = st.session_state.get("prova_t0")
    if t0 is None:
        st.session_state["questao_t0"] = t0 = time.time()
    if p0 is None:
        st.session_state["prova_t0"] = p0 = time.time()
    tempo_q = (q.tempo_segundos if q else 0) + (time.time() - t0)
    tempo_p = time.time() - p0
    c1, c2, c3 = st.columns(3)
    c1.metric("Tempo da questão", format_tempo(tempo_q))
    c2.metric("Tempo da prova", format_tempo(tempo_p))
    c3.metric("Esperado (questão)", format_tempo(q.tempo_medio_esperado if q else 90))


def persistir_estado(sess, escolha, marcar) -> None:
    """Grava resposta/tempo só quando há seleção explícita; mantém em branco caso contrário."""
    if isinstance(escolha, str) and escolha:
        responder(sess, escolha)
    marcar_revisao(sess, marcar)


bootstrap()
load_css()

if "tema" not in st.session_state:
    st.session_state["tema"] = "Claro"
if "sessao" not in st.session_state:
    st.session_state["sessao"] = None
if "resultado" not in st.session_state:
    st.session_state["resultado"] = None

with st.sidebar:
    st.markdown("### Simulador TRT4")
    st.caption("FCC · offline · análise por tempo")
    tema = st.radio(
        "Aparência",
        ["Claro", "Escuro"],
        horizontal=True,
        index=0 if st.session_state["tema"] == "Claro" else 1,
        help="Tema claro (papel) ou escuro (tinta profunda).",
    )
    st.session_state["tema"] = tema
    pagina = st.radio(
        "Navegação",
        ["Dashboard", "Simulado", "Análise", "Plano de estudo", "Banco de questões"],
    )
    st.divider()
    st.metric("Questões no banco", count_questoes())
    st.caption(str(DB_PATH))
    if st.button("Reimportar banco padrão"):
        n = importar_padrao(regenerar_json=True)
        st.success(f"Importadas {n} questões")
        st.rerun()
    if st.button("Limpar histórico de respostas"):
        n = limpar_historico()
        st.warning(f"Histórico limpo ({n} registros)")
        st.rerun()

apply_theme(tema)
template = st.session_state.get("plotly_template", "plotly_white")
tc = st.session_state.get("theme_colors")

st.markdown(
    """
    <div class="hero">
      <span class="badge">TRT4 · Fundação Carlos Chagas</span>
      <h1>Simulador de Provas TRT4</h1>
      <p>Treino offline no formato FCC: 30 gerais (peso 1) + 30 específicas (peso 2),
      cronômetro por questão, mapa de gargalos e plano de nivelamento personalizado.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

hist = carregar_historico()
resumo = resumo_geral(hist)

if pagina == "Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Respostas", resumo["respostas"])
    c2.metric("% acerto", f"{resumo['pct_acerto']}%")
    c3.metric("Tempo médio", f"{resumo['tempo_medio']} s")
    c4.metric("Sessões", resumo["sessoes"])

    left, right = st.columns(2)
    with left:
        st.plotly_chart(fig_radar_disciplinas(hist, template, tc), width=W, key="dash_radar")
    with right:
        st.plotly_chart(fig_tempo_vs_acerto(hist, template, tc), width=W, key="dash_scatter")

    st.subheader("Top 10 tópicos críticos")
    crit = top_criticos(hist, 10)
    if crit.empty:
        st.info("Faça um simulado para gerar o mapa de pontos fortes e fracos.")
    else:
        st.dataframe(crit, width=W, hide_index=True)

elif pagina == "Simulado":
    with st.expander(
        "Configurar novo simulado",
        expanded=st.session_state["sessao"] is None and not st.session_state.get("resultado"),
    ):
        modo = st.selectbox(
            "Modo",
            ["completo", "disciplina", "prova_antiga", "erros", "revisao"],
            format_func=lambda m: {
                "completo": "Simulado completo (60q · peso 1+2)",
                "disciplina": "Por disciplina",
                "prova_antiga": "Prova antiga (por ano)",
                "erros": "Só erros",
                "revisao": "Modo revisão rápida",
            }[m],
        )
        disc = None
        ano = None
        if modo == "disciplina":
            disc = st.selectbox("Disciplina", listar_disciplinas())
        if modo == "prova_antiga":
            anos = listar_anos()
            ano = st.selectbox("Ano de referência", anos) if anos else None
        if st.button("Iniciar", type="primary"):
            try:
                st.session_state["sessao"] = criar_sessao(modo, disciplina=disc, ano=ano)
                st.session_state["resultado"] = None
                st.session_state["prova_t0"] = time.time()
                start_timer()
                st.rerun()
            except Exception as e:
                st.error(str(e))

    sess = st.session_state.get("sessao")
    if sess and not sess.finalizada:
        q = questao_atual(sess)
        total = len(sess.questoes)
        respondidas = sum(1 for qq in sess.questoes if qq.resposta)
        st.progress((sess.indice + 1) / total, text=f"Questão {sess.indice + 1} de {total} · {respondidas} respondidas")
        painel_cronometro()

        cols = st.columns(4)
        cols[0].write(f"**Disciplina:** {q.disciplina}")
        cols[1].write(f"**Tópico:** {q.topico}")
        cols[2].write(f"**Peso:** {q.peso}")
        cols[3].write(f"**Ano/banca:** {q.ano or '—'} / {q.banca}")

        st.markdown(f'<div class="questao-box">{q.enunciado}</div>', unsafe_allow_html=True)
        labels = list(q.alternativas.keys())
        idx = labels.index(q.resposta) if q.resposta in labels else None
        escolha = st.radio(
            "Alternativas",
            options=labels,
            format_func=lambda k: f"{k}) {q.alternativas[k]}",
            index=idx,
            key=f"resp_{sess.sessao_id}_{sess.indice}",
        )
        marcar = st.checkbox(
            "Marcar para revisão",
            value=q.marcada_revisao,
            key=f"rev_{sess.sessao_id}_{sess.indice}",
        )

        st.caption("Navegação rápida (● respondida · ◆ revisão · ○ em branco)")
        nav_cols = st.columns(min(15, total))
        for i, qq in enumerate(sess.questoes):
            col = nav_cols[i % len(nav_cols)]
            if qq.marcada_revisao:
                label = f"◆{i+1}"
            elif qq.resposta:
                label = f"●{i+1}"
            else:
                label = f"○{i+1}"
            if col.button(label, key=f"nav_{sess.sessao_id}_{i}"):
                flush_tempo()
                persistir_estado(sess, escolha, marcar)
                navegar(sess, i)
                start_timer()
                st.rerun()

        b1, b2, b3, b4, b5 = st.columns(5)
        if b1.button("⟵ Anterior"):
            flush_tempo()
            persistir_estado(sess, escolha, marcar)
            anterior(sess)
            start_timer()
            st.rerun()
        if b2.button("Próxima ⟶"):
            flush_tempo()
            persistir_estado(sess, escolha, marcar)
            proxima(sess)
            start_timer()
            st.rerun()
        destino = b3.number_input("Ir para", min_value=1, max_value=total, value=sess.indice + 1)
        if b4.button("Ir"):
            flush_tempo()
            persistir_estado(sess, escolha, marcar)
            navegar(sess, int(destino) - 1)
            start_timer()
            st.rerun()
        if b5.button("Finalizar e ver gabarito", type="primary"):
            flush_tempo()
            persistir_estado(sess, escolha, marcar)
            st.session_state["resultado"] = finalizar(sess)
            st.session_state["prova_t0"] = None
            st.rerun()

    resultado = st.session_state.get("resultado")
    if resultado:
        st.success(
            f"Acertos: {resultado['acertos']}/{resultado['total']} "
            f"({resultado['pct_acerto']}%) · Pontos: {resultado['pontos']}/{resultado['pontos_max']} "
            f"({resultado['pct_pontos']}%) · Tempo: {format_tempo(resultado['tempo_total'])}"
        )
        if resultado.get("respondidas", 0) < resultado["total"]:
            st.warning(
                f"{resultado['total'] - resultado['respondidas']} questão(ões) em branco — "
                "contam como erro no resultado."
            )
        det = pd.DataFrame(resultado["detalhe"])
        st.dataframe(det, width=W, hide_index=True)
        if not det.empty:
            st.plotly_chart(
                fig_radar_disciplinas(carregar_historico(), template, tc),
                width=W,
                key="resultado_radar",
            )
        if st.button("Novo simulado"):
            st.session_state["sessao"] = None
            st.session_state["resultado"] = None
            st.session_state["prova_t0"] = None
            st.session_state["questao_t0"] = None
            st.rerun()

elif pagina == "Análise":
    if hist.empty:
        st.info("Sem histórico. Conclua um simulado primeiro.")
    else:
        st.plotly_chart(fig_heatmap_topicos(hist, template, tc), width=W, key="analise_heat")
        st.plotly_chart(fig_radar_disciplinas(hist, template, tc), width=W, key="analise_radar")
        st.plotly_chart(fig_tempo_vs_acerto(hist, template, tc), width=W, key="analise_scatter")
        st.subheader("Desempenho por disciplina")
        st.dataframe(por_disciplina(hist), width=W, hide_index=True)
        st.subheader("Tópicos mais críticos")
        st.dataframe(top_criticos(hist, 10), width=W, hide_index=True)

elif pagina == "Plano de estudo":
    plano = gerar_plano(hist, dias=14, questoes_por_dia=20)
    st.write(f"**Nível geral:** {plano['nivel_geral']}")
    st.write(plano["orientacao"])
    pri, cal = plano_para_dataframe(plano)
    st.subheader("Prioridades")
    st.dataframe(pri, width=W, hide_index=True)
    st.subheader("Calendário (14 dias) + revisão espaçada")
    st.dataframe(cal, width=W, hide_index=True)
    if not pri.empty and "disciplina" in pri.columns:
        foco = pri.iloc[0]
        st.subheader("Sugestão de questões para hoje")
        sug = sugerir_questoes(foco.get("disciplina"), foco.get("topico"), n=8)
        st.dataframe(sug, width=W, hide_index=True)

elif pagina == "Banco de questões":
    st.subheader("Importar questões (JSON ou Excel)")
    up = st.file_uploader("Arquivo legal próprio", type=["json", "xlsx"])
    if up and st.button("Importar arquivo"):
        try:
            n = importar_upload(up)
            st.success(f"Banco agora com {n} questões")
            st.rerun()
        except Exception as e:
            st.error(str(e))

    with connect() as conn:
        df = pd.read_sql_query(
            """
            SELECT id, ano, banca, disciplina, topico, dificuldade, peso, prova_ref, cargo,
                   substr(enunciado, 1, 140) AS enunciado
            FROM questoes
            ORDER BY ano DESC, disciplina, id
            """,
            conn,
        )
    f1, f2, f3 = st.columns(3)
    anos = ["Todos"] + sorted([int(a) for a in df["ano"].dropna().unique()], reverse=True)
    ano_f = f1.selectbox("Ano", anos)
    discs = ["Todas"] + sorted(df["disciplina"].unique().tolist())
    disc_f = f2.selectbox("Disciplina", discs)
    pesos = ["Todos", 1, 2]
    peso_f = f3.selectbox("Peso", pesos)
    view = df.copy()
    if ano_f != "Todos":
        view = view[view["ano"] == ano_f]
    if disc_f != "Todas":
        view = view[view["disciplina"] == disc_f]
    if peso_f != "Todos":
        view = view[view["peso"] == peso_f]
    st.caption(
        "Questões didáticas originais no estilo FCC/TRT4. "
        "Enunciados oficiais da banca são protegidos por direitos autorais."
    )
    st.dataframe(view, width=W, hide_index=True)
