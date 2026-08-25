import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)
N = 8_000
OUT = Path(__file__).parents[1] / "data" / "raw"

orders = pd.read_csv(OUT/"orders.csv", parse_dates=["order_date"])
items = pd.read_csv(OUT/"order_items.csv")
items = items[items.order_id.isin(orders.order_id)].copy()

idx = rng.choice(len(items), N, replace=False)
chosen = items.iloc[idx].copy()
order_lookup = chosen[["order_id"]].merge(orders[["order_id","order_date"]].drop_duplicates("order_id"), on="order_id", how="left")

reasons = rng.choice(
    ["Damaged","Wrong Product","Customer Changed Mind","Late Delivery","Quality Issue","Incorrect Size"],
    N, p=[.17,.13,.20,.08,.25,.17]
)

return_dates = order_lookup.order_date.to_numpy() + pd.to_timedelta(rng.integers(2,45,N), unit="D").to_numpy()
qty = np.maximum(1, np.minimum(chosen.quantity.to_numpy(), rng.choice([1,1,1,2,3], N)))

df = pd.DataFrame({
    "return_id":[f"RET{i:07d}" for i in range(1,N+1)],
    "order_id":chosen.order_id.to_numpy(),
    "product_id":chosen.product_id.to_numpy(),
    "return_date":pd.to_datetime(return_dates),
    "return_quantity":qty,
    "return_reason":reasons,
    "return_status":rng.choice(["Approved","Processed","Rejected","Pending"], N,
                                p=[.48,.35,.08,.09])
})

# Quality issues
idx1 = rng.choice(N, 18, replace=False)
df.loc[idx1, "return_quantity"] += 20
idx2 = rng.choice(N, 12, replace=False)
df.loc[idx2, "return_date"] = pd.Timestamp("2023-01-01")
idx3 = rng.choice(N, 20, replace=False)
df.loc[idx3, "return_reason"] = "quality issue"

df.to_csv(OUT/"returns.csv", index=False, date_format="%Y-%m-%d")
print(f"Created {len(df):,} returns")
