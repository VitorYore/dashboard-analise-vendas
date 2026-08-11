import pandas as pd
from pathlib import Path


# ===========================================
# FUNÇÕES
# =========================================== 
def exibir_resumo(titulo, dataframe, coluna_nome, coluna_valor, formato=None):
    print("\n" + "=" * 50)
    print(titulo)
    print("=" * 50)

    for _, linha in dataframe.iterrows():

        valor = linha[coluna_valor]

        if formato == "moeda":
            valor = moeda(valor)

        elif formato == "percentual":
            valor = f"{valor:.2f}%"

        print(f"{linha[coluna_nome]:<30}{valor}")




def exibir_trimestre(df):
    print("\n" + "=" * 50)
    print("RESULTADO DO TRIMESTRE")
    print("=" * 50)

    for indice, linha in df.iterrows():
        print(f"{indice}° Trimestre"
              f"| Faturamento: {moeda(linha["Valor_liquido"])}"
              f"| Lucro: {moeda(linha["Lucro"])}"
              )

def moeda(valor):
    """
    Formata valores monetários para o padrão brasileiro R$
    """
    return f"R$ {valor:,.2f}".replace(",","X").replace(".", ",").replace("X",".")

def exibir_indicadores(titulo, indicadores):
    print("=" * 50)
    print(titulo)
    print("=" * 50)

    for nome, valor in indicadores.items():
        print(f"{nome:.<20} {valor}")

def padronizar_pagamento(texto):
    if pd.isna(texto):
        return "OUTROS"

    texto = texto.upper().strip()

    if "PIX" in texto:
        return "PIX"

    if "DINHEIRO" in texto:
        return "DINHEIRO"

    if "DÉBITO" in texto or "DEBITO" in texto:
        return "DÉBITO"
    
    if"CHEQUE" in texto:
        return "CHEQUE"
    
    if "TRANSFER" in texto:
        return "TRANSFERÊNCIA"

    if "CRÉDITO" in texto or "CREDITO" in texto:
        for parcela in range(2, 7):
            if f"{parcela}X" in texto:
                return f"CRÉDITO {parcela}X"

        return "CRÉDITO"

    if "DEVOLU" in texto:
        return "DEVOLUÇÃO"

    if "CANCEL" in texto:
        return "CANCELADO"

    return "OUTROS"

def exibir_insights():
    print("\n" + "=" * 50)
    print("INSIGHTS DA ANÁLISE")
    print("=" * 50)

    print(f"• Melhor mês em faturamento: {melhor_mes_faturamento['Nome_mes']}")
    print(f"• Melhor mês em lucro: {melhor_mes_lucro['Nome_mes']}")
    print(f"• Melhor trimestre: {melhor_trimestre.name}º trimestre")

    print()

    print(f"• Cliente com maior faturamento: {cliente_faturamento['Cliente']}")
    print(f"• Cliente mais lucrativo: {cliente_lucro['Cliente']}")
    print(f"• Cliente mais recorrente: {cliente_recorrente['Cliente']}")

    print()

    print(f"• Forma de pagamento mais utilizada: {pagamento_utilizado['Pagamento']}")
    print(f"• Forma de pagamento com maior faturamento: {pagamento_faturamento['Pagamento']}")

    print()

    print(f"• Taxa de cancelamento: {taxa_cancelamento:.2f}%")
    print(f"• Total de devoluções: {devolucoes}")

# ==========================================
# CAMINHOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

arquivo = BASE_DIR / "data" / "processed" / "vendas_tratadas.csv"

df = pd.read_csv( 
    arquivo,
      encoding="utf-8-sig",
        parse_dates=["Data"] 
)

# ==================================
# CRIAÇÃO DE KPIs
# ================================== 

indicadores = {
    "Pedidos": len(df),
    "Faturamento": moeda(df["Valor_liquido"].sum()),
    "Lucro": moeda(df["Lucro"].sum()),
    "Ticket Médio": moeda(df["Valor_liquido"].mean()),
    "Margem Média": f"{df['Percentual_lucro'].mean():.2%}"
}

exibir_indicadores("Indicadores Gerais", indicadores)

# ==============================
# EVOLUÇÃO TEMPORAL 
# ==============================

#Trasnformando os meses em números
meses = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez"
}

df["Ano"] = df["Data"].dt.year.astype("Int64")
df["Mês"] = df["Data"].dt.month.astype("Int64")
df["Nome_mes"] = df["Mês"].map(meses)
df["Trimestre"] = df["Data"].dt.quarter.astype("Int64")

vendas_mes = (
    df.groupby(["Mês", "Nome_mes"])["Valor_liquido"]
      .sum()
      .reset_index()
      .sort_values("Mês")
)

lucro_mes = (
    df.groupby(["Mês", "Nome_mes"])["Lucro"]
      .sum()
      .reset_index()
      .sort_values("Mês")
)

trimestre = (
    df.groupby("Trimestre")
      [["Valor_liquido","Lucro"]]
      .sum()
) 

exibir_resumo(
    "FATURAMENTO POR MÊS",
    vendas_mes,
    "Nome_mes",
    "Valor_liquido",
    formato="moeda"
)

exibir_resumo(
    "LUCRO POR MÊS",
    lucro_mes,
    "Nome_mes",
    "Lucro",
    formato="moeda"
)

exibir_trimestre(trimestre)

print(
    df.groupby(["Mês", "Status"])["Valor_liquido"]
      .sum()
      .unstack(fill_value=0)
)

# ==========================================
# CLIENTES 
# ==========================================

