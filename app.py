import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="Sistema de Submissão de Artigos - SQL Runner",
    page_icon="�",
    layout="wide"
)

# Caminho do banco de dados
DB_PATH = "submissao.db"

def init_db():
    """Cria e popula o banco de dados do zero"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # DROP todas as tabelas se existirem
    cursor.executescript("""
        DROP TABLE IF EXISTS Revisao;
        DROP TABLE IF EXISTS Autoria;
        DROP TABLE IF EXISTS Artigo_Area;
        DROP TABLE IF EXISTS Artigo;
        DROP TABLE IF EXISTS Chamada_Especial;
        DROP TABLE IF EXISTS Edicao_Regular;
        DROP TABLE IF EXISTS Edicao;
        DROP TABLE IF EXISTS Area;
        DROP TABLE IF EXISTS Editor;
        DROP TABLE IF EXISTS Revisor;
        DROP TABLE IF EXISTS Autor;
        DROP TABLE IF EXISTS Usuario;
    """)
    
    # CREATE TABLES (DDL)
    cursor.executescript("""
        CREATE TABLE Usuario (
            ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Senha TEXT NOT NULL,
            Instituicao TEXT,
            Data_Cadastro DATE DEFAULT CURRENT_DATE
        );
        
        CREATE TABLE Autor (
            ID_Usuario INTEGER PRIMARY KEY,
            ORCID TEXT UNIQUE,
            Bio_Resumida TEXT,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
        );
        
        CREATE TABLE Revisor (
            ID_Usuario INTEGER PRIMARY KEY,
            Areas_Interesse TEXT,
            Nota_Media REAL,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
        );
        
        CREATE TABLE Editor (
            ID_Usuario INTEGER PRIMARY KEY,
            Cargo TEXT,
            Ativo BOOLEAN DEFAULT 1,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
        );
        
        CREATE TABLE Area (
            Cod_Area INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Area TEXT NOT NULL UNIQUE,
            Descricao TEXT
        );
        
        CREATE TABLE Edicao (
            Cod_Edicao INTEGER PRIMARY KEY AUTOINCREMENT,
            Ano INTEGER NOT NULL,
            Status TEXT CHECK(Status IN ('Aberta', 'Fechada', 'Publicada'))
        );
        
        CREATE TABLE Edicao_Regular (
            Cod_Edicao INTEGER PRIMARY KEY,
            Volume INTEGER,
            Numero INTEGER,
            FOREIGN KEY (Cod_Edicao) REFERENCES Edicao(Cod_Edicao) ON DELETE CASCADE
        );
        
        CREATE TABLE Chamada_Especial (
            Cod_Edicao INTEGER PRIMARY KEY,
            Titulo_Tematico TEXT,
            Descricao TEXT,
            Data_Limite DATE,
            FOREIGN KEY (Cod_Edicao) REFERENCES Edicao(Cod_Edicao) ON DELETE CASCADE
        );
        
        CREATE TABLE Artigo (
            Cod_Artigo INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Resumo TEXT,
            Arquivo TEXT,
            Status TEXT CHECK(Status IN ('Submetido', 'Em Revisao', 'Aceito', 'Rejeitado', 'Publicado')),
            Cod_Edicao INTEGER,
            FOREIGN KEY (Cod_Edicao) REFERENCES Edicao(Cod_Edicao) ON DELETE SET NULL
        );
        
        CREATE TABLE Artigo_Area (
            Cod_Artigo INTEGER,
            Cod_Area INTEGER,
            PRIMARY KEY (Cod_Artigo, Cod_Area),
            FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo) ON DELETE CASCADE,
            FOREIGN KEY (Cod_Area) REFERENCES Area(Cod_Area) ON DELETE CASCADE
        );
        
        CREATE TABLE Autoria (
            Cod_Autor INTEGER,
            Cod_Artigo INTEGER,
            Ordem_Autoria INTEGER,
            PRIMARY KEY (Cod_Autor, Cod_Artigo),
            FOREIGN KEY (Cod_Autor) REFERENCES Autor(ID_Usuario) ON DELETE CASCADE,
            FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo) ON DELETE CASCADE
        );
        
        CREATE TABLE Revisao (
            Cod_Revisao INTEGER PRIMARY KEY AUTOINCREMENT,
            Cod_Artigo INTEGER,
            Cod_Revisor INTEGER,
            Parecer TEXT,
            Nota REAL CHECK(Nota >= 0 AND Nota <= 10),
            Data_Entrega DATE,
            FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo) ON DELETE CASCADE,
            FOREIGN KEY (Cod_Revisor) REFERENCES Revisor(ID_Usuario) ON DELETE CASCADE
        );
    """)
    
    # INSERT dados fictícios (DML)
    
    # Usuários (15 usuários)
    usuarios = [
        ('Alan Turing', 'alan.turing@cs.ox.uk', 'enigma123', 'University of Oxford', '2023-01-10'),
        ('Grace Hopper', 'grace.hopper@navy.mil', 'cobol456', 'US Naval Reserve', '2023-01-15'),
        ('Ada Lovelace', 'ada.lovelace@math.uk', 'algorithm789', 'University of Cambridge', '2023-02-01'),
        ('Donald Knuth', 'knuth@stanford.edu', 'tex2024', 'Stanford University', '2023-02-10'),
        ('Barbara Liskov', 'liskov@mit.edu', 'abstraction5', 'MIT', '2023-02-20'),
        ('Edsger Dijkstra', 'dijkstra@tue.nl', 'goto2bad', 'TU Eindhoven', '2023-03-01'),
        ('John McCarthy', 'mccarthy@stanford.edu', 'lisp1958', 'Stanford University', '2023-03-05'),
        ('Dennis Ritchie', 'ritchie@bell-labs.com', 'unix1971', 'Bell Labs', '2023-03-10'),
        ('Ken Thompson', 'thompson@bell-labs.com', 'go2plan9', 'Bell Labs', '2023-03-15'),
        ('Tim Berners-Lee', 'timbl@w3.org', 'www1989', 'CERN', '2023-04-01'),
        ('Linus Torvalds', 'torvalds@linux.com', 'kernel2024', 'Linux Foundation', '2023-04-10'),
        ('Bjarne Stroustrup', 'bjarne@tamu.edu', 'cpp1985', 'Texas A&M University', '2023-04-15'),
        ('Guido van Rossum', 'guido@python.org', 'pythonic', 'Python Software Foundation', '2023-05-01'),
        ('James Gosling', 'gosling@sun.com', 'java1995', 'Sun Microsystems', '2023-05-10'),
        ('Margaret Hamilton', 'hamilton@nasa.gov', 'apollo11', 'NASA', '2023-05-15')
    ]
    
    cursor.executemany("""
        INSERT INTO Usuario (Nome, Email, Senha, Instituicao, Data_Cadastro) 
        VALUES (?, ?, ?, ?, ?)
    """, usuarios)
    
    # Autores (10 autores - IDs 1 a 10)
    autores = [
        (1, '0000-0001-1111-1111', 'Pioneiro da computação e inteligência artificial'),
        (2, '0000-0002-2222-2222', 'Desenvolveu o primeiro compilador'),
        (3, '0000-0003-3333-3333', 'Primeira programadora da história'),
        (4, '0000-0004-4444-4444', 'Especialista em análise de algoritmos'),
        (5, '0000-0005-5555-5555', 'Criadora do princípio de substituição'),
        (6, '0000-0006-6666-6666', 'Algoritmos de caminho mais curto'),
        (7, '0000-0007-7777-7777', 'Inventor da linguagem Lisp'),
        (8, '0000-0008-8888-8888', 'Co-criador do Unix e linguagem C'),
        (9, '0000-0009-9999-9999', 'Co-criador do Unix'),
        (10, '0000-0010-1010-1010', 'Inventor da World Wide Web')
    ]
    
    cursor.executemany("""
        INSERT INTO Autor (ID_Usuario, ORCID, Bio_Resumida) 
        VALUES (?, ?, ?)
    """, autores)
    
    # Revisores (3 revisores - IDs 11, 12, 13)
    revisores = [
        (11, 'Sistemas Operacionais, Kernel Development', 8.5),
        (12, 'Linguagens de Programação, Compiladores', 9.0),
        (13, 'Engenharia de Software, Web Development', 8.8)
    ]
    
    cursor.executemany("""
        INSERT INTO Revisor (ID_Usuario, Areas_Interesse, Nota_Media) 
        VALUES (?, ?, ?)
    """, revisores)
    
    # Editores (2 editores - IDs 14, 15)
    editores = [
        (14, 'Editor-Chefe', 1),
        (15, 'Editor Associado', 1)
    ]
    
    cursor.executemany("""
        INSERT INTO Editor (ID_Usuario, Cargo, Ativo) 
        VALUES (?, ?, ?)
    """, editores)
    
    # Áreas (10 áreas)
    areas = [
        ('Inteligência Artificial', 'Estudos sobre IA, ML e Deep Learning'),
        ('Sistemas Operacionais', 'Desenvolvimento e arquitetura de SO'),
        ('Banco de Dados', 'SGBDs, modelagem e otimização'),
        ('Redes de Computadores', 'Protocolos, segurança e infraestrutura'),
        ('Engenharia de Software', 'Metodologias, padrões e boas práticas'),
        ('Algoritmos', 'Análise e desenvolvimento de algoritmos'),
        ('Computação Gráfica', 'Renderização, modelagem 3D e visualização'),
        ('Arquitetura de Computadores', 'Hardware, microprocessadores e sistemas embarcados'),
        ('Segurança da Informação', 'Criptografia, ethical hacking e proteção de dados'),
        ('Computação em Nuvem', 'Cloud computing, virtualização e escalabilidade')
    ]
    
    cursor.executemany("""
        INSERT INTO Area (Nome_Area, Descricao) 
        VALUES (?, ?)
    """, areas)
    
    # Edições (10 edições)
    edicoes = [
        (2023, 'Publicada'),
        (2023, 'Publicada'),
        (2024, 'Publicada'),
        (2024, 'Aberta'),
        (2024, 'Aberta'),
        (2025, 'Aberta'),
        (2025, 'Aberta'),
        (2023, 'Fechada'),
        (2024, 'Fechada'),
        (2025, 'Aberta')
    ]
    
    cursor.executemany("""
        INSERT INTO Edicao (Ano, Status) 
        VALUES (?, ?)
    """, edicoes)
    
    # Edições Regulares (7 regulares)
    edicoes_regulares = [
        (1, 10, 1),
        (2, 10, 2),
        (3, 11, 1),
        (4, 11, 2),
        (5, 11, 3),
        (6, 12, 1),
        (7, 12, 2)
    ]
    
    cursor.executemany("""
        INSERT INTO Edicao_Regular (Cod_Edicao, Volume, Numero) 
        VALUES (?, ?, ?)
    """, edicoes_regulares)
    
    # Chamadas Especiais (3 especiais)
    chamadas = [
        (8, 'Inteligência Artificial em Saúde', 'Chamada especial sobre aplicações de IA na medicina', '2023-12-31'),
        (9, 'Sustentabilidade em TI', 'Green Computing e eficiência energética', '2024-06-30'),
        (10, 'Computação Quântica', 'Avanços recentes em computação quântica', '2025-12-31')
    ]
    
    cursor.executemany("""
        INSERT INTO Chamada_Especial (Cod_Edicao, Titulo_Tematico, Descricao, Data_Limite) 
        VALUES (?, ?, ?, ?)
    """, chamadas)
    
    # Artigos (15 artigos) - Garantindo que Alan Turing (ID 1) tenha 2 artigos
    artigos = [
        ('On Computable Numbers', 'Artigo fundamental sobre computabilidade', 'turing_1936.pdf', 'Publicado', 1),
        ('Computing Machinery and Intelligence', 'Propõe o teste de Turing', 'turing_test.pdf', 'Publicado', 2),
        ('The Education of a Computer', 'Sobre programação de computadores', 'hopper_1952.pdf', 'Publicado', 1),
        ('Notes on the Analytical Engine', 'Primeiro algoritmo computacional', 'lovelace_1843.pdf', 'Publicado', 3),
        ('The Art of Computer Programming Vol 1', 'Análise fundamental de algoritmos', 'knuth_vol1.pdf', 'Aceito', 4),
        ('Data Abstraction and Hierarchy', 'Princípios de abstração de dados', 'liskov_1988.pdf', 'Publicado', 2),
        ('A Note on Two Problems in Connexion with Graphs', 'Algoritmo de Dijkstra', 'dijkstra_1959.pdf', 'Publicado', 3),
        ('Recursive Functions of Symbolic Expressions', 'Fundamentos do Lisp', 'mccarthy_1960.pdf', 'Em Revisao', 4),
        ('The UNIX Time-Sharing System', 'Descrição do sistema Unix', 'ritchie_1974.pdf', 'Aceito', 5),
        ('Information Management: A Proposal', 'Proposta inicial da WWW', 'berners_lee_1989.pdf', 'Publicado', 1),
        ('Linux: A Portable Operating System', 'Arquitetura do kernel Linux', 'torvalds_1997.pdf', 'Em Revisao', 6),
        ('The C++ Programming Language', 'Design e evolução do C++', 'stroustrup_1985.pdf', 'Submetido', 7),
        ('Python Tutorial', 'Introdução à linguagem Python', 'van_rossum_1995.pdf', 'Aceito', 5),
        ('The Java Language Specification', 'Especificação completa do Java', 'gosling_1996.pdf', 'Rejeitado', 8),
        ('Apollo Guidance Computer', 'Software do programa Apollo', 'hamilton_1969.pdf', 'Publicado', 9)
    ]
    
    cursor.executemany("""
        INSERT INTO Artigo (Titulo, Resumo, Arquivo, Status, Cod_Edicao) 
        VALUES (?, ?, ?, ?, ?)
    """, artigos)
    
    # Artigo_Area (vincular artigos com áreas)
    artigo_areas = [
        (1, 1), (1, 6),  # Turing artigo 1: IA e Algoritmos
        (2, 1),          # Turing artigo 2: IA
        (3, 5),          # Hopper: Eng. Software
        (4, 6),          # Lovelace: Algoritmos
        (5, 6),          # Knuth: Algoritmos
        (6, 5),          # Liskov: Eng. Software
        (7, 6),          # Dijkstra: Algoritmos
        (8, 5),          # McCarthy: Eng. Software
        (9, 2),          # Ritchie: SO
        (10, 4), (10, 5),# Berners-Lee: Redes e Eng. Software
        (11, 2),         # Torvalds: SO
        (12, 5),         # Stroustrup: Eng. Software
        (13, 5),         # Van Rossum: Eng. Software
        (14, 5),         # Gosling: Eng. Software
        (15, 8),         # Hamilton: Arquitetura
        (11, 9),         # Torvalds: Segurança (área sem artigo dedicado para query 6)
    ]
    
    cursor.executemany("""
        INSERT INTO Artigo_Area (Cod_Artigo, Cod_Area) 
        VALUES (?, ?)
    """, artigo_areas)
    
    # Autoria (garantir que Alan Turing - ID 1 - tenha 2 artigos: artigos 1 e 2)
    autorias = [
        (1, 1, 1),   # Alan Turing - Artigo 1
        (1, 2, 1),   # Alan Turing - Artigo 2
        (2, 3, 1),   # Grace Hopper - Artigo 3
        (3, 4, 1),   # Ada Lovelace - Artigo 4
        (4, 5, 1),   # Donald Knuth - Artigo 5
        (5, 6, 1),   # Barbara Liskov - Artigo 6
        (6, 7, 1),   # Edsger Dijkstra - Artigo 7
        (7, 8, 1),   # John McCarthy - Artigo 8
        (8, 9, 1),   # Dennis Ritchie - Artigo 9
        (9, 9, 2),   # Ken Thompson - Artigo 9 (co-autor)
        (10, 10, 1), # Tim Berners-Lee - Artigo 10
        (1, 11, 1),  # Linus Torvalds - Artigo 11
        (2, 12, 1),  # Bjarne Stroustrup - Artigo 12
        (3, 13, 1),  # Guido van Rossum - Artigo 13
        (4, 14, 1),  # James Gosling - Artigo 14
        (5, 15, 1),  # Margaret Hamilton - Artigo 15
    ]
    
    cursor.executemany("""
        INSERT INTO Autoria (Cod_Autor, Cod_Artigo, Ordem_Autoria) 
        VALUES (?, ?, ?)
    """, autorias)
    
    # Revisões (15 revisões com notas variadas)
    revisoes = [
        (1, 11, 'Excelente trabalho, bem fundamentado', 9.5, '2024-01-15'),
        (2, 11, 'Muito bom, mas poderia expandir a metodologia', 8.7, '2024-01-20'),
        (3, 12, 'Trabalho interessante mas precisa de melhorias', 7.2, '2024-02-10'),
        (4, 12, 'Boa contribuição para a área', 8.0, '2024-02-15'),
        (5, 13, 'Artigo sólido com aplicações práticas', 8.5, '2024-03-01'),
        (7, 11, 'Precisa revisar a seção de resultados', 6.8, '2024-01-25'),
        (8, 12, 'Contribuição limitada, rejeitar', 5.5, '2024-02-20'),
        (9, 13, 'Aceitar com revisões menores', 8.2, '2024-03-05'),
        (10, 11, 'Trabalho de alta qualidade', 9.0, '2024-01-30'),
        (11, 12, 'Necessita de experimentos adicionais', 7.0, '2024-02-25'),
        (1, 13, 'Muito promissor', 8.8, '2024-03-10'),
        (2, 13, 'Bem escrito e fundamentado', 9.2, '2024-03-12'),
        (3, 11, 'Excelente estado da arte', 9.3, '2024-02-01'),
        (4, 11, 'Aceitar sem ressalvas', 9.8, '2024-02-05'),
        (5, 12, 'Trabalho satisfatório', 7.5, '2024-03-01')
    ]
    
    cursor.executemany("""
        INSERT INTO Revisao (Cod_Artigo, Cod_Revisor, Parecer, Nota, Data_Entrega) 
        VALUES (?, ?, ?, ?, ?)
    """, revisoes)
    
    conn.commit()
    conn.close()
    
    return "✅ Banco de dados criado e populado com sucesso!"

def execute_query(query):
    """Executa uma query SQL e retorna o resultado como DataFrame ou mensagem de sucesso"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verifica se é um comando de escrita (INSERT, UPDATE, DELETE)
        query_upper = query.strip().upper()
        is_write_command = any(query_upper.startswith(cmd) for cmd in ['INSERT', 'UPDATE', 'DELETE'])
        
        if is_write_command:
            cursor.execute(query)
            conn.commit()
            rows_affected = cursor.rowcount
            conn.close()
            return f"Comando executado com sucesso! {rows_affected} linha(s) afetada(s).", None
        else:
            # Comando de leitura (SELECT)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df, None
    except Exception as e:
        return None, str(e)

