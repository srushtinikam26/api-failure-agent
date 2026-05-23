import time
import json
import random
from datetime import datetime

LOG_FILE = "api_logs.json"

def generate_log():
    endpoints = ["/login", "/payment", "/user/profile", "/data"]
    method = random.choice(["GET", "POST"])
    endpoint = random.choice(endpoints)
    
    # Simulate more errors for /payment and /login
    if endpoint == "/payment":
        status = random.choices([200, 400, 500], weights=[0.6, 0.2, 0.2])[0]
    elif endpoint == "/login":
        status = random.choices([200, 401, 500], weights=[0.7, 0.2, 0.1])[0]
    else:
        status = random.choices([200, 400, 500], weights=[0.8, 0.1, 0.1])[0]
    
    latency = random.uniform(0.05, 0.5) if status == 200 else random.uniform(0.5, 2.0)
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": method,
        "endpoint": endpoint,
        "status_code": status,
        "latency_ms": round(latency * 1000, 2),
        "client_ip": f"192.168.1.{random.randint(1,255)}"
    }
    return log_entry

def main():
    print("✅ Log generator started. Writing to api_logs.json")
    print("Press Ctrl+C to stop when needed.")
    while True:
        entry = generate_log()
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        time.sleep(1)  # 1 log per second

if __name__ == "__main__":
    main()