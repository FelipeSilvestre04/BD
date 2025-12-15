import sqlite3
import pandas as pd

# Caminho do banco de dados
DB_PATH = "submissao.db"

# Dicionário com as 12 consultas obrigatórias aprovadas pela professora
CONSULTAS = {
    1: {
        "nome": "Listar Artigos e Anos de Edição",
        "sql": """
SELECT A.Titulo, E.Ano, A.Status
FROM Artigo A
JOIN Edicao E ON A.Cod_Edicao = E.Cod_Edicao;
"""
    },
    
    2: {
        "nome": "Autores e Seus Artigos",
        "sql": """
SELECT U.Nome AS Autor, AR.Titulo
FROM Usuario U
JOIN Autoria AUT ON U.ID_Usuario = AUT.Cod_Autor
JOIN Artigo AR ON AUT.Cod_Artigo = AR.Cod_Artigo;
"""
    },
    
    3: {
        "nome": "Revisores e Suas Áreas de Conhecimento",
        "sql": """
SELECT U.Nome AS Revisor, AREA.Nome_Area
FROM Usuario U
JOIN Revisor R ON U.ID_Usuario = R.ID_Usuario
JOIN Revisor_Area RA ON R.ID_Usuario = RA.ID_Revisor
JOIN Area AREA ON RA.Cod_Area = AREA.Cod_Area;
"""
    },
    
    4: {
        "nome": "Artigos com Pareceres e Notas",
        "sql": """
SELECT A.Titulo, U.Nome AS Revisor, R.Nota
FROM Artigo A
JOIN Revisao R ON A.Cod_Artigo = R.Cod_Artigo
JOIN Usuario U ON R.Cod_Revisor = U.ID_Usuario;
"""
    },
    
    5: {
        "nome": "Chamadas Especiais e Datas Limite",
        "sql": """
SELECT CE.Titulo_Tematico, CE.Data_Limite, E.Status
FROM Chamada_Especial CE
JOIN Edicao E ON CE.Cod_Edicao = E.Cod_Edicao;
"""
    },
    
    6: {
        "nome": "Usuários e Cargos de Editores (LEFT JOIN)",
        "sql": """
SELECT U.Nome, E.Cargo
FROM Usuario U
LEFT JOIN Editor E ON U.ID_Usuario = E.ID_Usuario;
"""
    },
    
    7: {
        "nome": "Áreas e Artigos Vinculados (LEFT JOIN)",
        "sql": """
SELECT AREA.Nome_Area, AR.Titulo
FROM Area AREA
LEFT JOIN Artigo_Area AA ON AREA.Cod_Area = AA.Cod_Area
LEFT JOIN Artigo AR ON AA.Cod_Artigo = AR.Cod_Artigo;
"""
    },
    
    8: {
        "nome": "Quantidade de Artigos por Status (HAVING)",
        "sql": """
SELECT Status, COUNT(*) AS Qtd_Artigos
FROM Artigo
GROUP BY Status
HAVING COUNT(*) > 1
ORDER BY Qtd_Artigos DESC;
"""
    },
    
    9: {
        "nome": "Média de Notas por Revisor (HAVING)",
        "sql": """
SELECT U.Nome AS Revisor, AVG(R.Nota) AS Media_Notas_Dadas
FROM Usuario U
JOIN Revisao R ON U.ID_Usuario = R.Cod_Revisor
GROUP BY U.Nome
HAVING AVG(R.Nota) > 7.0
ORDER BY Media_Notas_Dadas DESC;
"""
    },
    
    10: {
        "nome": "Áreas com 2+ Revisores",
        "sql": """
SELECT A.Nome_Area, COUNT(RA.ID_Revisor) AS Qtd_Revisores
FROM Area A
JOIN Revisor_Area RA ON A.Cod_Area = RA.Cod_Area
GROUP BY A.Nome_Area
HAVING COUNT(RA.ID_Revisor) >= 2
ORDER BY A.Nome_Area ASC;
"""
    },
    
    11: {
        "nome": "Edições por Soma de Notas (HAVING)",
        "sql": """
SELECT E.Ano, SUM(REV.Nota) AS Soma_Notas
FROM Edicao E
JOIN Artigo A ON E.Cod_Edicao = A.Cod_Edicao
JOIN Revisao REV ON A.Cod_Artigo = REV.Cod_Artigo
GROUP BY E.Ano
HAVING SUM(REV.Nota) > 10
ORDER BY Soma_Notas DESC;
"""
    },
    
    12: {
        "nome": "Contagem de Artigos por Autor",
        "sql": """
SELECT U.Nome AS Autor, COUNT(AUT.Cod_Artigo) AS Total_Artigos
FROM Usuario U
JOIN Autoria AUT ON U.ID_Usuario = AUT.Cod_Autor
GROUP BY U.Nome
HAVING COUNT(AUT.Cod_Artigo) >= 1
ORDER BY Total_Artigos DESC;
"""
    }
}

def executar_query(conn, sql):
    """Executa uma query e retorna o resultado como DataFrame"""
    try:
        df = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as e:
        return None, str(e)

def imprimir_resultado(num, nome, sql, df, erro=None):
    """Imprime o resultado de uma query no formato especificado"""
    print(f"\n{'=' * 70}")
    print(f"--- {num}. {nome} ---")
    print(f"\nSQL:{sql}")
    
    if erro:
        print(f"\n❌ ERRO: {erro}")
    elif df is not None and not df.empty:
        print(f"\nRESULTADO:")
        # Cabeçalho com os nomes das colunas
        colunas = " | ".join(df.columns)
        print(colunas)
        print("-" * 70)
        
        # Imprimir cada linha
        for idx, row in df.iterrows():
            valores = tuple(row)
            print(valores)
        
        print(f"\nTotal de linhas: {len(df)}")
    else:
        print(f"\nRESULTADO: Nenhum registro encontrado")
    
    print(f"{'=' * 70}\n")

def main():
    """Função principal que executa todas as queries"""
    print("\n" + "=" * 70)
    print("EXECUÇÃO DE TODAS AS QUERIES - TRABALHO FINAL DE BANCO DE DADOS")
    print("=" * 70)
    
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect(DB_PATH)
        print(f"\n✓ Conectado ao banco: {DB_PATH}")
        
        # Executa cada consulta
        for num in sorted(CONSULTAS.keys()):
            consulta = CONSULTAS[num]
            nome = consulta["nome"]
            sql = consulta["sql"]
            
            df, erro = executar_query(conn, sql)
            imprimir_resultado(num, nome, sql, df, erro)
        
        # Fecha conexão
        conn.close()
        print(f"\n✓ Conexão fechada")
        
    except sqlite3.Error as e:
        print(f"\n❌ Erro ao conectar ao banco de dados: {e}")
        print(f"Certifique-se de que o arquivo '{DB_PATH}' existe.")
        print(f"Execute o app.py e clique em 'Resetar/Criar Banco' primeiro.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 70)
    print("FIM DA EXECUÇÃO")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
