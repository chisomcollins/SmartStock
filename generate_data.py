import pandas as pd
import numpy as np
from datetime import datetime
import os

np.random.seed(42)

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

start_date = datetime(2025, 7, 1)
end_date = datetime(2025, 12, 31)
dates = pd.date_range(start_date, end_date)

products = [
    "Rice 50kg",
    "Indomie Carton",
    "Coca-Cola Crate",
    "Peak Milk Tin",
    "Golden Penny Flour",
    "Sugar 1kg",
    "Palm Oil 5L",
    "Dettol Soap",
    "Milo Refill",
    "Bread Loaf"
]

data = []

for product in products:
    base_demand = np.random.randint(20, 60)
    growth_rate = np.random.uniform(0.0005, 0.002)

    for i, date in enumerate(dates):
        trend = base_demand * (1 + growth_rate * i)
        weekend_boost = 1.2 if date.weekday() >= 4 else 1
        noise = np.random.normal(0, 5)

        sales = max(0, int(trend * weekend_boost + noise))
        data.append([date, product, sales])

df = pd.DataFrame(data, columns=["date", "product", "sales"])
df.to_csv("data/retail_sales_data.csv", index=False)

print("Dataset created successfully.")
