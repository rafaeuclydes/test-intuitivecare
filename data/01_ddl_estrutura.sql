CREATE TABLE operadoras (
    cnpj            VARCHAR(14) PRIMARY KEY,
    razao_social    TEXT NOT NULL,
    nome_fantasia   TEXT,
    modalidade      TEXT,
    uf              CHAR(2)
);

CREATE INDEX idx_operadoras_uf ON operadoras(uf);

CREATE TABLE despesas_consolidadas (
    id              SERIAL PRIMARY KEY,
    cnpj            VARCHAR(14) NOT NULL,
    ano             INT NOT NULL,
    trimestre       INT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    valor_despesas  DECIMAL(15,2) NOT NULL,

    CONSTRAINT fk_cnpj
        FOREIGN KEY (cnpj)
        REFERENCES operadoras(cnpj)
);

CREATE INDEX idx_despesas_cnpj ON despesas_consolidadas(cnpj);
CREATE INDEX idx_despesas_periodo ON despesas_consolidadas(ano, trimestre);

CREATE TABLE despesas_agregadas (
    id              SERIAL PRIMARY KEY,
    cnpj            VARCHAR(14) NOT NULL,
    uf              CHAR(2),
    total_despesas  DECIMAL(15,2),
    media_despesas  DECIMAL(15,2),

    CONSTRAINT fk_agregado_cnpj
        FOREIGN KEY (cnpj)
        REFERENCES operadoras(cnpj)
);

CREATE INDEX idx_agregado_uf ON despesas_agregadas(uf);
