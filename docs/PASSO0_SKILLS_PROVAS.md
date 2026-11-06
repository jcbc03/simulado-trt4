# Passo 0 — Skills, hooks e provas TRT4/FCC

## Skills e modos selecionados

| Ferramenta / modo | Uso neste projeto |
|---|---|
| **lean-build** | Construção do app de ponta a ponta, escopo fechado |
| **ponytail** | Menor mudança completa; sem overengineering |
| **caveman** | Respostas curtas sem perder precisão |
| **coding-tools-policy** | Escolher ferramenta só quando útil |
| **verify-and-stop** | Validar `streamlit run` e parar |
| **Codesight** | Adiado: repositório iniciou vazio |
| **Graphify** | Atualizar após módulos existirem |
| **RTK hook** | Já ativo em Shell (`rtk hook cursor`) |
| **Grok Build** | Só se ambiente autorizado e útil |

## Hooks relevantes

- `~/.cursor/hooks.json` → `preToolUse` Shell com `rtk hook cursor`

## Catálogo de provas anteriores TRT4 (referência)

Fontes públicas de índice (downloads oficiais: FCC / TRT4):

| Ano | Banca | Cargos principais |
|---|---|---|
| 2022 | FCC | Técnico Adm.; Analista Jud./Adm./TI e especialidades |
| 2015 | FCC | Analista Jud./Adm./TI/OJAF; Técnico Adm./TI |
| 2012 | FCC | Arquivologia, Eng. Civil, Psiquiatria, Juiz |
| 2011 | FCC | Analista Jud./Adm./Contab./OJAF/TI; Técnico Adm./TI/Enf. |
| 2009 | FCC | Comunicação, Engenharia, Estatística, Psicologia |
| 2006 | FCC | Analista Jud./Adm. e várias especialidades; Técnico Adm. |

Formato típico FCC (servidores): **60 questões objetivas** — 30 Gerais (peso 1) + 30 Específicas (peso 2).

## Política de conteúdo das questões

Enunciados oficiais da FCC são protegidos por direitos autorais. Este repositório inclui:

1. **Questões originais didáticas** no estilo de cobrança FCC/TRT, classificadas por disciplina, tópico, ano-referência e banca.
2. Metadados `ano` / `banca` / `prova_ref` para treino no formato das provas listadas acima.
3. Importador pronto para o usuário acrescentar seu próprio banco (JSON/Excel) obtido legalmente.

Matérias priorizadas: Português, Matemática/RLM, Legislação, Direitos Humanos, Informática, Direito do Trabalho, Processual do Trabalho, Administrativo, Constitucional.
