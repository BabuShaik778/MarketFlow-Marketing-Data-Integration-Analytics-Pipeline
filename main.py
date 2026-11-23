from database import connect_db, create_tables

def main():
    create_tables()
    tables = [
        "dim_customer", "dim_campaign", "fact_ad_spend_daily", "fact_lead",
        "fact_order", "dim_product", "fact_order_item", "rejected_rows", "pipeline_runs"
    ]
    with connect_db() as conn:
        print("\\nMARKETING DATABASE SUMMARY")
        print("-" * 40)
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table:24} {count}")
        print("\\nFIRST FIVE CUSTOMERS")
        for row in conn.execute(
            "SELECT customer_id, full_name, email FROM dim_customer ORDER BY customer_id LIMIT 5"
        ):
            print(dict(row))

if __name__ == "__main__":
    main()
