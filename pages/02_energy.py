import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import get_pue_history, get_energy_consumption, get_renewable_mix
from utils.charts import line_chart, stacked_bar, donut, _LAYOUT

st.set_page_config(page_title="NexCore | Energy", page_icon="⚡",
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
    <h2>⚡ Energy & Sustainability</h2>
    <p>PUE trends · Power consumption · Renewable energy mix · CO₂ impact calculator</p>
</div>
""", unsafe_allow_html=True)

pue_df    = get_pue_history()
energy_df = get_energy_consumption()
renew     = get_renewable_mix()

c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("Avg PUE · Site A", "1.48", "vs Mexico avg 1.65 (Uptime Inst. 2024)"),
    ("Avg PUE · Site B", "1.41", "Newest facility — better thermal design"),
    ("Renewable Energy", "62 %", "Target 80 % by 2027"),
    ("Annual CO₂ Saved", "~8,400 t", "vs industry avg PUE baseline"),
]
for col, (label, val, sub) in zip([c1, c2, c3, c4], kpis):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='label'>{label}</div>
            <div class='value'>{val}</div>
            <div class='sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='section-title'>PUE Trend — 24 Months (2024–2025)</div>", unsafe_allow_html=True)

fig_pue = line_chart(
    pue_df, "Month",
    ["Site A (CDMX)", "Site B (QRO)", "Mexico Average", "Global Average", "Hyperscale Avg"],
    "Power Usage Effectiveness Over Time",
    colors=["#10B981", "#3B82F6", "#F59E0B", "#8B5CF6", "#EC4899"],
    y_label="PUE",
)
fig_pue.update_layout(yaxis=dict(range=[1.1, 1.80]))
st.plotly_chart(fig_pue, use_container_width=True)
st.caption(
    "Source: Uptime Institute GTR 2024 — Mexico avg 1.65 · Global avg 1.58 · Hyperscale avg 1.18. "
    "NexCore figures from DCIM system (simulated)."
)

st.markdown("<div class='section-title'>Monthly Energy Consumption by Category (MW)</div>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Site A — CDMX", "Site B — Querétaro"])
with tab1:
    st.plotly_chart(stacked_bar(
        energy_df, "Month",
        ["IT Load A (MW)", "Cooling A (MW)", "UPS/Other A (MW)"],
        "Site A Energy Consumption (MW)",
        colors=["#10B981", "#3B82F6", "#F59E0B"], y_label="Power (MW)",
    ), use_container_width=True)
with tab2:
    st.plotly_chart(stacked_bar(
        energy_df, "Month",
        ["IT Load B (MW)", "Cooling B (MW)", "UPS/Other B (MW)"],
        "Site B Energy Consumption (MW)",
        colors=["#10B981", "#3B82F6", "#F59E0B"], y_label="Power (MW)",
    ), use_container_width=True)

st.markdown("<div class='section-title'>Renewable Energy Mix — 2025</div>", unsafe_allow_html=True)
c_donut, c_leg = st.columns([2, 1])
with c_donut:
    st.plotly_chart(donut(
        list(renew.keys()), list(renew.values()), "Energy Source Breakdown",
        colors=["#10B981", "#3B82F6", "#8B5CF6", "#F59E0B", "#6B7280"],
    ), use_container_width=True)
with c_leg:
    st.markdown("<br><br>", unsafe_allow_html=True)
    for source, pct in renew.items():
        color = "#10B981" if "conv" not in source.lower() else "#6B7280"
        st.markdown(f"<span style='color:{color}; font-weight:600;'>{pct} %</span>"
                    f"<span style='color:#9CA3AF; font-size:0.82rem;'> — {source}</span><br>",
                    unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-top:16px; padding:10px; background:#1F2937; border-radius:6px;'>
        <div style='color:#F59E0B; font-size:0.72rem; font-weight:600;'>TARGET 2027</div>
        <div style='color:#E2E8F0; font-size:1.1rem; font-weight:700;'>80 % Renewable</div>
        <div style='color:#9CA3AF; font-size:0.75rem;'>+6 MW solar PPA — Sonora</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='section-title'>Interactive PUE Calculator & CO₂ Estimator</div>",
            unsafe_allow_html=True)

with st.container():
    cc1, cc2 = st.columns(2)
    with cc1:
        it_load  = st.slider("IT Load (kW)", 100, 5000, 1000, 50)
        pue_val  = st.slider("PUE Value", 1.10, 2.50, 1.48, 0.01)
    with cc2:
        elec_cost = st.number_input("Electricity cost (USD/kWh)", value=0.085, step=0.005, format="%.3f")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Mexico CFE tariff HM (high-tension industrial, 2024): ~$0.085 USD/kWh avg.")

    total_power  = it_load * pue_val
    overhead     = total_power - it_load
    annual_kwh   = total_power * 8760
    annual_cost  = annual_kwh * elec_cost / 1000
    co2_t        = annual_kwh * 0.385 / 1000  # tCO2 — SENER 2024 grid factor
    ideal_kwh    = it_load * 1.20 * 8760
    savings_kwh  = annual_kwh - ideal_kwh
    savings_usd  = savings_kwh * elec_cost / 1000
    savings_co2  = savings_kwh * 0.385 / 1000

    r1, r2, r3, r4 = st.columns(4)
    for col, (label, val) in zip(
        [r1, r2, r3, r4],
        [("Total Facility Power", f"{total_power:,.0f} kW"),
         ("Cooling + Overhead", f"{overhead:,.0f} kW"),
         ("Annual Energy Cost", f"${annual_cost:,.0f} USD"),
         ("Annual CO₂", f"{co2_t:,.1f} t CO₂")]
    ):
        with col:
            st.metric(label, val)

    if pue_val > 1.20:
        st.success(
            f"🌱 Improving to PUE 1.20 saves **{savings_kwh/1000:,.0f} MWh/yr** "
            f"≈ **${savings_usd:,.0f} USD** and **{savings_co2:,.0f} t CO₂** annually."
        )

st.caption(
    "CO₂ emission factor: 0.385 kg CO₂/kWh — Mexico national grid (SENER 2024). "
    "PUE benchmark source: Uptime Institute Global Data Center Survey 2024."
)
