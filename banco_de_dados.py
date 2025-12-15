import sqlite3
import os

# Nome do arquivo do banco de dados
db_filename = 'submissao_artigos.db'

# Remove o banco antigo se existir para rodar limpo
if os.path.exists(db_filename):
    os.remove(db_filename)

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

print(">>> 1. CRIANDO TABELAS (DDL)...")

# DDL baseada no Modelo Relacional do seu PDF
ddl_script = """
PRAGMA foreign_keys = ON;

CREATE TABLE Usuario (
    ID_Usuario INTEGER PRIMARY KEY,
    Nome TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Senha TEXT NOT NULL,
    Instituicao TEXT,
    Data_Cadastro DATE
);

CREATE TABLE Area (
    Cod_Area INTEGER PRIMARY KEY,
    Nome_Area TEXT NOT NULL,
    Descricao TEXT
);

CREATE TABLE Edicao (
    Cod_Edicao INTEGER PRIMARY KEY,
    Ano INTEGER,
    Status TEXT -- 'Aberta', 'Fechada', 'Em Planejamento'
);

CREATE TABLE Autor (
    ID_Usuario INTEGER PRIMARY KEY,
    ORCID TEXT,
    Bio_Resumida TEXT,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

CREATE TABLE Revisor (
    ID_Usuario INTEGER PRIMARY KEY,
    Areas_Interesse TEXT,
    Nota_Media REAL,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

CREATE TABLE Editor (
    ID_Usuario INTEGER PRIMARY KEY,
    Cargo TEXT,
    Ativo BOOLEAN,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

CREATE TABLE Edicao_Regular (
    Cod_Edicao INTEGER PRIMARY KEY,
    Volume INTEGER,
    Numero INTEGER,
    FOREIGN KEY (Cod_Edicao) REFERENCES Edicao(Cod_Edicao)
);

CREATE TABLE Chamada_Especial (
    Cod_Edicao INTEGER PRIMARY KEY,
    Titulo_Tematico TEXT,
    Descricao TEXT,
    Data_Limite DATE,
    FOREIGN KEY (Cod_Edicao) REFERENCES Edicao(Cod_Edicao)
);

CREATE TABLE Artigo (
    Cod_Artigo INTEGER PRIMARY KEY,
    Titulo TEXT NOT NULL,
    Resumo TEXT,
    Arquivo TEXT,
    Status TEXT, -- 'Submetido', 'Em Revisão', 'Aceito', 'Rejeitado'
    Cod_Edicao INTEGER,
    FOREIGN KEY (Cod_Edicao) REFERENCES Edicao(Cod_Edicao)
);

CREATE TABLE Artigo_Area (
    Cod_Artigo INTEGER,
    Cod_Area INTEGER,
    PRIMARY KEY (Cod_Artigo, Cod_Area),
    FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo),
    FOREIGN KEY (Cod_Area) REFERENCES Area(Cod_Area)
);

CREATE TABLE Autoria (
    Cod_Autor INTEGER,
    Cod_Artigo INTEGER,
    Ordem_Autoria INTEGER,
    PRIMARY KEY (Cod_Autor, Cod_Artigo),
    FOREIGN KEY (Cod_Autor) REFERENCES Autor(ID_Usuario),
    FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo)
);

CREATE TABLE Revisao (
    Cod_Revisao INTEGER PRIMARY KEY,
    Cod_Artigo INTEGER,
    Cod_Revisor INTEGER,
    Parecer TEXT,
    Nota REAL,
    Data_Entrega DATE,
    FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo),
    FOREIGN KEY (Cod_Revisor) REFERENCES Revisor(ID_Usuario)
);
"""
cursor.executescript(ddl_script)
print(">>> Tabela criadas com sucesso.")

