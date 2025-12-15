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
        DROP TABLE IF EXISTS Revisor_Area;
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
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL,
            Instituicao TEXT,
            Data_Cadastro DATE NOT NULL
        );
        
        CREATE TABLE Autor (
            ID_Usuario INTEGER PRIMARY KEY,
            ORCID TEXT,
            Bio_Resumida TEXT,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
        );
        
        CREATE TABLE Revisor (
            ID_Usuario INTEGER PRIMARY KEY,
            Nota_Media REAL,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
        );
        
        CREATE TABLE Editor (
            ID_Usuario INTEGER PRIMARY KEY,
            Cargo TEXT,
            Ativo BOOLEAN DEFAULT 1,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
        );
        
        CREATE TABLE Area (
            Cod_Area INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Area TEXT NOT NULL,
            Descricao TEXT
        );
        
        CREATE TABLE Edicao (
            Cod_Edicao INTEGER PRIMARY KEY AUTOINCREMENT,
            Ano INTEGER NOT NULL,
            Status TEXT
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
            Cod_Artigo INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Resumo TEXT,
            Arquivo TEXT,
            Status TEXT,
            Cod_Edicao INTEGER NOT NULL,
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
            Cod_Artigo INTEGER,
            Cod_Revisor INTEGER,
            Parecer TEXT,
            Nota REAL,
            Data_Entrega DATE,
            PRIMARY KEY (Cod_Artigo, Cod_Revisor),
            FOREIGN KEY (Cod_Artigo) REFERENCES Artigo(Cod_Artigo),
            FOREIGN KEY (Cod_Revisor) REFERENCES Revisor(ID_Usuario)
        );
        
        CREATE TABLE Revisor_Area (
            ID_Revisor INTEGER,
            Cod_Area INTEGER,
            PRIMARY KEY (ID_Revisor, Cod_Area),
            FOREIGN KEY (ID_Revisor) REFERENCES Revisor(ID_Usuario),
            FOREIGN KEY (Cod_Area) REFERENCES Area(Cod_Area)
        );
    """)
    
    # INSERT dados fictícios (DML)
    
    # Usuários (12 usuários)
    usuarios = [
        ('João Silva', 'joao.silva@univ.edu.br', 'senha123', 'Universidade A', '2023-01-15'),
        ('Maria Santos', 'maria.santos@inst.org', 'senha456', 'Instituto B', '2023-02-20'),
        ('Pedro Souza', 'pedro.souza@tech.com', 'senha789', 'Tech Solutions', '2023-03-10'),
        ('Ana Oliveira', 'ana.oliveira@univ.edu.br', 'senhaabc', 'Universidade A', '2023-03-15'),
        ('Carlos Pereira', 'carlos.pereira@univ.c', 'senhadef', 'Universidade C', '2023-01-10'),
        ('Fernanda Costa', 'fernanda.costa@lab.net', 'senhaghi', 'Laboratório X', '2023-02-28'),
        ('Lucas Almeida', 'lucas.almeida@univ.edu.br', 'senhajkl', 'Universidade A', '2023-04-05'),
        ('Julia Lima', 'julia.lima@inst.org', 'senhamno', 'Instituto B', '2023-04-20'),
        ('Marcos Rocha', 'marcos.rocha@editora.com', 'senhapqr', 'Editora Global', '2022-11-01'),
        ('Patricia Gomes', 'patricia.gomes@univ.c', 'senhastu', 'Universidade C', '2022-12-15'),
        ('Rafael Mendes', 'rafael.mendes@univ.edu.br', 'senhavwx', 'Universidade A', '2022-10-30'),
        ('Sofia Martins', 'sofia.martins@tech.com', 'senhayz1', 'Tech Solutions', '2023-01-05')
    ]
    
    cursor.executemany("""
        INSERT INTO Usuario (Nome, Email, Senha, Instituicao, Data_Cadastro) 
        VALUES (?, ?, ?, ?, ?)
    """, usuarios)
    
    # Autores (4 autores - IDs 1 a 4)
    autores = [
        (1, '0000-0001-2345-6789', 'Pesquisador em IA.'),
        (2, '0000-0002-3456-7890', 'Especialista em Banco de Dados.'),
        (3, '0000-0003-4567-8901', 'Engenheiro de Software Sênior.'),
        (4, '0000-0004-5678-9012', 'Doutoranda em Redes.')
    ]
    
    cursor.executemany("""
        INSERT INTO Autor (ID_Usuario, ORCID, Bio_Resumida) 
        VALUES (?, ?, ?)
    """, autores)
    
    # Revisores (4 revisores - IDs 5 a 8)
    revisores = [
        (5, 9.5),
        (6, 8.7),
        (7, 9.0),
        (8, 7.5)
    ]
    
    cursor.executemany("""
        INSERT INTO Revisor (ID_Usuario, Nota_Media) 
        VALUES (?, ?)
    """, revisores)
    
    # Editores (4 editores - IDs 9 a 12)
    editores = [
        (9, 'Editor Chefe', 1),
        (10, 'Editor Associado', 1),
        (11, 'Editor Convidado', 0),
        (12, 'Editor Técnico', 1)
    ]
    
    cursor.executemany("""
        INSERT INTO Editor (ID_Usuario, Cargo, Ativo) 
        VALUES (?, ?, ?)
    """, editores)
    
    # Áreas (10 áreas)
    areas = [
        ('Inteligência Artificial', 'Estudo de agentes inteligentes e aprendizado de máquina.'),
        ('Banco de Dados', 'Gerenciamento, modelagem e otimização de dados.'),
        ('Engenharia de Software', 'Processos, métodos e ferramentas para desenvolvimento.'),
        ('Redes de Computadores', 'Comunicação de dados e protocolos.'),
        ('Segurança da Informação', 'Proteção de sistemas e dados.'),
        ('Sistemas Operacionais', 'Gerenciamento de recursos de hardware e software.'),
        ('Interação Humano-Computador', 'Design e avaliação de interfaces.'),
        ('Computação Gráfica', 'Processamento de imagens e renderização.'),
        ('Bioinformática', 'Aplicação de computação em biologia.'),
        ('Internet das Coisas', 'Conectividade de dispositivos embarcados.')
    ]
    
    cursor.executemany("""
        INSERT INTO Area (Nome_Area, Descricao) 
        VALUES (?, ?)
    """, areas)
    
    # Edições (10 edições)
    edicoes = [
        (2023, 'Fechada'),
        (2023, 'Fechada'),
        (2024, 'Publicada'),
        (2024, 'Publicada'),
        (2024, 'Em andamento'),
        (2025, 'Aberta'),
        (2025, 'Aberta'),
        (2025, 'Planejada'),
        (2025, 'Planejada'),
        (2026, 'Planejada')
    ]
    
    cursor.executemany("""
        INSERT INTO Edicao (Ano, Status) 
        VALUES (?, ?)
    """, edicoes)
    
    # Edições Regulares (5 regulares)
    edicoes_regulares = [
        (1, 10, 1),
        (2, 10, 2),
        (3, 11, 1),
        (4, 11, 2),
        (5, 11, 3)
    ]
    
    cursor.executemany("""
        INSERT INTO Edicao_Regular (Cod_Edicao, Volume, Numero) 
        VALUES (?, ?, ?)
    """, edicoes_regulares)
    
    # Chamadas Especiais (5 especiais)
    chamadas = [
        (6, 'Avanços em IA Generativa', 'Foco em LLMs e difusão.', '2025-06-30'),
        (7, 'Segurança em IoT', 'Desafios de privacidade em dispositivos conectados.', '2025-07-15'),
        (8, 'Big Data na Saúde', 'Análise de grandes volumes de dados médicos.', '2025-09-01'),
        (9, 'Computação Quântica', 'Algoritmos e arquiteturas quânticas.', '2025-10-20'),
        (10, 'Cidades Inteligentes', 'Tecnologia aplicada ao urbanismo.', '2026-01-15')
    ]
    
    cursor.executemany("""
        INSERT INTO Chamada_Especial (Cod_Edicao, Titulo_Tematico, Descricao, Data_Limite) 
        VALUES (?, ?, ?, ?)
    """, chamadas)
    
    # Artigos (10 artigos)
    artigos = [
        ('Uso de Redes Neurais em Finanças', 'Análise preditiva de mercado.', 'artigo1.pdf', 'Aceito', 1),
        ('Otimização de Queries SQL', 'Novas técnicas de indexação.', 'artigo2.pdf', 'Publicado', 1),
        ('Metodologias Ágeis em Startups', 'Estudo de caso.', 'artigo3.pdf', 'Rejeitado', 2),
        ('Protocolos de Roteamento', 'Comparação entre OSPF e BGP.', 'artigo4.pdf', 'Publicado', 2),
        ('Criptografia Pós-Quântica', 'Algoritmos resistentes a computadores quânticos.', 'artigo5.pdf', 'Em Revisão', 6),
        ('Interface para Idosos', 'Acessibilidade digital.', 'artigo6.pdf', 'Submetido', 7),
        ('Renderização em Tempo Real', 'Técnicas de Ray Tracing.', 'artigo7.pdf', 'Aceito', 3),
        ('Genômica Computacional', 'Alinhamento de sequências.', 'artigo8.pdf', 'Em Revisão', 8),
        ('Sensores em Agricultura', 'IoT no campo.', 'artigo9.pdf', 'Submetido', 9),
        ('Virtualização de Servidores', 'Docker e Kubernetes.', 'artigo10.pdf', 'Publicado', 4)
    ]
    
    cursor.executemany("""
        INSERT INTO Artigo (Titulo, Resumo, Arquivo, Status, Cod_Edicao) 
        VALUES (?, ?, ?, ?, ?)
    """, artigos)
    
    # Artigo_Area (vincular artigos com áreas)
    artigo_areas = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 6),
        (1, 2),
        (9, 4)
    ]
    
    cursor.executemany("""
        INSERT INTO Artigo_Area (Cod_Artigo, Cod_Area) 
        VALUES (?, ?)
    """, artigo_areas)
    
    # Autoria
    autorias = [
        (1, 1, 1),
        (2, 2, 1),
        (3, 3, 1),
        (4, 4, 1),
        (1, 5, 1),
        (2, 5, 2),
        (3, 6, 1),
        (4, 7, 1),
        (1, 8, 1),
        (2, 9, 1),
        (3, 10, 1),
        (4, 10, 2)
    ]
    
    cursor.executemany("""
        INSERT INTO Autoria (Cod_Autor, Cod_Artigo, Ordem_Autoria) 
        VALUES (?, ?, ?)
    """, autorias)
    
    # Revisor_Area (vincular revisores com áreas)
    revisor_areas = [
        (5, 1),
        (5, 2),
        (6, 3),
        (6, 4),
        (7, 5),
        (7, 6),
        (8, 7),
        (8, 8),
        (8, 9),
        (5, 10)
    ]
    
    cursor.executemany("""
        INSERT INTO Revisor_Area (ID_Revisor, Cod_Area) 
        VALUES (?, ?)
    """, revisor_areas)
    
    # Revisões (10 revisões)
    revisoes = [
        (1, 5, 'Excelente trabalho, metodologia sólida.', 9.5, '2023-02-10'),
        (2, 5, 'Bom, mas precisa de revisão bibliográfica.', 7.0, '2023-02-12'),
        (3, 6, 'Não atende aos requisitos da chamada.', 4.0, '2023-03-01'),
        (4, 6, 'Muito relevante para a área.', 8.5, '2023-03-05'),
        (5, 7, 'Inovador, recomendo publicação.', 9.0, '2025-01-10'),
        (6, 8, 'Amostragem pequena.', 6.0, '2025-02-15'),
        (7, 8, 'Visualmente impressionante.', 9.0, '2024-05-20'),
        (8, 5, 'Análise estatística fraca.', 5.5, '2025-03-01'),
        (9, 6, 'Aplicação prática interessante.', 8.0, '2025-04-10'),
        (10, 7, 'Bem escrito e fundamentado.', 9.0, '2024-06-01')
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

# Dicionário com as 12 consultas obrigatórias
CONSULTAS_PRONTAS = {
    "Selecione uma consulta...": "",
    
    "1. Listar Artigos e Anos de Edição": """
