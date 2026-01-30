import json
from aiokafka import AIOKafkaProducer
from .config import KAFKA_BOOTSTRAP_SERVERS, PAYMENT_TOPIC
import asyncio

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
    return producer

async def produce_payment_event(payment: dict):
    producer = await get_producer()
    await producer.send_and_wait(PAYMENT_TOPIC, json.dumps(payment).encode("utf-8"))

async def close_producer():
    global producer
    if producer:
        await producer.stop()
