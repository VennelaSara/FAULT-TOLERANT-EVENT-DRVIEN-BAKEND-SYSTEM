import os

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "shipping_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "shipping_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "shipping_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "shipping_postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
PAYMENT_TOPIC = os.getenv("PAYMENT_TOPIC", "payment-events")
SHIPPING_TOPIC = os.getenv("SHIPPING_TOPIC", "shipping-events")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Prometheus
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", 8003))

# App Environment
ENV = os.getenv("ENV", "development")
