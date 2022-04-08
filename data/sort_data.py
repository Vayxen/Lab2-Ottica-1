from os import path
import re

import numpy as np
import pandas as pd

here = path.dirname(__file__)

df = pd.read_csv(
    path.join(here, './_capstone.tsv'),
    sep=r'\s*\t\s*',
    engine='python',
    decimal=r',',
    quotechar=r'"',
)

sets = dict()
for col in df:
    match = re.search(r'(?P<col>[\w\s]+\(.+\)) (?P<set>.+$)', col)
    if match:
        set_df = sets.setdefault(match.group('set'), pd.DataFrame())
        set_df[match.group('col')] = df[col]
    else:
        raise Exception(f'No match found for {col}')

for key, value in sets.items():
    file = path.join(here, key + '.tsv')
    value.dropna().to_csv(file, sep='\t', index=False)
