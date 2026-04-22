import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Shared Plotly dark layout
_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,24,39,0.85)",
    font=dict(color="#E2E8F0", family="sans-serif", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
)

PALETTE = ["#10B981", "#F59E0B", "#3B82F6", "#8B5CF6", "#EF4444", "#EC4899", "#14B8A6"]
EMERALD = "#10B981"
AMBER   = "#F59E0B"
RED     = "#EF4444"


def gauge(value: float, target: float, title: str, suffix: str = "%",
          low: float = 95.0, high: float = 99.9) -> go.Figure:
    color = EMERALD if value >= target else (AMBER if value >= low else RED)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={"reference": target, "valueformat": ".3f"},
        number={"suffix": suffix, "valueformat": ".3f"},
        title={"text": title, "font": {"color": "#E2E8F0", "size": 13}},
        gauge={
            "axis": {"range": [low, 100], "tickcolor": "#6B7280"},
            "bar": {"color": color},
            "bgcolor": "#1F2937",
            "borderwidth": 0,
            "steps": [
                {"range": [low, high],  "color": "#1F2937"},
                {"range": [high, 100],  "color": "rgba(16,185,129,0.15)"},
            ],
            "threshold": {
                "line": {"color": AMBER, "width": 2},
                "thickness": 0.75,
                "value": target,
            },
        },
    ))
    fig.update_layout(**_LAYOUT, height=220)
    return fig


def line_chart(df: pd.DataFrame, x: str, y_cols: list[str], title: str,
               colors: list[str] | None = None, y_label: str = "") -> go.Figure:
    colors = colors or PALETTE
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col], name=col,
            line=dict(color=colors[i % len(colors)], width=2),
            mode="lines+markers", marker=dict(size=4),
        ))
    fig.update_layout(**_LAYOUT, title=title,
                      xaxis_title=x, yaxis_title=y_label)
    return fig


def stacked_bar(df: pd.DataFrame, x: str, y_cols: list[str], title: str,
                colors: list[str] | None = None, y_label: str = "") -> go.Figure:
    colors = colors or PALETTE
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Bar(
            x=df[x], y=df[col], name=col,
            marker_color=colors[i % len(colors)],
        ))
    fig.update_layout(**_LAYOUT, title=title, barmode="stack",
                      xaxis_title=x, yaxis_title=y_label,
                      xaxis=dict(tickangle=-30))
    return fig


def donut(labels: list, values: list, title: str,
          colors: list[str] | None = None) -> go.Figure:
    colors = colors or PALETTE
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#0A0E1A", width=2)),
        textfont=dict(color="#E2E8F0"),
    ))
    fig.update_layout(**_LAYOUT, title=title,
                      showlegend=True, height=320)
    return fig


def horizontal_bar(df: pd.DataFrame, x: str, y: str, title: str,
                   color: str = EMERALD) -> go.Figure:
    df_s = df.sort_values(x)
    fig = go.Figure(go.Bar(
        x=df_s[x], y=df_s[y], orientation="h",
        marker=dict(color=color),
        text=df_s[x].astype(str), textposition="auto",
    ))
    fig.update_layout(**_LAYOUT, title=title, height=max(300, len(df) * 32))
    return fig


def scatter_bubble(df: pd.DataFrame, x: str, y: str, size: str, color: str,
                   hover: str, title: str) -> go.Figure:
    fig = px.scatter(
        df, x=x, y=y, size=size, color=color, hover_name=hover,
        color_discrete_sequence=PALETTE,
        size_max=40,
        title=title,
    )
    fig.update_layout(**_LAYOUT)
    return fig


def radar_chart(categories: list, values_list: list, names: list) -> go.Figure:
    fig = go.Figure()
    colors = PALETTE
    for i, (vals, name) in enumerate(zip(values_list, names)):
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories + [categories[0]],
            name=name,
            line=dict(color=colors[i % len(colors)], width=2),
            fill="toself",
            fillcolor=colors[i % len(colors)].replace(")", ",0.15)").replace("rgb", "rgba")
                if "rgb" in colors[i % len(colors)] else colors[i % len(colors)] + "26",
        ))
    fig.update_layout(
        **_LAYOUT,
        polar=dict(
            bgcolor="rgba(17,24,39,0.85)",
            radialaxis=dict(visible=True, range=[0, 10], color="#6B7280"),
            angularaxis=dict(color="#9CA3AF"),
        ),
        height=380,
    )
    return fig


def map_mexico(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Scattergeo(
        lat=df["Lat"],
        lon=df["Lon"],
        text=df.apply(
            lambda r: f"<b>{r['City']}</b><br>{r['Installed MW']} MW<br>"
                      f"{r['Active DCs']} DCs<br>YoY Growth: +{r['Growth YoY %']}%",
            axis=1,
        ),
        mode="markers+text",
        textposition="top center",
        textfont=dict(color="#E2E8F0", size=10),
        marker=dict(
            size=df["Installed MW"] / 8,
            color=df["Growth YoY %"],
            colorscale=[[0, "#3B82F6"], [0.5, "#10B981"], [1, "#F59E0B"]],
            showscale=True,
            colorbar=dict(title="YoY Growth %", tickfont=dict(color="#E2E8F0")),
            line=dict(color="#0A0E1A", width=1),
        ),
        hoverinfo="text",
    ))
    fig.update_geos(
        visible=True,
        resolution=50,
        scope="north america",
        lataxis_range=[14, 34],
        lonaxis_range=[-118, -86],
        bgcolor="rgba(10,14,26,0)",
        landcolor="#1F2937",
        oceancolor="rgba(10,14,26,0.8)",
        lakecolor="rgba(59,130,246,0.3)",
        countrycolor="#374151",
        showocean=True,
        showlakes=True,
    )
    fig.update_layout(**_LAYOUT, title="Mexico DC Regional Hotspots — Installed Capacity & Growth",
                      height=460, geo=dict(showframe=False))
    return fig


def gantt_timeline(df: pd.DataFrame) -> go.Figure:
    phase_colors = {
        "Research":   "#3B82F6",
        "Pilot":      "#F59E0B",
        "Scale":      "#10B981",
        "Mainstream": "#8B5CF6",
    }
    techs = df["Technology"].unique().tolist()
    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["End"] - row["Start"]],
            y=[row["Technology"]],
            base=[row["Start"]],
            orientation="h",
            marker=dict(color=phase_colors[row["Phase"]], line=dict(width=0)),
            name=row["Phase"],
            legendgroup=row["Phase"],
            showlegend=row["Technology"] == techs[0],
            hovertemplate=f"<b>{row['Technology']}</b><br>{row['Phase']}: {row['Start']}–{row['End']}<extra></extra>",
        ))
    fig.update_layout(
        **_LAYOUT,
        title="Technology Adoption Timeline — NexCore Strategic Roadmap",
        xaxis=dict(title="Year", range=[2021, 2040], color="#9CA3AF"),
        yaxis=dict(autorange="reversed", color="#9CA3AF"),
        barmode="overlay",
        height=400,
        legend=dict(title="Phase"),
    )
    return fig
