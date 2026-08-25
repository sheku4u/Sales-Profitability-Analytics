import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)
N = 120_000
OUT = Path(__file__).parents[1] / "data" / "raw"

customers = pd.read_csv(OUT/"customers.csv")
regions = pd.read_csv(OUT/"regions.csv")
channels = pd.read_csv(OUT/"sales_channels.csv")

# Create realistic monthly seasonality.
dates = pd.date_range("2024-01-01", "2026-06-30", freq="D")
weights = np.ones(len(dates))
weights += np.where(dates.month.isin([10,11,12]), .55, 0)
weights += np.where(dates.day >= 25, .12, 0)
weights /= weights.sum()
order_dates = rng.choice(dates.values, N, p=weights)

# Customer repeat behavior: weighted sampling creates concentration.
customer_weights = rng.lognormal(mean=0, sigma=1.0, size=len(customers))
customer_weights /= customer_weights.sum()
customer_idx = rng.choice(len(customers), N, p=customer_weights)

customer_ids = customers.iloc[customer_idx]["customer_id"].to_numpy()
region_ids = customers.iloc[customer_idx]["region_id"].to_numpy()

channel = rng.choice(channels.channel_id, N, p=[.45,.22,.23,.10])
payment = rng.choice(["UPI","Credit Card","Debit Card","Net Banking","Cash","Wallet","COD"],
                     N, p=[.27,.18,.13,.11,.04,.08,.19])
status = rng.choice(["Completed","Cancelled","Pending","Returned","Partially Returned"],
                    N, p=[.86,.035,.015,.045,.045])

df = pd.DataFrame({
    "order_id":[f"ORD{i:07d}" for i in range(1,N+1)],
    "order_date":pd.to_datetime(order_dates),
    "customer_id":customer_ids,
    "region_id":region_ids,
    "channel_id":channel,
    "payment_method":payment,
    "order_status":status
})

# Quality issues
dup_idx = rng.choice(N, 300, replace=False)
df.loc[dup_idx, "order_id"] = df.loc[dup_idx-1, "order_id"].to_numpy()

df.loc[rng.choice(N, 94, replace=False), "customer_id"] = "C99999"
future_idx = rng.choice(N, 7, replace=False)
df.loc[future_idx, "order_date"] = pd.Timestamp("2027-01-15")
df.loc[rng.choice(N, 13, replace=False), "order_status"] = "completed "

df.to_csv(OUT/"orders.csv", index=False, date_format="%Y-%m-%d")
print(f"Created {len(df):,} orders")
