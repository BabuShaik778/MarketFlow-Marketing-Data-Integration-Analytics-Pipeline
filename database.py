import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "marketing.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    statements = [
        """CREATE TABLE IF NOT EXISTS dim_campaign (
            campaign_id TEXT PRIMARY KEY,
            campaign_name TEXT NOT NULL,
            platform TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS fact_ad_spend_daily (
            campaign_id TEXT NOT NULL,
            spend_date TEXT NOT NULL,
            spend_inr REAL NOT NULL CHECK(spend_inr >= 0),
            impressions INTEGER NOT NULL CHECK(impressions >= 0),
            clicks INTEGER NOT NULL CHECK(clicks >= 0),
            PRIMARY KEY(campaign_id, spend_date),
            FOREIGN KEY(campaign_id) REFERENCES dim_campaign(campaign_id)
        )""",
        """CREATE TABLE IF NOT EXISTS fact_lead (
            lead_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            campaign_id TEXT,
            source TEXT,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY(campaign_id) REFERENCES dim_campaign(campaign_id)
        )""",
        """CREATE TABLE IF NOT EXISTS fact_order (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id)
        )""",
        """CREATE TABLE IF NOT EXISTS dim_product (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL UNIQUE
        )""",
        """CREATE TABLE IF NOT EXISTS fact_order_item (
            order_item_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price_inr REAL NOT NULL CHECK(unit_price_inr >= 0),
            gst_rate REAL NOT NULL CHECK(gst_rate >= 0 AND gst_rate <= 1),
            FOREIGN KEY(order_id) REFERENCES fact_order(order_id),
            FOREIGN KEY(product_id) REFERENCES dim_product(product_id)
        )""",
        """CREATE TABLE IF NOT EXISTS rejected_rows (
            reject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name TEXT NOT NULL,
            source_key TEXT,
            reason TEXT NOT NULL,
            raw_record TEXT NOT NULL,
            rejected_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS pipeline_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT DEFAULT CURRENT_TIMESTAMP,
            finished_at TEXT,
            status TEXT NOT NULL,
            rows_loaded INTEGER DEFAULT 0,
            rows_rejected INTEGER DEFAULT 0,
            message TEXT
        )"""
    ]
    with connect_db() as conn:
        for sql in statements:
            conn.execute(sql)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lead_customer_date ON fact_lead(customer_id, created_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_order_customer_date ON fact_order(customer_id, order_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_spend_date ON fact_ad_spend_daily(spend_date)")

if __name__ == "__main__":
    create_tables()
    print(f"Database ready: {DB_PATH}")
