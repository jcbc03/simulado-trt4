from __future__ import annotations

import sys
import time
from pathlib import Path

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
from modules.db import DB_PATH, count_questoes, init_db
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


def apply_theme(tema: str) -> None:
    plotly_template = "plotly_white" if tema == "Claro" else "plotly_dark"
    st.session_state["plotly_template"] = plotly_template
    if tema == "Escuro":
        st.markdown(
            """
            <style>
            .stApp { background: linear-gradient(180deg, #0a121b 0%, #122233 100%); color: #e8eef5; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
              background:
                radial-gradient(900px 500px at 100% 0%, rgba(196,149,74,0.12), transparent 40%),
                linear-gradient(180deg, #fbf7f0 0%, #eef3f7 100%);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


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


bootstrap()
load_css()

with st.sidebar:
    st.markdown("### Simulador TRT4")
    st.caption("FCC · 100% offline · SQLite")
    tema = st.radio("Tema", ["Claro", "Escuro"], horizontal=True)
    pagina = st.radio(
        "Navegação",
        ["Dashboard", "Simulado", "Análise", "Plano de estudo", "Banco de questões"],
    )
    st.divider()
    st.metric("Questões no banco", count_questoes())
    st.metric("Arquivo DB", DB_PATH.name)
    if st.button("Reimportar banco padrão"):
        n = importar_padrao(regenerar_json=True)
        st.success(f"Importadas {n} questões")
        st.rerun()

apply_theme(tema)
template = st.session_state.get("plotly_template", "plotly_white")

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
        st.plotly_chart(fig_radar_disciplinas(hist, template), use_container_width=True)
    with right:
        st.plotly_chart(fig_tempo_vs_acerto(hist, template), use_container_width=True)

    st.subheader("Top 10 tópicos críticos")
    crit = top_criticos(hist, 10)
    if crit.empty:
        st.info("Faça um simulado para gerar o mapa de pontos fortes e fracos.")
    else:
        st.dataframe(crit, use_container_width=True, hide_index=True)

elif pagina == "Simulado":
    if "sessao" not in st.session_state:
        st.session_state["sessao"] = None
        st.session_state["resultado"] = None

    with st.expander("Configurar novo simulado", expanded=st.session_state["sessao"] is None):
        modo = st.selectbox(
            "Modo",
            ["completo", "disciplina", "prova_antiga", "erros", "revisao"],
            format_func=lambda m: {
                "completo": "Simulado completo (60q)",
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
                start_timer()
                st.rerun()
            except Exception as e:
                st.error(str(e))

    sess = st.session_state.get("sessao")
    if sess and not sess.finalizada:
        q = questao_atual(sess)
        total = len(sess.questoes)
        st.progress((sess.indice + 1) / total, text=f"Questão {sess.indice + 1} de {total}")
        cols = st.columns(4)
        cols[0].write(f"**Disciplina:** {q.disciplina}")
        cols[1].write(f"**Tópico:** {q.topico}")
        cols[2].write(f"**Peso:** {q.peso}")
        cols[3].write(f"**Ano/banca:** {q.ano or '—'} / {q.banca}")

        st.markdown(f'<div class="questao-box">{q.enunciado}</div>', unsafe_allow_html=True)
        opcoes = [f"{k}) {v}" for k, v in q.alternativas.items()]
        labels = list(q.alternativas.keys())
        idx = labels.index(q.resposta) if q.resposta in labels else None
        escolha = st.radio(
            "Alternativas",
            options=labels,
            format_func=lambda k: f"{k}) {q.alternativas[k]}",
            index=idx,
            key=f"resp_{sess.sessao_id}_{sess.indice}",
        )
        marcar = st.checkbox("Marcar para revisão", value=q.marcada_revisao)

        b1, b2, b3, b4, b5 = st.columns(5)
        if b1.button("⟵ Anterior"):
            flush_tempo()
            responder(sess, escolha)
            marcar_revisao(sess, marcar)
            anterior(sess)
            start_timer()
            st.rerun()
        if b2.button("Próxima ⟶"):
            flush_tempo()
            responder(sess, escolha)
            marcar_revisao(sess, marcar)
            proxima(sess)
            start_timer()
            st.rerun()
        destino = b3.number_input("Ir para", min_value=1, max_value=total, value=sess.indice + 1)
        if b4.button("Ir"):
            flush_tempo()
            responder(sess, escolha)
            marcar_revisao(sess, marcar)
            navegar(sess, int(destino) - 1)
            start_timer()
            st.rerun()
        if b5.button("Finalizar e ver gabarito", type="primary"):
            flush_tempo()
            responder(sess, escolha)
            marcar_revisao(sess, marcar)
            st.session_state["resultado"] = finalizar(sess)
            st.rerun()

        rev = [i + 1 for i, qq in enumerate(sess.questoes) if qq.marcada_revisao]
        if rev:
            st.caption(f"Marcadas para revisão: {rev}")

    resultado = st.session_state.get("resultado")
    if resultado:
        st.success(
            f"Acertos: {resultado['acertos']}/{resultado['total']} "
            f"({resultado['pct_acerto']}%) · Pontos: {resultado['pontos']}/{resultado['pontos_max']} "
            f"({resultado['pct_pontos']}%) · Tempo: {resultado['tempo_total']}s"
        )
        st.dataframe(resultado["detalhe"], use_container_width=True, hide_index=True)
        if st.button("Novo simulado"):
            st.session_state["sessao"] = None
            st.session_state["resultado"] = None
            st.rerun()

elif pagina == "Análise":
    if hist.empty:
        st.info("Sem histórico. Conclua um simulado primeiro.")
    else:
        st.plotly_chart(fig_heatmap_topicos(hist, template), use_container_width=True)
        st.plotly_chart(fig_radar_disciplinas(hist, template), use_container_width=True)
        st.plotly_chart(fig_tempo_vs_acerto(hist, template), use_container_width=True)
        st.subheader("Desempenho por disciplina")
        st.dataframe(por_disciplina(hist), use_container_width=True, hide_index=True)
        st.subheader("Tópicos mais críticos")
        st.dataframe(top_criticos(hist, 10), use_container_width=True, hide_index=True)

elif pagina == "Plano de estudo":
    plano = gerar_plano(hist, dias=14, questoes_por_dia=20)
    st.write(f"**Nível geral:** {plano['nivel_geral']}")
    st.write(plano["orientacao"])
    pri, cal = plano_para_dataframe(plano)
    st.subheader("Prioridades")
    st.dataframe(pri, use_container_width=True, hide_index=True)
    st.subheader("Calendário (14 dias) + revisão espaçada")
    st.dataframe(cal, use_container_width=True, hide_index=True)
    if not pri.empty and "disciplina" in pri.columns:
        foco = pri.iloc[0]
        st.subheader("Sugestão de questões para hoje")
        sug = sugerir_questoes(foco.get("disciplina"), foco.get("topico"), n=8)
        st.dataframe(sug, use_container_width=True, hide_index=True)

elif pagina == "Banco de questões":
    import pandas as pd
    from modules.db import connect

    with connect() as conn:
        df = pd.read_sql_query(
            """
            SELECT id, ano, banca, disciplina, topico, dificuldade, peso, prova_ref, cargo,
                   substr(enunciado, 1, 120) AS enunciado
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
        "Enunciados oficiais da banca são protegidos; importe seu JSON/Excel legal se desejar."
    )
    st.dataframe(view, use_container_width=True, hide_index=True)
