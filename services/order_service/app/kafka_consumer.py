import json
import asyncio
from aiokafka import AIOKafkaConsumer
from .config import KAFKA_BOOTSTRAP_SERVERS, ORDER_TOPIC
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Order

consumer = None

async def get_consumer():
    global consumer
    if consumer is None:
        consumer = AIOKafkaConsumer(
            ORDER_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="order-service-group",
            auto_offset_reset="earliest",
            enable_auto_commit=False
        )
        await consumer.start()
    return consumer

async def process_order_event(event: dict, db: Session):
    """
    Example: you can mark order as processed after some background processing
    """
    order_id = event.get("order_id")
    order = db.query(Order).filter(Order.id == order_id).first()
    if order and not order.processed:
        # Your business logic here
        order.processed = True
        order.status = "processed"
        db.commit()
        print(f"Processed order {order_id}")

async def consume_orders():
    consumer = await get_consumer()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode("utf-8"))
            db = SessionLocal()
            try:
                await process_order_event(event, db)
                await consumer.commit()
            except Exception as e:
                print(f"Failed to process order event: {e}")
            finally:
                db.close()
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_orders())
