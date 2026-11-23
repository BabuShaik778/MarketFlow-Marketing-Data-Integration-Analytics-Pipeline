import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(21)
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_csv(filename, columns, rows):
    with (DATA_DIR / filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

customers = []
for n in range(1, 41):
    customers.append({
        "customer_id": f"C{n:04}",
        "full_name": f"Customer {n}",
        "email": f"customer{n}@example.com",
        "phone": f"+91 98765 {n:05}",
        "created_at": (date(2026, 1, 1) + timedelta(days=n)).isoformat()
    })
save_csv("customers.csv", ["customer_id", "full_name", "email", "phone", "created_at"], customers)

campaigns = ["Summer Sale", "Brand Search", "Social Launch"]
leads = []
for n in range(1, 71):
    leads.append({
        "lead_id": f"L{n:04}",
        "customer_id": f"C{((n - 1) % 40) + 1:04}",
        "campaign_name": random.choice(campaigns),
        "source": random.choice(["Google", "Meta", "Email"]),
        "created_at": (date(2026, 2, 1) + timedelta(days=n % 25)).isoformat(),
        "status": random.choice(["new", "qualified", "converted", " NEW "])
    })
save_csv("leads.csv", ["lead_id", "customer_id", "campaign_name", "source", "created_at", "status"], leads)

orders, items = [], []
products = ["Running Shoes", "Backpack", "Water Bottle", "Sports T-shirt"]
for n in range(1, 31):
    oid = f"O{n:04}"
    orders.append({
        "order_id": oid,
        "customer_id": f"C{n:04}",
        "order_date": (date(2026, 3, 1) + timedelta(days=n)).isoformat(),
        "status": random.choice(["paid", "shipped", "cancelled", "returned"])
    })
    items.append({
        "order_item_id": f"OI{n:04}",
        "order_id": oid,
        "product_name": random.choice(products),
        "quantity": random.randint(1, 3),
        "unit_price_inr": random.choice([499, 799, 1299, 1999]),
        "gst_rate": 0.18
    })
save_csv("orders.csv", ["order_id", "customer_id", "order_date", "status"], orders)
save_csv("order_items.csv", ["order_item_id", "order_id", "product_name", "quantity", "unit_price_inr", "gst_rate"], items)

store = {"stores": [
    {"store_id": "S001", "store_name": "Bengaluru Online", "city": "Bengaluru"},
    {"store_id": "S002", "store_name": "Hyderabad Online", "city": "Hyderabad"}
]}
(DATA_DIR / "store.json").write_text(json.dumps(store, indent=2), encoding="utf-8")
print("Sample CSV and JSON files created in data/.")