SELECT A.Titulo, E.Ano, A.Status
FROM Artigo A
JOIN Edicao E ON A.Cod_Edicao = E.Cod_Edicao;
""",
    
    "2. Autores e Seus Artigos": """
SELECT U.Nome AS Autor, AR.Titulo
FROM Usuario U
JOIN Autoria AUT ON U.ID_Usuario = AUT.Cod_Autor
JOIN Artigo AR ON AUT.Cod_Artigo = AR.Cod_Artigo;
""",
    
    "3. Revisores e Suas Áreas de Conhecimento": """
SELECT U.Nome AS Revisor, AREA.Nome_Area
FROM Usuario U
JOIN Revisor R ON U.ID_Usuario = R.ID_Usuario
JOIN Revisor_Area RA ON R.ID_Usuario = RA.ID_Revisor
JOIN Area AREA ON RA.Cod_Area = AREA.Cod_Area;
""",
    
    "4. Artigos com Pareceres e Notas": """
SELECT A.Titulo, U.Nome AS Revisor, R.Nota
FROM Artigo A
JOIN Revisao R ON A.Cod_Artigo = R.Cod_Artigo
JOIN Usuario U ON R.Cod_Revisor = U.ID_Usuario;
""",
    
    "5. Chamadas Especiais e Datas Limite": """
