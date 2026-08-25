from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent
scripts = [
    "01_generate_regions.py",
    "02_generate_channels.py",
    "03_generate_customers.py",
    "04_generate_products.py",
    "05_generate_orders.py",
    "06_generate_order_items.py",
    "07_generate_returns.py",
    "08_generate_targets.py",
    "09_inject_data_quality_issues.py",
    "10_validate_generated_data.py",
]

for script in scripts:
    print("\n" + "="*70)
    print(f"RUNNING {script}")
    print("="*70)
    subprocess.run([sys.executable, str(ROOT/script)], check=True)

print("\nDATA GENERATION PIPELINE COMPLETED.")
