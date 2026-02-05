import pandas as pd
import numpy as np
import zipfile  

def validar_cnpj(cnpj):
    """Validação técnica de CNPJ para o requisito 2.1"""
    cnpj = str(cnpj).replace('.', '').replace('/', '').replace('-', '').strip()
    if not cnpj.isdigit() or len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    
    for n in [12, 13]:
        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2] if n == 12 else [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(n))
        digito = 0 if soma % 11 < 2 else 11 - (soma % 11)
        if int(cnpj[n]) != digito:
            return False
    return True

def executar_desafio_2():
    print("--- INICIANDO DESAFIO 2 ---")
    
    NOME_CSV = "despesas_agregadas.csv"
    NOME_ZIP = "Teste_Rafael_Euclydes.zip"
    
    df_despesas = pd.read_csv("consolidado_despesas.csv", sep=";")
    df_despesas['REG_ANS'] = df_despesas['REG_ANS'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

    URL_CAD = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    print("Lendo cadastro da ANS...")
    df_cadastral = pd.read_csv(URL_CAD, sep=";", encoding="latin1", low_memory=False)
    df_cadastral.columns = df_cadastral.columns.str.upper().str.strip()

    col_reg_cad = 'REGISTRO_OPERADORA' if 'REGISTRO_OPERADORA' in df_cadastral.columns else 'REGISTRO_ANS'
    df_cadastral[col_reg_cad] = df_cadastral[col_reg_cad].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

    df_final = pd.merge(
        df_despesas, 
        df_cadastral[[col_reg_cad, 'CNPJ', 'RAZAO_SOCIAL', 'MODALIDADE', 'UF']], 
        left_on='REG_ANS', 
        right_on=col_reg_cad, 
        how='left'
    )

    df_final['CNPJ_VALIDO'] = df_final['CNPJ'].apply(lambda x: validar_cnpj(x) if pd.notna(x) else False)
    
    def converter_valor(v):
        try: return float(str(v).replace('.', '').replace(',', '.'))
        except: return 0.0
    df_final['VL_SALDO_FINAL'] = df_final['VL_SALDO_FINAL'].apply(converter_valor)
    
    df_valido = df_final[(df_final['RAZAO_SOCIAL'].notna()) & (df_final['VL_SALDO_FINAL'] > 0)].copy()

    print("Agrupando dados e gerando colunas finais...")
    agregado = df_valido.groupby(['RAZAO_SOCIAL', 'UF', 'CNPJ', col_reg_cad, 'MODALIDADE']).agg(
        Total_Despesas=('VL_SALDO_FINAL', 'sum'),
        Media_Trimestral=('VL_SALDO_FINAL', 'mean'),
        Desvio_Padrao=('VL_SALDO_FINAL', 'std')
    ).reset_index()

    agregado = agregado.rename(columns={col_reg_cad: 'RegistroANS', 'RAZAO_SOCIAL': 'RazaoSocial'})

    agregado = agregado.sort_values(by='Total_Despesas', ascending=False)

    agregado.to_csv(NOME_CSV, index=False, sep=";", encoding="utf-8-sig")
    
    with zipfile.ZipFile(NOME_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(NOME_CSV)
    
    print("--- SUCESSO! ---")
    print(f"Arquivo CSV: {NOME_CSV}")
    print(f"Arquivo ZIP: {NOME_ZIP}")
    print(f"O arquivo contém {len(agregado)} operadoras.")

if __name__ == "__main__":
    executar_desafio_2()
