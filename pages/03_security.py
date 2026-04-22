import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import get_tia942_checklist, get_iso27001_domains
from utils.charts import horizontal_bar, gauge, _LAYOUT

st.set_page_config(page_title="NexCore | Security", page_icon="🔒",
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
.cert-row { display:flex; gap:10px; flex-wrap:wrap; margin: 12px 0; }
.cert-box {
    background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3);
    border-radius: 8px; padding: 14px 18px; flex: 1; min-width: 160px;
}
.cert-box .ctitle { color: #10B981; font-weight: 700; font-size: 0.95rem; }
.cert-box .cdate  { color: #9CA3AF; font-size: 0.75rem; margin-top: 4px; }
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

st.markdown("""
<div class='page-header'>
    <h2>🔒 Security & Compliance</h2>
    <p>TIA-942 Tier III controls · ISO/IEC 27001:2022 domains · Physical security posture</p>
</div>
""", unsafe_allow_html=True)

tia = get_tia942_checklist()
iso = get_iso27001_domains()

total_tia    = len(tia)
compliant    = len(tia[tia["Status"] == "Compliant"])
in_review    = len(tia[tia["Status"] == "In Review"])
tia_score    = round(compliant / total_tia * 100, 1)
iso_score    = round(iso["Controls_Implemented"].sum() / iso["Controls_Total"].sum() * 100, 1)
iso_controls = iso["Controls_Total"].sum()
iso_impl     = iso["Controls_Implemented"].sum()

# ── Certification cards ───────────────────────────────────────────────────────
st.markdown("""
<div class='cert-row'>
    <div class='cert-box'>
        <div class='ctitle'>Uptime Institute — Tier III+</div>
        <div class='cdate'>Rated 2018 · Renewed 2023 · Next audit 2026</div>
    </div>
    <div class='cert-box'>
        <div class='ctitle'>ISO/IEC 27001:2022</div>
        <div class='cdate'>Certified 2020 · Surveillance 2025 · Renewal 2026</div>
    </div>
    <div class='cert-box'>
        <div class='ctitle'>PCI-DSS v4.0</div>
        <div class='cdate'>Level 1 · QSA assessed 2025 · Valid through 2026</div>
    </div>
    <div class='cert-box'>
        <div class='ctitle'>SOC 2 Type II</div>
        <div class='cdate'>Security + Availability + Confidentiality · 2025</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Score gauges ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Compliance Scores</div>", unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1:
    st.plotly_chart(gauge(tia_score, 95.0, "TIA-942 Compliance", suffix=" %",
                          low=80, high=95), use_container_width=True)
with g2:
    st.plotly_chart(gauge(iso_score, 90.0, "ISO 27001 Controls", suffix=" %",
                          low=75, high=90), use_container_width=True)
with g3:
    st.markdown(f"""
    <div class='metric-card' style='margin-top:28px;'>
        <div class='label'>TIA-942 Controls</div>
        <div class='value'>{compliant}/{total_tia}</div>
        <div class='sub'>Compliant · {in_review} under review</div>
    </div>
    <div class='metric-card'>
        <div class='label'>ISO 27001 Controls</div>
        <div class='value'>{iso_impl}/{iso_controls}</div>
        <div class='sub'>Implemented across 14 domains</div>
    </div>
    """, unsafe_allow_html=True)

# ── TIA-942 Checklist ─────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>TIA-942 Tier III Control Checklist</div>", unsafe_allow_html=True)

domain_filter = st.selectbox(
    "Filter by Domain",
    ["All"] + sorted(tia["Domain"].unique().tolist()),
)
tia_view = tia if domain_filter == "All" else tia[tia["Domain"] == domain_filter]

def style_status(val):
    return {
        "Compliant":  "background-color:#052e16; color:#86EFAC;",
        "In Review":  "background-color:#451a03; color:#FCD34D;",
        "Non-Compliant": "background-color:#450a0a; color:#FCA5A5;",
    }.get(val, "")

styled_tia = tia_view.style.applymap(style_status, subset=["Status"])
st.dataframe(styled_tia, use_container_width=True, height=320)

# ── ISO 27001 Domain Scores ───────────────────────────────────────────────────
st.markdown("<div class='section-title'>ISO/IEC 27001:2022 — Control Domain Coverage</div>",
            unsafe_allow_html=True)

c_bar, c_table = st.columns([3, 2])
with c_bar:
    fig_iso = horizontal_bar(iso, "Score %", "Domain",
                             "ISO 27001 Control Implementation by Domain",
                             color="#10B981")
    fig_iso.update_traces(
        marker_color=[
            "#10B981" if v >= 90 else ("#F59E0B" if v >= 75 else "#EF4444")
            for v in iso["Score %"]
        ]
    )
    fig_iso.update_layout(xaxis=dict(range=[0, 105]))
    st.plotly_chart(fig_iso, use_container_width=True)

with c_table:
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(
        iso[["Domain", "Controls_Implemented", "Controls_Total", "Score %"]].sort_values("Score %"),
        use_container_width=True, height=420,
    )

# ── Physical Security Controls ────────────────────────────────────────────────
st.markdown("<div class='section-title'>Physical Security Controls Overview</div>", unsafe_allow_html=True)

phys_controls = [
    ("Access Control", "Multi-factor: biometric + RFID badge + PIN at all critical zones (server hall, power room, NOC)"),
    ("Video Surveillance", "432 IP cameras · 90-day retention · AI-based motion anomaly detection"),
    ("Intrusion Detection", "Vibration sensors on perimeter walls · PIR motion detectors · Glass-break sensors"),
    ("Visitor Management", "Pre-authorization required · Escorted at all times · Badge + photo log retained 12 months"),
    ("Loading Dock", "Separate entry with airlock · Inspection area before asset entry · X-ray screening"),
    ("Cable Management", "All fiber in locked conduit · MDA/HDA segregation · Colored locking port inserts"),
    ("Environmental Monitoring", "DCIM: temperature, humidity, water leak detection, smoke, airflow — alerts in < 30 s"),
]

for control, detail in phys_controls:
    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1F2937; border-radius:6px;
                padding:12px 16px; margin-bottom:6px; display:flex; gap:14px; align-items:flex-start;'>
        <span style='color:#10B981; font-weight:600; min-width:180px; font-size:0.83rem;'>{control}</span>
        <span style='color:#9CA3AF; font-size:0.82rem;'>{detail}</span>
    </div>
    """, unsafe_allow_html=True)

st.caption(
    "Standards reference: TIA-942-B (2017) · ISO/IEC 27001:2022 · NIST SP 800-53 Rev 5 · "
    "Uptime Institute Tier Standard: Operational Sustainability."
)
