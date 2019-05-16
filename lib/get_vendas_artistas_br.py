# coding: utf-8

import pandas as pd
import numpy as np

vendas_artistas_br = pd.read_csv("https://raw.githubusercontent.com/nazareno/ciencia-dados-descritiva/master/dados/vendas_artistas_br.csv")

vendas_artistas_br = vendas_artistas_br.assign(
    inicio_carreira = lambda row: row["Período"].str.split("-", expand=True, n=1)[0].str.strip().astype("int64"),
    final_carreira = lambda row: row["Período"].str.split("-", expand=True, n=1)[1].str.strip().str.lower(),
    vendas = lambda row: row["Vendas estimadas (milhões)"].str.replace(",", ".").astype("float64"),
    genero = lambda row: row["Gênero(s)"].str.replace(" e ", "/").str.replace(", ", "/").str.split("/", expand=True)[0]
).assign(
    final_carreira = lambda row: np.where(row.final_carreira.str.contains("presente|atualmente"), np.nan, row.final_carreira.astype(int, errors="ignore")),
    vendas = lambda row: np.where(row.Artista == "Tonico & Tinoco", 50, row.vendas)
).drop(
    ["Período", "Vendas estimadas (milhões)", "Gênero(s)"], 
    axis=1
).rename(
    columns = {
        "Artista": "artista"
    }
)

vendas_artistas_br = vendas_artistas_br[["artista", "genero", "inicio_carreira", "final_carreira", "vendas"]]

print(vendas_artistas_br)

vendas_artistas_br.to_csv("../docs/vendas_artistas_br.csv", index=False)
