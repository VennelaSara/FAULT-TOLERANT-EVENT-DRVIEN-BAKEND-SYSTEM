import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from .models import Order
from .schemas import OrderCreate
from .kafka_producer import produce_order_event
import redis
from prometheus_client import start_http_server, Counter

# Prometheus metrics
ORDERS_CREATED = Counter('orders_created_total', 'Total number of orders created')

# Redis for idempotency
r = redis.Redis(host="redis", port=6379, db=0)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders/")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Idempotency check
    idempotency_key = f"order:{order.user_id}:{order.item}"
    if r.get(idempotency_key):
        raise HTTPException(status_code=409, detail="Duplicate order detected")

    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Set idempotency
    r.set(idempotency_key, 1, ex=60*60)  # 1 hour

    # Produce event
    await produce_order_event({
        "order_id": db_order.id,
        "user_id": db_order.user_id,
        "item": db_order.item,
        "quantity": db_order.quantity
    })

    # Increment metric
    ORDERS_CREATED.inc()

    return db_order

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8001)
    uvicorn.run(app, host="0.0.0.0", port=8000)
