import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)
OUT = Path(__file__).parents[1] / "data" / "raw"

regions = pd.read_csv(OUT/"regions.csv")
months = pd.date_range("2024-01-01","2026-06-01",freq="MS")

rows=[]
for month in months:
    for _, r in regions.iterrows():
        base = rng.uniform(350_000, 2_000_000)
        season = 1.0 + (0.25 if month.month in [10,11,12] else 0)
        sales_target = base * season
        profit_target = sales_target * rng.uniform(.11,.20)
        rows.append([month, r.region_id, round(sales_target,2), round(profit_target,2)])

df = pd.DataFrame(rows, columns=["target_month","region_id","sales_target","profit_target"])
df.to_csv(OUT/"targets.csv", index=False, date_format="%Y-%m-%d")
print(f"Created {len(df):,} target rows")
