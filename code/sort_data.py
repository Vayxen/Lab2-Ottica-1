from os import path
import re

import numpy as np
import pandas as pd

POSITION_SCALE_FACTOR = 0.0789 / 0.15
N_SET = 22
N_COL = 2

here = path.dirname(__file__)
data_path = path.join(here, "../data")

df = pd.read_csv(
    path.join(data_path, "./Capstone Data.tsv"),
    sep='\t',
    engine='python',
    decimal=r',',
)

col_map = {
    r"Time (s)": 't',
    r"Relative Intensity": 'I',
    r"Angle (rad)": 'a',
    r"Position (cm)": 'y',
}

for i in range(0, N_SET * N_COL, N_COL):
    set_df = df.iloc[:, i:i + N_COL].copy()

    filename = ""
    for col in set_df.columns:
        for col_name in col_map:
            if col.startswith(col_name):
                filename = col.replace(col_name, "").strip()
                break
        break

    set_df.columns = [
        col_map[col_name]
        for col in set_df
        for col_name in col_map
        if col.startswith(col_name)
    ]

    set_df.dropna(inplace=True)

    set_df.loc[:, 'y'] *= POSITION_SCALE_FACTOR

    set_df.to_csv(path.join(data_path, "raw", filename + ".tsv"), sep='\t', index=False)

