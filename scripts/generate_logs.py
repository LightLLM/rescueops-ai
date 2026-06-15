import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[1] / "data" / "synthetic_logs.jsonl"
OUTPUT.parent.mkdir(exist_ok=True)

services = ["frontend", "checkout-api", "payment-service", "inventory-service", "database"]
endpoints = ["/", "/cart", "/checkout", "/pay", "/inventory"]

start = datetime.now(timezone.utc) - timedelta(hours=2)
events = []
random.seed(42)

for i in range(240):
    ts = start + timedelta(seconds=i * 30)

    service = random.choice(services)
    endpoint = random.choice(endpoints)
    status_code = random.choice([200, 200, 200, 200, 201, 204])
    latency = random.randint(80, 450)
    level = "INFO"
    message = "request completed successfully"
    deployment_version = "v2.3.0"

    if i == 105:
        service = "checkout-api"
        endpoint = "/deploy"
        status_code = 200
        latency = 300
        level = "INFO"
        message = "deployment completed for checkout-api"
        deployment_version = "v2.3.1"

    if 115 <= i <= 180:
        if random.random() < 0.65:
            service = random.choice(["checkout-api", "payment-service", "database"])
            endpoint = random.choice(["/checkout", "/pay"])
            status_code = random.choice([500, 502, 503])
            latency = random.randint(1500, 4800)
            level = "ERROR"
            deployment_version = "v2.3.1"

            if service == "database":
                message = "database connection pool exhausted"
            elif service == "payment-service":
                message = "payment authorization timeout"
            else:
                message = "checkout request failed after dependency timeout"

    event = {
        "time": ts.isoformat(),
        "timestamp": ts.isoformat(),
        "service": service,
        "endpoint": endpoint,
        "level": level,
        "status_code": status_code,
        "latency_ms": latency,
        "message": message,
        "deployment_version": deployment_version,
        "trace_id": f"trace-{random.randint(10000, 99999)}",
        "host": f"prod-{random.randint(1, 4)}",
        "environment": "production",
        "source_app": "rescueops-demo"
    }

    events.append(event)

with OUTPUT.open("w", encoding="utf-8") as f:
    for event in events:
        f.write(json.dumps(event) + "\n")

print(f"Generated {len(events)} events at {OUTPUT}")