SELECT CE.Titulo_Tematico, CE.Data_Limite, E.Status
FROM Chamada_Especial CE
JOIN Edicao E ON CE.Cod_Edicao = E.Cod_Edicao;
""",
    
    "6. Usuários e Cargos de Editores (LEFT JOIN)": """
SELECT U.Nome, E.Cargo
FROM Usuario U
LEFT JOIN Editor E ON U.ID_Usuario = E.ID_Usuario;
""",
    
    "7. Áreas e Artigos Vinculados (LEFT JOIN)": """
SELECT AREA.Nome_Area, AR.Titulo
FROM Area AREA
LEFT JOIN Artigo_Area AA ON AREA.Cod_Area = AA.Cod_Area
LEFT JOIN Artigo AR ON AA.Cod_Artigo = AR.Cod_Artigo;
""",
    
    "8. Quantidade de Artigos por Status (HAVING)": """
SELECT Status, COUNT(*) AS Qtd_Artigos
FROM Artigo
GROUP BY Status
HAVING COUNT(*) > 1
ORDER BY Qtd_Artigos DESC;
""",
    
    "9. Média de Notas por Revisor (HAVING)": """
SELECT U.Nome AS Revisor, AVG(R.Nota) AS Media_Notas_Dadas
FROM Usuario U
JOIN Revisao R ON U.ID_Usuario = R.Cod_Revisor
GROUP BY U.Nome
HAVING AVG(R.Nota) > 7.0
ORDER BY Media_Notas_Dadas DESC;
""",
    
    "10. Áreas com 2+ Revisores": """
