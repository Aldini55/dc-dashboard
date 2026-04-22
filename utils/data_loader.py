import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker("es_MX")
random.seed(42)
np.random.seed(42)

# ---------------------------------------------------------------------------
# OPERATIONS
# ---------------------------------------------------------------------------

def get_sla_metrics():
    return {
        "site_a": {
            "name": "Site A — CDMX Vallejo",
            "uptime_pct": 99.984,
            "target_sla": 99.982,
            "incidents_ytd": 3,
            "mttr_hours": 0.42,
            "power_uptime": 99.997,
            "capacity_mw": 8.0,
            "racks_total": 2100,
            "racks_occupied": 1834,
        },
        "site_b": {
            "name": "Site B — Querétaro",
            "uptime_pct": 99.991,
            "target_sla": 99.982,
            "incidents_ytd": 1,
            "mttr_hours": 0.18,
            "power_uptime": 99.999,
            "capacity_mw": 4.0,
            "racks_total": 1400,
            "racks_occupied": 1102,
        },
    }


def get_incident_log(n: int = 45):
    categories = ["Power", "Cooling", "Network", "Security", "Hardware", "Software"]
    severities = ["P1 — Critical", "P2 — High", "P3 — Medium", "P4 — Low"]
    sev_weights = [0.05, 0.15, 0.45, 0.35]
    sites = ["Site A (CDMX)", "Site B (QRO)"]
    statuses = ["Resolved", "Resolved", "Resolved", "In Progress", "Monitoring"]
    zones = ["A1", "A2", "A3", "B1", "B2", "C1"]

    rows = []
    for i in range(n):
        created = datetime.now() - timedelta(days=random.randint(1, 365))
        sev = random.choices(severities, sev_weights)[0]
        cat = random.choice(categories)
        if "P1" in sev:
            dur = round(random.uniform(0.5, 4.0), 1)
        elif "P2" in sev:
            dur = round(random.uniform(1.0, 8.0), 1)
        else:
            dur = round(random.uniform(2.0, 24.0), 1)
        rows.append({
            "Ticket": f"NX-{2024000 + i + 1}",
            "Date": created.strftime("%Y-%m-%d"),
            "Site": random.choice(sites),
            "Category": cat,
            "Severity": sev,
            "Description": f"{cat} anomaly in zone {random.choice(zones)}",
            "Duration (hrs)": dur,
            "Status": random.choice(statuses),
            "Technician": fake.name(),
        })
    return pd.DataFrame(rows).sort_values("Date", ascending=False).reset_index(drop=True)


