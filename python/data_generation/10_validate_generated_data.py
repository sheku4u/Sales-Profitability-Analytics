import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parents[1]
RAW = ROOT / "data" / "raw"

files = ["customers","products","regions","sales_channels","orders","order_items","returns","targets"]

for name in files:
    path = RAW / f"{name}.csv"
    df = pd.read_csv(path)
    print(f"{name:15} rows={len(df):>8,} cols={len(df.columns):>2}")

customers = pd.read_csv(RAW/"customers.csv")
products = pd.read_csv(RAW/"products.csv")
orders = pd.read_csv(RAW/"orders.csv")
items = pd.read_csv(RAW/"order_items.csv")
returns = pd.read_csv(RAW/"returns.csv")

checks = {
    "customer_id_duplicates": customers.customer_id.duplicated().sum(),
    "product_id_duplicates": products.product_id.duplicated().sum(),
    "order_id_duplicates": orders.order_id.duplicated().sum(),
    "order_items_invalid_qty": (items.quantity <= 0).sum(),
    "order_items_invalid_discount": ((items.discount_pct < 0) | (items.discount_pct > 1)).sum(),
    "orphan_customer_ids": (~orders.customer_id.isin(customers.customer_id)).sum(),
    "orphan_product_ids": (~items.product_id.isin(products.product_id)).sum(),
    "future_orders": (pd.to_datetime(orders.order_date) > pd.Timestamp("2026-06-30")).sum(),
}

print("\nQUALITY SIGNALS")
for k,v in checks.items():
    print(f"{k:30} {v:>8,}")

print("\nValidation completed. These are diagnostic signals, not automatic cleaning decisions.")
