from fastapi import FastAPI, Header, HTTPException
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

app = FastAPI(title="RetailCo Mock ERP API")
fake = Faker()

API_KEY = "test-api-key-123"

def make_stores():
    cities = ["Lagos", "Abuja", "Port Harcourt", "Kano"]
    return [
        {
            "id": str(i+1),
            "name": f"RetailCo {c}",
            "city": c,
            "region": c,
            "updated_at": "2024-01-01T00:00:00Z",
            "is_deleted": False
        }
        for i, c in enumerate(cities)
    ]

def make_employees(n=40):
    roles = ["cashier", "manager", "supervisor"]
    stores = ["1", "2", "3", "4"]
    rows = []
    for i in range(n):
        rows.append({
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "role": random.choice(roles),
            "store_id": random.choice(stores),
            "updated_at": fake.date_time_between("-1y").isoformat() + "Z",
            "is_deleted": False
        })
    return rows

def make_payment_methods():
    methods = ["cash", "card", "bank_transfer", "mobile_money"]
    return [
        {
            "id": str(i+1),
            "method_name": m,
            "updated_at": "2024-01-01T00:00:00Z",
            "is_deleted": False
        }
        for i, m in enumerate(methods)
    ]

def make_customers(n=200):
    segments = ["premium", "regular", "occasional"]
    rows = []
    for i in range(n):
        rows.append({
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "email": fake.email(),
            "segment": random.choice(segments),
            "address": fake.address().replace("\n", ", "),
            "city": random.choice(["Lagos", "Abuja", "Port Harcourt", "Kano"]),
            "is_deleted": random.random() < 0.05,
            "effective_from": "2023-01-01T00:00:00Z",
            "updated_at": fake.date_time_between("-1y").isoformat() + "Z",
        })
    return rows

def make_products(n=100):
    categories = ["Electronics", "Food", "Clothing", "Home", "Beauty"]
    rows = []
    for i in range(n):
        rows.append({
            "id": str(uuid.uuid4()),
            "name": fake.catch_phrase(),
            "category": random.choice(categories),
            "price": round(random.uniform(500, 50000), 2),
            "is_deleted": random.random() < 0.03,
            "effective_from": "2023-01-01T00:00:00Z",
            "updated_at": fake.date_time_between("-1y").isoformat() + "Z",
        })
    return rows

def make_orders(customers, stores, employees, n=500):
    statuses = ["pending", "paid", "shipped", "delivered", "cancelled"]
    rows = []
    for i in range(n):
        created = fake.date_time_between("-1y")
        rows.append({
            "id": str(uuid.uuid4()),
            "customer_id": random.choice(customers)["id"],
            "store_id": random.choice(stores)["id"],
            "employee_id": random.choice(employees)["id"],
            "status": random.choice(statuses),
            "order_date": created.isoformat() + "Z",
            "updated_at": (created + timedelta(days=random.randint(0,5))).isoformat() + "Z",
            "is_deleted": False
        })
    return rows

def make_order_items(orders, products, n=1200):
    rows = []
    for i in range(n):
        product = random.choice(products)
        qty = random.randint(1, 10)
        price = product["price"]
        discount = round(random.uniform(0, price * 0.2), 2)
        rows.append({
            "id": str(uuid.uuid4()),
            "order_id": random.choice(orders)["id"],
            "product_id": product["id"],
            "quantity": qty,
            "unit_price": price,
            "discount_amount": discount,
            "updated_at": fake.date_time_between("-1y").isoformat() + "Z",
        })
    return rows

def make_payments(orders, payment_methods, n=500):
    rows = []
    for order in orders[:n]:
        amount = round(random.uniform(1000, 100000), 2)
        quirk = random.random()
        if quirk < 0.03:
            amount = 0
        elif quirk < 0.06:
            amount = -abs(amount)
        rows.append({
            "id": str(uuid.uuid4()),
            "order_id": order["id"],
            "payment_method_id": random.choice(payment_methods)["id"],
            "amount_paid": amount,
            "is_refund": amount < 0,
            "updated_at": order["updated_at"],
        })
    return rows