# Dicionário com as consultas (12 obrigatórias + exemplos de INSERT/UPDATE/DELETE)
CONSULTAS_PRONTAS = {
    "Selecione uma consulta...": "",
    
    "1. Listar Artigos e Autores": """
SELECT 
    A.Cod_Artigo,
    A.Titulo AS Titulo_Artigo,
    U.Nome AS Nome_Autor,
    AU.Ordem_Autoria,
    A.Status
FROM Artigo A
INNER JOIN Autoria AU ON A.Cod_Artigo = AU.Cod_Artigo
INNER JOIN Usuario U ON AU.Cod_Autor = U.ID_Usuario
ORDER BY A.Cod_Artigo, AU.Ordem_Autoria;
""",
    
    "2. Artigos, Áreas e Edições": """
SELECT 
    A.Cod_Artigo,
    A.Titulo AS Titulo_Artigo,
    AR.Nome_Area,
    E.Ano AS Ano_Edicao,
    E.Status AS Status_Edicao
FROM Artigo A
INNER JOIN Artigo_Area AA ON A.Cod_Artigo = AA.Cod_Artigo
INNER JOIN Area AR ON AA.Cod_Area = AR.Cod_Area
INNER JOIN Edicao E ON A.Cod_Edicao = E.Cod_Edicao
ORDER BY A.Cod_Artigo;
""",
    
    "3. Revisores e Notas": """
SELECT 
    U.Nome AS Nome_Revisor,
    A.Titulo AS Titulo_Artigo,
    R.Nota,
    R.Parecer,
    R.Data_Entrega
FROM Revisao R
INNER JOIN Revisor REV ON R.Cod_Revisor = REV.ID_Usuario
INNER JOIN Usuario U ON REV.ID_Usuario = U.ID_Usuario
INNER JOIN Artigo A ON R.Cod_Artigo = A.Cod_Artigo
ORDER BY R.Nota DESC;
""",
    
    "4. Chamadas Especiais": """
SELECT 
    CE.Titulo_Tematico,
    CE.Descricao,
    CE.Data_Limite,
    E.Ano,
    E.Status
FROM Chamada_Especial CE
INNER JOIN Edicao E ON CE.Cod_Edicao = E.Cod_Edicao
ORDER BY CE.Data_Limite;
""",
    
    "5. Editores e Cargos": """
SELECT 
    U.Nome,
    U.Email,
    U.Instituicao,
    ED.Cargo,
    CASE WHEN ED.Ativo = 1 THEN 'Sim' ELSE 'Não' END AS Ativo
FROM Editor ED
INNER JOIN Usuario U ON ED.ID_Usuario = U.ID_Usuario
ORDER BY ED.Cargo;
""",
    
    "6. Áreas sem artigos": """
SELECT 
    AR.Cod_Area,
    AR.Nome_Area,
    AR.Descricao,
    COUNT(AA.Cod_Artigo) AS Num_Artigos
FROM Area AR
LEFT JOIN Artigo_Area AA ON AR.Cod_Area = AA.Cod_Area
GROUP BY AR.Cod_Area, AR.Nome_Area, AR.Descricao
HAVING COUNT(AA.Cod_Artigo) = 0;
""",
    
    "7. Usuários vs Autores": """
SELECT 
    U.ID_Usuario,
    U.Nome,
    U.Email,
    U.Instituicao,
    CASE WHEN AU.ID_Usuario IS NULL THEN 'Não' ELSE 'Sim' END AS Eh_Autor,
    AU.ORCID
FROM Usuario U
LEFT JOIN Autor AU ON U.ID_Usuario = AU.ID_Usuario
ORDER BY U.Nome;
""",
    
    "8. Média de Notas por Status": """
SELECT 
    A.Status,
    COUNT(R.Cod_Revisao) AS Total_Revisoes,
    ROUND(AVG(R.Nota), 2) AS Nota_Media,
    ROUND(MIN(R.Nota), 2) AS Nota_Minima,
    ROUND(MAX(R.Nota), 2) AS Nota_Maxima
FROM Artigo A
INNER JOIN Revisao R ON A.Cod_Artigo = R.Cod_Artigo
GROUP BY A.Status
ORDER BY Nota_Media DESC;
""",
    
    "9. Contagem de Artigos por Área": """
SELECT 
    AR.Nome_Area,
    COUNT(AA.Cod_Artigo) AS Total_Artigos
FROM Area AR
INNER JOIN Artigo_Area AA ON AR.Cod_Area = AA.Cod_Area
GROUP BY AR.Nome_Area
ORDER BY Total_Artigos DESC;
""",
    
    "10. Total de Revisões por Revisor": """
SELECT 
    U.Nome AS Nome_Revisor,
    COUNT(R.Cod_Revisao) AS Total_Revisoes,
    ROUND(AVG(R.Nota), 2) AS Nota_Media_Atribuida
FROM Revisor REV
INNER JOIN Usuario U ON REV.ID_Usuario = U.ID_Usuario
INNER JOIN Revisao R ON REV.ID_Usuario = R.Cod_Revisor
GROUP BY U.Nome
HAVING COUNT(R.Cod_Revisao) >= 1
ORDER BY Total_Revisoes DESC;
""",
    
    "11. Nota Máxima/Mínima por Ano": """
SELECT 
    E.Ano,
    COUNT(DISTINCT A.Cod_Artigo) AS Total_Artigos,
    ROUND(MAX(R.Nota), 2) AS Nota_Maxima,
    ROUND(MIN(R.Nota), 2) AS Nota_Minima,
    ROUND(AVG(R.Nota), 2) AS Nota_Media
FROM Edicao E
INNER JOIN Artigo A ON E.Cod_Edicao = A.Cod_Edicao
INNER JOIN Revisao R ON A.Cod_Artigo = R.Cod_Artigo
GROUP BY E.Ano
ORDER BY E.Ano;
""",
    
    "12. Autores com mais de 1 Artigo": """
SELECT 
    U.Nome AS Nome_Autor,
    U.Email,
    AU.ORCID,
    COUNT(AUT.Cod_Artigo) AS Total_Artigos
FROM Autor AU
INNER JOIN Usuario U ON AU.ID_Usuario = U.ID_Usuario
INNER JOIN Autoria AUT ON AU.ID_Usuario = AUT.Cod_Autor
GROUP BY U.Nome, U.Email, AU.ORCID
HAVING COUNT(AUT.Cod_Artigo) > 1
ORDER BY Total_Artigos DESC;
""",
    
    "--- EXEMPLOS DE ESCRITA ---": "",
    
    "INSERT - Novo Usuário": """
INSERT INTO Usuario (Nome, Email, Senha, Instituicao, Data_Cadastro)
VALUES ('Novo Autor', 'novo.autor@exemplo.com', 'senha123', 'Universidade Exemplo', '2025-01-15');
""",
    
    "UPDATE - Atualizar Status de Artigo": """
UPDATE Artigo 
SET Status = 'Aceito'
WHERE Cod_Artigo = 12;
""",
    
    "DELETE - Remover Revisão": """
DELETE FROM Revisao
WHERE Cod_Revisao = 15;
"""
}

