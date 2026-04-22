import streamlit as st
import pandas as pd
from utils.data_loader import get_sla_metrics, get_incident_log, get_mac_processes
from utils.charts import gauge

st.set_page_config(page_title="NexCore | Operations", page_icon="⚙️",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #0D1320; border-right: 1px solid #1F2937; }
.metric-card {
    background: #111827; border: 1px solid #1F2937; border-radius: 8px;
    padding: 18px 22px; margin-bottom: 8px;
}
.metric-card .label { font-size: 0.72rem; color: #6B7280; letter-spacing: 0.08em; text-transform: uppercase; }
.metric-card .value { font-size: 1.9rem; font-weight: 700; color: #10B981; line-height: 1.1; }
.metric-card .sub   { font-size: 0.78rem; color: #9CA3AF; margin-top: 4px; }
.page-header { border-left: 3px solid #10B981; padding-left: 14px; margin-bottom: 24px; }
.page-header h2 { color: #E2E8F0; font-size: 1.4rem; font-weight: 600; }
.page-header p  { color: #6B7280; font-size: 0.82rem; margin-top: 2px; }
.section-title { color: #F59E0B; font-size: 0.72rem; letter-spacing: 0.15em;
                 text-transform: uppercase; margin: 20px 0 10px; font-weight: 600; }
.cert-pill { display: inline-block; background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35); color: #10B981;
    padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; margin: 3px 3px 3px 0; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <div style='font-size:2rem;'>🏢</div>
        <div style='font-size:1.05rem; font-weight:700; color:#E2E8F0;'>NexCore DataSystems</div>
        <div style='font-size:0.72rem; color:#6B7280;'>MX DC OPERATIONS</div>
    </div>
    <hr style='border-color:#1F2937; margin:10px 0;'>
    """, unsafe_allow_html=True)
    st.markdown("**Facilities**")
    st.markdown("🟢 Site A — CDMX Vallejo")
    st.markdown("🟢 Site B — Querétaro")
    st.caption("Dashboard v2.0 · April 2026")

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='page-header'>
    <h2>⚙️ Operations Center</h2>
    <p>Real-time SLA monitoring · Incident management · MAC process tracker</p>
</div>
""", unsafe_allow_html=True)

sla = get_sla_metrics()

# ── SLA Gauges ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Uptime SLA — Rolling 12 Months</div>", unsafe_allow_html=True)

g1, g2, g3, g4 = st.columns(4)
with g1:
    st.plotly_chart(gauge(sla["site_a"]["uptime_pct"], sla["site_a"]["target_sla"],
                          "Site A · Overall Uptime", low=99.0, high=99.982), use_container_width=True)
with g2:
    st.plotly_chart(gauge(sla["site_a"]["power_uptime"], 99.995,
                          "Site A · Power Uptime", low=99.9, high=99.995), use_container_width=True)
with g3:
    st.plotly_chart(gauge(sla["site_b"]["uptime_pct"], sla["site_b"]["target_sla"],
                          "Site B · Overall Uptime", low=99.0, high=99.982), use_container_width=True)
with g4:
    st.plotly_chart(gauge(sla["site_b"]["power_uptime"], 99.995,
                          "Site B · Power Uptime", low=99.9, high=99.995), use_container_width=True)

# ── Summary metrics ───────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Facility Overview</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
metrics = [
    ("Total Incidents YTD", str(sla["site_a"]["incidents_ytd"] + sla["site_b"]["incidents_ytd"]), "All sites"),
    ("MTTR · Site A", f"{sla['site_a']['mttr_hours']} hrs", "Mean time to resolve"),
    ("MTTR · Site B", f"{sla['site_b']['mttr_hours']} hrs", "Mean time to resolve"),
    ("Racks · Site A", f"{sla['site_a']['racks_occupied']:,} / {sla['site_a']['racks_total']:,}", "Occupied"),
    ("Racks · Site B", f"{sla['site_b']['racks_occupied']:,} / {sla['site_b']['racks_total']:,}", "Occupied"),
    ("SLA Target (Tier III+)", "99.982 %", "≤ 1.6 hrs downtime/yr"),
]
for col, (label, val, sub) in zip([c1, c2, c3, c4, c5, c6], metrics):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='label'>{label}</div>
            <div class='value' style='font-size:1.3rem;'>{val}</div>
            <div class='sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Incident Log ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Incident Log</div>", unsafe_allow_html=True)

incidents = get_incident_log()

f1, f2, f3 = st.columns([2, 2, 2])
with f1:
    site_f = st.selectbox("Filter by Site", ["All"] + sorted(incidents["Site"].unique().tolist()))
with f2:
    sev_f = st.selectbox("Filter by Severity", ["All"] + sorted(incidents["Severity"].unique().tolist()))
with f3:
    cat_f = st.selectbox("Filter by Category", ["All"] + sorted(incidents["Category"].unique().tolist()))

filtered = incidents.copy()
if site_f != "All": filtered = filtered[filtered["Site"] == site_f]
if sev_f  != "All": filtered = filtered[filtered["Severity"] == sev_f]
if cat_f  != "All": filtered = filtered[filtered["Category"] == cat_f]

def color_severity(val):
    colors = {
        "P1 — Critical": "background-color:#450a0a; color:#FCA5A5;",
        "P2 — High":     "background-color:#451a03; color:#FCD34D;",
        "P3 — Medium":   "background-color:#1c1917; color:#D1D5DB;",
        "P4 — Low":      "background-color:#052e16; color:#86EFAC;",
    }
    return colors.get(val, "")

styled = filtered.style.applymap(color_severity, subset=["Severity"])
st.dataframe(styled, use_container_width=True, height=360)

# Export button (extra feature)
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Export filtered incidents (CSV)", data=csv,
                   file_name="nexcore_incidents.csv", mime="text/csv")

# ── MAC Process Tracker ───────────────────────────────────────────────────────
st.markdown("<div class='section-title'>MAC Process Tracker — Moves, Adds, Changes</div>", unsafe_allow_html=True)

mac = get_mac_processes()

status_colors = {
    "Completed":        "🟢",
    "In Progress":      "🔵",
    "Scheduled":        "🟡",
    "Pending Approval": "🔴",
}
mac["⬤"] = mac["Status"].map(status_colors)
display_cols = ["⬤", "ID", "Type", "Category", "Client", "Site", "Zone", "Rack", "Status", "Created", "Due"]

mac_site = st.selectbox("Filter MAC by Site", ["All", "Site A", "Site B"])
mac_filtered = mac if mac_site == "All" else mac[mac["Site"] == mac_site]

st.dataframe(mac_filtered[display_cols], use_container_width=True, height=320)

col_stats = st.columns(4)
for col, status in zip(col_stats, ["Completed", "In Progress", "Scheduled", "Pending Approval"]):
    count = len(mac[mac["Status"] == status])
    with col:
        st.metric(status, count)
