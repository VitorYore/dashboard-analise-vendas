CREATE TABLE vendas (
    pedido VARCHAR(50),
    data DATE,
    total_custo NUMERIC(12,2),
    valor_liquido NUMERIC(12,2),
    forma_pagamento TEXT,
    cliente TEXT,
    lucro NUMERIC(12,2),
    percentual_lucro NUMERIC(12,6),
    status VARCHAR(30),
    ano INTEGER,
    mes INTEGER,
    nome_mes VARCHAR(10),
    trimestre INTEGER,
    pagamento VARCHAR(50)
);