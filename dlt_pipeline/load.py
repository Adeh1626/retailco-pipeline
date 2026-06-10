import dlt
import json
from sqlalchemy import create_engine, text
from datetime import datetime

# ── Settings ───────────────────────────────────────────────────
LAKE_CONN      = "postgresql://postgres:Ardey@172.30.96.1:5432/lake"
WAREHOUSE_CONN = "postgresql://postgres:Ardey@172.30.96.1:5432/warehouse"

ENTITIES = [
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

# ── Load one entity from lake to warehouse ──────────────────────
def get_rows_from_lake(entity_name):
    """Read raw data from the lake database"""
    engine = create_engine(LAKE_CONN)
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT id, raw_data, loaded_at
            FROM raw.{entity_name}
        """))
        rows = [dict(r._mapping) for r in result]
    engine.dispose()
    return rows


def flatten_rows(rows):
    """
    The lake stores data as JSON blobs.
    This unpacks each blob into proper flat columns.
    """
    flat = []
    for row in rows:
        data = row["raw_data"]
        if isinstance(data, str):
            data = json.loads(data)
        data["_loaded_at"] = str(row["loaded_at"])
        flat.append(data)
    return flat


def load_entity(entity_name):
    """Move one entity from lake to warehouse using dlt"""
    print(f"\nLoading {entity_name}...")

    rows = get_rows_from_lake(entity_name)
    if not rows:
        print(f"  No data found for {entity_name}")
        return

    flat_rows = flatten_rows(rows)
    print(f"  Found {len(flat_rows)} rows in lake")

    # Set up dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name=f"retailco_{entity_name}",
        destination=dlt.destinations.postgres(WAREHOUSE_CONN),
        dataset_name="raw",
    )

    # Run the load
    load_info = pipeline.run(
        flat_rows,
        table_name=entity_name,
        write_disposition="merge",   # upsert — no duplicates
        primary_key="id",
    )

    print(f"  Loaded successfully: {load_info.loads_ids}")


def run_all():
    print(f"\ndlt pipeline started at {datetime.now()}")
    for entity in ENTITIES:
        load_entity(entity)
    print(f"\ndlt pipeline complete at {datetime.now()}")


if __name__ == "__main__":
    run_all()``