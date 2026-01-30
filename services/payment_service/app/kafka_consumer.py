import json
import asyncio
from aiokafka import AIOKafkaConsumer
from .config import KAFKA_BOOTSTRAP_SERVERS, ORDER_TOPIC
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Payment
import redis
from .kafka_producer import produce_payment_event

r = redis.Redis(host="redis", port=6379, db=0)
consumer = None

async def get_consumer():
    global consumer
    if consumer is None:
        consumer = AIOKafkaConsumer(
            ORDER_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="payment-service-group",
            auto_offset_reset="earliest",
            enable_auto_commit=False
        )
        await consumer.start()
    return consumer

async def process_payment_event(event: dict, db: Session):
    order_id = event.get("order_id")
    user_id = event.get("user_id")
    # Idempotency check
    key = f"payment:{order_id}"
    if r.get(key):
        print(f"Payment for order {order_id} already processed")
        return

    payment = Payment(order_id=order_id, user_id=user_id, status="completed", processed=True)
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Set Redis idempotency
    r.set(key, 1, ex=60*60)  # 1 hour

    # Produce PaymentProcessed event
    await produce_payment_event({
        "payment_id": payment.id,
        "order_id": payment.order_id,
        "user_id": payment.user_id,
        "status": payment.status
    })
    print(f"Processed payment for order {order_id}")

async def consume_orders():
    consumer = await get_consumer()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode("utf-8"))
            db = SessionLocal()
            try:
                await process_payment_event(event, db)
                await consumer.commit()
            except Exception as e:
                print(f"Failed to process payment event: {e}")
            finally:
                db.close()
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_orders())
