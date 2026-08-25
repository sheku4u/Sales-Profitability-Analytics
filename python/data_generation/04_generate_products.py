import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)
N = 2_000
OUT = Path(__file__).parents[1] / "data" / "raw"

categories = {
    "Electronics":["Laptops","Mobiles","Audio","Accessories"],
    "Furniture":["Chairs","Desks","Storage","Home Office"],
    "Office Supplies":["Stationery","Paper","Writing","Printing"],
    "Clothing":["Men","Women","Kids","Footwear"],
    "Home Appliances":["Kitchen","Cleaning","Cooling","Small Appliances"],
    "Accessories":["Bags","Watches","Personal Accessories","Travel"]
}
cats = rng.choice(list(categories), N, p=[.22,.16,.18,.18,.14,.12])
subcats = [rng.choice(categories[c]) for c in cats]
brands = rng.choice(["Nova","Vertex","Urbanix","Prime","Apex","HomePro","TechOne","ValueMax"], N)

# Mixture of price bands
price = np.exp(rng.normal(np.log(1200), 1.0, N))
price = np.clip(price, 100, 150_000).round(2)

margin = np.clip(rng.normal(.27, .10, N), .04, .55)
cost = (price * (1-margin)).round(2)
launch = pd.to_datetime(rng.integers(
    pd.Timestamp("2021-01-01").value//10**9,
    pd.Timestamp("2025-12-31").value//10**9, N
), unit="s")

df = pd.DataFrame({
    "product_id":[f"P{i:05d}" for i in range(1,N+1)],
    "product_name":[f"{cats[i]} Product {i+1:04d}" for i in range(N)],
    "category":cats, "subcategory":subcats, "brand":brands,
    "unit_cost":cost, "standard_price":price,
    "supplier_id":[f"S{rng.integers(1,301):04d}" for _ in range(N)],
    "launch_date":launch
})

# Controlled master-data issues
df.loc[rng.choice(N, 20, replace=False), "unit_cost"] = [-20,0,50,100,150,200,250,300,400,500,
                                                          600,700,800,900,1000,1100,1200,1300,1400,1500]
idx = rng.choice(N, 30, replace=False)
df.loc[idx, "category"] = df.loc[idx, "category"].str.lower()
df.loc[rng.choice(N, 15, replace=False), "category"] = pd.NA

df.to_csv(OUT/"products.csv", index=False, date_format="%Y-%m-%d")
print(f"Created {len(df):,} products")
