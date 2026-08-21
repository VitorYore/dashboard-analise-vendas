import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Caminho do CSV final
arquivo = "data/processed/vendas_analise.csv"

# Ler CSV tratado
df = pd.read_csv(
    arquivo,
    sep=";",
    decimal=",",
    encoding="utf-8-sig"
)

# Padronizar nomes das colunas para o PostgreSQL
df.columns = [
    "pedido",
    "data",
    "total_custo",
    "valor_liquido",
    "forma_pagamento",
    "cliente",
    "lucro",
    "percentual_lucro",
    "status",
    "ano",
    "mes",
    "nome_mes",
    "trimestre",
    "pagamento",
]

# Converter data
df["data"] = pd.to_datetime(
    df["data"],
    format="mixed",
    errors="coerce"
)

print("Datas inválidas encontradas:")
print(df.loc[df["data"].isna(), ["pedido", "data"]])

df["data"] = df["data"].dt.date
df["data"] = df["data"].where(df["data"].notna(), None)

# Converter NaN / NaT em None para o PostgreSQL
df = df.astype(object).where(pd.notna(df), None)

# Criar conexão
conexao = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conexao.cursor()

sql = """
INSERT INTO vendas (
    pedido,
    data,
    total_custo,
    valor_liquido,
    forma_pagamento,
    cliente,
    lucro,
    percentual_lucro,
    status,
    ano,
    mes,
    nome_mes,
    trimestre,
    pagamento
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""
registros_inseridos = 0

try:
    for linha in df.itertuples(index=False, name=None):
        cursor.execute(sql, linha)
        registros_inseridos += 1

    conexao.commit()
    print(f"{registros_inseridos} registros inseridos com sucesso.")

except Exception as e:
    conexao.rollback()
    print("Erro ao inserir os dados:")
    print(e)

finally:
    cursor.close()
    conexao.close()
    
print(f"{len(df)} registros inseridos com sucesso.")