def get_mac_processes():
    mac_types = ["Move", "Add", "Change"]
    categories = ["Server", "Network", "Power", "Storage", "Cabling"]
    statuses = ["Completed", "In Progress", "Scheduled", "Pending Approval"]
    clients = [
        "BBVA México", "Banorte", "PEMEX", "CFE Digital", "Netflix MX",
        "Amazon AWS", "Google Cloud", "GBM Grupo", "Grupo Modelo", "Cemex",
        "Televisa", "Megacable", "Izzi Telecom", "Clip", "Kueski",
    ]

    rows = []
    for i in range(28):
        created = datetime.now() - timedelta(days=random.randint(0, 90))
        rows.append({
            "ID": f"MAC-{1100 + i}",
            "Type": random.choice(mac_types),
            "Category": random.choice(categories),
            "Client": random.choice(clients),
            "Site": random.choice(["Site A", "Site B"]),
            "Zone": f"Zone {random.choice(['A1','A2','A3','B1','B2'])}",
            "Rack": f"R{random.randint(1, 99):02d}",
            "Status": random.choice(statuses),
            "Created": created.strftime("%Y-%m-%d"),
            "Due": (created + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows).sort_values("Created", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# ENERGY
# ---------------------------------------------------------------------------

def get_pue_history():
    months = pd.date_range("2024-01", periods=24, freq="MS")
    site_a, site_b = [], []
    for m in months:
        seasonal = 0.08 * np.sin(2 * np.pi * (m.month - 6) / 12)
        site_a.append(round(1.48 + seasonal + random.uniform(-0.02, 0.02), 3))
        site_b.append(round(1.41 + seasonal * 0.7 + random.uniform(-0.02, 0.02), 3))
    return pd.DataFrame({
        "Month": months,
        "Site A (CDMX)": site_a,
        "Site B (QRO)": site_b,
        "Mexico Average": [1.65] * 24,
        "Global Average": [1.58] * 24,
        "Hyperscale Avg": [1.18] * 24,
    })


def get_energy_consumption():
    months = pd.date_range("2024-01", periods=12, freq="MS")
    rows = []
    for m in months:
        s = 1 + 0.15 * np.sin(2 * np.pi * (m.month - 1) / 12)
        it_a = round(4.2 * s + random.uniform(-0.3, 0.3), 2)
        rows.append({
            "Month": m,
            "IT Load A (MW)": it_a,
            "Cooling A (MW)": round(it_a * 0.35, 2),
            "UPS/Other A (MW)": round(it_a * 0.05 + 0.15, 2),
            "IT Load B (MW)": round(2.1 * s + random.uniform(-0.2, 0.2), 2),
            "Cooling B (MW)": round(2.1 * s * 0.30, 2),
            "UPS/Other B (MW)": round(2.1 * s * 0.05 + 0.08, 2),
        })
    df = pd.DataFrame(rows)
    df["Total (MW)"] = df[[c for c in df.columns if c != "Month"]].sum(axis=1).round(2)
    return df


def get_renewable_mix():
    return {
        "Solar (on-site PV)": 18,
        "Wind (PPA — Oaxaca)": 24,
        "Hydro (CFE contract)": 8,
        "Grid clean energy": 12,
        "Grid conventional": 38,
    }


# ---------------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------------

def get_tia942_checklist():
    items = [
        ("Physical Security", "Perimeter security fence ≥3 m height", "Compliant", "Inspection 2025-11"),
        ("Physical Security", "Anti-ram bollards at all vehicle entry points", "Compliant", "Inspection 2025-11"),
        ("Physical Security", "CCTV 100% coverage — no blind spots", "Compliant", "Security audit 2025-10"),
        ("Physical Security", "Biometric + badge access at all entry points", "Compliant", "Access audit 2025-09"),
        ("Physical Security", "Mantrap / airlock at server hall entry", "Compliant", "Physical inspection 2025-11"),
        ("Physical Security", "24/7 on-site armed security personnel", "Compliant", "HR records 2025"),
        ("Physical Security", "Visitor escort and log policy enforced", "Compliant", "Policy v3.2"),
        ("Power", "2N UPS redundancy (A+B feeds per rack)", "Compliant", "Load test 2025-06"),
        ("Power", "Diesel generators — 72-hour fuel reserve", "Compliant", "Fuel audit 2025-11"),
        ("Power", "Automatic Transfer Switch (ATS) tested quarterly", "Compliant", "Test 2025-09"),
        ("Power", "Smart PDU monitoring per rack", "Compliant", "DCIM verified"),
        ("Power", "N+1 UPS modules per PDU bus", "Compliant", "Config audit 2025"),
        ("Cooling", "N+1 CRAH/CRAC units per hall", "Compliant", "Facility audit 2025-07"),
        ("Cooling", "Hot/cold aisle containment deployed", "Compliant", "Thermal survey 2025-05"),
        ("Cooling", "Temperature sensors — ≤3 m spacing", "Compliant", "DCIM verified"),
        ("Cooling", "Humidity maintained 40–60 % RH", "Compliant", "DCIM verified"),
        ("Cooling", "Secondary cooling loop (emergency)", "In Review", "Review Q1-2026"),
        ("Connectivity", "Diverse fiber entry — 4 carrier-neutral providers", "Compliant", "Network audit 2025-09"),
        ("Connectivity", "BGP multi-homing active", "Compliant", "Net config 2025-10"),
        ("Connectivity", "DDoS scrubbing (Cloudflare Magic Transit)", "Compliant", "Contract 2025"),
        ("Fire Suppression", "Inert gas suppression — FM-200 per zone", "Compliant", "Test 2025-04"),
        ("Fire Suppression", "VESDA early-warning smoke detection", "Compliant", "Inspection 2025-04"),
        ("Fire Suppression", "Annual fire drill completed", "Compliant", "Drill 2025-03"),
        ("Fire Suppression", "Suppression zone isolation valves", "Compliant", "Facility audit 2025"),
    ]
    return pd.DataFrame(items, columns=["Domain", "Control", "Status", "Evidence"])


def get_iso27001_domains():
    data = [
        ("Information Security Policies", 2, 2),
        ("Organization of IS", 7, 7),
        ("Human Resource Security", 6, 5),
        ("Asset Management", 10, 9),
        ("Access Control", 14, 14),
        ("Cryptography", 2, 2),
        ("Physical & Environmental Security", 15, 15),
        ("Operations Security", 14, 13),
        ("Communications Security", 7, 7),
        ("System Acquisition & Development", 13, 10),
        ("Supplier Relationships", 5, 4),
        ("IS Incident Management", 7, 7),
        ("Business Continuity", 4, 4),
        ("Compliance", 8, 7),
    ]
    df = pd.DataFrame(data, columns=["Domain", "Controls_Total", "Controls_Implemented"])
    df["Score %"] = (df["Controls_Implemented"] / df["Controls_Total"] * 100).round(0).astype(int)
    return df


# ---------------------------------------------------------------------------
# MARKET
# ---------------------------------------------------------------------------

def get_mexico_market_size():
    years = list(range(2019, 2029))
    sizes = [1.4, 1.6, 1.85, 2.1, 2.45, 2.80, 3.22, 3.73, 4.32, 5.01]
    types = ["Historical"] * 6 + ["Projected"] * 4
    return pd.DataFrame({"Year": years, "Market Size (USD B)": sizes, "Type": types})


def get_market_share():
    return pd.DataFrame({
        "Provider": ["KIO Networks", "Telmex/Triara", "MCM Telecom", "Ascenty", "Iron Mountain", "Equinix", "Others"],
        "Market Share %": [23, 18, 14, 11, 9, 7, 18],
        "Capacity (MW)": [82, 65, 48, 38, 31, 24, 62],
        "Type": ["Local", "Local", "Local", "International", "International", "International", "Mixed"],
    })


def get_regional_data():
    return pd.DataFrame({
        "City": ["Mexico City", "Querétaro", "Guadalajara", "Monterrey", "Tijuana", "Mérida", "León"],
        "State": ["CDMX", "Querétaro", "Jalisco", "Nuevo León", "Baja California", "Yucatán", "Guanajuato"],
        "Lat": [19.4326, 20.5888, 20.6597, 25.6866, 32.5027, 20.9674, 21.1221],
        "Lon": [-99.1332, -100.3899, -103.3496, -100.3161, -117.0037, -89.5926, -101.6820],
        "Installed MW": [270, 68, 42, 38, 18, 6, 8],
        "Active DCs": [18, 5, 4, 4, 2, 1, 1],
        "Growth YoY %": [14, 28, 18, 22, 35, 45, 20],
        "Key Driver": [
            "Finance, cloud anchors",
            "Nearshoring, connectivity",
            "Tech ecosystem (Silicon Valley MX)",
            "Industrial nearshoring",
            "US proximity, manufacturing",
            "Tourism & regional growth",
            "Industrial corridor",
        ],
    })


def get_deployment_models():
    return pd.DataFrame({
        "Model": ["Colocation", "Hyperscale", "Edge", "Managed Services", "Hybrid Cloud"],
        "Market Share %": [38, 29, 15, 11, 7],
        "Avg Deal (USD M)": [0.8, 45.0, 0.15, 2.5, 5.2],
        "Growth YoY %": [12, 28, 42, 18, 35],
        "Key Clients": ["Enterprise / SME", "AWS · GCP · Azure", "Telcos · Retail", "Gov · Financial", "Large Enterprise"],
    })


def get_investment_trends():
    quarters = ["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25", "Q3-25", "Q4-25"]
    return pd.DataFrame({
        "Quarter": quarters,
        "FDI (USD M)": [320, 410, 380, 520, 460, 580, 620, 710],
        "Domestic (USD M)": [180, 210, 195, 260, 230, 285, 310, 350],
        "New Capacity (MW)": [12, 18, 15, 22, 19, 24, 28, 32],
    })


def get_provider_comparison():
    return pd.DataFrame({
        "Provider": ["KIO Networks", "Telmex/Triara", "MCM Telecom", "Ascenty", "Iron Mountain", "Equinix"],
        "Uptime SLA %": [99.999, 99.99, 99.98, 99.999, 99.99, 99.9999],
        "Tier": [4, 3, 3, 4, 3, 4],
        "Price Index": [7, 6, 5, 8, 7, 9],
        "Sustainability Score": [7, 5, 5, 8, 6, 9],
        "Compliance Score": [9, 8, 7, 9, 9, 10],
        "Connectivity Score": [9, 9, 8, 7, 7, 10],
        "Support Score": [8, 7, 7, 8, 8, 9],
    })


# ---------------------------------------------------------------------------
# EMERGING TECH
# ---------------------------------------------------------------------------

def get_tech_radar():
    return pd.DataFrame({
        "Technology": [
            "AI/ML Workload Optimization", "Green Energy Integration",
            "Liquid Cooling (Direct-to-Chip)", "Software-Defined DC", "Zero Trust Network Access",
            "Immersion Cooling", "Edge Computing Infrastructure",
            "Kubernetes Orchestration", "Digital Twin (DC)", "AI-Driven Predictive Maintenance",
            "Quantum-Safe Cryptography", "Neuromorphic Computing",
            "Hydrogen Fuel Cells", "Optical Networking (800G)", "Automated Provisioning",
            "Legacy MPLS Networks", "Air-Only Cooling", "On-Prem-Only Storage", "Manual Capacity Planning",
        ],
        "Quadrant": [
            "Adopt", "Adopt", "Adopt", "Adopt", "Adopt",
            "Trial", "Trial", "Trial", "Trial", "Trial",
            "Assess", "Assess", "Assess", "Assess", "Assess",
            "Hold", "Hold", "Hold", "Hold",
        ],
        "Maturity": [9, 8, 7, 8, 9, 5, 6, 7, 4, 6, 3, 2, 3, 5, 6, 8, 7, 8, 9],
        "Strategic Value": [9, 9, 8, 8, 9, 8, 7, 8, 7, 8, 9, 8, 7, 7, 7, 2, 2, 1, 1],
        "Market Adoption %": [65, 72, 38, 55, 71, 18, 42, 48, 22, 35, 8, 3, 5, 15, 45, 45, 38, 42, 28],
    })


def get_adoption_timeline():
    configs = [
        ("AI/ML Optimization",     2022, 2024, 2026, 2028),
        ("Liquid Cooling",         2023, 2025, 2027, 2029),
        ("Edge Computing",         2021, 2023, 2026, 2028),
        ("Digital Twin",           2024, 2026, 2028, 2030),
        ("Immersion Cooling",      2024, 2026, 2029, 2031),
        ("Quantum-Safe Crypto",    2025, 2027, 2030, 2033),
        ("Hydrogen Fuel Cells",    2026, 2028, 2031, 2035),
        ("Neuromorphic Computing", 2027, 2030, 2033, 2038),
    ]
    phases = ["Research", "Pilot", "Scale", "Mainstream"]
    rows = []
    for tech, y1, y2, y3, y4 in configs:
        years = [y1, y2, y3, y4]
        next_years = [y2, y3, y4, y4 + 3]
        for i, phase in enumerate(phases):
            rows.append({
                "Technology": tech,
                "Phase": phase,
                "Start": years[i],
                "End": next_years[i],
            })
    return pd.DataFrame(rows)


def get_strategic_recommendations():
    return pd.DataFrame({
        "Priority": ["High", "High", "High", "Medium", "Medium", "Low"],
        "Initiative": [
            "Deploy direct-to-chip liquid cooling in high-density GPU zones",
            "Achieve 80% renewable energy mix by 2027 (add 6 MW solar PPA)",
            "Implement AI-driven DCIM for predictive maintenance",
            "Pilot digital twin for Site B capacity planning",
            "Obtain ISO 50001 (Energy Management) certification",
            "Evaluate neuromorphic accelerators for edge inference",
        ],
        "Horizon": ["2025–2026", "2025–2027", "2026", "2026", "2026–2027", "2027–2028"],
        "Impact": ["Cost + Perf", "ESG + Cost", "OPEX", "Capacity", "Compliance", "Perf"],
        "CAPEX (USD M)": [4.2, 8.5, 1.8, 0.6, 0.3, 0.9],
    })
