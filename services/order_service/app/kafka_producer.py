import json
from aiokafka import AIOKafkaProducer
from .config import KAFKA_BOOTSTRAP_SERVERS, ORDER_TOPIC
import asyncio

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
    return producer

async def produce_order_event(order: dict):
    producer = await get_producer()
    await producer.send_and_wait(ORDER_TOPIC, json.dumps(order).encode("utf-8"))

async def close_producer():
    global producer
    if producer:
        await producer.stop()
