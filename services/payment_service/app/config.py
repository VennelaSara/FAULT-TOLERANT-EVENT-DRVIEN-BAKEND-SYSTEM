import os

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "payment_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "payment_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "payment_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "payment_postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
ORDER_TOPIC = os.getenv("ORDER_TOPIC", "order-events")
PAYMENT_TOPIC = os.getenv("PAYMENT_TOPIC", "payment-events")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Prometheus
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", 8002))

# App Environment
ENV = os.getenv("ENV", "development")
