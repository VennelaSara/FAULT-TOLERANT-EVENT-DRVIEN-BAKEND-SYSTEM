import uvicorn
from fastapi import FastAPI
from prometheus_client import start_http_server, Counter

# Metrics
PAYMENTS_PROCESSED = Counter("payments_processed_total", "Total payments processed")

app = FastAPI(title="Payment Service")

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8002)
    uvicorn.run(app, host="0.0.0.0", port=8000)