clientes_unicos = df["Cliente"].nunique()

print("=" * 50)
print("CLIENTES")
print("=" * 50)
print(f"Clientes únicos: {clientes_unicos}")

clientes_faturamento = (
    df.groupby("Cliente")["Valor_liquido"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

clientes_lucro = (
    df.groupby("Cliente")["Lucro"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

compras_clientes =(
    df.groupby("Cliente")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Quantidade")
)

exibir_resumo(
    "TOP 10 FATURAMENTO POR CLIENTES",
    clientes_faturamento,
    "Cliente",
    "Valor_liquido",
    formato="moeda"
)

exibir_resumo(
    "TOP 10 LUCRO POR CLIENTES",
    clientes_lucro,
    "Cliente",
    "Lucro",
    formato="moeda"
)

exibir_resumo(
    "TOP 10 CLIENTES POR PEDIDOS",
    compras_clientes,
    "Cliente",
    "Quantidade",
)

# =============================================
# FORMAS DE PAGAMENTOS
# =============================================

df["Pagamento"] = df["Forma_pagamento"].apply(padronizar_pagamento)

pagamentos_qtd = (
    df["Pagamento"]
      .value_counts()
      .reset_index()
)

pagamentos_qtd.columns = ["Pagamento", "Quantidade"]

exibir_resumo(
    "QUANTIDADE POR FORMA DE PAGAMENTO",
    pagamentos_qtd,
    "Pagamento",
    "Quantidade"
)

pagamentos_faturamento = (
    df.groupby("Pagamento")["Valor_liquido"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

exibir_resumo(
    "FATURAMENTO POR FORMA DE PAGAMENTO",
    pagamentos_faturamento,
    "Pagamento",
    "Valor_liquido",
    formato="moeda"
)

pagamentos_lucro = (
    df.groupby("Pagamento")["Lucro"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

exibir_resumo(
    "LUCRO POR FORMA DE PAGAMENTO",
    pagamentos_lucro,
    "Pagamento",
    "Lucro",
    formato="moeda"
)

pagamentos_percentual = (
    df["Pagamento"]
      .value_counts(normalize=True)
      .mul(100)
      .round(2)
      .reset_index()
)

pagamentos_percentual.columns = ["Pagamento", "Percentual"]

exibir_resumo(
    "PARTICIPAÇÃO DAS FORMAS DE PAGAMENTO",
    pagamentos_percentual,
    "Pagamento",
    "Percentual",
    formato="percentual"
)

#print(
    #df.loc[df["Pagamento"] == "OUTROS", "Forma_pagamento"]             #=== Caso queira ver o que contém na categoria "OUTROS" SÓ DESCOMENTAR ===#
    #.value_counts()
    #.head(100)
#)

# ==========================================
# CANCELAMENTOS E DEVOLUÇÕES
# ==========================================

status_qtd =(
    df["Status"]
    .value_counts()
    .reset_index()
)

status_qtd.columns = ["Status", "Quantidade"]

exibir_resumo(
    "QUANTIDADE POR STATUS",
    status_qtd,
    "Status",
    "Quantidade"
)

status_faturamento =(
    df.groupby("Status")["Valor_liquido"]
    .sum()
    .reset_index()
)

exibir_resumo(
    "FATURAMENTO POR STATUS",
    status_faturamento,
    "Status",
    "Valor_liquido",
    formato="moeda"
)

status_lucro =(
    df.groupby("Status")["Lucro"]
    .sum()
    .reset_index()
)

exibir_resumo(
    "LUCRO POR STATUS",
    status_lucro,
    "Status",
    "Lucro",
    formato="moeda"
)

status_percentual =(
    df["Status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index()
)

status_percentual.columns = ["Status", "Percentual"]

exibir_resumo(
    "PARTICIPAÇÃO DOS STATUS",
    status_percentual,
    "Status",
    "Percentual",
    formato="percentual"
)

# ========================================
# INSIGHTS DA ANÁLISE
# ========================================

# Melhores meses
melhor_mes_faturamento = vendas_mes.loc[
    vendas_mes["Valor_liquido"].idxmax()
]

melhor_mes_lucro = lucro_mes.loc[
    lucro_mes["Lucro"].idxmax()
]

melhor_trimestre = trimestre.loc[
    trimestre["Valor_liquido"].idxmax()
]

#Clientes
cliente_faturamento = clientes_faturamento.iloc[0]

cliente_lucro = clientes_lucro.iloc[0]

cliente_recorrente = compras_clientes.iloc[0]

# Melhores formas de pagamentos
pagamento_utilizado = pagamentos_qtd.iloc[0]

pagamento_faturamento = pagamentos_faturamento.iloc[0]

# Status

taxa_cancelamento = (
    df["Status"]
    .value_counts(normalize=True)["Cancelado"]
    *100
)

devolucoes = (
    df["Status"] == "Devolução"
).sum()

exibir_insights()

# =======================================
# EXPORTAÇÃO DO CSV
# =======================================

# Garantir tipos numéricos
colunas_numericas = [
    "Total_custo",
    "Valor_liquido",
    "Lucro",
    "Percentual_lucro"
]

df[colunas_numericas] = df[colunas_numericas].astype(float)

#Exportar para CSV no padrão brasileiro
saida = BASE_DIR / "data" / "processed" / "vendas_analise.csv"

df.to_csv(
    saida,
    sep=";",          # separador de colunas
    decimal=",",      # separador decimal
    index=False,
    encoding="utf-8-sig"
)

print(f"Arquivo salvo em: {saida}") 
