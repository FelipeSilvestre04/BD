# Sistema de Submissão de Artigos em Periódicos

## Descrição

Sistema de gerenciamento de submissão de artigos científicos desenvolvido como Trabalho Final da disciplina de Banco de Dados. O projeto implementa um **SQL Runner** completo com interface web interativa usando Streamlit, permitindo executar consultas SQL em um banco de dados SQLite que modela todo o fluxo de submissão, revisão e publicação de artigos em periódicos científicos.

## Funcionalidades

- **Gerenciamento Completo de Banco de Dados**
  - Criação automática do schema SQLite com 13 tabelas relacionadas
  - População automática com dados fictícios (12 usuários, 10 artigos, 10 revisões)
  - Botão de reset para reinicializar o banco com um clique

- **SQL Runner Interativo**
  - Editor SQL com syntax highlighting
  - Suporte para comandos `SELECT`, `INSERT`, `UPDATE` e `DELETE`
  - Visualização de resultados em tabelas interativas
  - Download de resultados em formato CSV

- **12 Consultas Obrigatórias Pré-configuradas**
  - JOINs entre múltiplas tabelas
  - LEFT JOINs para análise de dados opcionais
  - Funções agregadas (COUNT, AVG, SUM)
  - Agrupamentos com GROUP BY e HAVING
  - Consultas com filtros e ordenações

- **Dashboard de Estatísticas**
  - Contadores em tempo real de usuários, artigos e revisões
  - Informações do banco de dados

## Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit** - Framework para criação da interface web
- **SQLite3** - Sistema de gerenciamento de banco de dados
- **Pandas** - Manipulação e visualização de dados

## Instalação

### Pré-requisitos

- Python 3.7 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/BD.git
   cd BD
   ```

2. **Instale as dependências**
   ```bash
   pip install streamlit pandas
   ```

3. **Execute o aplicativo**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador**
   - O aplicativo abrirá automaticamente em `http://localhost:8501`
   - Caso não abra, acesse manualmente o endereço acima

## Como Usar

### 1. Inicializar o Banco de Dados

Na primeira execução (ou para resetar):
1. Clique no botão **"Resetar/Criar Banco"** na barra lateral
2. Aguarde a mensagem de sucesso
3. Verifique as estatísticas atualizadas na sidebar

### 2. Executar Consultas Pré-configuradas

1. No menu dropdown **"Consultas Prontas"**, selecione uma das 12 consultas obrigatórias
2. O código SQL aparecerá automaticamente no editor
3. Clique em **"Executar"**
4. Visualize os resultados na tabela abaixo
5. (Opcional) Clique em **"Download CSV"** para exportar os dados

### 3. Escrever Consultas Personalizadas

1. Digite ou edite o SQL diretamente no editor de texto
2. Clique em **"Executar"**
3. Para comandos SELECT: veja a tabela de resultados
4. Para INSERT/UPDATE/DELETE: veja a mensagem de confirmação

### 4. Testar Comandos de Escrita

Experimente os exemplos no menu:
- **INSERT - Novo Usuário**: Adiciona um usuário ao banco
- **UPDATE - Atualizar Status de Artigo**: Modifica o status de um artigo
- **DELETE - Remover Revisão**: Remove uma revisão específica

## Estrutura do Banco de Dados

### Modelo Entidade-Relacionamento

O banco possui **13 tabelas** organizadas em 4 módulos principais:

#### 1. Módulo de Usuários
- **Usuario**: Dados básicos (ID, Nome, Email, Senha, Instituição, Data_Cadastro)
- **Autor**: Informações específicas de autores (ORCID, Bio_Resumida)
- **Revisor**: Dados de revisores (Nota_Media)
- **Editor**: Informações de editores (Cargo, Ativo)
- **Revisor_Area**: Relação N:N entre revisores e áreas de conhecimento

#### 2. Módulo de Classificação
- **Area**: Áreas do conhecimento (IA, Banco de Dados, Redes, etc.)

#### 3. Módulo de Edições
- **Edicao**: Edições do periódico (Ano, Status)
- **Edicao_Regular**: Edições regulares (Volume, Número)
- **Chamada_Especial**: Chamadas temáticas especiais (Título, Descrição, Data Limite)

#### 4. Módulo de Artigos
- **Artigo**: Artigos submetidos (Título, Resumo, Status)
- **Artigo_Area**: Relação N:N entre artigos e áreas
- **Autoria**: Relação entre autores e artigos (com ordem)
- **Revisao**: Revisões de artigos (Parecer, Nota, Data) - PK composta: (Cod_Artigo, Cod_Revisor)

