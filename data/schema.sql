PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS topicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    pai TEXT,
    peso_edital REAL DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enunciado TEXT NOT NULL,
    alt_a TEXT NOT NULL,
    alt_b TEXT NOT NULL,
    alt_c TEXT NOT NULL,
    alt_d TEXT NOT NULL,
    alt_e TEXT NOT NULL,
    gabarito TEXT NOT NULL CHECK (gabarito IN ('A','B','C','D','E')),
    disciplina TEXT NOT NULL,
    topico TEXT NOT NULL,
    subtopico TEXT,
    dificuldade INTEGER DEFAULT 2 CHECK (dificuldade BETWEEN 1 AND 5),
    ano INTEGER,
    banca TEXT DEFAULT 'FCC',
    tempo_medio_esperado INTEGER DEFAULT 90,
    peso INTEGER DEFAULT 1 CHECK (peso IN (1, 2)),
    prova_ref TEXT,
    cargo TEXT DEFAULT 'Técnico Judiciário - Área Administrativa'
);

CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_questao INTEGER NOT NULL,
    resposta_usuario TEXT,
    correta INTEGER NOT NULL CHECK (correta IN (0, 1)),
    tempo_segundos REAL NOT NULL DEFAULT 0,
    data_hora TEXT NOT NULL,
    sessao_id TEXT,
    modo TEXT,
    FOREIGN KEY (id_questao) REFERENCES questoes(id)
);

CREATE INDEX IF NOT EXISTS idx_questoes_disciplina ON questoes(disciplina);
CREATE INDEX IF NOT EXISTS idx_questoes_ano ON questoes(ano);
CREATE INDEX IF NOT EXISTS idx_historico_questao ON historico(id_questao);
CREATE INDEX IF NOT EXISTS idx_historico_sessao ON historico(sessao_id);
