import pandas as pd
from pathlib import Path

OUT = Path(__file__).parents[1] / "data" / "raw"
channels = [
    ("CH01","Online","Digital"),
    ("CH02","Retail Store","Offline"),
    ("CH03","Marketplace","Digital"),
    ("CH04","Corporate Sales","B2B"),
]
df = pd.DataFrame(channels, columns=["channel_id","channel_name","channel_type"])
df.to_csv(OUT/"sales_channels.csv", index=False)
print(f"Created {len(df):,} sales channels")
