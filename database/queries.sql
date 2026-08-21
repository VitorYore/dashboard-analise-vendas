-- ==================================
-- 1. FATURAMENTO TOTAL 
-- ==================================
SELECT 
    SUM(valor_liquido) AS faturamento_total
FROM vendas; 

-- =================================
-- 2. LUCRO TOTAL 
-- =================================
SELECT
    SUM(lucro) AS lucro_total
FROM vendas;

-- =================================
-- 3. MARGEM TOTAL 
-- =================================
SELECT
    ROUND(
        SUM(lucro) / NULLIF(SUM(valor_liquido),0)*100, 2
    ) AS margem_percentual
FROM vendas;

-- ================================
-- 4. TOTAL DE PEDIDOS
-- ================================
SELECT 
    COUNT(DISTINCT pedido) AS total_pedidos
FROM vendas; 

-- ================================
-- 5. CLIENTES ÚNICOS
-- ================================
SELECT
    COUNT(DISTINCT cliente) AS clientes_unicos 
FROM vendas; 

-- ================================
-- 6. FATURAMENTO E LUCRO POR MÊS
-- ================================
SELECT
    mes,
    nome_mes,
    SUM(valor_liquido) AS faturamento,
    SUM(lucro) AS lucro
FROM vendas
WHERE data IS NOT NULL 
GROUP BY mes, nome_mes
ORDER BY mes;

-- ====================================
-- 7. TOP 10 CLIENTE POR FATURAMENTO
-- ====================================
SELECT
    cliente,
    SUM(valor_liquido) AS faturamento
FROM vendas
GROUP BY cliente
ORDER BY faturamento DESC
LIMIT 10;

-- =================================
-- 8. MARGEM POR FORMA DE PAGAMENTO
-- =================================
SELECT 
    pagamento,
    SUM(valor_liquido) AS faturamento,
    SUM(lucro) AS lucro,
    ROUND(
        SUM(lucro) / NULLIF(SUM(valor_liquido),0) *100, 2 
    ) AS margem_percentual
FROM vendas
GROUP BY pagamento 
ORDER BY margem_percentual DESC 

-- =========================================
-- 9. PARTICIPAÇÃO DOS CLIENTES NO FATURAMENTO
-- =========================================

SELECT
    cliente,
    SUM(valor_liquido) AS faturamento_cliente,
    ROUND(
        SUM(valor_liquido) /
        SUM(SUM(valor_liquido)) OVER () * 100,
        2
    ) AS participacao_percentual
FROM vendas
GROUP BY cliente
ORDER BY faturamento_cliente DESC;

-- ====================================
-- 10. RANKING DE CLIENTES POR FATURAMENTO 
-- ====================================
 SELECT
    cliente, 
    SUM(valor_liquido) AS faturamento_cliente,
    RANK () OVER(
        ORDER BY SUM(valor_liquido) DESC
    ) AS posicao_ranking 
FROM vendas
GROUP BY cliente
ORDER BY posicao_ranking

-- ======================================
-- 11. CRESCIMENTO MENSAL DO FATURAMENTO
-- ======================================
WITH faturamento_mensal AS (
    SELECT
        mes,
        nome_mes,
        SUM(valor_liquido) AS faturamento
    FROM vendas
    WHERE mes IS NOT NULL
    GROUP BY mes, nome_mes
)

SELECT
    mes,
    nome_mes,
    faturamento,

    LAG(faturamento) OVER (
        ORDER BY mes
    ) AS faturamento_mes_anterior,

    ROUND(
        (
            faturamento -
            LAG(faturamento) OVER (ORDER BY mes)
        )
        /
        NULLIF(
            LAG(faturamento) OVER (ORDER BY mes),
            0
        )
        * 100,
        2
    ) AS crescimento_percentual

FROM faturamento_mensal
ORDER BY mes;

-- =========================================
-- 12. MELHOR MÊS EM FATURAMENTO
-- =========================================
SELECT
    mes,
    nome_mes,
    SUM(valor_liquido) AS faturamento
FROM vendas
WHERE mes IS NOT NULL
GROUP BY mes, nome_mes
ORDER BY faturamento DESC
LIMIT 1;

-- =========================================
-- 14. VISÃO CONSOLIDADA POR CLIENTE
-- =========================================
WITH resumo_clientes AS (
    SELECT
        cliente,
        COUNT(DISTINCT pedido) AS total_pedidos,
        SUM(valor_liquido) AS faturamento,
        SUM(lucro) AS lucro
    FROM vendas
    GROUP BY cliente
)

SELECT
    cliente,
    total_pedidos,
    ROUND(faturamento, 2) AS faturamento,
    ROUND(lucro, 2) AS lucro,

    ROUND(
        lucro / NULLIF(faturamento, 0) * 100,
        2
    ) AS margem_percentual,

    ROUND(
        faturamento / NULLIF(total_pedidos, 0),
        2
    ) AS ticket_medio,

    RANK() OVER (
        ORDER BY faturamento DESC
    ) AS ranking_faturamento,

    RANK() OVER (
        ORDER BY lucro DESC
    ) AS ranking_lucro

FROM resumo_clientes
ORDER BY faturamento DESC;