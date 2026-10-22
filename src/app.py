import streamlit as st
import pandas as pd
from feature_engineering import extract_features
from model import LogAnomalyDetector
from llm_triage import generate_triage_summary

st.set_page_config(page_title="SentinelLog AI Dashboard", layout="wide")
st.title("🛡️ SentinelLog AI: Security Anomaly Detector")

sample_logs = pd.DataFrame([
    {"ip": "192.168.1.10", "request_path": "/index.html", "status_code": 200, "response_size": 450},
    {"ip": "192.168.1.11", "request_path": "/about.html", "status_code": 200, "response_size": 310},
    {"ip": "10.0.0.99", "request_path": "/admin' OR '1'='1", "status_code": 500, "response_size": 9800},
    {"ip": "192.168.1.12", "request_path": "/contact.html", "status_code": 200, "response_size": 500},
])

st.subheader("Raw Ingested Logs")
st.dataframe(sample_logs)

if st.button("Run Anomaly Detection"):
    X = extract_features(sample_logs)
    detector = LogAnomalyDetector(contamination=0.25)
    results = detector.train_and_predict(X)
    
    sample_logs['is_anomaly'] = results['is_anomaly']
    sample_logs['anomaly_score'] = results['anomaly_score']
    
    st.subheader("Detection Results")
    st.dataframe(sample_logs)
    
    anomalies = sample_logs[sample_logs['is_anomaly'] == True]
    if not anomalies.empty:
        st.warning(f"Detected {len(anomalies)} Potential Security Incident(s)!")
        for idx, row in anomalies.iterrows():
            st.markdown(f"**Target Log:** `{row['request_path']}` (Score: {row['anomaly_score']:.2f})")
            triage_text = generate_triage_summary(row.to_dict())
            st.info(f"**AI Triage Summary:**\n{triage_text}")