print("\n>>> 2. INSERINDO DADOS (DML)...")
# Inserção de dados fictícios (Mínimo 10 tuplas onde possível para cumprir requisitos)
dml_script = """
-- 1. Usuarios (15 usuarios mistos)
INSERT INTO Usuario VALUES 
(1, 'Felipe Silvestre', 'felipe@email.com', '123', 'UNIFESP', '2024-01-10'),
(2, 'João Vitor', 'joao@email.com', '123', 'UNIFESP', '2024-01-12'),
(3, 'Abner Augusto', 'abner@email.com', '123', 'UNIFESP', '2024-01-15'),
(4, 'Daniela Musa', 'daniela@email.com', 'pass', 'UNIFESP', '2023-05-20'),
(5, 'Alan Turing', 'alan@comp.com', 'pass', 'Cambridge', '2023-01-01'),
(6, 'Ada Lovelace', 'ada@comp.com', 'pass', 'Independent', '2023-01-02'),
(7, 'Grace Hopper', 'grace@navy.com', 'pass', 'Yale', '2023-02-15'),
(8, 'Donald Knuth', 'donald@stanford.edu', 'pass', 'Stanford', '2023-03-10'),
(9, 'Tim Berners-Lee', 'tim@web.com', 'pass', 'MIT', '2023-04-12'),
(10, 'Linus Torvalds', 'linus@linux.com', 'pass', 'Helsinki', '2023-06-30'),
(11, 'Guido van Rossum', 'guido@python.org', 'pass', 'Google', '2023-07-20'),
(12, 'Ken Thompson', 'ken@bell.com', 'pass', 'Bell Labs', '2023-08-05'),
(13, 'Dennis Ritchie', 'dennis@c.com', 'pass', 'Bell Labs', '2023-08-05'),
(14, 'Barbara Liskov', 'barbara@mit.edu', 'pass', 'MIT', '2023-09-10'),
(15, 'Margaret Hamilton', 'margaret@nasa.gov', 'pass', 'NASA', '2023-10-01');

-- 2. Areas
INSERT INTO Area VALUES 
(1, 'Banco de Dados', 'Estudo de dados persistentes'),
(2, 'Engenharia de Software', 'Processos de desenvolvimento'),
(3, 'Inteligência Artificial', 'Algoritmos inteligentes'),
(4, 'Redes', 'Comunicação de dados'),
(5, 'Segurança', 'Proteção da informação');

-- 3. Edicoes
INSERT INTO Edicao VALUES
(101, 2024, 'Fechada'),
(102, 2024, 'Aberta'),
(103, 2025, 'Em Planejamento'),
(104, 2025, 'Em Planejamento');

-- 4. Especialização Usuarios
-- Autores
INSERT INTO Autor VALUES 
(1, '0000-0001', 'Estudante Mestrado'),
(2, '0000-0002', 'Pesquisador'),
(3, '0000-0003', 'Estudante Graduação'),
(5, '0000-0005', 'Pai da Computação'),
(6, '0000-0006', 'Primeira Programadora'),
(7, '0000-0007', 'Criadora do COBOL'),
(10, '0000-0010', 'Criador do Linux');

-- Revisores
INSERT INTO Revisor VALUES 
(8, 'Algoritmos', 9.5),
(9, 'Web, Redes', 8.8),
(11, 'Linguagens', 9.0),
(12, 'Sistemas Operacionais', 9.2),
(13, 'Linguagens, SO', 9.3);

-- Editores
INSERT INTO Editor VALUES 
(4, 'Editor Chefe', 1),
(14, 'Editor Associado', 1),
(15, 'Editor Convidado', 1);

-- 5. Tipos de Edição
INSERT INTO Edicao_Regular VALUES (101, 10, 1), (103, 11, 1);
INSERT INTO Chamada_Especial VALUES (102, 'IA Generativa', 'Impactos da IA', '2024-12-31'), (104, 'Segurança em Cloud', 'SecOps', '2025-06-30');

-- 6. Artigos
INSERT INTO Artigo VALUES
(1, 'Otimização com RKO', 'Estudo comparativo RKO vs Li', 'pdf1.pdf', 'Aceito', 101),
(2, 'SQL Avançado', 'Consultas complexas em BD', 'pdf2.pdf', 'Em Revisão', 102),
(3, 'Redes Neurais', 'Deep Learning basico', 'pdf3.pdf', 'Rejeitado', 101),
(4, 'Compiladores Modernos', 'Otimização de código', 'pdf4.pdf', 'Submetido', 103),
(5, 'Segurança Zero Trust', 'Novos paradigmas', 'pdf5.pdf', 'Em Revisão', 102),
(6, 'História da Computação', 'De Babbage a hoje', 'pdf6.pdf', 'Aceito', 101),
(7, 'Sistemas Distribuídos', 'Consenso em redes', 'pdf7.pdf', 'Submetido', 103),
(8, 'Python para Dados', 'Pandas e NumPy', 'pdf8.pdf', 'Aceito', 101),
(9, 'Linux Kernel', 'Gerenciamento de memória', 'pdf9.pdf', 'Em Revisão', 102),
(10, 'Ética em IA', 'Viés algorítmico', 'pdf10.pdf', 'Aceito', 102);

-- 7. Artigo_Area e Autoria
INSERT INTO Artigo_Area VALUES (1, 3), (2, 1), (3, 3), (4, 2), (5, 5), (6, 2), (7, 4), (8, 1), (9, 2), (10, 3);
INSERT INTO Autoria VALUES (1, 1, 1), (2, 1, 2), (5, 2, 1), (6, 3, 1), (7, 4, 1), (10, 9, 1);

-- 8. Revisao
INSERT INTO Revisao VALUES
(1, 1, 8, 'Excelente trabalho', 9.5, '2024-11-20'),
(2, 2, 8, 'Bom, mas precisa ajustes', 7.0, '2024-12-01'),
(3, 3, 11, 'Fora do escopo', 3.0, '2024-11-15'),
(4, 5, 9, 'Muito relevante', 8.5, '2024-12-05'),
(5, 6, 12, 'Texto clássico', 10.0, '2024-11-10'),
(6, 8, 13, 'Código limpo', 9.0, '2024-11-25'),
(7, 9, 12, 'Análise profunda', 8.8, '2024-12-02'),
(8, 10, 11, 'Importante discussão', 9.2, '2024-12-10');
"""
cursor.executescript(dml_script)
print(">>> Dados inseridos com sucesso.")
conn.commit()

