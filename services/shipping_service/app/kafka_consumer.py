import json
import asyncio
from aiokafka import AIOKafkaConsumer
from .config import KAFKA_BOOTSTRAP_SERVERS, PAYMENT_TOPIC
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Shipping
import redis
from .kafka_producer import produce_shipping_event

r = redis.Redis(host="redis", port=6379, db=0)
consumer = None

async def get_consumer():
    global consumer
    if consumer is None:
        consumer = AIOKafkaConsumer(
            PAYMENT_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="shipping-service-group",
            auto_offset_reset="earliest",
            enable_auto_commit=False
        )
        await consumer.start()
    return consumer

async def process_shipping_event(event: dict, db: Session):
    order_id = event.get("order_id")
    user_id = event.get("user_id")
    # Simulate address and item
    address = "123 Main Street"
    item = event.get("item", "unknown")
    quantity = event.get("quantity", 1)

    # Idempotency check
    key = f"shipping:{order_id}"
    if r.get(key):
        print(f"Shipping for order {order_id} already processed")
        return

    shipping = Shipping(order_id=order_id, user_id=user_id, item=item, quantity=quantity, address=address, status="shipped", processed=True)
    db.add(shipping)
    db.commit()
    db.refresh(shipping)

    # Set Redis idempotency
    r.set(key, 1, ex=60*60)

    # Optionally produce shipping delivered event
    # await produce_shipping_event({
    #     "shipping_id": shipping.id,
    #     "order_id": shipping.order_id,
    #     "status": shipping.status
    # }, topic="shipping-events")

    print(f"Shipping processed for order {order_id}")

async def consume_payments():
    consumer = await get_consumer()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode("utf-8"))
            db = SessionLocal()
            try:
                await process_shipping_event(event, db)
                await consumer.commit()
            except Exception as e:
                print(f"Failed to process shipping event: {e}")
            finally:
                db.close()
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_payments())
