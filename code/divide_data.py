from os import path
import re

import numpy as np
import pandas as pd

RAD_TO_METER = 0.0789 / (2 * np.pi)

here = path.dirname(__file__)
data_path = path.join(here, "../data")

df = pd.read_csv(
    path.join(data_path, "./Capstone Data.csv"),
    sep=';',
    engine='python',
    decimal=r',',
    quotechar=r'"',
)

symbol_map = {
    r"Time (s)": 't',
    r"Relative Intensity": 'I',
    r"Angle (rad)": 'a',
    r"Position (m)": 'y',
}

sets = dict()
for col in df:
    for data_name in symbol_map.keys():
        if col.startswith(data_name):
            set_name = col.replace(data_name, "").strip()

            match_set_name = re.search(
                r"(?P<author>[\w]+) (?P<slit>[\d\.]+) (?P<sensor>[\d\.]+)( (?P<scale>[\w]+))?", set_name)
            if match_set_name:
                file_name = '_'.join([
                    match_set_name.group("slit"),
                    match_set_name.group("sensor"),
                    "1" if match_set_name.group("scale") else "100",
                    match_set_name.group("author")[0:2],
                ])
            else:
                file_name = set_name

            set_df = sets.setdefault(file_name, pd.DataFrame())

            data_symbol = symbol_map[data_name]
            set_df[data_symbol] = df[col]

            break
        else:
            continue
    else:
        raise Exception(f'No match found for {col}')

for key, value in sets.items():
    file = path.join(data_path, key + '.tsv')
    value.dropna(inplace=True)
    value['y'] = value['a'] * RAD_TO_METER
    value.to_csv(file, sep='\t', index=False)
