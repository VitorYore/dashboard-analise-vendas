#%%
import pandas as pd
from pathlib import Path
# ==========================================================
# ETL - PLANILHA DE VENDAS
# Objetivo: transformar o relatório do Excel em uma base
# de dados limpa para análise.
# ==========================================================


# ==========================================================
# FUNÇÕES
# ==========================================================

def auditoria(df, etapa):
    """
    Exibe informações gerais do DataFrame durante o ETL.
    """

    print("\n" + "=" * 50)
    print(etapa)
    print("=" * 50)

    print(f"Linhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}")

    print("\nTipos das colunas:")
    df.info()

    print("\nValores nulos por coluna:")
    print(df.isnull().sum())

    print("\nLinhas duplicadas:")
    print(df.duplicated().sum())


# ==========================================================
# EXTRAÇÃO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
arquivo = BASE_DIR / "data" / "raw" / "PLANILHA VITOR.xlsx"

df = pd.read_excel(
    arquivo,
    sheet_name="VENDAS",
    header=None
)

# Auditoria inicial
auditoria(df, "ANTES DO ETL")


# ==========================================================
# TRANSFORMAÇÃO DOS DADOS
# ==========================================================

# Mantém apenas as colunas identificadas como úteis
df = df.iloc[:, :8]

# Renomeia as colunas
df.columns = [
    "Pedido",
    "Data",
    "Total_custo",
    "Valor_liquido",
    "Forma_pagamento",
    "Cliente",
    "Lucro",
    "Percentual_lucro"
]

# Remove linhas completamente vazias
df = df.dropna(how="all")

# Lista dos meses presentes no relatório
meses = [
    "JANEIRO",
    "FEVEREIRO",
    "MARÇO",
    "ABRIL",
    "MAIO",
    "JUNHO",
    "JULHO",
    "AGOSTO",
    "SETEMBRO",
    "OUTUBRO",
    "NOVEMBRO",
    "DEZEMBRO"
]

# Remove as linhas que representam apenas a divisão mensal
df = df[~df["Valor_liquido"].isin(meses)]

# Remove registros sem número de pedido
df = df[df["Pedido"].notna()]

# Reinicia o índice
df = df.reset_index(drop=True)

# Auditoria após a limpeza
auditoria(df, "DEPOIS DO ETL")

# ==========================================================

# ==========================================================
# VISUALIZAÇÃO
# ==========================================================

df

# ==========================================================
# EXPORTAÇÃO
# ==========================================================
saida = BASE_DIR / "data" / "processed" / "vendas_limpo.csv"

df.to_csv(
    saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo salvo com sucesso em:\n{saida}")

