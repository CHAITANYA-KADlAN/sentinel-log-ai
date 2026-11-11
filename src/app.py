import html
from io import StringIO

import altair as alt
import pandas as pd
import streamlit as st

from feature_engineering import REQUIRED, clean_logs, extract_features, find_signatures
from llm_triage import generate_triage_summary
from model import LogAnomalyDetector, severity
import streamlit.components.v1 as components
from styles import CSS, HERO, JS
from synthetic import generate_traffic

st.set_page_config(page_title="SentinelLog AI", page_icon="🛡️", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(HERO, unsafe_allow_html=True)
components.html(JS, height=0)

import re
LOG_RX = re.compile(r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[.*?\]\s+"(?P<m>\S+)\s+(?P<p>\S+)[^"]*"\s+(?P<s>\d{3})\s+(?P<b>\d+|-)')


def parse_raw_log_lines(text: str) -> pd.DataFrame:
    rows = []
    for line in text.strip().splitlines():
        m = LOG_RX.search(line)
        if m:
            rows.append({"ip": m["ip"], "request_path": m["p"], "status_code": int(m["s"]),
                         "response_size": 0 if m["b"] == "-" else int(m["b"])})
    return pd.DataFrame(rows)


PRESETS = {
    "A · SQL injection & path traversal": [
        ("192.168.1.10", "/index.html", 200, 420), ("192.168.1.11", "/static/css/style.css", 200, 1840),
        ("192.168.1.12", "/api/v1/user/profile", 200, 560), ("10.0.0.99", "/api/login?user=admin' OR '1'='1", 500, 14200),
        ("10.0.0.99", "/../../etc/passwd", 403, 8900), ("192.168.1.14", "/dashboard", 200, 610)],
    "B · Brute-force authentication": [
        ("45.33.32.156", "/wp-login.php", 401, 320)] * 3 + [("192.168.1.15", "/home", 200, 490), ("45.33.32.156", "/wp-login.php", 200, 15400)],
    "C · Normal traffic baseline": [
        ("192.168.1.20", "/home", 200, 450), ("192.168.1.21", "/docs", 200, 1200), ("192.168.1.22", "/about", 200, 380)],
}

with st.sidebar:
    st.markdown('<div class="sb-tab"><i></i>Data source</div>', unsafe_allow_html=True)
    source = st.radio("Input", ["Synthetic traffic (600 requests)", "Preset scenario", "Upload log file"], label_visibility="collapsed")
    logs = pd.DataFrame()
    if source.startswith("Synthetic"):
        logs = generate_traffic()
    elif source == "Preset scenario":
        name = st.selectbox("Scenario", list(PRESETS))
        logs = pd.DataFrame(PRESETS[name], columns=REQUIRED)
    else:
        up = st.file_uploader("CSV, .log or .txt", type=["csv", "log", "txt"])
        if up:
            try:
                if up.name.endswith(".csv"):
                    logs = pd.read_csv(up)
                    if not set(REQUIRED).issubset(logs.columns):
                        st.error(f"CSV needs columns: {', '.join(REQUIRED)}")
                        logs = pd.DataFrame()
                else:
                    logs = parse_raw_log_lines(StringIO(up.getvalue().decode("utf-8", "ignore")).read())
            except Exception as e:  # noqa: BLE001
                st.error(f"Could not parse file: {e}")
    st.markdown("**Sensitivity**")
    contamination = st.slider("Expected anomaly rate", 0.01, 0.50, 0.08, 0.01)
    max_triage = st.slider("LLM triage reports", 1, 10, 4)

if logs.empty:
    st.info("Choose a data source in the sidebar to begin.")
    st.stop()

logs = clean_logs(logs)
if len(logs) < 30:
    st.warning("Fewer than 30 requests: Isolation Forest needs volume to learn a baseline. Try the synthetic dataset for a meaningful run.")

st.markdown(f'<div class="panel-h"><i></i>Ingested logs<em>{len(logs):,} requests</em></div>', unsafe_allow_html=True)
st.dataframe(logs.drop(columns=["is_attack"], errors="ignore"), use_container_width=True, height=240)

if st.button("Run detection pipeline"):
    with st.spinner("Scoring requests…"):
        res = LogAnomalyDetector(contamination).train_and_predict(extract_features(logs))
        out = logs.copy()
        out["anomaly_score"] = res["anomaly_score"].round(3)
        out["ml_flag"] = res["is_anomaly"]
        out["signatures"] = out["request_path"].map(find_signatures)
        out["flagged"] = out["ml_flag"] | out["signatures"].str.len().gt(0)
        st.session_state["out"] = out

out = st.session_state.get("out")
if out is not None and len(out) == len(logs):
    flagged = out[out["flagged"]].sort_values("anomaly_score", ascending=False)
    top = severity(flagged["anomaly_score"].max()) if len(flagged) else "None"
    st.markdown(
        f'<div class="kpis"><div class="card kpi"><small>Requests analysed</small><b>{len(out):,}</b></div>'
        f'<div class="card kpi bad"><small>Flagged events</small><b>{len(flagged)}</b></div>'
        f'<div class="card kpi"><small>Source IPs flagged</small><b>{flagged["ip"].nunique()}</b></div>'
        f'<div class="card kpi"><small>Peak severity</small><b>{top}</b></div></div>', unsafe_allow_html=True)

    if "is_attack" in out:
        tp = int((out["flagged"] & out["is_attack"]).sum())
        st.caption(f"Ground-truth check · recall {tp / max(out['is_attack'].sum(), 1):.0%} · precision {tp / max(len(flagged), 1):.0%}")

    chart = alt.Chart(out.reset_index()).mark_circle(size=70, opacity=.85).encode(
        x=alt.X("index:Q", title="Request #"), y=alt.Y("anomaly_score:Q", title="Anomaly score"),
        color=alt.Color("flagged:N", scale=alt.Scale(domain=[False, True], range=["#4DD9FF55", "#FF4D6D"]), legend=None),
        tooltip=["ip", "request_path", "status_code", "anomaly_score"]).properties(height=240).configure_view(strokeWidth=0).configure_axis(
        gridColor="#1b2740", labelColor="#7E8DA8", titleColor="#7E8DA8", domainColor="#1b2740")
    st.altair_chart(chart, use_container_width=True, theme=None)

    if flagged.empty:
        st.success("No threats flagged at the current sensitivity.")
    else:
        st.markdown(f'<div class="panel-h"><i></i>Incident queue<em>{len(flagged)} flagged</em></div>', unsafe_allow_html=True)
        for n, (_, r) in enumerate(flagged.iterrows()):
            sev = severity(r["anomaly_score"])
            sigs = "".join(f'<span class="chip">{html.escape(s)}</span>' for s in r["signatures"]) or '<span class="chip">statistical outlier</span>'
            st.markdown(
                f'<div class="inc"><code>{html.escape(r["request_path"])}</code><div class="meta">'
                f'<span class="chip sev-{sev}">{sev} · {r["anomaly_score"]:.2f}</span><span class="chip">{html.escape(str(r["ip"]))}</span>'
                f'<span class="chip">HTTP {r["status_code"]}</span><span class="chip">{r["response_size"]:,} B</span>{sigs}</div></div>',
                unsafe_allow_html=True)
            if n < max_triage:
                text, src = generate_triage_summary(r[REQUIRED].to_dict(), r["signatures"])
                label = "LLM triage (local model)" if src == "llm" else "Offline heuristic · start Ollama for LLM triage"
                st.markdown(f'<div class="tri">{html.escape(text)}<small>{label}</small></div>', unsafe_allow_html=True)
        st.download_button("Export incident report (CSV)", flagged.astype(str).to_csv(index=False), "sentinel_incidents.csv", "text/csv")
