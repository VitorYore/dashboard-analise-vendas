# 📊 Análise de Vendas — Python, PostgreSQL & Power BI

Projeto de análise de dados desenvolvido para transformar uma base de vendas em informações gerenciais por meio de **Python, Pandas, PostgreSQL, SQL e Power BI**.

O projeto contempla tratamento e preparação dos dados, armazenamento em banco de dados, consultas analíticas em SQL e construção de um dashboard interativo para acompanhamento de **faturamento, lucro, clientes, pagamentos e evolução temporal**.

---

## 🎯 Objetivo

O objetivo do projeto é analisar o desempenho comercial da empresa e transformar os dados de vendas em indicadores que apoiem a tomada de decisão.

Entre as principais perguntas analisadas estão:

- Quanto a empresa faturou?
- Qual foi o lucro e a margem obtida?
- Quais clientes geram maior faturamento?
- Quais clientes são mais lucrativos?
- Como os clientes estão distribuídos por faixa de faturamento?
- Quais formas de pagamento são mais utilizadas?
- Qual forma de pagamento concentra maior faturamento?
- Como faturamento, lucro e margem evoluem ao longo dos meses?
- Qual foi o melhor mês em faturamento?
- Como o ticket médio varia ao longo do período?
- Qual a participação de cada cliente no faturamento?
- Como o faturamento evoluiu em relação ao mês anterior?

---

## 🛠️ Tecnologias utilizadas

- **Python**
- **Pandas**
- **PostgreSQL**
- **SQL**
- **psycopg2**
- **python-dotenv**
- **Excel**
- **Power BI**
- **DAX**
- **Git / GitHub**

---

## 🔄 Pipeline do projeto

O fluxo de tratamento, armazenamento e análise foi estruturado da seguinte forma:

```text
Base original em Excel
        ↓
Tratamento e limpeza com Python / Pandas
        ↓
Geração dos arquivos CSV processados
        ↓
Carga dos dados tratados com Python
        ↓
PostgreSQL
        ↓
Consultas e análises em SQL
        ↓
Power BI / DAX
        ↓
Dashboard interativo
```

A base original utilizada no projeto não foi disponibilizada no repositório por questões de privacidade e segurança dos dados.

As credenciais utilizadas para conexão com o PostgreSQL também não são versionadas. Elas são armazenadas localmente em variáveis de ambiente por meio de um arquivo `.env`, ignorado pelo Git.

---

## 📁 Estrutura do projeto

```text
Portifólio Analise/
│
├── dashboard/
│   ├── Dashboard_vendas.pbix
│   └── Esboco.pptx
│
├── data/
│   ├── processed/
│   │   ├── vendas_analise.csv
│   │   ├── vendas_limpo.csv
│   │   └── vendas_tratadas.csv
│   │
│   └── raw/
│       └── .gitkeep
│
├── database/
│   ├── schema.sql
│   └── queries.sql
│
├── scripts/
│   ├── analise_vendas.py
│   ├── etl.py
│   ├── tratamento_vendas_limpo.py
│   └── carregar_postgresql.py
│
├── .gitignore
└── README.md
```

### `dashboard/`

Contém o arquivo final do Power BI e o esboço utilizado durante o desenvolvimento visual do dashboard.

### `data/processed/`

Contém as versões processadas da base utilizadas durante as etapas de análise.

### `data/raw/`

Mantida no projeto para representar a etapa de dados brutos. A base original não foi publicada.

### `database/`

Contém os arquivos relacionados ao PostgreSQL:

- `schema.sql` — definição da estrutura da tabela utilizada no banco;
- `queries.sql` — consultas SQL desenvolvidas para análise dos dados.

### `scripts/`

Contém os scripts Python utilizados nas etapas de ETL, tratamento, análise exploratória e integração com PostgreSQL.

O arquivo `carregar_postgresql.py` é responsável por ler a base processada, preparar os dados para compatibilidade com o banco e realizar a carga dos registros na tabela `vendas`.

---

# 🗄️ PostgreSQL e SQL

Após o tratamento realizado com Python e Pandas, a base processada é carregada em um banco **PostgreSQL**.

A comunicação entre Python e PostgreSQL é realizada com a biblioteca `psycopg2`.

