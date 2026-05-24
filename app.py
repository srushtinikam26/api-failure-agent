import streamlit as st
import pandas as pd
import time
from anomaly_detector import load_recent_logs, detect_anomalies, get_sample_logs_for_llm, log_queue
from llm_explainer import explain_anomaly
from utils import inject_error_log

st.set_page_config(page_title="API Failure Detector", layout="wide")
st.title("🕵️ API Failure Detection & Debugging Agent")
st.markdown("Monitors API logs in real-time and alerts on failures with AI-powered root cause analysis.")

# Auto-refresh every 5 seconds
placeholder = st.empty()

# To avoid repeated API calls on every rerun, we'll store the last explanation in session state
if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = None
if "last_anomalies" not in st.session_state:
    st.session_state.last_anomalies = None

while True:
    df = load_recent_logs()
    if df.empty:
        with placeholder.container():
            st.info("⏳ Waiting for logs... Generating now...")
    else:
        anomalies = detect_anomalies(df)
        with placeholder.container():
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                st.subheader("📊 Recent API Logs (last 20 requests)")
                # Show most relevant columns
                display_df = df[['timestamp', 'method', 'endpoint', 'status_code', 'latency_ms']].copy()
                # Highlight error rows (status >= 400) in red
                def color_status(val):
                    if val >= 400:
                        return 'background-color: #ffcccc'
                    return ''
                st.dataframe(display_df.style.applymap(color_status, subset=['status_code']))
                
                # Simple metrics
                error_rate = (df['status_code'] >= 400).mean()
                avg_latency = df['latency_ms'].mean()
                col1a, col1b = st.columns(2)
                col1a.metric("📈 Error Rate", f"{error_rate*100:.1f}%")
                col1b.metric("⏱️ Avg Latency (ms)", f"{avg_latency:.1f}")
            
            with col2:
                st.subheader("🚨 Anomaly Detection")
                
                # --- DEMO BUTTON: Simulate a failure (injects directly into in-memory queue) ---
                if st.button("🎮 Simulate API Failure (for demo)", use_container_width=True):
                    # Create an error log entry
                    error_log = inject_error_log("/payment", 500, 2000)
                    # Add it directly to the global log_queue from anomaly_detector
                    log_queue.append(error_log)
                    # Keep only last 20 logs
                    if len(log_queue) > 20:
                        # Remove oldest if needed (handled in load_recent_logs, but we can trim here too)
                        pass
                    st.success("✅ Injected a 500 error on /payment! Wait 5 seconds to see anomaly detected.")
                
                if anomalies:
                    for a in anomalies:
                        st.error(a)
                    
                    # Show AI explanation if anomalies changed or user clicks button
                    if st.button("🤖 Run AI Debug Analysis", key="debug_btn", use_container_width=True):
                        with st.spinner("🧠 Asking AI to analyze anomalies..."):
                            recent = get_sample_logs_for_llm(df)
                            explanation = explain_anomaly(anomalies, recent)
                            st.session_state.last_explanation = explanation
                            st.session_state.last_anomalies = anomalies
                    
                    if st.session_state.last_explanation and st.session_state.last_anomalies == anomalies:
                        st.markdown("### 🧠 AI Debugging Report")
                        st.text(st.session_state.last_explanation)
                else:
                    st.success("✅ No anomalies detected in last 20 requests")
                    # Clear previous explanation if any
                    st.session_state.last_explanation = None
                    st.session_state.last_anomalies = None
    
    time.sleep(5)  # refresh every 5 seconds
    st.rerun()  # Force rerun to refresh
