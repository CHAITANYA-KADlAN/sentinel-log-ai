# 🛡️ SentinelLog AI: Security Anomaly Detector

An AI-driven SIEM extension that ingests streaming server logs, identifies novel zero-day attack patterns using unsupervised machine learning (Isolation Forests), and produces plain-English incident triage reports via LLM integration.

---

## 🏗️ System Architecture

```text
[ Raw Web / Server Logs ]
           │
           ▼
[ Feature Extraction & TF-IDF ]
           │
           ▼
[ Isolation Forest Anomaly Engine ] ──► (Anomaly Score > Threshold)
           │                                        │
           ▼                                        ▼
[ Streamlit Analyst Dashboard ]        [ Local LLM Incident Triage ]
                                       (Attack Summary & SOC Action)


