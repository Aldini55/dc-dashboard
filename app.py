import streamlit as st
from utils.data_loader import get_sla_metrics, get_pue_history, get_mexico_market_size

st.set_page_config(
    page_title="NexCore DC-Ops Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #0D1320; border-right: 1px solid #1F2937; }
[data-testid="stSidebar"] .stMarkdown p { color: #9CA3AF; font-size: 0.82rem; }
.metric-card {
    background: #111827; border: 1px solid #1F2937; border-radius: 8px;
    padding: 18px 22px; margin-bottom: 8px;
}
.metric-card .label { font-size: 0.72rem; color: #6B7280; letter-spacing: 0.08em; text-transform: uppercase; }
.metric-card .value { font-size: 2rem; font-weight: 700; color: #10B981; line-height: 1.1; }
.metric-card .sub   { font-size: 0.78rem; color: #9CA3AF; margin-top: 4px; }
.page-header { border-left: 3px solid #10B981; padding-left: 14px; margin-bottom: 24px; }
.page-header h2 { color: #E2E8F0; font-size: 1.4rem; font-weight: 600; }
.page-header p  { color: #6B7280; font-size: 0.82rem; margin-top: 2px; }
.kpi-badge-green { background: rgba(16,185,129,0.15); color: #10B981; padding: 2px 8px;
                   border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.kpi-badge-amber { background: rgba(245,158,11,0.15); color: #F59E0B; padding: 2px 8px;
                   border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.kpi-badge-red   { background: rgba(239,68,68,0.15); color: #EF4444; padding: 2px 8px;
                   border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.cert-pill {
    display: inline-block; background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35); color: #10B981;
    padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; margin: 3px 3px 3px 0;
}
.divider { border: none; border-top: 1px solid #1F2937; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
        <div style='font-size:2rem;'>🏢</div>
        <div style='font-size:1.05rem; font-weight:700; color:#E2E8F0;'>NexCore DataSystems</div>
        <div style='font-size:0.72rem; color:#6B7280; letter-spacing:0.08em;'>MX DC OPERATIONS</div>
    </div>
    <hr style='border-color:#1F2937; margin:10px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**Facilities**")
    st.markdown("🟢 Site A — CDMX Vallejo *(8 MW)*")
    st.markdown("🟢 Site B — Querétaro *(4 MW)*")
    st.markdown("<hr style='border-color:#1F2937;'>", unsafe_allow_html=True)
    st.markdown("**Certifications**")
    st.markdown("""
    <span class='cert-pill'>Tier III+</span>
    <span class='cert-pill'>ISO 27001</span>
    <span class='cert-pill'>PCI-DSS</span>
    <span class='cert-pill'>SOC 2</span>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1F2937;'>", unsafe_allow_html=True)
    st.caption("Dashboard v2.0 · April 2026\nData Centers E-CED-2 · UPY")

# ── Home ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='page-header'>
    <h2>DC-Ops Dashboard</h2>
    <p>NexCore DataSystems MX · Tier III+ Colocation & Managed Services · Founded 2012</p>
</div>
""", unsafe_allow_html=True)

sla = get_sla_metrics()
pue = get_pue_history()
mkt = get_mexico_market_size()

# Hero KPIs
col1, col2, col3, col4, col5 = st.columns(5)
kpis = [
    ("Total Capacity", "12 MW", "2 facilities · 3,500 racks"),
    ("Combined Uptime", "99.987 %", "Rolling 12-month average"),
    ("Average PUE", "1.45", f"vs Mexico avg 1.65"),
    ("Active Clients", "180+", "Enterprise & cloud providers"),
    ("Mexico Market", "$2.8 B", "2024 · CAGR 13.2 % (source: JLL)"),
]
for col, (label, val, sub) in zip([col1, col2, col3, col4, col5], kpis):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='label'>{label}</div>
            <div class='value'>{val}</div>
            <div class='sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# Site overview cards
col_a, col_b = st.columns(2)
for col, site_key in [(col_a, "site_a"), (col_b, "site_b")]:
    s = sla[site_key]
    occupancy = round(s["racks_occupied"] / s["racks_total"] * 100, 1)
    uptime_badge = "kpi-badge-green" if s["uptime_pct"] >= s["target_sla"] else "kpi-badge-red"
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size:1rem; font-weight:600; color:#E2E8F0; margin-bottom:12px;'>
                🏗 {s['name']}
            </div>
            <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px;'>
                <div>
                    <div class='label'>Uptime</div>
                    <div style='font-size:1.25rem; font-weight:700; color:#10B981;'>{s['uptime_pct']} %</div>
                    <span class='{uptime_badge}'>SLA ≥ {s['target_sla']} %</span>
                </div>
                <div>
                    <div class='label'>Capacity</div>
                    <div style='font-size:1.25rem; font-weight:700; color:#E2E8F0;'>{s['capacity_mw']} MW</div>
                    <div class='sub'>{s['racks_total']:,} racks total</div>
                </div>
                <div>
                    <div class='label'>Occupancy</div>
                    <div style='font-size:1.25rem; font-weight:700; color:#F59E0B;'>{occupancy} %</div>
                    <div class='sub'>{s['racks_occupied']:,} racks live</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# Navigation guide
st.markdown("### Navigate the Dashboard")
nav_items = [
    ("⚙️", "01 · Operations", "SLA gauges · Incident log · MAC process tracker"),
    ("⚡", "02 · Energy",     "PUE trends · Consumption chart · PUE calculator · CO₂ estimator"),
    ("🔒", "03 · Security",   "TIA-942 compliance · ISO 27001 controls · Physical security"),
    ("📊", "04 · Market",     "Mexico DC market · Regional map · Provider comparison tool"),
    ("🚀", "05 · Emerging Tech", "Tech radar · Adoption timeline · Strategic roadmap"),
]
cols = st.columns(5)
for col, (icon, title, desc) in zip(cols, nav_items):
    with col:
        st.markdown(f"""
        <div style='background:#111827; border:1px solid #1F2937; border-radius:8px;
                    padding:16px; text-align:center; height:140px;'>
            <div style='font-size:1.5rem;'>{icon}</div>
            <div style='font-size:0.82rem; font-weight:600; color:#10B981; margin:6px 0 4px;'>{title}</div>
            <div style='font-size:0.72rem; color:#6B7280; line-height:1.5;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.caption(
    "Data sources: JLL Mexico DC Report 2024 · Mordor Intelligence · CBRE LatAm · "
    "Uptime Institute GTR 2024 · NexCore internal DCIM (simulated). "
    "Market figures updated Q4-2025."
)