As informações de conexão são armazenadas em variáveis de ambiente utilizando `python-dotenv`, evitando a exposição de usuário e senha no código-fonte.

Durante a carga também são tratados valores ausentes e datas inválidas para permitir sua representação adequada como `NULL` no PostgreSQL.

## Consultas desenvolvidas

O arquivo `database/queries.sql` contém consultas para análise e validação dos indicadores, incluindo:

- faturamento total;
- lucro total;
- margem total;
- quantidade de pedidos;
- quantidade de clientes únicos;
- faturamento e lucro por mês;
- Top 10 clientes por faturamento;
- margem por forma de pagamento;
- participação dos clientes no faturamento;
- ranking de clientes por faturamento;
- crescimento mensal do faturamento;
- identificação do melhor mês em faturamento;
- visão consolidada dos clientes.

Entre os conceitos SQL utilizados estão:

- `SUM()`;
- `COUNT()`;
- `DISTINCT`;
- `GROUP BY`;
- `ORDER BY`;
- `LIMIT`;
- `ROUND()`;
- `NULLIF()`;
- CTEs (`WITH`);
- Window Functions;
- `RANK()`;
- `LAG()`.

---

# 📈 Dashboard

O dashboard foi dividido em quatro páginas principais:

## 1. Visão Geral

Apresenta uma visão executiva do desempenho das vendas.

Principais indicadores:

- Faturamento
- Lucro
- Margem média
- Quantidade de clientes
- Total de pedidos
- Ticket médio

Também são apresentados:

- Faturamento por mês
- Faturamento por cliente
- Lucro por mês
- Faturamento por forma de pagamento

---

## 2. Clientes

Página dedicada à análise da carteira de clientes.

Principais indicadores:

- Clientes únicos
- Ticket médio por cliente
- Cliente com maior faturamento
- Cliente mais lucrativo

Análises realizadas:

- Faturamento por cliente
- Distribuição dos clientes por faixa de faturamento
- Top 10 clientes por quantidade de pedidos
- Participação do lucro por cliente

A distribuição por faixa de faturamento permite avaliar se a empresa possui uma carteira concentrada em poucos clientes grandes ou distribuída entre clientes de menor e médio porte.

---

## 3. Pagamentos

Página dedicada ao comportamento dos clientes em relação às formas de pagamento.

Principais indicadores:

- Pagamento mais utilizado
- Participação da transferência no faturamento
- Ticket médio por pagamento
- Margem por forma de pagamento

Análises realizadas:

- Faturamento por forma de pagamento
- Quantidade de pedidos por forma de pagamento
- Margem por pagamento
- Evolução mensal do faturamento por forma de pagamento

Um dos principais pontos observados é a concentração relevante do faturamento em **transferências**, enquanto o volume de pedidos apresenta comportamento diferente entre as formas de pagamento.

---

## 4. Evolução Temporal

Página destinada à análise do desempenho ao longo dos meses.

Principais indicadores:

- Melhor mês em faturamento
- Faturamento do melhor mês
- Participação do melhor mês no faturamento total
- Margem de lucro

Análises realizadas:

- Faturamento e lucro por mês
- Ticket médio mensal
- Margem mensal
- Quantidade de pedidos por mês

A análise da margem mensal permite observar que **um mês com faturamento elevado não necessariamente apresenta a maior margem de lucro**. Isso acontece porque o volume de vendas e a rentabilidade das vendas são indicadores diferentes.

---

# 🔎 Principais insights

### 📌 Concentração de faturamento

O faturamento apresenta concentração relevante em determinados clientes, com destaque para os maiores clientes da carteira.

Isso permite avaliar o risco de dependência de poucos clientes e identificar contas estratégicas.

### 📌 Formas de pagamento

A **transferência** representa uma parcela significativa do faturamento total, sendo a principal forma de pagamento em valor faturado.

Por outro lado, a forma de pagamento mais utilizada em quantidade de pedidos pode ser diferente da forma que concentra maior faturamento.

Isso demonstra a importância de analisar **volume e valor separadamente**.

### 📌 Faturamento × margem

O projeto também evidencia uma diferença importante entre faturamento e rentabilidade.

Um mês pode apresentar o maior faturamento do período e, ainda assim, apresentar uma margem inferior a outros meses.

