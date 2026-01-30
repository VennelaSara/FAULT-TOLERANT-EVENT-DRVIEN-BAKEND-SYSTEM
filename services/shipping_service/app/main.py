import uvicorn
from fastapi import FastAPI
from prometheus_client import start_http_server, Counter

# Metrics
SHIPPING_PROCESSED = Counter("shipping_processed_total", "Total shipping orders processed")

app = FastAPI(title="Shipping Service")

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8003)
    uvicorn.run(app, host="0.0.0.0", port=8000)
