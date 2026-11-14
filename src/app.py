import html
import re
from io import StringIO

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from content import HERO, HOME_BODY, LEGAL, SPECS
from feature_engineering import MITRE, REQUIRED, brute_force_mask, clean_logs, extract_features, find_signatures
from llm_triage import generate_triage_summary
from model import LogAnomalyDetector, severity
from styles import JS, css, topbar
from synthetic import generate_traffic

st.set_page_config(page_title="SentinelLog AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
ss = st.session_state
for k, v in {"tab": "Home", "uk": 0, "light": False}.items():
    ss.setdefault(k, v)
TABS = ["Home", "Features", "Specs / Info"]

LOG_RX = re.compile(r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[.*?\]\s+"(?P<m>\S+)\s+(?P<p>\S+)[^"]*"\s+(?P<s>\d{3})\s+(?P<b>\d+|-)')
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


def parse_raw_log_lines(text: str) -> pd.DataFrame:
    rows = []
    for line in text.strip().splitlines():
        m = LOG_RX.search(line)
        if m:
            rows.append({"ip": m["ip"], "request_path": m["p"], "status_code": int(m["s"]),
                         "response_size": 0 if m["b"] == "-" else int(m["b"])})
    return pd.DataFrame(rows)


def reset_logs():
    ss.pop("out", None)
    ss["uk"] += 1


def set_tab(t):
    ss["tab"] = t


def toggle_theme():
    ss["light"] = not ss["light"]


def go_features():
    ss["tab"] = "Features"


# ---------- shell: styles, glass top bar, tabs, settings ----------
st.markdown(css(ss["light"], ss["tab"] != "Home"), unsafe_allow_html=True)
if ss["tab"] != "Features":
    st.markdown("<style>[data-testid='stSidebar']{display:none!important}</style>", unsafe_allow_html=True)
st.markdown(topbar(ss["tab"], ss["light"], TABS), unsafe_allow_html=True)
with st.container(key="hid"):  # hidden Streamlit buttons that the glass bar triggers
    for t in TABS:
        st.button(t, key="bt_" + t.split()[0].lower(), on_click=set_tab, args=(t,))
    st.button("theme", key="bt_theme", on_click=toggle_theme)
    st.button("reset", key="bt_reset", on_click=reset_logs)
components.html(JS, height=0)


def home():
    st.markdown(HERO, unsafe_allow_html=True)
    with st.container(key="cta"):
        _, b, c, _ = st.columns([3, 2, 2, 3])
        b.button("Open the dashboard", on_click=go_features, use_container_width=True)
        c.markdown('<a class="pill-red" href="#learn">Learn more</a>', unsafe_allow_html=True)
    st.markdown(HOME_BODY, unsafe_allow_html=True)


def features():
    with st.sidebar:
        st.markdown('<div class="sb-tab"><i></i>Data source</div>', unsafe_allow_html=True)
        source = st.radio("Input", ["Synthetic traffic (600 requests)", "Preset scenario", "Upload log file"], label_visibility="collapsed")
        logs = pd.DataFrame()
        if source.startswith("Synthetic"):
            logs = generate_traffic()
        elif source == "Preset scenario":
            logs = pd.DataFrame(PRESETS[st.selectbox("Scenario", list(PRESETS))], columns=REQUIRED)
        else:
            up = st.file_uploader("CSV, .log or .txt", type=["csv", "log", "txt"], key=f"up{ss['uk']}")
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

    st.markdown('<div class="fhead"><div class="dcore"><div class="r2"><span class="blip" style="top:20%;left:62%;animation-delay:.6s"></span>'
                '<span class="blip" style="top:64%;left:26%;animation-delay:2.4s"></span></div></div><div><h2>Detection console</h2>'
                '<p>Pick a data source in the floating panel, then run the pipeline.</p></div></div>', unsafe_allow_html=True)
    if logs.empty:
        st.info("Choose a data source in the floating panel to begin.")
        return
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
            bf = brute_force_mask(out)
            out["signatures"] = [s + ["Brute force"] if b else s for s, b in zip(out["signatures"], bf)]
            out["flagged"] = out["ml_flag"] | out["signatures"].str.len().gt(0)
            ss["out"] = out

    out = ss.get("out")
    if out is None or len(out) != len(logs):
        return
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

    off, mut = ("#00000055", "#6b5d5f") if ss["light"] else ("#FFFFFF66", "#B9A9AC")
    chart = alt.Chart(out.reset_index()).mark_circle(size=70, opacity=.85).encode(
        x=alt.X("index:Q", title="Request #"), y=alt.Y("anomaly_score:Q", title="Anomaly score"),
        color=alt.Color("flagged:N", scale=alt.Scale(domain=[False, True], range=[off, "#FF2D45"]), legend=None),
        tooltip=["ip", "request_path", "status_code", "anomaly_score"]).properties(height=240).configure_view(strokeWidth=0).configure_axis(
        gridColor="#80808030", labelColor=mut, titleColor=mut, domainColor="#80808030")
    st.altair_chart(chart, use_container_width=True, theme=None)

    if flagged.empty:
        st.success("No threats flagged at the current sensitivity.")
        return
    top_ips = flagged.groupby("ip").agg(n=("ip", "size"), s=("anomaly_score", "max")).sort_values(["n", "s"], ascending=False).head(5)
    rows = "".join(f'<div class="row"><span>{html.escape(str(ip))}</span><div class="bar"><i style="width:{int(v["s"] * 100)}%"></i></div><b>{int(v["n"])}</b></div>'
                   for ip, v in top_ips.iterrows())
    st.markdown(f'<div class="panel-h"><i></i>Top offenders<em>by flagged requests</em></div><div class="card off">{rows}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-h"><i></i>Incident queue<em>{len(flagged)} flagged</em></div>', unsafe_allow_html=True)
    sev_pick = st.multiselect("Filter by severity", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"])
    hot = sorted(set(out[out["flagged"] & (out["anomaly_score"] >= 0.6)]["ip"].astype(str)))
    flagged = flagged[flagged["anomaly_score"].map(severity).isin(sev_pick)]
    for n, (_, r) in enumerate(flagged.iterrows()):
        sev = severity(r["anomaly_score"])
        sigs = "".join(f'<span class="chip">{html.escape(s)} · {MITRE[s]}</span>' for s in r["signatures"]) or '<span class="chip">statistical outlier</span>'
        st.markdown(
            f'<div class="inc"><code>{html.escape(r["request_path"])}</code><div class="meta">'
            f'<span class="chip sev-{sev}">{sev} · {r["anomaly_score"]:.2f}</span><span class="chip">{html.escape(str(r["ip"]))}</span>'
            f'<span class="chip">HTTP {r["status_code"]}</span><span class="chip">{r["response_size"]:,} B</span>{sigs}</div></div>', unsafe_allow_html=True)
        if n < max_triage:
            text, src = generate_triage_summary(r[REQUIRED].to_dict(), r["signatures"])
            label = "LLM triage (local model)" if src == "llm" else "Offline heuristic · start Ollama for LLM triage"
            st.markdown(f'<div class="tri">{html.escape(text)}<small>{label}</small></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.download_button("Export incident report (CSV)", flagged.astype(str).to_csv(index=False), "sentinel_incidents.csv", "text/csv")
    if hot:
        c2.download_button("Export IP blocklist (TXT)", "\n".join(hot), "blocklist.txt", "text/plain")


if ss["tab"] == "Home":
    home()
elif ss["tab"] == "Features":
    features()
else:
    st.markdown(SPECS, unsafe_allow_html=True)
st.markdown(LEGAL, unsafe_allow_html=True)