SELECT A.Nome_Area, COUNT(RA.ID_Revisor) AS Qtd_Revisores
FROM Area A
JOIN Revisor_Area RA ON A.Cod_Area = RA.Cod_Area
GROUP BY A.Nome_Area
HAVING COUNT(RA.ID_Revisor) >= 2
ORDER BY A.Nome_Area ASC;
""",
    
    "11. Edições por Soma de Notas (HAVING)": """
SELECT E.Ano, SUM(REV.Nota) AS Soma_Notas
FROM Edicao E
JOIN Artigo A ON E.Cod_Edicao = A.Cod_Edicao
JOIN Revisao REV ON A.Cod_Artigo = REV.Cod_Artigo
GROUP BY E.Ano
HAVING SUM(REV.Nota) > 10
ORDER BY Soma_Notas DESC;
""",
    
    "12. Contagem de Artigos por Autor": """
SELECT U.Nome AS Autor, COUNT(AUT.Cod_Artigo) AS Total_Artigos
FROM Usuario U
JOIN Autoria AUT ON U.ID_Usuario = AUT.Cod_Autor
GROUP BY U.Nome
HAVING COUNT(AUT.Cod_Artigo) >= 1
ORDER BY Total_Artigos DESC;
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
    <small>Sistema desenvolvido para o Trabalho Final de Banco de Dados | 2025</small>
</div>
""", unsafe_allow_html=True)
