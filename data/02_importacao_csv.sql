COPY operadoras (
    cnpj,
    razao_social,
    nome_fantasia,
    modalidade,
    uf
)
FROM 'C:/caminho/operadoras.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8'
NULL '';

COPY despesas_consolidadas (
    cnpj,
    ano,
    trimestre,
    valor_despesas
)
FROM 'C:/caminho/consolidado_despesas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8'
NULL '';

COPY despesas_agregadas (
    cnpj,
    uf,
    total_despesas,
    media_despesas
)
FROM 'C:/caminho/despesas_agregadas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8'
NULL '';