### Diagrama Simplificado

```
Usuario
├── Autor ────> Autoria ────> Artigo ────> Edicao
├── Revisor ──> Revisao ────┘     │          │
│             │                   │          ├── Edicao_Regular
│             └── Revisor_Area    │          └── Chamada_Especial
└── Editor                        │
                                  │
Area <────> Artigo_Area <────────┘
     └────> Revisor_Area
```

## Consultas Disponíveis

### Consultas Obrigatórias (1-12)

1. **Listar Artigos e Anos de Edição** - JOIN simples entre Artigo e Edição
2. **Autores e Seus Artigos** - JOIN de 3 tabelas (Usuario, Autoria, Artigo)
3. **Revisores e Suas Áreas de Conhecimento** - JOIN de 4 tabelas usando Revisor_Area
4. **Artigos com Pareceres e Notas** - JOIN entre Artigo, Revisao e Usuario
5. **Chamadas Especiais e Datas Limite** - JOIN entre Chamada_Especial e Edicao
6. **Usuários e Cargos de Editores** - LEFT JOIN mostrando todos os usuários
7. **Áreas e Artigos Vinculados** - LEFT JOIN mostrando áreas sem artigos
8. **Quantidade de Artigos por Status** - GROUP BY com HAVING COUNT > 1
9. **Média de Notas por Revisor** - AVG com HAVING > 7.0
10. **Áreas com 2+ Revisores** - COUNT com HAVING usando Revisor_Area
11. **Edições por Soma de Notas** - SUM com HAVING > 10
12. **Contagem de Artigos por Autor** - COUNT de artigos por autor

## Exemplos de Uso

### Exemplo 1: Buscar todos os artigos aceitos

```sql
SELECT Cod_Artigo, Titulo, Status 
FROM Artigo 
WHERE Status = 'Aceito';
```

### Exemplo 2: Inserir um novo autor

```sql
INSERT INTO Usuario (Nome, Email, Senha, Instituicao, Data_Cadastro)
VALUES ('Ada Lovelace Jr', 'ada.jr@exemplo.com', 'senha456', 'MIT', '2025-01-20');
```

### Exemplo 3: Atualizar nota média de um revisor

```sql
UPDATE Revisor 
SET Nota_Media = 9.2 
WHERE ID_Usuario = 11;
```

## Dados Fictícios

O banco é populado automaticamente com dados fictícios de exemplo:

- **Usuários**: João Silva, Maria Santos, Pedro Souza, Ana Oliveira, entre outros (12 total)
- **Autores**: 4 autores com ORCID
- **Revisores**: 4 revisores vinculados a diferentes áreas
- **Editores**: 4 editores com diferentes cargos
- **Artigos**: 10 artigos sobre temas variados (IA, Banco de Dados, Segurança, IoT, etc.)
- **Áreas**: 10 áreas do conhecimento (IA, Banco de Dados, Engenharia de Software, Redes, etc.)

## Arquivos do Projeto

```
BD/
├── app.py                 # Aplicação principal Streamlit
├── submissao.db          # Banco de dados SQLite (gerado automaticamente)
├── banco_de_dados.py     # (opcional) Script auxiliar
└── README.md             # Este arquivo
```

## Requisitos do Sistema

- **SO**: Windows, Linux ou macOS
- **Python**: 3.7+
- **Memória**: 100 MB (mínimo)
- **Espaço em Disco**: 10 MB

## Solução de Problemas

### O banco está vazio
- Clique no botão **"Resetar/Criar Banco"** na sidebar

### Erro ao executar INSERT/UPDATE/DELETE
- Verifique se o registro existe (para UPDATE/DELETE)
- Confirme que os valores inseridos respeitam as constraints (PKs, FKs, CHECKs)

### Consulta retorna vazio
- Execute uma consulta simples primeiro: `SELECT * FROM Usuario LIMIT 5`
- Verifique se o banco foi inicializado corretamente

## Melhorias Futuras

- [ ] Autenticação de usuários
- [ ] Editor SQL com autocomplete
- [ ] Visualizações gráficas (charts)
- [ ] Export para outros formatos (Excel, JSON)
- [ ] Histórico de consultas executadas
- [ ] Modo escuro

## Grupo

**Trabalho Final - Disciplina de Banco de Dados**  
Universidade Federal de São Paulo (UNIFESP)

- Felipe Silvestre Cardoso Roberto - 170 425
- Abner Augusto Diniz - 168 476
- João Vitor de Moura - 168 887

## Licença

Este projeto foi desenvolvido para fins educacionais como parte do Trabalho Final da disciplina de Banco de Dados.

---


