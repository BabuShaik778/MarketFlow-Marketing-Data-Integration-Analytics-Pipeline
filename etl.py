import csv
import json
import requests
from datetime import date
from decimal import Decimal
from pathlib import Path

from database import connect_db, create_tables

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
API_URL = "http://127.0.0.1:5000/ads"

def clean_text(value):
    return str(value or "").strip()

def normalize_status(value):
    return clean_text(value).lower()

def normalize_phone(value):
    digits = "".join(ch for ch in clean_text(value) if ch.isdigit())
    if len(digits) < 10:
        raise ValueError("Phone must contain at least 10 digits")
    return digits[-10:]

def parse_date(value):
    return date.fromisoformat(clean_text(value)[:10]).isoformat()

def read_csv(filename):
    with (DATA / filename).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def fetch_all_ads():
    result = []
    page = 1
    while True:
        response = requests.get(API_URL, params={"page": page, "page_size": 2}, timeout=10)
        response.raise_for_status()
        payload = response.json()
        result.extend(payload["data"])
        if not payload["has_next"]:
            break
        page += 1
    return result

def reject(conn, source, key, reason, record):
    conn.execute(
        "INSERT INTO rejected_rows(source_name, source_key, reason, raw_record) VALUES (?, ?, ?, ?)",
        (source, key, reason, json.dumps(record))
    )

def run_pipeline():
    create_tables()
    loaded = rejected = 0

    with connect_db() as conn:
        run_id = conn.execute(
            "INSERT INTO pipeline_runs(status) VALUES ('running')"
        ).lastrowid

        try:
            # Load customers first because leads and orders refer to them.
            for row in read_csv("customers.csv"):
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO dim_customer
                        (customer_id, full_name, email, phone, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        clean_text(row["customer_id"]),
                        clean_text(row["full_name"]),
                        clean_text(row["email"]).lower(),
                        normalize_phone(row["phone"]),
                        parse_date(row["created_at"])
                    ))
                    loaded += 1
                except Exception as error:
                    reject(conn, "customers.csv", row.get("customer_id"), str(error), row)
                    rejected += 1

            # Fetch every page from the advertising API.
            for row in fetch_all_ads():
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO dim_campaign(campaign_id, campaign_name, platform)
                        VALUES (?, ?, ?)
                    """, (row["campaign_id"], clean_text(row["campaign_name"]), clean_text(row["platform"])))
                    rupees = float(Decimal(str(row["spend_paise"])) / Decimal("100"))
                    conn.execute("""
                        INSERT OR REPLACE INTO fact_ad_spend_daily
                        (campaign_id, spend_date, spend_inr, impressions, clicks)
                        VALUES (?, ?, ?, ?, ?)
                    """, (row["campaign_id"], parse_date(row["spend_date"]), rupees,
                          int(row["impressions"]), int(row["clicks"])))
                    loaded += 1
                except Exception as error:
                    reject(conn, "ads_api", row.get("campaign_id"), str(error), row)
                    rejected += 1

            campaign_rows = conn.execute(
                "SELECT campaign_id, campaign_name FROM dim_campaign"
            ).fetchall()
            campaign_map = {r["campaign_name"].lower(): r["campaign_id"] for r in campaign_rows}

            for row in read_csv("leads.csv"):
                try:
                    campaign_id = campaign_map.get(clean_text(row["campaign_name"]).lower())
                    conn.execute("""
                        INSERT OR REPLACE INTO fact_lead
                        (lead_id, customer_id, campaign_id, source, created_at, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (row["lead_id"], row["customer_id"], campaign_id, clean_text(row["source"]),
                          parse_date(row["created_at"]), normalize_status(row["status"])))
                    loaded += 1
                except Exception as error:
                    reject(conn, "leads.csv", row.get("lead_id"), str(error), row)
                    rejected += 1

            for row in read_csv("orders.csv"):
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO fact_order(order_id, customer_id, order_date, status)
                        VALUES (?, ?, ?, ?)
                    """, (row["order_id"], row["customer_id"], parse_date(row["order_date"]),
                          normalize_status(row["status"])))
                    loaded += 1
                except Exception as error:
                    reject(conn, "orders.csv", row.get("order_id"), str(error), row)
                    rejected += 1

            for row in read_csv("order_items.csv"):
                try:
                    product_name = clean_text(row["product_name"])
                    product_id = "P" + str(abs(hash(product_name)) % 1000000).zfill(6)
                    conn.execute(
                        "INSERT OR IGNORE INTO dim_product(product_id, product_name) VALUES (?, ?)",
                        (product_id, product_name)
                    )
                    conn.execute("""
                        INSERT OR REPLACE INTO fact_order_item
                        (order_item_id, order_id, product_id, quantity, unit_price_inr, gst_rate)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (row["order_item_id"], row["order_id"], product_id, int(row["quantity"]),
                          float(row["unit_price_inr"]), float(row["gst_rate"])))
                    loaded += 1
                except Exception as error:
                    reject(conn, "order_items.csv", row.get("order_item_id"), str(error), row)
                    rejected += 1

            store_path = DATA / "store.json"
            if store_path.exists():
                json.loads(store_path.read_text(encoding="utf-8"))

            conn.execute("""
                UPDATE pipeline_runs
                SET finished_at=CURRENT_TIMESTAMP, status='success',
                    rows_loaded=?, rows_rejected=?, message='Pipeline completed'
                WHERE run_id=?
            """, (loaded, rejected, run_id))
            print(f"Pipeline complete. Processed {loaded}; rejected {rejected}.")
        except Exception as error:
            conn.execute("""
                UPDATE pipeline_runs SET finished_at=CURRENT_TIMESTAMP,
                status='failed', message=? WHERE run_id=?
            """, (str(error), run_id))
            raise

if __name__ == "__main__":
    run_pipeline()