def make_inventory_movements(products, stores, n=2000):
    movement_types = ["purchase", "sale", "adjustment", "return"]
    rows = []
    for i in range(n):
        rows.append({
            "id": str(uuid.uuid4()),
            "product_id": random.choice(products)["id"],
            "store_id": random.choice(stores)["id"],
            "movement_type": random.choice(movement_types),
            "quantity": random.randint(-50, 100),
            "movement_date": fake.date_time_between("-1y").isoformat() + "Z",
            "updated_at": fake.date_time_between("-1y").isoformat() + "Z",
        })
    return rows

# Build all data when server starts
STORES              = make_stores()
EMPLOYEES           = make_employees(40)
PAYMENT_METHODS     = make_payment_methods()
CUSTOMERS           = make_customers(200)
PRODUCTS            = make_products(100)
ORDERS              = make_orders(CUSTOMERS, STORES, EMPLOYEES, 500)
ORDER_ITEMS         = make_order_items(ORDERS, PRODUCTS, 1200)
PAYMENTS            = make_payments(ORDERS, PAYMENT_METHODS, 500)
INVENTORY_MOVEMENTS = make_inventory_movements(PRODUCTS, STORES, 2000)

def check_auth(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

def maybe_fail():
    if random.random() < 0.03:
        raise HTTPException(status_code=500, detail="Simulated server error")

def filter_updated_after(data, updated_after):
    if not updated_after:
        return data
    return [row for row in data if row.get("updated_at", "") >= updated_after]

def paginate(data, cursor, limit):
    start = int(cursor) if cursor else 0
    page  = data[start : start + limit]
    next_cursor = str(start + limit) if (start + limit) < len(data) else None
    return {
        "data": page,
        "meta": {
            "cursor": next_cursor,
            "has_more": next_cursor is not None,
            "total": len(data)
        }
    }

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/stores/")
def get_stores(cursor: str = None, limit: int = 50,
               x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    return paginate(STORES, cursor, limit)

@app.get("/employees/")
def get_employees(cursor: str = None, limit: int = 50,
                  updated_after: str = None,
                  x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(EMPLOYEES, updated_after)
    return paginate(data, cursor, limit)

@app.get("/payment_methods/")
def get_payment_methods(cursor: str = None, limit: int = 50,
                        x_api_key: str = Header(...)):
    check_auth(x_api_key)
    return paginate(PAYMENT_METHODS, cursor, limit)

@app.get("/customers/")
def get_customers(cursor: str = None, limit: int = 50,
                  updated_after: str = None,
                  x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(CUSTOMERS, updated_after)
    return paginate(data, cursor, limit)

@app.get("/customers/{id}")
def get_customer(id: str, x_api_key: str = Header(...)):
    check_auth(x_api_key)
    match = next((c for c in CUSTOMERS if c["id"] == id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Customer not found")
    return match

@app.get("/products/")
def get_products(cursor: str = None, limit: int = 50,
                 updated_after: str = None,
                 x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(PRODUCTS, updated_after)
    return paginate(data, cursor, limit)

@app.get("/products/{id}")
def get_product(id: str, x_api_key: str = Header(...)):
    check_auth(x_api_key)
    match = next((p for p in PRODUCTS if p["id"] == id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Product not found")
    return match

@app.get("/orders/")
def get_orders(cursor: str = None, limit: int = 50,
               updated_after: str = None,
               x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(ORDERS, updated_after)
    return paginate(data, cursor, limit)

@app.get("/orders/{id}")
def get_order(id: str, x_api_key: str = Header(...)):
    check_auth(x_api_key)
    match = next((o for o in ORDERS if o["id"] == id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    return match

@app.get("/order_items/")
def get_order_items(cursor: str = None, limit: int = 50,
                    updated_after: str = None,
                    x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(ORDER_ITEMS, updated_after)
    return paginate(data, cursor, limit)

@app.get("/payments/")
def get_payments(cursor: str = None, limit: int = 50,
                 updated_after: str = None,
                 x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(PAYMENTS, updated_after)
    return paginate(data, cursor, limit)

@app.get("/inventory_movements/")
def get_inventory_movements(cursor: str = None, limit: int = 50,
                             updated_after: str = None,
                             x_api_key: str = Header(...)):
    check_auth(x_api_key)
    maybe_fail()
    data = filter_updated_after(INVENTORY_MOVEMENTS, updated_after)
    return paginate(data, cursor, limit)