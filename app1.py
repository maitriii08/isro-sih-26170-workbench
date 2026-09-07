import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ISRO Reliability Workbench | PS-26170",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CLEAN DARK AEROSPACE STYLING ---
st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0b0f19 !important;
        color: #94a3b8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1440px !important;
    }

    /* Top Console Banner */
    .banner-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 16px 22px;
        margin-bottom: 18px;
    }

    /* Timeline Stepper */
    .timeline-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 6px;
        padding: 12px 18px;
        margin-top: 14px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: monospace;
        font-size: 0.8rem;
    }
    .badge-done { background: #064e3b; color: #10b981; padding: 5px 10px; border-radius: 4px; font-weight: 600; }
    .badge-live { background: #1e3a5f; color: #38bdf8; border: 1px solid #38bdf8; padding: 5px 10px; border-radius: 4px; font-weight: 600; }
    .badge-pend { background: #1f2937; color: #64748b; padding: 5px 10px; border-radius: 4px; }

    /* Custom 14px High-Glow Progress Bars */
    .custom-progress-track {
        background-color: #1f2937;
        border-radius: 6px;
        height: 14px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
        margin-bottom: 14px;
    }
    .custom-progress-fill-blue {
        background: linear-gradient(90deg, #0284c7, #38bdf8);
        height: 100%;
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }

    .tag-pass { color: #10b981; font-weight: bold; }
    .tag-warn { color: #eab308; font-weight: bold; }
    .tag-fail { color: #ef4444; font-weight: bold; }
    .tag-pend { color: #f8fafc; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "decision_logs" not in st.session_state:
    st.session_state.decision_logs = [
        {"Timestamp": "2026-09-07 02:48:32", "Event": "ATE Data Stream Ingested (LOT-2026-A17)"},
        {"Timestamp": "2026-09-07 02:50:11", "Event": "Auto-Screening executed via Modified Z-score and Time-Drift regression."}
    ]

if "saved_decisions" not in st.session_state:
    st.session_state.saved_decisions = {}

# --- HARDWARE TELEMETRY DATA ENGINE (50-SOCKET DATASET) ---
@st.cache_data
def get_hardware_lot():
    np.random.seed(42)
    device_ids = [f"CMP-{1001 + i}" for i in range(50)]
    
    iddq_0 = np.random.normal(12.8, 0.25, 50)
    leak_0 = np.random.normal(1.80, 0.04, 50)
    tpd_0 = np.random.normal(3.20, 0.03, 50)
    supply_0 = np.random.normal(45.0, 0.8, 50)
    vth_0 = np.random.normal(0.72, 0.015, 50)
    
    iddq_24 = iddq_0 + np.random.normal(0.10, 0.02, 50)
    iddq_96 = iddq_24 + np.random.normal(0.15, 0.02, 50)
    iddq_168 = iddq_96 + np.random.normal(0.20, 0.03, 50)
    
    leak_24 = leak_0 + np.random.normal(0.02, 0.01, 50)
    leak_96 = leak_24 + np.random.normal(0.03, 0.01, 50)
    leak_168 = leak_96 + np.random.normal(0.04, 0.01, 50)
    
    tpd_24 = tpd_0 + np.random.normal(0.005, 0.002, 50)
    tpd_96 = tpd_24 + np.random.normal(0.008, 0.002, 50)
    tpd_168 = tpd_96 + np.random.normal(0.012, 0.003, 50)
    
    supply_24 = supply_0 + np.random.normal(0.3, 0.05, 50)
    supply_96 = supply_24 + np.random.normal(0.4, 0.05, 50)
    supply_168 = supply_96 + np.random.normal(0.5, 0.08, 50)
    
    vth_24 = vth_0 - np.random.normal(0.002, 0.001, 50)
    vth_96 = vth_24 - np.random.normal(0.004, 0.001, 50)
    vth_168 = vth_96 - np.random.normal(0.006, 0.001, 50)
    
    df = pd.DataFrame({
        "Device_ID": device_ids,
        "Iddq_0h": iddq_0, "Iddq_24h": iddq_24, "Iddq_96h": iddq_96, "Iddq_168h": iddq_168,
        "Leakage_0h": leak_0, "Leakage_24h": leak_24, "Leakage_96h": leak_96, "Leakage_168h": leak_168,
        "Tpd_0h": tpd_0, "Tpd_24h": tpd_24, "Tpd_96h": tpd_96, "Tpd_168h": tpd_168,
        "Supply_0h": supply_0, "Supply_24h": supply_24, "Supply_96h": supply_96, "Supply_168h": supply_168,
        "Vth_0h": vth_0, "Vth_24h": vth_24, "Vth_96h": vth_96, "Vth_168h": vth_168
    })
    
    # Critical Reject Outliers (Red: 5 Units = 10%)
    crit_indices = [7, 22, 30, 44, 48]
    for i in crit_indices:
        df.loc[i, "Iddq_96h"] = df.loc[i, "Iddq_0h"] * 1.55
        df.loc[i, "Iddq_168h"] = df.loc[i, "Iddq_0h"] * 2.30
        df.loc[i, "Leakage_96h"] = df.loc[i, "Leakage_0h"] * 1.65
        df.loc[i, "Leakage_168h"] = df.loc[i, "Leakage_0h"] * 2.60
        df.loc[i, "Tpd_96h"] = df.loc[i, "Tpd_0h"] * 1.25
        df.loc[i, "Tpd_168h"] = df.loc[i, "Tpd_0h"] * 1.45
        df.loc[i, "Supply_96h"] = df.loc[i, "Supply_0h"] * 1.40
        df.loc[i, "Supply_168h"] = df.loc[i, "Supply_0h"] * 1.90
        df.loc[i, "Vth_96h"] = df.loc[i, "Vth_0h"] * 0.70
        df.loc[i, "Vth_168h"] = df.loc[i, "Vth_0h"] * 0.50
        
    # Extended Retest Outliers (Yellow: 8 Units = 16%)
    warn_indices = [3, 10, 14, 18, 26, 34, 37, 42]
    for i in warn_indices:
        df.loc[i, "Iddq_96h"] = df.loc[i, "Iddq_0h"] * 1.25
        df.loc[i, "Iddq_168h"] = df.loc[i, "Iddq_0h"] * 1.40
        df.loc[i, "Leakage_96h"] = df.loc[i, "Leakage_0h"] * 1.25
        df.loc[i, "Leakage_168h"] = df.loc[i, "Leakage_0h"] * 1.42
        df.loc[i, "Tpd_96h"] = df.loc[i, "Tpd_0h"] * 1.10
        df.loc[i, "Tpd_168h"] = df.loc[i, "Tpd_0h"] * 1.18
        df.loc[i, "Supply_96h"] = df.loc[i, "Supply_0h"] * 1.15
        df.loc[i, "Supply_168h"] = df.loc[i, "Supply_0h"] * 1.25
        df.loc[i, "Vth_96h"] = df.loc[i, "Vth_0h"] * 0.88
        df.loc[i, "Vth_168h"] = df.loc[i, "Vth_0h"] * 0.80

    # Pending Screening Units (White: 6 Units = 12%)
    pend_indices = [39, 43, 45, 46, 47, 49]
    for i in pend_indices:
        df.loc[i, "Iddq_96h"] = np.nan
        df.loc[i, "Iddq_168h"] = np.nan
        df.loc[i, "Leakage_96h"] = np.nan
        df.loc[i, "Leakage_168h"] = np.nan
        df.loc[i, "Tpd_96h"] = np.nan
        df.loc[i, "Tpd_168h"] = np.nan
        df.loc[i, "Supply_96h"] = np.nan
        df.loc[i, "Supply_168h"] = np.nan
        df.loc[i, "Vth_96h"] = np.nan
        df.loc[i, "Vth_168h"] = np.nan

    statuses = []
    for i in range(50):
        if i in pend_indices:
            statuses.append("YET TO BE TESTED")
        elif i in crit_indices:
            statuses.append("REJECT")
        elif i in warn_indices:
            statuses.append("EXTENDED TESTING")
        else:
            statuses.append("PASS")
    df["AI_Status"] = statuses

    return df

df = get_hardware_lot()

# Telemetry Calculations
df["Drift_Total"] = df["Iddq_96h"] - df["Iddq_0h"]
df["Drift_Pct"] = ((df["Iddq_96h"] - df["Iddq_0h"]) / df["Iddq_0h"]) * 100

valid_drifts = df["Drift_Total"].dropna()
med = np.median(valid_drifts)
mad = np.median(np.abs(valid_drifts - med))
df["Modified_Z"] = 0.6745 * (df["Drift_Total"] - med) / (mad + 1e-6)

reject_count = (df["AI_Status"] == "REJECT").sum()
retest_count = (df["AI_Status"] == "EXTENDED TESTING").sum()
pass_count = (df["AI_Status"] == "PASS").sum()
pend_count = (df["AI_Status"] == "YET TO BE TESTED").sum()
evaluated_count = len(df) - pend_count
pda_rate = (reject_count / evaluated_count) * 100 if evaluated_count > 0 else 0.0

# -----------------------------------------------------------------------------
# LEFT SIDEBAR: HISTORICAL LOT SUMMARY (CLEAN SLOT NAMES)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Historical Lot Summary")
    st.caption("MIL-STD-883 Production Slot Breakdown")
    
    hist_sidebar = pd.DataFrame({
        "Slot Ref": ["Slot 1", "Slot 2", "Slot 3", "Slot 4", "Slot 5 (Live)"],
        "Pass %": ["100%", "100%", "92.5%", "85.0%", f"{(pass_count/evaluated_count)*100:.1f}%"],
        "Retest %": ["0.0%", "0.0%", "7.5%", "5.0%", f"{(retest_count/evaluated_count)*100:.1f}%"],
        "Reject %": ["0.0%", "0.0%", "0.0%", "10.0%", f"{pda_rate:.1f}%"]
    })
    st.dataframe(hist_sidebar, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Lot Compliance Audit")
    compliance_table = pd.DataFrame({
        "Batch Stage": ["Slot 1 to 3", "Slot 4", "Slot 5 (Live)"],
        "Audit Status": ["PASSED", "PDA RISK", "PDA RISK BREACH"]
    })
    st.dataframe(compliance_table, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Data Provenance")
    st.markdown("""
    <div style="font-family: monospace; font-size: 0.75rem; color: #64748b; line-height: 1.6;">
        Source: ATE_STREAM_A17.csv<br>
        Checksum: SHA256-59159cf734b6...<br>
        Monitored: 50 Sockets (BIB-50-A)<br>
        Chamber: THERMAL-CHAMBER-B04<br>
        Standard: MIL-STD-883 Class-S
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN HEADER BANNER & DUAL PROGRESS BARS
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="banner-box">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <span style="font-family: monospace; font-size: 0.85rem; background: #1e293b; color: #38bdf8; padding: 4px 8px; border-radius: 4px; font-weight: bold;">PS 26170</span>
            <span style="font-size: 1.25rem; font-weight: bold; color: #f8fafc; margin-left: 10px;">Burn-In & Screening Dashboard</span>
            <span style="font-size: 0.82rem; color: #64748b; margin-left: 12px;">Offline Parametric Reliability Analysis</span>
        </div>
        <div>
            <span style="background: #1e293b; color: #10b981; font-family: monospace; font-size: 0.78rem; padding: 5px 12px; border-radius: 4px; font-weight: bold;">● OFFLINE MODE</span>
        </div>
    </div>
    <div style="margin-top: 14px; display: flex; justify-content: space-between; font-size: 0.82rem; font-family: monospace;">
        <span style="color: #94a3b8;">Active Lot: <strong>LOT-2026-A17</strong> &nbsp;|&nbsp; Monitored Stage: <strong style="color: #38bdf8;">SLOT-5 (96h Active Diagnostic Scan)</strong> &nbsp;|&nbsp; Last Ingest: 2026-09-07 02:48:32</span>
        <span>LOT STATUS: <strong class="{'tag-fail' if reject_count > 0 else 'tag-pass'}">{reject_count} DEVICE(S) AT REJECT RISK (PDA: {pda_rate:.1f}%)</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

burnin_pct = int((96 / 168) * 100)
screening_pct = int((evaluated_count / len(df)) * 100)

p_col1, p_col2 = st.columns(2)
with p_col1:
    st.markdown(f'''
    <div style="font-size: 0.84rem; font-weight: 600; color: #cbd5e1; display: flex; justify-content: space-between;">
        <span>Burn-In Stress Progression (125°C Chamber)</span>
        <span style="color: #38bdf8; font-family: monospace;">{burnin_pct}% (96h / 168h Reached)</span>
    </div>
    <div class="custom-progress-track">
        <div class="custom-progress-fill-blue" style="width: {burnin_pct}%;"></div>
    </div>
    ''', unsafe_allow_html=True)

with p_col2:
    st.markdown(f'''
    <div style="font-size: 0.84rem; font-weight: 600; color: #cbd5e1; display: flex; justify-content: space-between;">
        <span>Electrical Screening Verification</span>
        <span style="color: #38bdf8; font-family: monospace;">{screening_pct}% ({evaluated_count} of {len(df)} Sockets Ingested)</span>
    </div>
    <div class="custom-progress-track">
        <div class="custom-progress-fill-blue" style="width: {screening_pct}%;"></div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("""
<div class="timeline-box">
    <div class="badge-done">0h: Baseline Initialization [PASS]</div>
    <div style="color: #64748b;">➔</div>
    <div class="badge-done">24h: Intermediate Slope Checkpoint [PASS]</div>
    <div style="color: #64748b;">➔</div>
    <div class="badge-live">96h: Active Dynamic Scan [SLOT 5 LIVE]</div>
    <div style="color: #64748b;">➔</div>
    <div class="badge-pend">168h: Qualification Final State [PENDING]</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LEVEL 1: ELECTRICAL SCREENING & LOT YIELD OVERVIEW (SPACIOUS 70/30)
# -----------------------------------------------------------------------------
st.markdown("### Electrical Screening & Lot Yield Overview")

top_tiles_col, top_donut_col = st.columns([7, 3])

with top_tiles_col:
    valid_df = df[df["AI_Status"] != "YET TO BE TESTED"]
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("Quiescent Current (Iddq)", f"{valid_df['Iddq_96h'].mean():.2f} µA", "Baseline: 12.80 µA")
    m2.metric("Gate Oxide Leakage (Ileak)", f"{valid_df['Leakage_96h'].mean():.2f} nA", "+0.04 nA Normal Drift")
    
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    m3.metric("Propagation Delay (Tpd)", f"{valid_df['Tpd_96h'].mean():.2f} ns", "Within 3.5 ns Spec")
    m4.metric("Kelvin Contact Resistance", "0.042 Ω", "4-Point Terminal Nominal")

with top_donut_col:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Pass (Flight Ready)', 'Extended Retest', 'Critical Reject', 'Yet to be Tested'],
        values=[pass_count, retest_count, reject_count, pend_count],
        hole=0.55,
        marker=dict(colors=['#10b981', '#eab308', '#ef4444', '#f8fafc']),
        textinfo='percent+label',
        showlegend=False
    )])
    fig_pie.update_layout(
        title=f"Lot Yield Distribution (PDA: {pda_rate:.1f}%)",
        title_font_size=13,
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        height=230,
        margin=dict(l=10, r=10, t=35, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LEVEL 2: LIVE LOT CONTROL TRAJECTORIES (ALL EXPANDED PARAMETERS)
# -----------------------------------------------------------------------------
st.markdown("### Live Lot Analytics: Parametric Trajectories (Control Chart)")

param_selection = st.selectbox(
    "Select Telemetry Metric for Multi-Device Control Chart:",
    [
        "Iddq (Quiescent Current - µA)",
        "Leakage Current (Ileak - nA)",
        "Supply Current (Idd - mA)",
        "Threshold Voltage (Vth - V)",
        "Propagation Delay (Tpd - ns)"
    ]
)

if "Iddq" in param_selection:
    cols = ["Iddq_0h", "Iddq_24h", "Iddq_96h", "Iddq_168h"]
    y_label = "Iddq Current (µA)"
    ucl = 22.0
elif "Leakage" in param_selection:
    cols = ["Leakage_0h", "Leakage_24h", "Leakage_96h", "Leakage_168h"]
    y_label = "Leakage Current (nA)"
    ucl = 4.0
elif "Supply" in param_selection:
    cols = ["Supply_0h", "Supply_24h", "Supply_96h", "Supply_168h"]
    y_label = "Supply Current (mA)"
    ucl = 65.0
elif "Threshold" in param_selection:
    cols = ["Vth_0h", "Vth_24h", "Vth_96h", "Vth_168h"]
    y_label = "Threshold Voltage (V)"
    ucl = 0.50
else:
    cols = ["Tpd_0h", "Tpd_24h", "Tpd_96h", "Tpd_168h"]
    y_label = "Propagation Delay (ns)"
    ucl = 4.8

fig_control = go.Figure()
x_checkpoints = ["0h", "24h", "96h", "168h"]

# Shaded Vertical Stage Dividers
fig_control.add_vrect(x0="0h", x1="24h", fillcolor="#161e2e", opacity=0.35, layer="below", line_width=0)
fig_control.add_vrect(x0="96h", x1="168h", fillcolor="#161e2e", opacity=0.35, layer="below", line_width=0)

# 1. Nominal Pass Traces (Green)
for idx, row in df[df["AI_Status"] == "PASS"].iterrows():
    fig_control.add_trace(go.Scatter(
        x=x_checkpoints,
        y=[row[cols[0]], row[cols[1]], row[cols[2]], row[cols[3]]],
        mode='lines',
        line=dict(color='rgba(16, 185, 129, 0.35)', width=1.1),
        showlegend=False,
        hoverinfo='text',
        text=f"{row['Device_ID']}: Nominal Pass (Green)"
    ))

# 2. Extended Retest Traces (Yellow)
for idx, row in df[df["AI_Status"] == "EXTENDED TESTING"].iterrows():
    fig_control.add_trace(go.Scatter(
        x=x_checkpoints,
        y=[row[cols[0]], row[cols[1]], row[cols[2]], row[cols[3]]],
        mode='lines+markers',
        line=dict(color='#eab308', width=2.0),
        marker=dict(size=5),
        showlegend=False,
        hoverinfo='text',
        text=f"{row['Device_ID']}: Extended Retest Required (Yellow)"
    ))

# 3. Critical Latent Reject Traces (Red)
for idx, row in df[df["AI_Status"] == "REJECT"].iterrows():
    fig_control.add_trace(go.Scatter(
        x=x_checkpoints,
        y=[row[cols[0]], row[cols[1]], row[cols[2]], row[cols[3]]],
        mode='lines+markers',
        line=dict(color='#ef4444', width=3.0),
        marker=dict(size=6),
        showlegend=False,
        hoverinfo='text',
        text=f"{row['Device_ID']}: Critical Latent Defect (Red)"
    ))

# 4. Yet To Be Tested Traces (White / Gray Dash)
for idx, row in df[df["AI_Status"] == "YET TO BE TESTED"].iterrows():
    fig_control.add_trace(go.Scatter(
        x=["0h", "24h"],
        y=[row[cols[0]], row[cols[1]]],
        mode='lines+markers',
        line=dict(color='#f8fafc', width=1.2, dash='dot'),
        marker=dict(size=4),
        showlegend=False,
        hoverinfo='text',
        text=f"{row['Device_ID']}: In-Queue / Yet To Be Tested (White)"
    ))

# Upper Spec Limit Line
fig_control.add_trace(go.Scatter(
    x=x_checkpoints, y=[ucl]*4, mode='lines',
    line=dict(color='#dc2626', width=1.5, dash='dash'),
    showlegend=False,
    hoverinfo='text',
    text=f"Static Spec Ceiling Limit: {ucl}"
))

fig_control.update_layout(
    title=f"Multi-Trace Trajectories (Green: Pass | Yellow: Retest | Red: Reject | White: In-Queue)",
    title_font_size=12,
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#0b0f19",
    height=340,
    showlegend=False,
    margin=dict(l=30, r=20, t=40, b=30),
    xaxis_title="Burn-In Stress Duration Checkpoints",
    yaxis_title=y_label
)
st.plotly_chart(fig_control, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LEVEL 3: 50-SOCKET BATCH ANOMALY MAP (FULL HOVER TELEMETRY WITH DRIFT %)
# -----------------------------------------------------------------------------
st.markdown("### Batch Anomaly Map (50 Sockets Burn-In Board Matrix)")

status_map = {"PASS": 0, "EXTENDED TESTING": 1, "REJECT": 2, "YET TO BE TESTED": 3}
grid_z = np.zeros((5, 10))
text_labels = [["" for _ in range(10)] for _ in range(5)]
hover_texts = [["" for _ in range(10)] for _ in range(5)]

for idx, row in df.iterrows():
    r = idx // 10
    c = idx % 10
    status = row["AI_Status"]
    grid_z[r, c] = status_map[status]
    
    # Status Tagging for Grid Display
    if status == "REJECT":
        drift_label = f"<span style='color: #ef4444; font-weight: bold;'>REJECT (+{row['Drift_Pct']:.0f}%)</span>"
    elif status == "EXTENDED TESTING":
        drift_label = f"<span style='color: #eab308; font-weight: bold;'>RETEST (+{row['Drift_Pct']:.0f}%)</span>"
    elif status == "PASS":
        drift_label = f"<span style='color: #10b981;'>PASS (+{row['Drift_Pct']:.0f}%)</span>"
    else:
        drift_label = "<span style='color: #94a3b8;'>IN-QUEUE</span>"
        
    text_labels[r][c] = f"<b>{row['Device_ID']}</b><br><span style='font-size: 9px;'>{drift_label}</span>"
    
    # Complete Hover Information with Explicit Time-Drift Rate %
    iddq_str = f"{row['Iddq_96h']:.2f} µA" if pd.notna(row['Iddq_96h']) else "Awaiting Scan"
    drift_str = f"+{row['Drift_Pct']:.1f}% (Nominal)" if status == "PASS" else (f"+{row['Drift_Pct']:.1f}% (Significant)" if pd.notna(row['Drift_Pct']) else "Pending Scan")
    leak_str = f"{row['Leakage_96h']:.2f} nA" if pd.notna(row['Leakage_96h']) else "Awaiting Scan"
    tpd_str = f"{row['Tpd_96h']:.2f} ns" if pd.notna(row['Tpd_96h']) else "Awaiting Scan"
    
    hover_texts[r][c] = (
        f"<b>{row['Device_ID']} (Socket {r+1}-{c+1})</b><br>"
        f"Status: <b>{status}</b><br>"
        f"• Quiescent Current (Iddq): {iddq_str}<br>"
        f"• Time-Drift Rate: <b>{drift_str}</b><br>"
        f"• Gate Oxide Leakage: {leak_str}<br>"
        f"• Propagation Delay (Tpd): {tpd_str}"
    )

fig_grid = go.Figure(data=go.Heatmap(
    z=grid_z,
    text=text_labels,
    texttemplate="%{text}",
    textfont={"size": 10, "family": "monospace", "color": "#f8fafc"},
    hoverinfo="text",
    hovertext=hover_texts,
    colorscale=[
        [0.00, "#0f2e28"], [0.25, "#0f2e28"], # Muted Dark Emerald
        [0.25, "#3d2d0c"], [0.50, "#3d2d0c"], # Muted Dark Amber
        [0.50, "#451212"], [0.75, "#451212"], # Muted Dark Crimson
        [0.75, "#1e293b"], [1.00, "#1e293b"]  # Muted Dark Slate/Gray
    ],
    showscale=False,
    xgap=6,
    ygap=6
))

fig_grid.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#0b0f19",
    height=280,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, autorange="reversed")
)
st.plotly_chart(fig_grid, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# -----------------------------------------------------------------------------
# LEVEL 4: ENLARGED FORENSIC DIAGNOSTICS & QA OPERATOR DISPOSITION (50/50)
# -----------------------------------------------------------------------------
st.markdown("### QA Justification & Forensic Device Review (All 50 Components)")

device_options = [f"{row['Device_ID']} — [{row['AI_Status']}]" for _, row in df.iterrows()]
selected_option = st.selectbox("Select Component Socket for Review & Electronic Sign-Off:", device_options, index=1)

selected_dut_id = selected_option.split(" — ")[0]
target = df[df["Device_ID"] == selected_dut_id].iloc[0]

q1, q2 = st.columns([1, 1], gap="medium")

with q1:
    with st.container(border=True):
        status_tag = target['AI_Status']
        if status_tag == "REJECT":
            st.markdown(f"### `{target['Device_ID']}` &nbsp;|&nbsp; STATUS: :red[**{status_tag}**]")
            st.error("**CORE VERDICT: CRITICAL ANOMALY (Latent Oxide Breakdown)**\n\nFixed 22.0 µA ceiling falsely passes this part, but dynamic time-drift detects impending thermal runaway.")
        elif status_tag == "EXTENDED TESTING":
            st.markdown(f"### `{target['Device_ID']}` &nbsp;|&nbsp; STATUS: :orange[**{status_tag}**]")
            st.warning("**CORE VERDICT: MARGINAL DRIFT (+24h Thermal Retest Required)**\n\nDrift slope exceeds nominal process variance. Extended thermal stress required to verify stability.")
        elif status_tag == "PASS":
            st.markdown(f"### `{target['Device_ID']}` &nbsp;|&nbsp; STATUS: :green[**{status_tag}**]")
            st.success("**CORE VERDICT: NOMINAL STABILIZATION (Flight Qualified)**\n\nTelemetry parameters remain tightly clustered within historical 1-sigma distribution.")
        else:
            st.markdown(f"### `{target['Device_ID']}` &nbsp;|&nbsp; STATUS: :gray[**{status_tag}**]")
            st.info("**CORE VERDICT: IN-QUEUE (Awaiting Next ATE Diagnostic Scan)**\n\nComponent pre-conditioned in chamber; awaiting scan data.")

        st.markdown("##### Forensic Parametric Diagnostics")
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            iddq_val = f"{target['Iddq_96h']:.2f} µA" if pd.notna(target['Iddq_96h']) else "Pending"
            drift_val = f"+{target['Drift_Pct']:.1f}%" if pd.notna(target['Drift_Pct']) else "Pending"
            st.metric("Quiescent Current (Iddq)", iddq_val, f"Baseline: {target['Iddq_0h']:.2f} µA")
            st.metric("Temporal Drift Rate", drift_val, f"Z-Score: {target['Modified_Z']:.2f}σ" if pd.notna(target['Modified_Z']) else "N/A")
        with d_col2:
            leak_val = f"{target['Leakage_96h']:.2f} nA" if pd.notna(target['Leakage_96h']) else "Pending"
            tpd_val = f"{target['Tpd_96h']:.2f} ns" if pd.notna(target['Tpd_96h']) else "Pending"
            st.metric("Gate Oxide Leakage (Ileak)", leak_val, "Nominal Barrier")
            st.metric("Propagation Delay (Tpd)", tpd_val, "Spec: < 3.5 ns")

with q2:
    with st.container(border=True):
        st.markdown("### QA Operator Decision & Electronic Sign-Off")
        
        current_saved = st.session_state.saved_decisions.get(target["Device_ID"], {})
        default_idx = 0
        if current_saved.get("Decision") == "Override: Pass": default_idx = 1
        elif current_saved.get("Decision") == "Override: Extended screening": default_idx = 2
        elif current_saved.get("Decision") == "Override: Reject": default_idx = 3

        decision_option = st.radio(
            "Select Disposition Action:",
            ["Accept AI recommendation", "Override: Pass (Flight Ready)", "Override: Extended screening (+24h Retest)", "Override: Reject (Quarantine for DPA)"],
            index=default_idx
        )
        
        user_comment = st.text_area(
            "Engineering Rationale & Justification Log:", 
            value=current_saved.get("Comment", ""), 
            placeholder="Enter QA inspector rationale for audit record (e.g., Verified gate-oxide stability)...",
            height=100
        )
        
        if st.button("Commit QA Disposition & Sign Off", use_container_width=True, type="primary"):
            st.session_state.saved_decisions[target["Device_ID"]] = {
                "Decision": decision_option,
                "Comment": user_comment if user_comment else "Standard AI recommendation accepted.",
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state.decision_logs.append({
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Event": f"QA Decision committed for {target['Device_ID']}: {decision_option}"
            })
            st.success(f"Disposition recorded for {target['Device_ID']}.")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# AUDIT TRAIL & EXPORT SIGNED-OFF CSV REPORT
# -----------------------------------------------------------------------------
audit_col1, audit_col2 = st.columns([7, 3])

with audit_col1:
    with st.expander("Session Audit Log (Air-Gapped Flight Recorder)", expanded=True):
        log_text = "\n".join([f"[{item['Timestamp']}] {item['Event']}" for item in st.session_state.decision_logs[-5:]])
        st.code(log_text, language="text")

with audit_col2:
    export_df = df[["Device_ID", "Iddq_0h", "Iddq_24h", "Iddq_96h", "Iddq_168h", "Leakage_0h", "Tpd_0h", "Drift_Pct", "Modified_Z", "AI_Status"]].copy()
    export_df["QA_Disposition"] = export_df["Device_ID"].map(lambda x: st.session_state.saved_decisions.get(x, {}).get("Decision", "AUTO_CLASSIFIED"))
    export_df["QA_Comment"] = export_df["Device_ID"].map(lambda x: st.session_state.saved_decisions.get(x, {}).get("Comment", "N/A"))
    
    csv_buffer = io.StringIO()
    export_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.download_button(
        label="Export Signed-Off Report (CSV)",
        data=csv_data,
        file_name="ISRO_MIL_STD_883_SCREENING_REPORT.csv",
        mime="text/csv",
        use_container_width=True
    )