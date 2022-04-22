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

column_map = {
    r"Time (s)": 't',
    r"Light Intensity (% of scale max)": 'I',
    r"Angle (rad)": 'a',
    r"Position (m)": 'y',
}

sets = dict()
for col in df:
    match_raw = re.search(r'(?P<col>[\w\s]+\(.+\)) (?P<set>.+$)', col)
    if match_raw:
        match_file_name = re.search(
            r"(?P<author>[\w]+) (?P<slit>[\d\.]+) (?P<sensor>[\d\.]+)( (?P<scale>[\w]+))?", match_raw.group('set'))
        if match_file_name:
            file_name = '_'.join([
                match_file_name.group("slit"),
                match_file_name.group("sensor"),
                "1" if match_file_name.group("scale") else "100",
                match_file_name.group("author")[0:2],
            ])
        else:
            file_name = match_raw.group('set')

        set_df = sets.setdefault(file_name, pd.DataFrame())

        col_name = column_map[match_raw.group('col')]
        set_df[col_name] = df[col]
    else:
        raise Exception(f'No match found for {col}')

for key, value in sets.items():
    file = path.join(data_path, key + '.tsv')
    value.dropna(inplace=True)
    value['y'] = value['a'] * RAD_TO_METER
    value.to_csv(file, sep='\t', index=False)