> **Vender mais não significa necessariamente lucrar proporcionalmente mais.**

Essa análise pode indicar períodos com custos ou composição de vendas menos favoráveis.

### 📌 Ticket médio

O ticket médio varia ao longo dos meses e permite identificar períodos em que os pedidos apresentam maior valor médio.

Esse indicador complementa a análise de quantidade de pedidos e faturamento.

---

# 🧹 Tratamento dos dados

O projeto utiliza scripts Python para preparar os dados antes da utilização nas etapas posteriores.

Entre as etapas realizadas estão:

- limpeza da base;
- tratamento dos dados;
- organização das informações;
- tratamento de valores ausentes;
- preparação dos arquivos para análise;
- criação de bases processadas em CSV;
- análise exploratória;
- preparação e carga dos dados no PostgreSQL.

O objetivo foi garantir uma base mais consistente para a construção dos indicadores, consultas e visualizações.

---

# 📊 Power BI

O dashboard utiliza medidas e cálculos em **DAX** para criação dos principais indicadores.

Entre os conceitos utilizados estão:

- faturamento;
- lucro;
- margem;
- ticket médio;
- quantidade de pedidos;
- clientes únicos;
- participação percentual;
- análise mensal;
- ranking de clientes;
- análise por forma de pagamento.

O dashboard também possui navegação entre páginas por meio de botões personalizados, integrados ao layout visual desenvolvido para o projeto.

---

# 🚀 Como utilizar

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Acesse a pasta

```bash
cd portfolio-analise-vendas
```

### 3. Scripts Python

Os scripts estão disponíveis em:

```text
scripts/
```

As bases processadas estão disponíveis em:

```text
data/processed/
```

### 4. Banco de dados

A estrutura da tabela PostgreSQL está disponível em:

```text
database/schema.sql
```

As consultas analíticas estão disponíveis em:

```text
database/queries.sql
```

O script responsável pela carga dos dados no PostgreSQL está disponível em:

```text
scripts/carregar_postgresql.py
```

### 5. Dashboard

Abra:

```text
dashboard/Dashboard_vendas.pbix
```

com o **Microsoft Power BI Desktop**.

### 🌐 Dashboard interativo

[Visualizar Dashboard no Power BI](https://app.powerbi.com/view?r=eyJrIjoiZmE3MDIyODMtMDUwNS00ZmRjLWI1ZjctYzIzNzcyMjgzZDJlIiwidCI6IjkwOTc0N2Q1LWJhM2MtNGQ0YS05NjI2LWMxOWI5YjhhZmY5YSJ9)

---

# 📷 Dashboard

## 📊 Capa

<img width="1442" height="811" alt="Capa" src="https://github.com/user-attachments/assets/5e44ed0f-3912-49ec-9099-9804d46beef0" />

## 📈 Visão Geral do Dashboard

<img width="1445" height="809" alt="VisaoGeral" src="https://github.com/user-attachments/assets/c6193ab9-b7cf-4420-9ffb-f7e0dc8d4825" />

## 👥 Análise de Clientes

<img width="1442" height="808" alt="Clientes" src="https://github.com/user-attachments/assets/7c2d24ae-6c02-4241-869e-f08f75c8c456" />

## 💳 Fluxo de Pagamentos

<img width="1442" height="809" alt="Pagamentos" src="https://github.com/user-attachments/assets/3100067a-f278-4cab-8b69-fff6b7f78d7c" />

## 🚀 Desempenho

<img width="1444" height="809" alt="Desempenho" src="https://github.com/user-attachments/assets/cf83d763-86a0-40f3-8cb8-f39799229739" />

---

# 📌 Objetivo profissional

Este projeto foi desenvolvido especificamente para **portfólio profissional na área de Análise de Dados**, demonstrando conhecimentos em:

- tratamento e preparação de dados;
- ETL;
- análise exploratória;
- Python e Pandas;
- PostgreSQL;
- SQL para análise de dados;
- integração entre Python e banco de dados;
- consultas analíticas;
- construção de indicadores;
- DAX;
- Power BI;
- visualização de dados;
- criação de dashboards orientados à tomada de decisão;
- Git e GitHub.

---

## 👨‍💻 Autor

**Vitor Yore**

Projeto desenvolvido para portfólio profissional em **Análise de Dados**.