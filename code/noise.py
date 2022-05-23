from os import path
import pandas as pd

df = pd.read_csv(
    path.join(path.dirname(__file__), "../data/raw/Laser rumore costante sole.tsv"),
    sep='\t',
    engine="python",
)

print(df.I.std() / df.I.mean())
print(
    (df.I.max() - df.I.min()) / (df.I.max() + df.I.min())
)
