# Orientação dos 5 subagentes internos

## 1 — Banco de Dados e Questões
- `data/schema.sql`, `data/questoes_iniciais.json`, `modules/importar_questoes.py`, `modules/db.py`
- Popular SQLite offline; commit após concluir

## 2 — Motor de Simulado e Cronômetro
- `modules/simulador.py`
- Modos: completo 60q, disciplina, erros, revisão, prova antiga
- Tempo por questão + prova; marcar revisão; histórico

## 3 — Análise de Desempenho + Mapa
- `modules/analise.py`
- Acerto/tempo por disciplina e tópico; gargalos; Plotly; top 10 críticos

## 4 — Plano de Nivelamento
- `modules/plano_estudo.py`
- Prioridade baixo acerto + alto tempo; trilhas; revisão espaçada

## 5 — Interface e Integração
- `app.py` Streamlit; tema claro/escuro; dashboard; `requirements.txt`
- verify-and-stop + commit/push final
