# coding: utf-8

import pandas as pd
import numpy as np

series_imdb = pd.read_csv("https://raw.githubusercontent.com/nazareno/imdb-series/master/data/series_from_imdb.csv")

got_e_bb = series_imdb.query(
    "series_name == 'Breaking Bad' | series_name == 'Game of Thrones'"
).reset_index(
    drop=True
).filter(
    items=["series_name", "episode", "series_ep", "season", "season_ep", "user_rating", "user_votes"]        
)

got_e_bb.to_csv("../docs/series_imdb.csv", index=False)
