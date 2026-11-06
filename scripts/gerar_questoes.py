"""Gera banco didático original estilo FCC/TRT4 (não copia enunciados oficiais)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "questoes_iniciais.json"


def q(
    enunciado: str,
    alts: list[str],
    gab: str,
    disciplina: str,
    topico: str,
    *,
    sub: str = "",
    dif: int = 2,
    ano: int = 2022,
    peso: int = 1,
    tempo: int = 90,
    prova: str = "TRT4 estilo FCC",
    cargo: str = "Técnico Judiciário - Área Administrativa",
) -> dict:
    a, b, c, d, e = alts
    return {
        "enunciado": enunciado,
        "alt_a": a,
        "alt_b": b,
        "alt_c": c,
        "alt_d": d,
        "alt_e": e,
        "gabarito": gab.upper(),
        "disciplina": disciplina,
        "topico": topico,
        "subtopico": sub or topico,
        "dificuldade": dif,
        "ano": ano,
        "banca": "FCC",
        "tempo_medio_esperado": tempo,
        "peso": peso,
        "prova_ref": prova,
        "cargo": cargo,
    }


def build() -> list[dict]:
    qs: list[dict] = []

    # ——— Língua Portuguesa (peso 1) ———
    port = [
        q(
            "No trecho “Embora o servidor tenha se esforçado, o prazo não foi cumprido”, a oração iniciada por “Embora” expressa ideia de:",
            ["causa", "concessão", "finalidade", "proporção", "comparação"],
            "B", "Língua Portuguesa", "Sintaxe", sub="Conectivos", ano=2022, dif=2,
        ),
        q(
            "Assinale a alternativa em que a concordância verbal está de acordo com a norma-padrão.",
            [
                "Fazem dois anos que o edital foi publicado.",
                "Houveram várias irregularidades no processo.",
                "Faz dois anos que o edital foi publicado.",
                "Existe muitas dúvidas sobre o cronograma.",
                "Bateu três horas no relógio da sala.",
            ],
            "C", "Língua Portuguesa", "Concordância", ano=2022, dif=2,
        ),
        q(
            "Em “O juiz determinou que se cumprisse a decisão”, a partícula “se” indica:",
            ["voz passiva sintética", "índice de indeterminação do sujeito", "pronome reflexivo", "conjunção integrante", "partícula expletiva"],
            "A", "Língua Portuguesa", "Pronomes", sub="Partícula se", ano=2015, dif=3,
        ),
        q(
            "A crase está corretamente empregada em:",
            [
                "Referiu-se àquela norma regulamentar.",
                "Chegou à tempo para a audiência.",
                "Vou à Porto Alegre amanhã.",
                "Assistiu à uma palestra.",
                "Deu preferência à ela.",
            ],
            "A", "Língua Portuguesa", "Ortografia e acentuação", sub="Crase", ano=2015, dif=2,
        ),
        q(
            "No período “O relatório que o analista elaborou foi arquivado”, o termo “que” classifica-se como:",
            ["conjunção integrante", "pronome relativo", "advérbio", "preposição", "interjeição"],
            "B", "Língua Portuguesa", "Sintaxe", sub="Pronome relativo", ano=2011, dif=1,
        ),
        q(
            "Assinale a opção em que o emprego da vírgula está correto.",
            [
                "O técnico, que chegou cedo iniciou o plantão.",
                "Ontem, o servidor protocolou o recurso.",
                "A prova objetiva, foi aplicada em julho.",
                "Quem estuda, passa, com certeza, sempre.",
                "O gabarito preliminar, saiu ontem à noite.",
            ],
            "B", "Língua Portuguesa", "Pontuação", ano=2011, dif=2,
        ),
        q(
            "A regência verbal está correta em:",
            [
                "O servidor aspirava o cargo de analista.",
                "Assistimos o julgamento com atenção.",
                "Obedeceram as normas internas do tribunal.",
                "Preferiu estudar do que descansar.",
                "O chefe simpatiza com a proposta apresentada.",
            ],
            "E", "Língua Portuguesa", "Regência", ano=2006, dif=3,
        ),
        q(
            "Em interpretação de texto, o sentido denotativo corresponde a:",
            [
                "sentido figurado e subjetivo",
                "sentido literal e objetivo",
                "ironia contextual",
                "ambiguidade proposital",
                "metáfora estendida",
            ],
            "B", "Língua Portuguesa", "Interpretação de texto", ano=2022, dif=1,
        ),
        q(
            "Assinale a alternativa em que todas as palavras estão grafadas corretamente.",
            [
                "excessão, assensão, previlégio",
                "exceção, ascensão, privilégio",
                "excessão, ascensão, privilégio",
                "exceção, assensão, previlégio",
                "exessão, ascenção, privilegio",
            ],
            "B", "Língua Portuguesa", "Ortografia e acentuação", ano=2006, dif=2,
        ),
        q(
            "O sujeito da oração “É necessário cumprir o edital” é:",
            ["oculto", "inexistente", "oracional", "composto", "indeterminado"],
            "C", "Língua Portuguesa", "Sintaxe", sub="Tipos de sujeito", ano=2015, dif=3,
        ),
        q(
            "Em “Não obstante as críticas, o projeto avançou”, a expressão destacada introduz ideia de:",
            ["conclusão", "explicação", "concessão", "adição", "tempo"],
            "C", "Língua Portuguesa", "Sintaxe", sub="Conectivos", ano=2022, dif=2,
        ),
        q(
            "A colocação pronominal está adequada em:",
            [
                "Me entregue o processo agora.",
                "Entregar-me-ão o processo amanhã.",
                "Nunca se falou sobre isso na reunião.",
                "Se precisa de ajuda, avise.",
                "Diria-se que a decisão foi justa.",
            ],
            "C", "Língua Portuguesa", "Pronomes", sub="Colocação", ano=2011, dif=3,
        ),
        q(
            "Quanto à tipicidade textual, um edital de concurso é predominantemente:",
            ["narrativo", "descritivo literário", "injuntivo/prescritivo", "poético", "dialógico"],
            "C", "Língua Portuguesa", "Interpretação de texto", sub="Tipologia", ano=2015, dif=2,
        ),
        q(
            "Assinale a alternativa em que há erro de paralelismo sintático.",
            [
                "O cargo exige disciplina, organização e responsabilidade.",
                "É preciso estudar, revisar e praticar.",
                "O servidor deve ser pontual, ético e trabalhar com zelo.",
                "A banca cobrou português, lógica e informática.",
                "O plano inclui leitura, resumos e simulados.",
            ],
            "C", "Língua Portuguesa", "Sintaxe", sub="Paralelismo", ano=2006, dif=3,
        ),
        q(
            "Em “Havia candidatos na sala”, o verbo “haver” está empregado como:",
            ["auxiliar", "impessoal com sentido de existir", "pessoal transitivo direto", "ligação", "pronominal"],
            "B", "Língua Portuguesa", "Concordância", ano=2022, dif=2,
        ),
    ]
    qs.extend(port)

    # ——— Matemática / RLM ———
    mat = [
        q(
            "Em uma prova com 60 questões, um candidato acertou 75%. Quantas questões acertou?",
            ["40", "42", "45", "48", "50"],
            "C", "Matemática e Raciocínio Lógico", "Porcentagem", ano=2022, dif=1, tempo=60,
        ),
        q(
            "Se 3 analistas concluem um serviço em 8 dias, em quantos dias 6 analistas iguais concluem o mesmo serviço?",
            ["2", "3", "4", "6", "8"],
            "C", "Matemática e Raciocínio Lógico", "Proporcionalidade", ano=2022, dif=2, tempo=75,
        ),
        q(
            "A sequência 2, 5, 10, 17, 26, … segue um padrão. O próximo termo é:",
            ["35", "37", "38", "39", "41"],
            "B", "Matemática e Raciocínio Lógico", "Sequências", ano=2015, dif=2, tempo=70,
        ),
        q(
            "Se todo A é B e algum B é C, então é necessariamente verdadeiro que:",
            [
                "todo A é C",
                "algum A é C",
                "nenhum A é C",
                "algum A pode não ser C",
                "todo C é A",
            ],
            "D", "Matemática e Raciocínio Lógico", "Lógica proposicional", ano=2015, dif=3, tempo=90,
        ),
        q(
            "A negação de “Todo servidor é pontual” é:",
            [
                "Nenhum servidor é pontual",
                "Todo servidor não é pontual",
                "Algum servidor não é pontual",
                "Algum servidor é pontual",
                "Nenhum servidor não é pontual",
            ],
            "C", "Matemática e Raciocínio Lógico", "Lógica proposicional", sub="Negação", ano=2011, dif=2,
        ),
        q(
            "Um capital de R$ 2.000,00 rende juros simples de 1% ao mês. Após 5 meses, o montante é:",
            ["R$ 2.050,00", "R$ 2.100,00", "R$ 2.150,00", "R$ 2.200,00", "R$ 2.500,00"],
            "B", "Matemática e Raciocínio Lógico", "Juros", ano=2011, dif=2, tempo=80,
        ),
        q(
            "Em um conjunto de 5 números, a média aritmética é 12. Se quatro números somam 40, o quinto é:",
            ["16", "18", "20", "22", "24"],
            "C", "Matemática e Raciocínio Lógico", "Estatística básica", ano=2006, dif=1, tempo=60,
        ),
        q(
            "Se p → q é falsa, então:",
            ["p falsa e q verdadeira", "p verdadeira e q falsa", "ambas falsas", "ambas verdadeiras", "p falsa e q falsa"],
            "B", "Matemática e Raciocínio Lógico", "Lógica proposicional", ano=2006, dif=2,
        ),
        q(
            "Uma urna tem 4 bolas azuis e 6 vermelhas. A probabilidade de retirar uma azul (sem reposição, 1ª retirada) é:",
            ["2/5", "3/5", "4/6", "1/2", "2/3"],
            "A", "Matemática e Raciocínio Lógico", "Probabilidade", ano=2022, dif=2, tempo=70,
        ),
        q(
            "O número de anagramas distintos da palavra TRT (considerando letras distintas por posição das T iguais) é:",
            ["3", "4", "6", "9", "27"],
            "A", "Matemática e Raciocínio Lógico", "Combinatória", ano=2015, dif=3, tempo=90,
        ),
        q(
            "Se 20% de X = 40, então X vale:",
            ["80", "100", "160", "200", "400"],
            "D", "Matemática e Raciocínio Lógico", "Porcentagem", ano=2011, dif=1, tempo=45,
        ),
        q(
            "Em uma progressão aritmética com a1 = 3 e razão 4, o 6º termo é:",
            ["19", "21", "23", "25", "27"],
            "C", "Matemática e Raciocínio Lógico", "Sequências", ano=2006, dif=2, tempo=60,
        ),
        q(
            "A equivalente de ∼(p ∧ q) é:",
            ["∼p ∧ ∼q", "∼p ∨ ∼q", "p ∨ q", "p ∧ ∼q", "∼p ∧ q"],
            "B", "Matemática e Raciocínio Lógico", "Lógica proposicional", sub="De Morgan", ano=2022, dif=3,
        ),
        q(
            "Um retângulo de lados 8 e 5 tem perímetro igual a:",
            ["13", "26", "40", "45", "80"],
            "B", "Matemática e Raciocínio Lógico", "Geometria", ano=2015, dif=1, tempo=45,
        ),
        q(
            "Se A está para B assim como 2 está para 5, e A = 10, então B é:",
            ["4", "15", "20", "25", "50"],
            "D", "Matemática e Raciocínio Lógico", "Proporcionalidade", ano=2006, dif=1, tempo=50,
        ),
    ]
    qs.extend(mat)

    # ——— Legislação ———
    leg = [
        q(
            "Nos termos da Constituição Federal, são direitos sociais, entre outros:",
            [
                "propriedade e herança",
                "educação, saúde e trabalho",
                "apenas liberdade de locomoção",
                "somente direitos políticos",
                "apenas a livre iniciativa",
            ],
            "B", "Noções de Legislação", "Constituição Federal", sub="Direitos sociais", ano=2022, dif=1,
        ),
        q(
            "O concurso público, em regra, é exigido para investidura em cargo público efetivo, conforme:",
            ["apenas lei estadual", "CF/88", "apenas regimento interno", "ato do presidente do tribunal", "contrato administrativo"],
            "B", "Noções de Legislação", "Constituição Federal", sub="Administração Pública", ano=2022, dif=1,
        ),
        q(
            "A estabilidade do servidor público estatutário, em regra, exige:",
            [
                "1 ano de efetivo exercício",
                "2 anos de efetivo exercício",
                "3 anos de efetivo exercício",
                "5 anos de efetivo exercício",
                "aprovação em qualquer estágio",
            ],
            "C", "Noções de Legislação", "Servidores públicos", ano=2015, dif=2,
        ),
        q(
            "São poderes da União, independentes e harmônicos entre si:",
            [
                "somente Executivo e Legislativo",
                "Legislativo, Executivo e Judiciário",
                "Executivo, Ministério Público e Defensoria",
                "Judiciário e Tribunais de Contas",
                "Presidência e Congresso apenas",
            ],
            "B", "Noções de Legislação", "Constituição Federal", sub="Organização do Estado", ano=2015, dif=1,
        ),
        q(
            "A Justiça do Trabalho é órgão do Poder:",
            ["Executivo", "Legislativo", "Judiciário", "Ministério Público", "Tribunal de Contas"],
            "C", "Noções de Legislação", "Organização judiciária", ano=2011, dif=1,
        ),
        q(
            "O habeas corpus protege, em essência, a:",
            ["intimidade", "liberdade de locomoção", "propriedade", "honra objetiva", "liberdade religiosa apenas"],
            "B", "Noções de Legislação", "Remédios constitucionais", ano=2011, dif=2,
        ),
        q(
            "Mandado de segurança exige, em regra, direito líquido e certo não amparado por:",
            ["ação popular", "habeas corpus ou habeas data", "ação civil pública", "recurso ordinário", "reclamação"],
            "B", "Noções de Legislação", "Remédios constitucionais", ano=2006, dif=3,
        ),
        q(
            "A República Federativa do Brasil é formada pela união indissolúvel dos:",
            [
                "Estados e Municípios apenas",
                "Estados, Municípios e Distrito Federal",
                "Estados, Municípios e Territórios",
                "Estados e Distrito Federal apenas",
                "apenas da União e Estados",
            ],
            "B", "Noções de Legislação", "Constituição Federal", ano=2006, dif=2,
        ),
        q(
            "No âmbito da ética no serviço público, o servidor deve, entre outros deveres:",
            [
                "usar cargo para benefício próprio",
                "atuar com honestidade e urbanidade",
                "omitir informações públicas sem motivo",
                "favorecer parentes em licitações",
                "divulgar sigilo funcional",
            ],
            "B", "Noções de Legislação", "Ética no serviço público", ano=2022, dif=1,
        ),
        q(
            "A Lei de Acesso à Informação (LAI) tem como diretriz a:",
            [
                "publicidade como regra e sigilo como exceção",
                "sigilo como regra absoluta",
                "acesso apenas judicial",
                "vedação total a dados pessoais",
                "publicidade apenas de atos secretos",
            ],
            "A", "Noções de Legislação", "Transparência", ano=2015, dif=2,
        ),
    ]
    qs.extend(leg)

    # ——— Direitos Humanos ———
    dh = [
        q(
            "A Declaração Universal dos Direitos Humanos foi adotada pela ONU em:",
            ["1919", "1945", "1948", "1966", "1988"],
            "C", "Noções de Direitos Humanos", "Sistema internacional", ano=2022, dif=1,
        ),
        q(
            "São características clássicas dos direitos humanos, entre outras:",
            [
                "relatividade absoluta e alienabilidade",
                "universalidade e indivisibilidade",
                "exclusividade estatal",
                "disponibilidade irrestrita",
                "aplicação só a nacionais",
            ],
            "B", "Noções de Direitos Humanos", "Fundamentos", ano=2022, dif=2,
        ),
        q(
            "A Convenção Americana sobre Direitos Humanos é conhecida como:",
            ["Pacto de San José da Costa Rica", "Pacto de Nova York", "Carta de Bogotá apenas", "Tratado de Roma", "Protocolo de Kyoto"],
            "A", "Noções de Direitos Humanos", "Sistema interamericano", ano=2015, dif=2,
        ),
        q(
            "No Brasil, tratados de direitos humanos aprovados com rito equivalente a emenda constitucional têm status de:",
            ["lei ordinária", "lei complementar", "norma constitucional", "decreto regulamentar", "portaria ministerial"],
            "C", "Noções de Direitos Humanos", "Hierarquia normativa", ano=2015, dif=3,
        ),
        q(
            "A dignidade da pessoa humana, na CF/88, figura como:",
            ["objetivo da ordem econômica apenas", "fundamento da República", "princípio exclusivo do processo penal", "meta do Poder Legislativo", "regra de transição"],
            "B", "Noções de Direitos Humanos", "Constituição e DH", ano=2011, dif=1,
        ),
        q(
            "O princípio da não discriminação veda, em regra, distinções injustificadas baseadas em:",
            ["mérito profissional", "raça, sexo, religião, origem etc.", "capacidade técnica", "experiência comprovada", "titulação acadêmica"],
            "B", "Noções de Direitos Humanos", "Igualdade", ano=2011, dif=1,
        ),
        q(
            "Órgão do sistema interamericano que analisa petições individuais é a:",
            ["ONU-Habitat", "Comissão Interamericana de Direitos Humanos", "OMC", "OIT apenas", "UNESCO"],
            "B", "Noções de Direitos Humanos", "Sistema interamericano", ano=2006, dif=2,
        ),
        q(
            "Direitos humanos de primeira geração relacionam-se historicamente a:",
            ["direitos sociais", "direitos civis e políticos", "direitos ambientais", "direitos difusos apenas", "direitos econômicos coletivos"],
            "B", "Noções de Direitos Humanos", "Gerações/dimensões", ano=2006, dif=2,
        ),
    ]
    qs.extend(dh)

    # ——— Informática ———
    info = [
        q(
            "No Windows, a combinação Ctrl+C normalmente:",
            ["cola", "recorta", "copia", "desfaz", "salva"],
            "C", "Noções de Informática", "Sistemas operacionais", ano=2022, dif=1, tempo=45,
        ),
        q(
            "Em planilhas, a função que soma um intervalo é:",
            ["MÉDIA", "CONT.NÚM", "SOMA", "SE", "PROCV"],
            "C", "Noções de Informática", "Planilhas", ano=2022, dif=1, tempo=40,
        ),
        q(
            "Phishing é tipicamente:",
            [
                "atualização legítima de antivírus",
                "técnica de engenharia social para capturar dados",
                "backup automático em nuvem",
                "compactação de arquivos",
                "protocolo de rede seguro",
            ],
            "B", "Noções de Informática", "Segurança da informação", ano=2015, dif=2,
        ),
        q(
            "HTTP e HTTPS diferem, em essência, porque HTTPS:",
            [
                "é mais lento sempre e sem criptografia",
                "usa criptografia (TLS) na comunicação",
                "não permite cookies",
                "só funciona em intranet",
                "substitui o DNS",
            ],
            "B", "Noções de Informática", "Internet", ano=2015, dif=2,
        ),
        q(
            "Backup completo copia:",
            ["apenas arquivos alterados desde o último diferencial", "todos os dados selecionados", "somente o sistema operacional", "apenas e-mails", "somente atalhos"],
            "B", "Noções de Informática", "Segurança da informação", sub="Backup", ano=2011, dif=1,
        ),
        q(
            "No Word, estilo de formatação que se aplica a parágrafos inteiros com um clique costuma ser gerido por:",
            ["macros VBA apenas", "Estilos", "hiperlinks", "comentários", "revisão ortográfica"],
            "B", "Noções de Informática", "Editor de texto", ano=2011, dif=1, tempo=50,
        ),
        q(
            "Um endereço IPv4 clássico possui:",
            ["32 bits", "64 bits", "128 bits", "16 bits", "256 bits"],
            "A", "Noções de Informática", "Redes", ano=2006, dif=2,
        ),
        q(
            "Extensão típica de planilha do Excel é:",
            [".docx", ".pptx", ".xlsx", ".pdf", ".txt"],
            "C", "Noções de Informática", "Planilhas", ano=2006, dif=1, tempo=30,
        ),
        q(
            "Autenticação de dois fatores (2FA) aumenta segurança porque:",
            [
                "elimina senhas",
                "exige segundo fator além da senha",
                "desativa antivírus",
                "abre todas as portas de rede",
                "compartilha credenciais",
            ],
            "B", "Noções de Informática", "Segurança da informação", ano=2022, dif=2,
        ),
        q(
            "Na nuvem, SaaS significa tipicamente:",
            ["Software como Serviço", "Servidor como Sistema", "Storage como Switch", "Security as Script", "System as Socket"],
            "A", "Noções de Informática", "Computação em nuvem", ano=2015, dif=2,
        ),
    ]
    qs.extend(info)

    # ——— Específicos (peso 2) ———
    esp_dt = [
        q(
            "São direitos dos trabalhadores urbanos e rurais, entre outros previstos na CF:",
            [
                "fundo de garantia apenas para comissionados",
                "salário mínimo, 13º e FGTS, nos termos da Constituição",
                "jornada semanal livre sem limite",
                "aviso prévio inexistente",
                "proibição absoluta de greve",
            ],
            "B", "Direito do Trabalho", "Direitos constitucionais do trabalho", peso=2, ano=2022, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "O contrato de trabalho por prazo determinado, em regra, não pode exceder:",
            ["6 meses", "1 ano", "2 anos", "3 anos", "5 anos"],
            "C", "Direito do Trabalho", "Contrato de trabalho", peso=2, ano=2022, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "A duração normal do trabalho, salvo exceções legais, não deve exceder:",
            ["6h diárias e 30 semanais", "8h diárias e 44 semanais", "10h diárias e 50 semanais", "4h diárias", "12h diárias contínuas"],
            "B", "Direito do Trabalho", "Jornada", peso=2, ano=2015, dif=1,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Férias anuais remuneradas, em regra, correspondem a:",
            ["15 dias", "20 dias", "30 dias", "45 dias", "60 dias"],
            "C", "Direito do Trabalho", "Férias", peso=2, ano=2015, dif=1,
            cargo="Técnico Judiciário - Área Administrativa",
        ),
        q(
            "O intervalo intrajornada para jornadas contínuas superiores a 6 horas é, em regra, de:",
            ["15 minutos", "no mínimo 1 hora e no máximo 2 horas", "3 horas fixas", "4 horas", "inexistente"],
            "B", "Direito do Trabalho", "Jornada", sub="Intervalos", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "A estabilidade provisória da gestante, em regra, vai da confirmação da gravidez até:",
            ["o parto", "30 dias após o parto", "5 meses após o parto", "1 ano após o parto", "o fim do contrato a termo"],
            "C", "Direito do Trabalho", "Estabilidade", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "FGTS é regido, em linhas gerais, pela legislação que institui o:",
            ["seguro-desemprego apenas", "fundo de garantia do tempo de serviço", "PIS/PASEP exclusivo", "INSS rural", "vale-transporte"],
            "B", "Direito do Trabalho", "FGTS", peso=2, ano=2006, dif=1,
            cargo="Técnico Judiciário - Área Administrativa",
        ),
        q(
            "Equiparação salarial exige, entre outros requisitos clássicos, identidade de função e trabalho de igual valor no mesmo:",
            ["país", "estabelecimento empresarial", "município apenas", "sindicato", "estado"],
            "B", "Direito do Trabalho", "Salário", peso=2, ano=2006, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "A rescisão indireta ocorre quando:",
            [
                "o empregado pede demissão sem motivo",
                "o empregador comete falta grave ensejando ruptura por iniciativa do empregado",
                "há acordo coletivo obrigatório",
                "o contrato é nulo ab initio",
                "há aposentadoria compulsória",
            ],
            "B", "Direito do Trabalho", "Rescisão", peso=2, ano=2022, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Horas extras habituais, em regra, integram o salário para fins de:",
            ["apenas INSS", "reflexos em DSR e demais parcelas salariais pertinentes", "somente FGTS", "nenhum reflexo", "apenas 13º"],
            "B", "Direito do Trabalho", "Jornada", sub="Horas extras", peso=2, ano=2015, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
    ]
    qs.extend(esp_dt)

    esp_pt = [
        q(
            "A Justiça do Trabalho é competente, em regra, para ações oriundas da relação de trabalho, nos termos da:",
            ["CF e legislação processual trabalhista", "apenas lei municipal", "Código Civil exclusivo", "CPC estadual", "CLT internacional"],
            "A", "Direito Processual do Trabalho", "Competência", peso=2, ano=2022, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "O prazo para contestação no rito ordinário trabalhista, em regra, é de:",
            ["5 dias", "10 dias", "15 dias a partir da notificação (regra clássica CLT)", "30 dias", "60 dias"],
            "C", "Direito Processual do Trabalho", "Prazos", peso=2, ano=2022, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Recurso ordinário no processo do trabalho, em regra, interposto contra decisões definitivas ou terminativas, tem prazo de:",
            ["5 dias", "8 dias", "10 dias", "15 dias", "30 dias"],
            "B", "Direito Processual do Trabalho", "Recursos", peso=2, ano=2015, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "O depósito recursal é, em regra, pressuposto de admissibilidade de recursos empresariais no processo do trabalho, salvo hipóteses legais de:",
            ["isenção/isenções legais e benesses processuais cabíveis", "sempre dispensa total", "substituição por fiança bancária obrigatória", "pagamento em espécie apenas", "garantia imobiliária exclusiva"],
            "A", "Direito Processual do Trabalho", "Recursos", peso=2, ano=2015, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "A execução trabalhista, em regra, promove-se de ofício ou a requerimento do interessado, conforme a sistemática da:",
            ["CLT", "apenas CPC", "Lei de Execução Fiscal exclusiva", "Código Penal", "ECA"],
            "A", "Direito Processual do Trabalho", "Execução", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "No rito sumaríssimo, em regra, o valor da causa não excede:",
            ["10 salários mínimos", "20 salários mínimos", "40 salários mínimos", "60 salários mínimos", "100 salários mínimos"],
            "C", "Direito Processual do Trabalho", "Ritos", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "A reclamação trabalhista pode ser apresentada:",
            ["apenas por advogado obrigatoriamente", "pelo próprio empregado, nos termos legais", "somente pelo sindicato", "apenas pelo MPT", "somente por preposto"],
            "B", "Direito Processual do Trabalho", "Petição inicial", peso=2, ano=2006, dif=1,
            cargo="Técnico Judiciário - Área Administrativa",
        ),
        q(
            "Audiência trabalhista, no modelo clássico, é una e contínua, podendo o juiz:",
            ["adiá-la sem motivação", "converter o julgamento em diligência quando necessário", "dispensar sempre a prova oral", "proibir acordo", "impedir preposto"],
            "B", "Direito Processual do Trabalho", "Audiência", peso=2, ano=2006, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
    ]
    qs.extend(esp_pt)

    esp_adm = [
        q(
            "São princípios expressos da Administração Pública na CF/88:",
            ["LIMPE (legalidade, impessoalidade, moralidade, publicidade, eficiência)", "apenas legalidade e eficiência", "somente publicidade", "autotutela exclusiva", "supremacia absoluta sem limites"],
            "A", "Direito Administrativo", "Princípios", peso=2, ano=2022, dif=1,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Ato administrativo vinculado é aquele em que a lei:",
            ["deixa ampla discricionariedade", "não deixa margem de escolha quanto aos elementos vinculados", "dispensa motivação sempre", "é sempre nulo", "depende só da vontade política"],
            "B", "Direito Administrativo", "Atos administrativos", peso=2, ano=2022, dif=2,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Licença para tratar de interesses particulares, em regra, é:",
            ["ato vinculado obrigatório", "ato discricionário", "direito subjetivo absoluto", "prêmio automático", "indenização compulsória"],
            "B", "Direito Administrativo", "Servidores", peso=2, ano=2015, dif=2,
            cargo="Técnico Judiciário - Área Administrativa",
        ),
        q(
            "A anulação do ato administrativo ilegal pela própria Administração fundamenta-se no poder de:",
            ["polícia apenas", "autotutela", "eminente domínio", "hierarquia exclusiva", "tutela política"],
            "B", "Direito Administrativo", "Controle", peso=2, ano=2015, dif=2,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Poder de polícia autoriza a Administração a:",
            ["limitar/fiscalizar direitos em prol do interesse público, nos termos legais", "criar tributos sem lei", "extinguir o Judiciário", "editar emendas constitucionais", "substituir o Legislativo"],
            "A", "Direito Administrativo", "Poderes administrativos", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Contratos administrativos, em regra, admitem cláusulas exorbitantes, como:",
            ["alteração unilateral nos limites legais", "impossibilidade absoluta de rescisão", "igualdade plena com contratos privados sem peculiaridades", "vedação a fiscalização", "pagamento sem empenho"],
            "A", "Direito Administrativo", "Contratos", peso=2, ano=2011, dif=3,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Responsabilidade civil do Estado por atos comissivos, no modelo de risco administrativo, é tipicamente:",
            ["subjetiva sempre", "objetiva", "inexistente", "apenas contratual", "penal exclusiva"],
            "B", "Direito Administrativo", "Responsabilidade civil", peso=2, ano=2006, dif=2,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Serviço público pode ser prestado:",
            ["apenas pela iniciativa privada sem título", "diretamente ou por delegação, nos termos legais", "somente por empresas estrangeiras", "apenas por ONGs", "sem qualquer regulação"],
            "B", "Direito Administrativo", "Serviços públicos", peso=2, ano=2006, dif=2,
            cargo="Técnico Judiciário - Área Administrativa",
        ),
    ]
    qs.extend(esp_adm)

    esp_const = [
        q(
            "O controle de constitucionalidade concentrado no STF processa, entre outras, a:",
            ["ADI", "reclamação trabalhista", "ação monitória", "execução fiscal municipal", "inventário"],
            "A", "Direito Constitucional", "Controle de constitucionalidade", peso=2, ano=2022, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Direitos e garantias fundamentais têm aplicação imediata, nos termos do art. 5º, §1º, da:",
            ["CLT", "CF/88", "CPC", "CTN", "ECA"],
            "B", "Direito Constitucional", "Direitos fundamentais", peso=2, ano=2022, dif=1,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "O STF é o guardião da Constituição Federal e compõe-se de:",
            ["5 ministros", "7 ministros", "11 ministros", "15 ministros", "27 ministros"],
            "C", "Direito Constitucional", "Organização do Judiciário", peso=2, ano=2015, dif=1,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Súmula vinculante exige, entre outros, reiteradas decisões sobre matéria constitucional e aprovação por:",
            ["maioria absoluta do STF (2/3)", "unanimidade do CNJ", "decreto legislativo", "plebiscito", "medida provisória"],
            "A", "Direito Constitucional", "Súmula vinculante", peso=2, ano=2015, dif=3,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Compete privativamente à União legislar sobre:",
            ["direito do trabalho", "transporte coletivo municipal exclusivo", "serviços funerários locais", "eventos culturais de bairro", "iluminção pública municipal"],
            "A", "Direito Constitucional", "Competências", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "O princípio federativo, na CF/88, é cláusula pétrea no sentido de vedar emenda tendente a abolir a:",
            ["forma federativa de Estado", "organização de partidos", "criação de municípios", "existência de TCU", "publicidade dos atos"],
            "A", "Direito Constitucional", "Emendas", peso=2, ano=2011, dif=2,
            cargo="Analista Judiciário - Área Judiciária",
        ),
        q(
            "Iniciativa popular de lei exige, entre outros, percentual de eleitores e distribuição em:",
            ["pelo menos 5 Estados", "1 Estado apenas", "todos os municípios", "apenas o DF", "apenas o Senado"],
            "A", "Direito Constitucional", "Processo legislativo", peso=2, ano=2006, dif=3,
            cargo="Analista Judiciário - Área Administrativa",
        ),
        q(
            "Medida provisória, em regra, deve atender aos requisitos de:",
            ["relevância e urgência", "apenas conveniência política", "autorização do STF prévia", "referendo popular", "aprovação do CNJ"],
            "A", "Direito Constitucional", "Processo legislativo", peso=2, ano=2006, dif=2,
            cargo="Analista Judiciário - Área Administrativa",
        ),
    ]
    qs.extend(esp_const)

    # Expansão por variação de anos/provas para volume de treino
    extras: list[dict] = []
    templates = [
        (
            "Sobre {tema}, assinale a alternativa correta no estilo de cobrança FCC.",
            "Língua Portuguesa",
            "Interpretação de texto",
            1,
            [
                ("A coesão textual depende, entre outros fatores, do uso adequado de conectivos.", "A"),
                ("Coesão e coerência são conceitos idênticos e sempre intercambiáveis.", "B"),
                ("Textos administrativos dispensam clareza.", "C"),
                ("Ambiguidade é sempre desejável em editais.", "D"),
                ("Pontuação não interfere na interpretação.", "E"),
            ],
        ),
        (
            "Em raciocínio lógico aplicado a concursos, considere a proposição e escolha a correta.",
            "Matemática e Raciocínio Lógico",
            "Lógica proposicional",
            1,
            [
                ("A condicional p→q é equivalente a ∼p∨q.", "A"),
                ("A condicional p→q é equivalente a p∧∼q.", "B"),
                ("A bicondicional nunca é verdadeira.", "C"),
                ("A conjunção é verdadeira com uma falsa.", "D"),
                ("A disjunção exige ambas verdadeiras.", "E"),
            ],
        ),
        (
            "No âmbito da legislação aplicável ao serviço público federal, é correto afirmar:",
            "Noções de Legislação",
            "Servidores públicos",
            1,
            [
                ("A investidura em cargo efetivo depende, em regra, de aprovação em concurso público.", "A"),
                ("Cargo em comissão dispensa qualquer nomeação.", "B"),
                ("Estabilidade se adquire no ato da posse.", "C"),
                ("Servidor não tem dever de sigilo.", "D"),
                ("Nepotismo é incentivado pela CF.", "E"),
            ],
        ),
        (
            "Acerca de direitos humanos e sua incidência no Brasil, assinale a correta.",
            "Noções de Direitos Humanos",
            "Fundamentos",
            1,
            [
                ("A dignidade da pessoa humana é fundamento da República.", "A"),
                ("Direitos humanos aplicam-se só a estrangeiros.", "B"),
                ("Tratados de DH nunca vinculam o Estado.", "C"),
                ("Discriminação racial é admitida em concursos.", "D"),
                ("DH de 1ª geração são só econômicos.", "E"),
            ],
        ),
        (
            "Em informática básica para tribunais, é correto afirmar:",
            "Noções de Informática",
            "Segurança da informação",
            1,
            [
                ("Senhas fortes e atualização de software reduzem riscos.", "A"),
                ("Antivirus elimina a necessidade de backups.", "B"),
                ("Phishing é sempre um falso positivo do firewall.", "C"),
                ("HTTPS remove toda necessidade de autenticação.", "D"),
                ("Compartilhar senha institucional é boa prática.", "E"),
            ],
        ),
        (
            "Sobre Direito do Trabalho, à luz da CLT/CF, assinale a correta.",
            "Direito do Trabalho",
            "Princípios",
            2,
            [
                ("O princípio da proteção informa a interpretação das normas trabalhistas.", "A"),
                ("O empregado nunca pode rescindir o contrato.", "B"),
                ("Jornada pode ser ilimitada por acordo verbal.", "C"),
                ("FGTS é facultativo para celetistas.", "D"),
                ("Férias podem ser convertidas integralmente em dinheiro sem regra legal.", "E"),
            ],
        ),
        (
            "No processo do trabalho, assinale a alternativa correta.",
            "Direito Processual do Trabalho",
            "Princípios processuais",
            2,
            [
                ("Há oralidade e concentração de atos na audiência, em regra.", "A"),
                ("Não existe recurso no processo trabalhista.", "B"),
                ("A execução é sempre privada e voluntária.", "C"),
                ("O juiz não pode conciliar.", "D"),
                ("Prazos recursais são sempre de 30 dias.", "E"),
            ],
        ),
        (
            "Em Direito Administrativo, é correto afirmar:",
            "Direito Administrativo",
            "Princípios",
            2,
            [
                ("A legalidade vincula a Administração à lei.", "A"),
                ("Impessoalidade autoriza favorecimentos pessoais.", "B"),
                ("Moralidade é princípio meramente ético sem relevância jurídica.", "C"),
                ("Publicidade veda a divulgação de atos oficiais.", "D"),
                ("Eficiência autoriza ilegalidades.", "E"),
            ],
        ),
        (
            "Em Direito Constitucional, assinale a correta.",
            "Direito Constitucional",
            "Direitos fundamentais",
            2,
            [
                ("Ninguém será obrigado a fazer ou deixar de fazer algo senão em virtude de lei.", "A"),
                ("A CF permite pena de caráter perpétuo em regra.", "B"),
                ("Habeas data protege a liberdade de locomoção.", "C"),
                ("O STF possui 15 ministros.", "D"),
                ("Emenda pode abolir o voto direto.", "E"),
            ],
        ),
    ]

    anos = [2022, 2015, 2011, 2006, 2009]
    for i, (enun, disc, top, peso, alts_g) in enumerate(templates):
        for j, ano in enumerate(anos):
            alts = [t[0] for t in alts_g]
            gab = alts_g[0][1]
            # leve variação no enunciado
            texto = enun.format(tema="coesão e coerência") if "{tema}" in enun else enun
            texto = f"{texto} (referência de treino: TRT4/{ano})."
            extras.append(
                q(
                    texto,
                    alts,
                    gab,
                    disc,
                    top,
                    ano=ano,
                    peso=peso,
                    dif=2 + (j % 2),
                    prova=f"TRT4 estilo FCC {ano}",
                    cargo="Técnico Judiciário - Área Administrativa" if peso == 1 else "Analista Judiciário - Área Judiciária",
                    tempo=80 if peso == 1 else 100,
                )
            )
    qs.extend(extras)

    # Topicos auxiliares como metadados embutidos (importador cria tabela)
    return qs


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Geradas {len(data)} questões → {OUT}")


if __name__ == "__main__":
    main()
