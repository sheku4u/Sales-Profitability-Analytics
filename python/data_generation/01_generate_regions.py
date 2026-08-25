import pandas as pd
from pathlib import Path

OUT = Path(__file__).parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

regions = [
    ("R01","North"),("R02","South"),("R03","East"),("R04","West"),
    ("R05","Central"),("R06","North-East"),("R07","NCR"),
    ("R08","Metro"),("R09","Tier-2"),("R10","Tier-3")
]
df = pd.DataFrame(regions, columns=["region_id","region_name"])
df["state_count"] = [5,5,4,4,3,4,2,8,12,10]
df.to_csv(OUT/"regions.csv", index=False)
print(f"Created {len(df):,} regions")
