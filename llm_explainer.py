import os
import json

# No real API call — mock for demo
def explain_anomaly(anomalies, recent_logs):
    # Generate a realistic-looking response based on the anomalies
    anomalies_text = " ".join(anomalies)
    if "500" in anomalies_text or "error rate" in anomalies_text:
        return """ROOT_CAUSE: The /payment endpoint is receiving malformed JSON payloads, causing repeated 500 errors.

FIX_SUGGESTIONS:
- Add input validation on the /payment endpoint to reject malformed requests
- Implement a retry mechanism with exponential backoff for transient failures
- Monitor database connection pool as errors spike during high load

IMPACT: Users cannot complete payments, leading to lost revenue and poor user experience."""
    elif "latency" in anomalies_text:
        return """ROOT_CAUSE: Database query on /user/profile is missing an index, causing full table scans under load.

FIX_SUGGESTIONS:
- Add composite index on (user_id, last_login)
- Implement caching for frequently requested profiles
- Reduce payload size by removing unnecessary fields

IMPACT: Slow page loads cause user frustration and increased bounce rate."""
    else:
        return """ROOT_CAUSE: Intermittent network timeouts between API gateway and upstream service.

FIX_SUGGESTIONS:
- Increase timeout threshold from 5s to 10s for critical endpoints
- Add circuit breaker pattern to prevent cascading failures
- Review load balancer health check intervals

IMPACT: Unreliable API responses affect all dependent features."""