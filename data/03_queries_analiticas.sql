WITH base AS (
    SELECT
        cnpj,
        MIN(ano * 10 + trimestre) AS periodo_inicial,
        MAX(ano * 10 + trimestre) AS periodo_final
    FROM despesas_consolidadas
    GROUP BY cnpj
),
valores AS (
    SELECT
        d.cnpj,
        MAX(CASE WHEN (ano * 10 + trimestre) = b.periodo_inicial THEN valor_despesas END) AS inicial,
        MAX(CASE WHEN (ano * 10 + trimestre) = b.periodo_final THEN valor_despesas END) AS final
    FROM despesas_consolidadas d
    JOIN base b ON d.cnpj = b.cnpj
    GROUP BY d.cnpj
)
SELECT
    o.razao_social,
    ((final - inicial) / inicial) * 100 AS crescimento_percentual
FROM valores v
JOIN operadoras o ON o.cnpj = v.cnpj
WHERE inicial > 0
ORDER BY crescimento_percentual DESC
LIMIT 5;

SELECT
    o.uf,
    SUM(d.valor_despesas) AS total_despesas,
    AVG(d.valor_despesas) AS media_por_operadora
FROM despesas_consolidadas d
JOIN operadoras o ON o.cnpj = d.cnpj
GROUP BY o.uf
ORDER BY total_despesas DESC
LIMIT 5;

WITH media_geral AS (
    SELECT AVG(valor_despesas) AS media
    FROM despesas_consolidadas
),
comparacao AS (
    SELECT
        cnpj,
        COUNT(*) AS qtd_acima_media
    FROM despesas_consolidadas d
    CROSS JOIN media_geral m
    WHERE d.valor_despesas > m.media
    GROUP BY cnpj
)
SELECT COUNT(*) AS total_operadoras
FROM comparacao
WHERE qtd_acima_media >= 2;
