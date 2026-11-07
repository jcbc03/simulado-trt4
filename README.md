# Simulador TRT4 — Fundação Carlos Chagas (FCC)

App desktop/local **100% offline** para treino no formato das provas do TRT da 4ª Região (FCC): cronômetro por questão, mapa de desempenho e plano de nivelamento.

## Instalação completa (Windows)

1. Baixe/extraia o pacote `dist/SimuladorTRT4-Instalador.zip`
2. Execute **`instalar.bat`** (sem perguntas)
3. O instalador:
   - copia para `%LOCALAPPDATA%\SimuladorTRT4`
   - cria ambiente virtual e instala dependências
   - gera o banco de questões
   - cria o atalho **Simulador TRT4** na Área de Trabalho (e no Menu Iniciar)
   - abre o app no navegador

Desinstalar: `%LOCALAPPDATA%\SimuladorTRT4\desinstalar.bat`

Para gerar o ZIP de distribuição de novo:

```bash
powershell -ExecutionPolicy Bypass -File scripts/empacotar.ps1
```

## Desenvolvimento local

```bash
pip install -r requirements.txt
python -m modules.importar_questoes
streamlit run app.py
```

Ou duplo clique em `run.bat`. Abre em http://localhost:8600

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
