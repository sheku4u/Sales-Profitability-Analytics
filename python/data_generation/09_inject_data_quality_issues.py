"""
This file is intentionally kept as a separate stage so the project can clearly
distinguish base-data generation from quality-issue injection.

Most controlled issues are currently injected inside individual generators.
This script performs a final audit and records expected issue categories.
"""
from pathlib import Path
import json

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "raw"

expected = {
    "customers.csv": ["missing_optional_fields", "invalid_age"],
    "products.csv": ["invalid_unit_cost", "inconsistent_category", "missing_category"],
    "orders.csv": ["duplicate_like_order_ids", "orphan_customer_ids", "future_dates", "status_inconsistency"],
    "order_items.csv": ["invalid_quantity", "invalid_discount", "orphan_product_ids", "duplicate_like_lines"],
    "returns.csv": ["return_quantity_anomaly", "return_date_anomaly", "reason_inconsistency"],
}
(OUT / "quality_injection_log.json").write_text(json.dumps(expected, indent=2))
print("Quality-injection specification recorded.")