# ==========================
# INTERFACE STREAMLIT
# ==========================

# Título principal
st.title("Sistema de Submissão de Artigos em Periódicos")
st.markdown("### SQL Runner - Trabalho Final de Banco de Dados")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Configurações")
    
    # Botão para resetar/criar banco
    if st.button("Resetar/Criar Banco", type="primary", use_container_width=True):
        with st.spinner("Criando banco de dados..."):
            mensagem = init_db()
            st.success(mensagem)
            st.balloons()
    
    st.divider()
    
    # Menu de consultas prontas
    st.header("Consultas Prontas")
    consulta_selecionada = st.selectbox(
        "Selecione uma consulta:",
        options=list(CONSULTAS_PRONTAS.keys()),
        index=0
    )
    
    st.divider()
    
    # Informações do sistema
    st.header("Informações")
    st.markdown(f"""
    **Banco:** `submissao.db`  
    **Tipo:** SQLite  
    **Tabelas:** 12  
    
    ---
    
    #### Estatísticas do Banco
    """)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Contagens
        cursor.execute("SELECT COUNT(*) FROM Usuario")
        num_usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Artigo")
        num_artigos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Revisao")
        num_revisoes = cursor.fetchone()[0]
        
        conn.close()
        
        st.metric("Usuários", num_usuarios)
        st.metric("Artigos", num_artigos)
        st.metric("Revisões", num_revisoes)
        
    except:
        st.warning("Banco ainda não inicializado")

