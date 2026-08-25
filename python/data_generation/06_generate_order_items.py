import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)
OUT = Path(__file__).parents[1] / "data" / "raw"

orders = pd.read_csv(OUT/"orders.csv", parse_dates=["order_date"])
products = pd.read_csv(OUT/"products.csv")

# Basket size distribution.
basket_sizes = rng.choice([1,2,3,4,5,6], len(orders), p=[.42,.28,.15,.08,.04,.03])
n_items = int(basket_sizes.sum())

order_repeated = np.repeat(orders.index.to_numpy(), basket_sizes)
product_idx = rng.integers(0, len(products), n_items)

p = products.iloc[product_idx].reset_index(drop=True)
o = orders.iloc[order_repeated].reset_index(drop=True)

# Actual price differs from standard price due to promotions and negotiated pricing.
price_factor = rng.normal(1.0, .035, n_items)
unit_price = np.clip(p.standard_price.to_numpy() * price_factor, 50, None)

# Channel/category-dependent discount behavior.
discount = rng.choice([0,.05,.10,.15,.20,.25,.30,.40,.50], n_items,
                       p=[.31,.18,.17,.12,.09,.06,.04,.02,.01])

df = pd.DataFrame({
    "order_item_id":[f"OI{i:08d}" for i in range(1,n_items+1)],
    "order_id":o.order_id.to_numpy(),
    "product_id":p.product_id.to_numpy(),
    "quantity":rng.choice([1,2,3,4,5,6,8,10], n_items,
                          p=[.40,.25,.15,.08,.05,.035,.02,.015]),
    "unit_price":unit_price.round(2),
    "discount_pct":discount,
    "unit_cost":p.unit_cost.to_numpy()
})

# Deliberate economics: some transactions become low/negative margin after discounts.
high_discount = df.discount_pct >= .30
df.loc[high_discount, "unit_price"] *= rng.uniform(.90, .98, high_discount.sum())
df["unit_price"] = df["unit_price"].round(2)

# Quality issues
bad_qty_idx = rng.choice(len(df), 42, replace=False)
df.loc[bad_qty_idx, "quantity"] = rng.choice([-3,-2,-1,0], len(bad_qty_idx))

bad_discount_idx = rng.choice(len(df), 18, replace=False)
df.loc[bad_discount_idx, "discount_pct"] = rng.choice([-0.05,1.10,1.50], len(bad_discount_idx))

bad_product_idx = rng.choice(len(df), 31, replace=False)
df.loc[bad_product_idx, "product_id"] = "P99999"

# A small number of duplicate-like lines.
dup_rows = df.iloc[rng.choice(len(df), 220, replace=False)].copy()
dup_rows["order_item_id"] = [f"DUP{i:06d}" for i in range(len(dup_rows))]
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_csv(OUT/"order_items.csv", index=False)
print(f"Created {len(df):,} order items")
