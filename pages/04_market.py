import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import (
    get_mexico_market_size, get_market_share, get_regional_data,
    get_deployment_models, get_investment_trends, get_provider_comparison,
)
from utils.charts import line_chart, donut, horizontal_bar, map_mexico, radar_chart, _LAYOUT, PALETTE

st.set_page_config(page_title="NexCore | Market", page_icon="📊",
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
    <h2>📊 Market Intelligence — Mexico DC Market (U4)</h2>
    <p>Market size · Regional hotspots · Deployment models · Provider comparison tool</p>
</div>
""", unsafe_allow_html=True)

mkt  = get_mexico_market_size()
sh   = get_market_share()
reg  = get_regional_data()
dep  = get_deployment_models()
inv  = get_investment_trends()
prov = get_provider_comparison()

# ── Hero KPIs ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    ("Market Size 2024", "$2.8 B USD", "Source: JLL Mexico DC Report 2024"),
    ("CAGR 2024–2029", "13.2 %", "Mordor Intelligence 2024"),
    ("Installed Capacity", "~450 MW", "CDMX + secondary markets"),
    ("Active Data Centers", "35+", "Carrier-neutral colocation"),
    ("FDI Attraction", "$1.94 B", "2024 cumulative DC investment"),
]
for col, (label, val, sub) in zip([c1, c2, c3, c4, c5], kpis):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='label'>{label}</div>
            <div class='value' style='font-size:1.4rem;'>{val}</div>
            <div class='sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Market Size Chart ─────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Mexico DC Market Size — Historical & Projected (USD Billions)</div>",
            unsafe_allow_html=True)

fig_mkt = go.Figure()
hist = mkt[mkt["Type"] == "Historical"]
proj = mkt[mkt["Type"] == "Projected"]

fig_mkt.add_trace(go.Bar(
    x=hist["Year"], y=hist["Market Size (USD B)"],
    name="Historical", marker_color="#10B981",
    text=hist["Market Size (USD B)"].apply(lambda v: f"${v}B"),
    textposition="outside",
))
fig_mkt.add_trace(go.Bar(
    x=proj["Year"], y=proj["Market Size (USD B)"],
    name="Projected", marker_color="#3B82F6", opacity=0.75,
    text=proj["Market Size (USD B)"].apply(lambda v: f"${v}B"),
    textposition="outside",
))
fig_mkt.add_trace(go.Scatter(
    x=mkt["Year"], y=mkt["Market Size (USD B)"],
    mode="lines", line=dict(color="#F59E0B", dash="dash", width=1.5),
    name="Trend",
))
fig_mkt.update_layout(
    **_LAYOUT,
    title="Mexico Data Center Market (2019–2028) — USD Billions",
    xaxis_title="Year", yaxis_title="Market Size (USD B)",
    barmode="group",
)
st.plotly_chart(fig_mkt, use_container_width=True)
st.caption("Sources: JLL Mexico DC Market Report 2024 · Mordor Intelligence · CBRE LatAm Outlook 2024.")

# ── Regional Map ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Regional DC Hotspots — Installed Capacity & YoY Growth</div>",
            unsafe_allow_html=True)
st.plotly_chart(map_mexico(reg), use_container_width=True)

col_tbl, col_dep = st.columns(2)
with col_tbl:
    st.markdown("<div class='section-title'>Regional Data</div>", unsafe_allow_html=True)
    st.dataframe(
        reg[["City", "State", "Installed MW", "Active DCs", "Growth YoY %", "Key Driver"]],
        use_container_width=True, height=280,
    )
with col_dep:
    st.markdown("<div class='section-title'>Deployment Models — Market Share</div>",
                unsafe_allow_html=True)
    fig_dep = donut(
        dep["Model"].tolist(), dep["Market Share %"].tolist(),
        "Deployment Model Mix",
        colors=PALETTE,
    )
    st.plotly_chart(fig_dep, use_container_width=True)

# ── Market Share ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Provider Market Share by Capacity (MW)</div>",
            unsafe_allow_html=True)

c_share, c_inv = st.columns(2)
with c_share:
    fig_sh = horizontal_bar(sh, "Market Share %", "Provider",
                            "Market Share by Provider — 2024", color="#10B981")
    fig_sh.update_traces(
        text=[f"{v}% · {c} MW" for v, c in zip(sh["Market Share %"], sh["Capacity (MW)"])],
        textposition="auto",
    )
    st.plotly_chart(fig_sh, use_container_width=True)

with c_inv:
    st.markdown("<div class='section-title'>Investment Trends (FDI + Domestic)</div>",
                unsafe_allow_html=True)
    fig_inv = go.Figure()
    fig_inv.add_trace(go.Bar(x=inv["Quarter"], y=inv["FDI (USD M)"],
                             name="FDI", marker_color="#3B82F6"))
    fig_inv.add_trace(go.Bar(x=inv["Quarter"], y=inv["Domestic (USD M)"],
                             name="Domestic", marker_color="#10B981"))
    fig_inv.update_layout(**_LAYOUT, barmode="stack",
                          xaxis_title="Quarter", yaxis_title="Investment (USD M)",
                          title="Quarterly DC Investment — 2024–2025")
    st.plotly_chart(fig_inv, use_container_width=True)

# ── EXTRA FEATURE: Provider Comparison Radar Tool ────────────────────────────
st.markdown("""
<div class='section-title'>⭐ Extra Feature: Provider Comparison Tool</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:#111827; border:1px solid #F59E0B; border-radius:8px; padding:14px 18px; margin-bottom:16px;'>
    <span style='color:#F59E0B; font-weight:600; font-size:0.82rem;'>INTERACTIVE</span>
    <span style='color:#9CA3AF; font-size:0.82rem;'> — Select two providers to compare across 6 dimensions.</span>
</div>
""", unsafe_allow_html=True)

providers_list = prov["Provider"].tolist()
cc1, cc2 = st.columns(2)
with cc1:
    p1 = st.selectbox("Provider A", providers_list, index=0)
with cc2:
    p2 = st.selectbox("Provider B", providers_list, index=3)

dimensions = ["Uptime SLA", "Tier", "Price", "Sustainability", "Compliance", "Connectivity", "Support"]

def get_scores(provider: str):
    row = prov[prov["Provider"] == provider].iloc[0]
    return [
        min(row["Uptime SLA %"] - 99.98, 0.02) / 0.02 * 10,  # normalize 99.98–100 to 0–10
        row["Tier"] * 2.5,
        row["Price Index"],
        row["Sustainability Score"],
        row["Compliance Score"],
        row["Connectivity Score"],
        row["Support Score"],
    ]

if p1 != p2:
    s1 = get_scores(p1)
    s2 = get_scores(p2)
    fig_radar = radar_chart(dimensions, [s1, s2], [p1, p2])
    st.plotly_chart(fig_radar, use_container_width=True)

    comp_col1, comp_col2 = st.columns(2)
    for col, pname, scores in [(comp_col1, p1, s1), (comp_col2, p2, s2)]:
        with col:
            row = prov[prov["Provider"] == pname].iloc[0]
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1rem; font-weight:700; color:#E2E8F0; margin-bottom:10px;'>{pname}</div>
                <div class='label'>Uptime SLA</div>
                <div style='color:#10B981; font-weight:600;'>{row["Uptime SLA %"]} %</div>
                <div class='label' style='margin-top:8px;'>Tier</div>
                <div style='color:#E2E8F0;'>{int(row["Tier"])}</div>
                <div class='label' style='margin-top:8px;'>Sustainability Score</div>
                <div style='color:#3B82F6;'>{row["Sustainability Score"]} / 10</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Please select two different providers to compare.")

st.caption(
    "Data: estimated from public disclosures, Uptime Institute ratings, and industry reports. "
    "Price and support scores are relative indices (1–10 scale). "
    "Sources: Uptime Institute 2024 · Data Center Dynamics · JLL Mexico."
)