# --- FUNÇÃO PARA EXECUTAR E MOSTRAR CONSULTAS ---
def run_query(title, sql):
    print(f"\n--- {title} ---")
    print(f"SQL: {sql}")
    print("RESULTADO:")
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        # Pega nome das colunas para exibir bonitinho
        colnames = [description[0] for description in cursor.description]
        print(f"{' | '.join(colnames)}")
        print("-" * 50)
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Erro: {e}")

print("\n>>> 3. EXECUTANDO CONSULTAS OBRIGATÓRIAS...")

# --- GRUPO 1: CONSULTAS BÁSICAS COM JOIN (5 consultas) ---
run_query("1. Listar Artigos e seus Autores (JOIN)", 
          """SELECT Artigo.Titulo, Usuario.Nome as Autor 
             FROM Artigo 
             JOIN Autoria ON Artigo.Cod_Artigo = Autoria.Cod_Artigo 
             JOIN Usuario ON Autoria.Cod_Autor = Usuario.ID_Usuario;""")

run_query("2. Listar Artigos, suas Áreas e Edições (JOIN 3 Tabelas)",
          """SELECT Artigo.Titulo, Area.Nome_Area, Edicao.Ano 
             FROM Artigo 
             JOIN Artigo_Area ON Artigo.Cod_Artigo = Artigo_Area.Cod_Artigo 
             JOIN Area ON Artigo_Area.Cod_Area = Area.Cod_Area 
             JOIN Edicao ON Artigo.Cod_Edicao = Edicao.Cod_Edicao;""")

run_query("3. Listar Revisores e as notas que deram (JOIN)",
          """SELECT Usuario.Nome as Revisor, Artigo.Titulo, Revisao.Nota 
             FROM Revisao 
             JOIN Revisor ON Revisao.Cod_Revisor = Revisor.ID_Usuario 
             JOIN Usuario ON Revisor.ID_Usuario = Usuario.ID_Usuario
             JOIN Artigo ON Revisao.Cod_Artigo = Artigo.Cod_Artigo;""")

