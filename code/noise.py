from os import path
import pandas as pd

df = pd.read_csv(
    path.join(path.dirname(__file__), "../data/measure/Corrente di buio t candela.tsv"),
    sep='\t',
    engine="python",
)

print(df.I.mean())
print(df.I.std())
print(
    (df.I.max() - df.I.min()) / 2
)
