#%%
# ==========================================
# TRATAMENTO DOS DADOS 
# Objetivo: 
# Receber o CSV gerado pelo ETL e Prepará-lo para análise
# ==========================================

import pandas as pd
from pathlib import Path

# ==========================================
# CAMINHOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

arquivo = BASE_DIR / "data" / "processed" / "vendas_limpo.csv"

saida = BASE_DIR / "data" / "processed" / "vendas_tratadas.csv"

# ==========================================
# EXTRAÇÃO  
# ==========================================

df = pd.read_csv(
    arquivo, 
    encoding="utf-8-sig"
)  

# =========================================
# AUDITORIA INICIAL
# =========================================

print("=" * 50)
print ("Antes do tratamento")
print("=" * 50)

df.info()

print("\nPrimeiras linhas:")
print(df.head())

# Olhando a planilha gerada, foi indentificado que a cada fim do mês, existem comentários não relevantes.
# Este trecho abaixo fica responsável por verificar as palavras e valores desnecessários
print(df[pd.to_numeric(df["Pedido"], errors="coerce").isna()])

# =======================================
# REMOÇÃO DOS RESUMOS MENSAIS
# =======================================

linhas_antes = len(df) 

df["Pedido"] = df["Pedido"].astype(str)

df = df[
    df["Pedido"].str.match(r"^\d+", na=False)
]

df = df.reset_index(drop=True)

linhas_depois = len(df)

print(f"Linhas removidas: {linhas_antes - linhas_depois}")

# =====================================
# CONVERSÃO DOS TIPOS
# =====================================

print("\nTipos antes da conversão:")
print(df.dtypes)

# Converter a coluna Data para datetime

df["Data"] = pd.to_datetime(
    df["Data"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)

df["Data"] = df["Data"].dt.normalize()

print("\nTipos após a conversão")
print(df.dtypes)

# =====================================
# PADRONIZAÇÃO DOS TEXTOS
# =====================================

df["Cliente"] = (
    df["Cliente"]
    .str.strip()
    .str.upper()
)

df["Forma_pagamento"] = (
    df["Forma_pagamento"]
    .str.strip()
    .str.upper()
)

# ============================================
# STATUS DA VENDA 
# ============================================

df["Status"] = "Concluído"

df.loc[
    df["Forma_pagamento"].str.contains("CANCELADO", case=False, na=False),
    "Status"
] = "Cancelado" 

df.loc[
    df["Forma_pagamento"].str.contains("DEVOLU", case=False, na=False),
    "Status"
] = "Devolução"

print("=" * 50)
print("STATUS DAS VENDAS")
print("=" * 50)
print(df["Status"].value_counts())

# ==========================================
# AUDITORIA DOS VALORES NULOS
# ==========================================

print("\n" + "=" * 50)
print("VALORES NULOS")
print("=" * 50)

print(df.isnull().sum())

print("\n" + "=" * 50)
print("NULOS POR STATUS")
print("=" * 50)
#print(df["Data"].head(30)) #verifica como as datas estavam sendo interpretadas
#print(df["Data"].tail(30)) #verifica como as datas estavam sendo interpretadas
print(
    df.isnull()
      .groupby(df["Status"])
      .sum()
)

    #   print(df[df["Data"].isna()])
    #   print(df[df["Lucro"].isna()])
    #   print(df[df["Percentual_lucro"].isna()])

print("\n" + "=" * 50)
print("REGISTROS COM ALGUM VALOR NULO")
print("=" * 50)

print(df[df.isnull().any(axis=1)])

# ==========================================
# CASOS ESPECIAIS
# Pedidos com lucro igual a zero.
# Necessário verificar se são cancelamentos,
# devoluções ou erros de preenchimento.
# ==========================================

print(
    df.loc[df["Lucro"] == 0,
           ["Pedido", "Forma_pagamento", "Status", "Lucro", "Percentual_lucro"]]
)

# ==========================================================
# VALIDAÇÃO DE PEDIDOS REPETIDOS
# ==========================================================

# O número do pedido não é uma chave única no sistema.
# Um mesmo número pode existir para clientes diferentes.
# Portanto esta etapa é apenas informativa.

pedidos_repetidos = df["Pedido"].value_counts()
pedidos_repetidos = pedidos_repetidos[pedidos_repetidos > 1]

print("=" * 50)
print("PEDIDOS REPETIDOS")
print("=" * 50)
print(f"Quantidade de números repetidos: {len(pedidos_repetidos)}")
# Para visualizar os pedidos repetidos:
# print(pedidos_repetidos)

# =====================================
# EXPORTAÇÃO
# =====================================

df.to_csv(
    saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo salvo em:\n{saida}")
# %%
