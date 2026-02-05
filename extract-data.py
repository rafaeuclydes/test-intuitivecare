import requests, zipfile, io, re, os
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
CSV_FINAL = "consolidado_despesas.csv"
ZIP_FINAL = "consolidado_despesas.zip" 

def get_links():
    html = requests.get(BASE_URL).text
    soup = BeautifulSoup(html, "html.parser")
    anos = sorted([a.get("href") for a in soup.find_all("a") if re.fullmatch(r"\d{4}/", a.get("href", ""))], reverse=True)
    
    links = []
    for ano in anos:
        html_ano = requests.get(BASE_URL + ano).text
        matches = re.findall(r"([1-4]T\d{4}\.zip)", html_ano)
        for m in sorted(set(matches), reverse=True):
            if len(links) < 3:
                links.append({"url": BASE_URL + ano + m, "t": m[:2], "a": m[2:6]})
    return links

def executar_desafio_1():
    links = get_links()
    lista_dfs = []

    for l in links:
        print(f" Baixando {l['t']}/{l['a']}...")
        r = requests.get(l["url"])
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for name in z.namelist():
                if name.lower().endswith(".csv"):
                    with z.open(name) as f:
                        df = pd.read_csv(f, sep=";", encoding="latin1", low_memory=False)
                        df.columns = df.columns.str.upper().str.strip()
                        
                        if "DESCRICAO" in df.columns:
                            df = df[df["DESCRICAO"].str.contains("EVENTOS|SINISTROS", case=False, na=False)].copy()
                            
                            df["Trimestre"] = l["t"]
                            df["Ano"] = l["a"]
                            
                            colunas = ["REG_ANS", "DESCRICAO", "VL_SALDO_FINAL", "Trimestre", "Ano"]
                            lista_dfs.append(df[[c for c in colunas if c in df.columns]])

    df_total = pd.concat(lista_dfs, ignore_index=True)
    df_total.to_csv(CSV_FINAL, index=False, sep=";", encoding="utf-8-sig")
    print(f" CSV Consolidado gerado com as colunas: {list(df_total.columns)}")

    with zipfile.ZipFile(ZIP_FINAL, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(CSV_FINAL)
    print(f" Arquivo ZIP final gerado: {ZIP_FINAL}")
    # -----------------------------------------------

if __name__ == "__main__":
    executar_desafio_1()
