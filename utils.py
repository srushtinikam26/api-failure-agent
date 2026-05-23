# utils.py
import json
import time
from datetime import datetime

LOG_FILE = "api_logs.json"

def inject_error_log(endpoint="/payment", status=500, latency_ms=1500):
    """Inject a fake error log into api_logs.json for demo purposes"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": "POST",
        "endpoint": endpoint,
        "status_code": status,
        "latency_ms": latency_ms,
        "client_ip": "192.168.1.99"
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"✅ Injected {status} error on {endpoint}")