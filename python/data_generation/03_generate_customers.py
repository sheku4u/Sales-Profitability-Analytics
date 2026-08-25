import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)
N = 10_000
OUT = Path(__file__).parents[1] / "data" / "raw"

states = {
    "Delhi":"R07","Haryana":"R01","Punjab":"R01","Uttar Pradesh":"R07",
    "Rajasthan":"R01","Maharashtra":"R04","Gujarat":"R04",
    "Karnataka":"R02","Tamil Nadu":"R02","Telangana":"R02",
    "West Bengal":"R03","Bihar":"R03","Odisha":"R03",
    "Madhya Pradesh":"R05","Chhattisgarh":"R05","Assam":"R06",
    "Kerala":"R02","Andhra Pradesh":"R02","Jharkhand":"R03",
    "Uttarakhand":"R01"
}
cities = {
    "Delhi":["Delhi"], "Haryana":["Gurugram","Faridabad"], "Punjab":["Ludhiana","Amritsar"],
    "Uttar Pradesh":["Noida","Lucknow","Kanpur"], "Rajasthan":["Jaipur","Jodhpur"],
    "Maharashtra":["Mumbai","Pune","Nagpur"], "Gujarat":["Ahmedabad","Surat"],
    "Karnataka":["Bengaluru","Mysuru"], "Tamil Nadu":["Chennai","Coimbatore"],
    "Telangana":["Hyderabad"], "West Bengal":["Kolkata"], "Bihar":["Patna"],
    "Odisha":["Bhubaneswar"], "Madhya Pradesh":["Indore","Bhopal"],
    "Chhattisgarh":["Raipur"], "Assam":["Guwahati"], "Kerala":["Kochi"],
    "Andhra Pradesh":["Vijayawada","Visakhapatnam"], "Jharkhand":["Ranchi"],
    "Uttarakhand":["Dehradun"]
}
state_names = list(states)
state_probs = np.array([.10,.07,.04,.05,.04,.10,.06,.09,.06,.05,.05,.04,.03,.05,.02,.02,.04,.03,.02,.02])
state_probs /= state_probs.sum()

state = rng.choice(state_names, N, p=state_probs)
city = [rng.choice(cities[s]) for s in state]
region = [states[s] for s in state]

segment = rng.choice(["Consumer","Corporate","Small Business","Enterprise"], N,
                      p=[.58,.16,.20,.06])
gender = rng.choice(["Male","Female","Other"], N, p=[.49,.49,.02])
age = np.clip(rng.normal(35, 10, N).round().astype(int), 18, 80)
signup = pd.to_datetime(rng.integers(
    pd.Timestamp("2022-01-01").value//10**9,
    pd.Timestamp("2026-01-01").value//10**9, N
), unit="s")
acq = rng.choice(["Organic","Paid Search","Social","Referral","Email","Partner"], N,
                 p=[.28,.18,.16,.14,.10,.14])

df = pd.DataFrame({
    "customer_id":[f"C{i:05d}" for i in range(1,N+1)],
    "customer_name":[f"Customer {i:05d}" for i in range(1,N+1)],
    "gender":gender, "age":age, "city":city, "state":state,
    "region_id":region, "customer_segment":segment,
    "signup_date":signup, "acquisition_channel":acq
})

# Controlled optional-field quality issues
df.loc[rng.random(N)<0.025, "state"] = pd.NA
df.loc[rng.random(N)<0.015, "gender"] = pd.NA
df.loc[rng.random(N)<0.012, "acquisition_channel"] = pd.NA
df.loc[rng.choice(N, 12, replace=False), "age"] = [8, 95, 121, 4, 99, 150, 12, 83, 200, 17, 81, 250]

df.to_csv(OUT/"customers.csv", index=False, date_format="%Y-%m-%d")
print(f"Created {len(df):,} customers")
