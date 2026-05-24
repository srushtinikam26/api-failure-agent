import pandas as pd
from utils import generate_log

# Initialize with 20 logs
log_queue = [generate_log() for _ in range(20)]

WINDOW_SIZE = 20

def load_recent_logs(n=WINDOW_SIZE):
    global log_queue
    # Add a new log and keep only the last 20
    log_queue.append(generate_log())
    if len(log_queue) > WINDOW_SIZE:
        log_queue = log_queue[-WINDOW_SIZE:]
    return pd.DataFrame(log_queue)

def detect_anomalies(df):
    if df.empty:
        return None
    
    error_rate = (df['status_code'] >= 400).mean()
    p95_latency = df['latency_ms'].quantile(0.95)
    
    anomalies = []
    
    # Rule 1: High error rate (>30%)
    if error_rate > 0.3:
        anomalies.append(f"🔴 High error rate: {error_rate*100:.1f}% of requests failing")
    
    # Rule 2: Latency spike (p95 > 1000ms)
    if p95_latency > 1000:
        anomalies.append(f"🐌 Latency spike: p95 latency = {p95_latency:.0f}ms (normal <500ms)")
    
    # Rule 3: Recurring 500 errors on same endpoint
    error_endpoints = df[df['status_code'] >= 500]['endpoint'].value_counts()
    for ep, count in error_endpoints.items():
        if count >= 2:
            anomalies.append(f"⚠️ Recurring 500 errors on {ep} ({count} times in last {WINDOW_SIZE} requests)")
    
    return anomalies if anomalies else None

def get_sample_logs_for_llm(df):
    return df.tail(5).to_dict(orient='records')