run_query("4. Detalhes das Chamadas Especiais (JOIN)",
          """SELECT Edicao.Ano, Chamada_Especial.Titulo_Tematico, Chamada_Especial.Data_Limite
             FROM Chamada_Especial
             JOIN Edicao ON Chamada_Especial.Cod_Edicao = Edicao.Cod_Edicao;""")

run_query("5. Listar Editores e suas Instituições (JOIN)",
          """SELECT Usuario.Nome, Usuario.Instituicao, Editor.Cargo
             FROM Editor
             JOIN Usuario ON Editor.ID_Usuario = Usuario.ID_Usuario;""")

# --- GRUPO 2: LEFT/RIGHT JOIN (2 consultas) ---
run_query("6. Listar TODAS as Áreas, mesmo as sem artigos vinculados (LEFT JOIN)",
          """SELECT Area.Nome_Area, Artigo.Titulo 
             FROM Area 
             LEFT JOIN Artigo_Area ON Area.Cod_Area = Artigo_Area.Cod_Area
             LEFT JOIN Artigo ON Artigo_Area.Cod_Artigo = Artigo.Cod_Artigo;""")

run_query("7. Listar TODOS os Usuários e verificar se são Autores (LEFT JOIN)",
          """SELECT Usuario.Nome, Autor.ORCID 
             FROM Usuario 
             LEFT JOIN Autor ON Usuario.ID_Usuario = Autor.ID_Usuario
             WHERE Usuario.ID_Usuario <= 10;""")

# --- GRUPO 3: AGREGADORES, GROUP BY, HAVING, ORDER BY (5 consultas) ---
run_query("8. Média das notas dos artigos por Status (AVG, GROUP BY)",
          """SELECT Artigo.Status, AVG(Revisao.Nota) as Media_Nota
             FROM Artigo
             JOIN Revisao ON Artigo.Cod_Artigo = Revisao.Cod_Artigo
             GROUP BY Artigo.Status;""")

run_query("9. Contar quantos artigos existem por Área (COUNT, GROUP BY, ORDER BY)",
          """SELECT Area.Nome_Area, COUNT(Artigo_Area.Cod_Artigo) as Qtd_Artigos
             FROM Area
             JOIN Artigo_Area ON Area.Cod_Area = Artigo_Area.Cod_Area
             GROUP BY Area.Nome_Area
             ORDER BY Qtd_Artigos DESC;""")

run_query("10. Somar total de revisões feitas por cada revisor (SUM/COUNT, HAVING)",
          """SELECT Usuario.Nome, COUNT(Revisao.Cod_Revisao) as Total_Revisoes
             FROM Revisao
             JOIN Usuario ON Revisao.Cod_Revisor = Usuario.ID_Usuario
             GROUP BY Usuario.Nome
             HAVING Total_Revisoes >= 1;""")

run_query("11. Nota Máxima e Mínima dada em revisões por ano de Edição",
          """SELECT Edicao.Ano, MAX(Revisao.Nota) as Nota_Max, MIN(Revisao.Nota) as Nota_Min
             FROM Revisao
             JOIN Artigo ON Revisao.Cod_Artigo = Artigo.Cod_Artigo
             JOIN Edicao ON Artigo.Cod_Edicao = Edicao.Cod_Edicao
             GROUP BY Edicao.Ano;""")

run_query("12. Listar Autores com mais de 1 artigo submetido",
          """SELECT Usuario.Nome, COUNT(Autoria.Cod_Artigo) as Qtd_Artigos
             FROM Autoria
             JOIN Usuario ON Autoria.Cod_Autor = Usuario.ID_Usuario
             GROUP BY Usuario.Nome
             HAVING Qtd_Artigos > 0 -- Coloquei >0 para aparecer no exemplo, mude para >1 se popular mais
             ORDER BY Usuario.Nome;""")

conn.close()
print("\n>>> FIM DO PROCESSAMENTO.")