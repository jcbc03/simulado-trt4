# Simulador TRT4 — Fundação Carlos Chagas (FCC)

App desktop/local **100% offline** para treino no formato das provas do TRT da 4ª Região (FCC): cronômetro por questão, mapa de desempenho e plano de nivelamento.

## Como rodar

```bash
pip install -r requirements.txt
python -m modules.importar_questoes
streamlit run app.py
```

A interface abre no navegador.

## Formato FCC

- 60 questões no modo completo
- 30 Conhecimentos Gerais (peso 1)
- 30 Conhecimentos Específicos (peso 2)
- Tempo por questão + histórico em SQLite

## Conteúdo das questões

O banco inclui **questões didáticas originais** no estilo de cobrança FCC/TRT4, classificadas por ano-referência (2022, 2015, 2011, 2006, 2009) e disciplina. Enunciados oficiais da FCC são protegidos por direitos autorais — use o importador para acrescentar um JSON próprio obtido legalmente.

## Estrutura

- `app.py` — interface Streamlit
- `modules/` — simulador, análise, plano, importação
- `data/schema.sql` — schema SQLite
- `docs/` — Passo 0 (skills/provas) e orientação dos subagentes

## Temas

Claro e escuro na barra lateral.
