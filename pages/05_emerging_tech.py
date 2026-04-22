import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import get_tech_radar, get_adoption_timeline, get_strategic_recommendations
from utils.charts import gantt_timeline, _LAYOUT, PALETTE

st.set_page_config(page_title="NexCore | Emerging Tech", page_icon="🚀",
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
.quadrant-legend {
    display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px;
}
.q-pill {
    padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 600;
}
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
    <h2>🚀 Emerging Technologies (U4)</h2>
    <p>Technology radar · Adoption timeline 2024–2038 · Strategic roadmap for NexCore</p>
</div>
""", unsafe_allow_html=True)

radar_df = get_tech_radar()
timeline = get_adoption_timeline()
recs     = get_strategic_recommendations()

# ── Summary metrics ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("Technologies Tracked", "19", "Across 4 quadrants"),
    ("Ready to Adopt", "5", "High maturity + high value"),
    ("Active Pilots", "5", "Trial phase — 2025–2026"),
    ("R&D Horizon", "3", "Assess — 2026–2030"),
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

# ── Technology Radar ──────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Technology Radar — Maturity vs Strategic Value</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='quadrant-legend'>
    <span class='q-pill' style='background:rgba(16,185,129,0.15); color:#10B981;'>● Adopt</span>
    <span class='q-pill' style='background:rgba(59,130,246,0.15); color:#3B82F6;'>● Trial</span>
    <span class='q-pill' style='background:rgba(245,158,11,0.15); color:#F59E0B;'>● Assess</span>
    <span class='q-pill' style='background:rgba(107,114,128,0.15); color:#9CA3AF;'>● Hold</span>
    <span style='font-size:0.72rem; color:#6B7280; margin-left:8px;'>
        Bubble size = Market Adoption % · X = Maturity · Y = Strategic Value
    </span>
</div>
""", unsafe_allow_html=True)

quadrant_colors = {
    "Adopt":  "#10B981",
    "Trial":  "#3B82F6",
    "Assess": "#F59E0B",
    "Hold":   "#6B7280",
}

fig_radar = go.Figure()
for quadrant, color in quadrant_colors.items():
    sub = radar_df[radar_df["Quadrant"] == quadrant]
    fig_radar.add_trace(go.Scatter(
        x=sub["Maturity"],
        y=sub["Strategic Value"],
        mode="markers+text",
        name=quadrant,
        text=sub["Technology"],
        textposition="top center",
        textfont=dict(size=9, color="#E2E8F0"),
        marker=dict(
            size=sub["Market Adoption %"] / 2.5 + 10,
            color=color,
            opacity=0.8,
            line=dict(color="#0A0E1A", width=1),
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Maturity: %{x}/10<br>"
            "Strategic Value: %{y}/10<br>"
            "Market Adoption: " + sub["Market Adoption %"].astype(str) + " %"
            "<extra></extra>"
        ),
    ))

# Add quadrant dividers
for v in [5]:
    fig_radar.add_vline(x=v, line=dict(color="#374151", dash="dot", width=1))
    fig_radar.add_hline(y=v, line=dict(color="#374151", dash="dot", width=1))

# Quadrant labels
annotations = [
    dict(x=2.5, y=8.5, text="ASSESS", font=dict(color="#6B7280", size=10), showarrow=False),
    dict(x=7.5, y=8.5, text="ADOPT / TRIAL", font=dict(color="#6B7280", size=10), showarrow=False),
    dict(x=2.5, y=1.5, text="HOLD", font=dict(color="#6B7280", size=10), showarrow=False),
    dict(x=7.5, y=1.5, text="TRIAL / ADOPT", font=dict(color="#6B7280", size=10), showarrow=False),
]
fig_radar.update_layout(
    **_LAYOUT,
    title="NexCore Technology Radar — 2025",
    xaxis=dict(title="Technology Maturity (1–10)", range=[0, 11], color="#9CA3AF"),
    yaxis=dict(title="Strategic Value for DC Ops (1–10)", range=[0, 11], color="#9CA3AF"),
    height=520,
    annotations=annotations,
)
st.plotly_chart(fig_radar, use_container_width=True)

# Filter by quadrant
quad_filter = st.selectbox("Filter technologies by quadrant",
                           ["All", "Adopt", "Trial", "Assess", "Hold"])
view = radar_df if quad_filter == "All" else radar_df[radar_df["Quadrant"] == quad_filter]
st.dataframe(
    view[["Technology", "Quadrant", "Maturity", "Strategic Value", "Market Adoption %"]].sort_values(
        ["Quadrant", "Strategic Value"], ascending=[True, False]
    ),
    use_container_width=True, height=240,
)

# ── Adoption Timeline ─────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Technology Adoption Timeline — 2021–2038</div>",
            unsafe_allow_html=True)

st.plotly_chart(gantt_timeline(timeline), use_container_width=True)

# ── Strategic Recommendations ─────────────────────────────────────────────────
st.markdown("<div class='section-title'>NexCore Strategic Roadmap — Technology Initiatives</div>",
            unsafe_allow_html=True)

priority_colors = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#3B82F6"}

for _, row in recs.iterrows():
    color = priority_colors[row["Priority"]]
    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1F2937; border-left:3px solid {color};
                border-radius:6px; padding:14px 18px; margin-bottom:8px;
                display:flex; justify-content:space-between; align-items:flex-start; gap:16px;'>
        <div style='flex:1;'>
            <span style='color:{color}; font-size:0.65rem; font-weight:700; letter-spacing:0.1em;
                         text-transform:uppercase; background:rgba({
                             "239,68,68" if row["Priority"]=="High" else
                             ("245,158,11" if row["Priority"]=="Medium" else "59,130,246")
                         },0.15); padding:2px 7px; border-radius:3px;'>{row["Priority"]}</span>
            <div style='color:#E2E8F0; font-size:0.88rem; font-weight:500; margin-top:6px;'>{row["Initiative"]}</div>
        </div>
        <div style='text-align:right; white-space:nowrap; min-width:140px;'>
            <div style='color:#9CA3AF; font-size:0.72rem;'>{row["Horizon"]}</div>
            <div style='color:#F59E0B; font-size:0.78rem; font-weight:600;'>${row["CAPEX (USD M)"]}M CAPEX</div>
            <div style='color:#6B7280; font-size:0.72rem;'>{row["Impact"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption(
    "Technology radar methodology adapted from ThoughtWorks Technology Radar. "
    "Market adoption data: Gartner Hype Cycle for Data Center Infrastructure 2024 · "
    "IDC WW Data Center Trends 2025 · Uptime Institute GTR 2024."
)
