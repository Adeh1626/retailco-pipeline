import os
import time
import requests
import psycopg2
import json
from datetime import datetime

# ── Settings ───────────────────────────────────────────────────
API_BASE  = "http://localhost:8000"
API_KEY   = "test-api-key-123"
DB_CONN   = "postgresql://postgres:Ardey@172.30.96.1:5432/lake"

HEADERS   = {"X-API-Key": API_KEY}

ENTITIES  = [
    "stores",
    "employees",
    "payment_methods",
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "inventory_movements",
]

def api_get(url, params=None, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url, headers=HEADERS, params=params, timeout=30
            )

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 60))
                print(f"Rate limited. Waiting {wait} seconds...")
                time.sleep(wait)

            elif response.status_code >= 500:
                wait = (2 ** attempt) * 5
                print(f"Server error. Retrying in {wait}s...")
                time.sleep(wait)

            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.Timeout:
            wait = (2 ** attempt) * 5
            print(f"Timeout. Retrying in {wait}s...")
            time.sleep(wait)

    raise Exception(f"Failed after {max_retries} attempts")


def fetch_all_pages(entity, updated_after=None):
    url      = f"{API_BASE}/{entity}/"
    cursor   = None
    all_rows = []

    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor
        if updated_after:
            params["updated_after"] = updated_after

        result = api_get(url, params=params)
        rows   = result.get("data", [])
        meta   = result.get("meta", {})
        all_rows.extend(rows)

        print(f"  Got {len(rows)} rows (total: {len(all_rows)})")

        if not meta.get("has_more", False):
            break
        cursor = meta.get("cursor")

    return all_rows


def setup_schema(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.watermarks (
                entity_name     TEXT PRIMARY KEY,
                last_updated_at TIMESTAMPTZ
            );
        """)
        for entity in ENTITIES:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS raw.{entity} (
                    id        TEXT PRIMARY KEY,
                    raw_data  JSONB NOT NULL,
                    loaded_at TIMESTAMPTZ DEFAULT now()
                );
            """)
    conn.commit()
    print("Database schema ready.")


def get_watermark(conn, entity):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT last_updated_at FROM raw.watermarks WHERE entity_name = %s",
            (entity,)
        )
        row = cur.fetchone()
        return row[0].isoformat() if row else None


def set_watermark(conn, entity, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO raw.watermarks (entity_name, last_updated_at)
            VALUES (%s, %s)
            ON CONFLICT (entity_name)
            DO UPDATE SET last_updated_at = EXCLUDED.last_updated_at
        """, (entity, timestamp))
    conn.commit()


def upsert_rows(conn, entity, rows):
    if not rows:
        return
    with conn.cursor() as cur:
        for row in rows:
            cur.execute(f"""
                INSERT INTO raw.{entity} (id, raw_data, loaded_at)
                VALUES (%s, %s::jsonb, now())
                ON CONFLICT (id)
                DO UPDATE SET
                    raw_data  = EXCLUDED.raw_data,
                    loaded_at = EXCLUDED.loaded_at
            """, (row.get("id"), json.dumps(row)))
    conn.commit()
    print(f"  Saved {len(rows)} rows to raw.{entity}")


def run_extraction():
    print(f"\nExtraction started at {datetime.now()}")
    conn = psycopg2.connect(DB_CONN)
    setup_schema(conn)

    for entity in ENTITIES:
        print(f"\nExtracting: {entity}")
        watermark = get_watermark(conn, entity)

        if watermark:
            print(f"  Incremental — rows updated after {watermark}")
        else:
            print(f"  First run — downloading everything")

        rows = fetch_all_pages(entity, updated_after=watermark)

        if rows:
            upsert_rows(conn, entity, rows)
            timestamps = [r.get("updated_at") for r in rows if r.get("updated_at")]
            if timestamps:
                latest = max(timestamps)
                set_watermark(conn, entity, latest)
                print(f"  Watermark saved: {latest}")

    conn.close()
    print(f"\nExtraction complete at {datetime.now()}")


if __name__ == "__main__":
    run_extraction()