# Área principal
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Editor SQL")

with col2:
    st.markdown("")  # espaçamento

# Campo de texto SQL
query_sql = st.text_area(
    "Digite ou edite seu comando SQL:",
    value=CONSULTAS_PRONTAS.get(consulta_selecionada, ""),
    height=200,
    placeholder="SELECT * FROM Usuario LIMIT 10;"
)

# Botão executar
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])

with col_btn1:
    executar = st.button("Executar", type="primary", use_container_width=True)

with col_btn2:
    limpar = st.button("Limpar", use_container_width=True)

# Executar query
if executar and query_sql.strip():
    with st.spinner("Executando consulta..."):
        resultado, erro = execute_query(query_sql)
        
        if erro:
            st.error(f"Erro na execução: {erro}")
        else:
            # Verifica se é um DataFrame (SELECT) ou mensagem de sucesso (INSERT/UPDATE/DELETE)
            if isinstance(resultado, pd.DataFrame):
                st.success(f"Consulta executada com sucesso! {len(resultado)} linha(s) retornada(s).")
                
                # Exibir resultado
                st.subheader("Resultado da Consulta")
                st.dataframe(
                    resultado, 
                    use_container_width=True,
                    height=400
                )
                
                # Opção de download
                csv = resultado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="resultado_query.csv",
                    mime="text/csv"
                )
            else:
                # Mensagem de sucesso para INSERT/UPDATE/DELETE
                st.success(resultado)

elif executar and not query_sql.strip():
    st.warning("Por favor, insira uma consulta SQL.")

# Limpar campo
if limpar:
    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <small>Sistema desenvolvido para o Trabalho Final de Banco de Dados | 2024</small>
</div>
""", unsafe_allow_html=True)
