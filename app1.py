import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ISRO Reliability Workbench | PS-26170",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit Default Chrome
st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden !important; height: 0 !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border-radius: 0 !important; width: 100% !important; min-height: 100vh !important;}
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISRO Reliability Workbench</title>
    <!-- Professional Enterprise Typography -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            color: #94a3b8;
            min-height: 100vh;
            background: 
                radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.20) 0%, transparent 45%),
                radial-gradient(circle at 80% 80%, rgba(0, 245, 155, 0.14) 0%, transparent 40%),
                linear-gradient(rgba(8, 14, 28, 0.55), rgba(4, 8, 18, 0.70)),
                url('https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
            background-size: cover;
            padding: 24px;
            overflow-x: hidden;
        }

        .glass-card {
            background: rgba(13, 22, 40, 0.68);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-top: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 18px;
            box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.75);
        }

        .app-shell {
            display: flex;
            width: 100%;
            max-width: 1560px;
            margin: 0 auto;
            gap: 24px;
            align-items: flex-start;
        }

        .sidebar-panel {
            width: 310px;
            min-width: 310px;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            flex-shrink: 0;
        }

        .sidebar-panel.collapsed {
            width: 0;
            min-width: 0;
            margin-right: -24px;
            opacity: 0;
            overflow: hidden;
            pointer-events: none;
        }

        .main-dashboard {
            flex: 1;
            min-width: 0;
            width: 100%;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .sidebar-close-btn {
            position: absolute;
            top: 20px;
            right: 16px;
            width: 30px;
            height: 30px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #38bdf8;
            cursor: pointer;
            z-index: 10;
            transition: all 0.2s ease;
        }

        .sidebar-close-btn:hover {
            background: #0284c7;
            color: #fff;
            transform: scale(1.1);
        }

        .reopen-sidebar-btn {
            display: none;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #38bdf8;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.76rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .reopen-sidebar-btn:hover {
            background: #0284c7;
            color: #fff;
        }

        .top-navbar-single {
            padding: 16px 24px;
            margin-bottom: 22px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            flex-wrap: nowrap;
            overflow: hidden;
        }

        .header-left-cluster {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 1;
            min-width: 0;
            overflow: hidden;
        }

        .header-meta-chip {
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
            color: #94a3b8;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 5px 12px;
            border-radius: 8px;
            white-space: nowrap;
        }

        .header-right-cluster {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-shrink: 0;
            white-space: nowrap;
        }

        .pill-badge-blue {
            background: rgba(56, 189, 248, 0.16);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.6px;
            font-family: 'JetBrains Mono', monospace;
            white-space: nowrap;
        }

        .pill-badge-green {
            background: rgba(0, 245, 155, 0.16);
            color: #00F59B;
            border: 1px solid rgba(0, 245, 155, 0.4);
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        .pill-badge-yellow {
            background: rgba(255, 184, 0, 0.18);
            color: #FFB800;
            border: 1px solid rgba(255, 184, 0, 0.45);
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            white-space: nowrap;
        }

        .pill-badge-white {
            background: rgba(255, 255, 255, 0.14);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            white-space: nowrap;
        }

        .pill-badge-red {
            background: rgba(255, 42, 95, 0.18);
            color: #FF2A5F;
            border: 1px solid rgba(255, 42, 95, 0.45);
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            white-space: nowrap;
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            background: #00F59B;
            border-radius: 50%;
            box-shadow: 0 0 8px #00F59B;
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.7; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.7; }
        }

        .milestone-stepper {
            padding: 14px 20px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .milestone-step {
            flex: 1;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 10px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
            position: relative;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .milestone-step:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 24px rgba(0,0,0,0.6), 0 0 15px rgba(56, 189, 248, 0.25);
            z-index: 50;
        }

        .milestone-step.done {
            border-color: rgba(0, 245, 155, 0.35);
            color: #00F59B;
        }

        .milestone-step.active {
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.2);
            font-weight: 700;
        }

        .milestone-step.pending {
            color: #64748b;
        }

        .milestone-arrow {
            color: #475569;
            font-size: 0.8rem;
        }

        .progress-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            margin-bottom: 22px;
        }

        .progress-box { padding: 16px 22px; }
        .progress-header {
            display: flex;
            justify-content: space-between;
            font-size: 0.84rem;
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 8px;
        }
        .progress-track {
            background: rgba(30, 41, 59, 0.75);
            border-radius: 9999px;
            height: 9px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #0284c7, #38bdf8);
            border-radius: 9999px;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.6);
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr) 2.4fr;
            gap: 14px;
            margin-bottom: 24px;
        }

        .metric-card { 
            padding: 14px 16px; 
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            min-height: 115px;
        }

        .metric-card:hover {
            border-color: rgba(56, 189, 248, 0.45);
            transform: translateY(-3px);
            box-shadow: 0 20px 48px -8px rgba(0, 0, 0, 0.85), 0 0 20px rgba(56, 189, 248, 0.15);
        }
        
        .metric-title {
            font-size: 0.76rem;
            font-weight: 600;
            color: #94a3b8;
            margin-bottom: 4px;
        }
        .metric-number {
            font-size: 1.55rem;
            font-weight: 800;
            color: #f8fafc;
            letter-spacing: -0.5px;
            margin-bottom: 2px;
        }
        .metric-delta {
            font-size: 0.70rem;
            font-family: 'JetBrains Mono', monospace;
            color: #00F59B;
        }

        .donut-highlight-card {
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .panel-container {
            padding: 24px 26px;
            margin-bottom: 24px;
        }

        .section-header {
            font-size: 1.15rem;
            font-weight: 800;
            color: #f8fafc;
            letter-spacing: -0.3px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .matrix-grid {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 10px;
            margin-top: 14px;
        }

        .socket-chip {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 11px 4px;
            text-align: center;
            cursor: pointer;
            position: relative;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .socket-chip:hover {
            transform: translateY(-4px) scale(1.05);
            box-shadow: 0 10px 28px rgba(0,0,0,0.7), 0 0 14px rgba(56, 189, 248, 0.35);
            border-color: rgba(255,255,255,0.45);
            z-index: 50;
        }

        .socket-id {
            font-size: 0.76rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            color: #f8fafc;
            margin-bottom: 4px;
        }

        .socket-pill {
            font-size: 0.68rem;
            font-weight: 700;
            border-radius: 9999px;
            padding: 2px 7px;
            display: inline-block;
        }

        .chip-pass { border-top: 2px solid #00F59B; }
        .chip-pass .socket-pill { background: rgba(0, 245, 155, 0.18); color: #00F59B; }

        .chip-warn { border-top: 2px solid #FFB800; }
        .chip-warn .socket-pill { background: rgba(255, 184, 0, 0.18); color: #FFB800; }

        .chip-fail { border-top: 2px solid #FF2A5F; }
        .chip-fail .socket-pill { background: rgba(255, 42, 95, 0.20); color: #FF2A5F; }

        .chip-pend { border-top: 2px solid #94a3b8; }
        .chip-pend .socket-pill { background: rgba(148, 163, 184, 0.22); color: #FFFFFF; }

        .tooltip-card {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            bottom: 115%;
            left: 50%;
            transform: translateX(-50%) translateY(10px);
            width: 260px;
            background: rgba(15, 23, 42, 0.96);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 16px 36px rgba(0,0,0,0.85);
            pointer-events: none;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 100;
            text-align: left;
            font-size: 0.76rem;
            line-height: 1.6;
            white-space: nowrap;
        }

        .socket-chip:hover .tooltip-card,
        .milestone-step:hover .tooltip-card,
        .metric-card:hover .tooltip-card {
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }

        .filter-btn-group {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        .filter-btn {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94a3b8;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.74rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .filter-btn:hover {
            color: #f8fafc;
            border-color: rgba(56, 189, 248, 0.4);
        }

        .filter-btn.active {
            background: rgba(56, 189, 248, 0.16);
            color: #38bdf8;
            border-color: #38bdf8;
        }

        select, textarea {
            width: 100%;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: #f8fafc;
            padding: 12px 16px;
            font-family: 'Inter', sans-serif;
            font-size: 0.88rem;
            outline: none;
        }
        select:focus, textarea:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
        }

        .radio-option {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 11px 14px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            margin-bottom: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }
        .radio-option:hover {
            border-color: rgba(56, 189, 248, 0.4);
            background: rgba(56, 189, 248, 0.08);
        }
        .radio-option.selected {
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.12);
            color: #f8fafc;
        }

        .btn-action {
            width: 100%;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: #ffffff;
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 12px;
            padding: 14px 20px;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35);
            transition: all 0.2s ease;
            margin-top: 14px;
        }
        .btn-action:hover {
            background: linear-gradient(135deg, #0369a1 100%, #0284c7 100%);
            box-shadow: 0 8px 24px rgba(56, 189, 248, 0.55);
            transform: translateY(-1px);
        }

        .bottom-export-bar {
            margin-top: 10px;
            padding: 18px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .btn-download-csv {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #38bdf8;
            padding: 10px 22px;
            border-radius: 10px;
            font-size: 0.86rem;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
        }

        .btn-download-csv:hover {
            background: #0284c7;
            color: #ffffff;
            box-shadow: 0 4px 18px rgba(2, 132, 199, 0.45);
            transform: translateY(-1px);
        }

        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(4, 7, 15, 0.75);
            backdrop-filter: blur(16px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .modal-box {
            width: 480px;
            background: rgba(17, 24, 39, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-top: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 20px;
            padding: 32px;
            text-align: center;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.9);
            transform: scale(0.9);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .modal-overlay.active .modal-box { transform: scale(1); }

        .modal-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(0, 245, 155, 0.15);
            border: 1px solid rgba(0, 245, 155, 0.35);
            color: #00F59B;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            margin: 0 auto 16px;
        }

        .sidebar-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.78rem;
            margin-top: 10px;
            margin-bottom: 16px;
        }
        .sidebar-table th {
            text-align: left;
            padding: 8px 8px;
            color: #94a3b8;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            font-weight: 600;
        }
        .sidebar-table td {
            padding: 8px 8px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
            color: #cbd5e1;
        }
    </style>
</head>
<body>

    <div class="app-shell">
        
        <div class="sidebar-panel" id="sidebarPanel">
            <div class="glass-card panel-container" style="padding: 22px; position: relative;">
                
                <div class="sidebar-close-btn" onclick="toggleSidebar()" title="Collapse Panel">
                    <i class="fa-solid fa-chevron-left"></i>
                </div>

                <div style="font-size: 1.1rem; font-weight: 800; color: #f8fafc; margin-bottom: 2px;">Historical Lot Summary</div>
                <div style="font-size: 0.76rem; color: #64748b; margin-bottom: 12px;">MIL-STD-883 Production Slot Breakdown</div>
                
                <table class="sidebar-table">
                    <thead>
                        <tr><th>Slot Ref</th><th>Passed %</th><th>Retest %</th><th>Rejected %</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Slot 1</td><td>100%</td><td>0.0%</td><td>0.0%</td></tr>
                        <tr><td>Slot 2</td><td>100%</td><td>0.0%</td><td>0.0%</td></tr>
                        <tr><td>Slot 3</td><td>92.5%</td><td>7.5%</td><td>0.0%</td></tr>
                        <tr><td>Slot 4</td><td>85.0%</td><td>5.0%</td><td>10.0%</td></tr>
                        <tr><td>Slot 5 (Live)</td><td style="color:#00F59B; font-weight:700;">70.5%</td><td style="color:#FFB800; font-weight:700;">18.2%</td><td style="color:#FF2A5F; font-weight:700;">11.4%</td></tr>
                    </tbody>
                </table>

                <div style="font-size: 0.95rem; font-weight: 700; color: #f8fafc; margin-top: 16px; margin-bottom: 6px;">Lot Compliance Audit</div>
                <table class="sidebar-table">
                    <thead>
                        <tr><th>Batch Stage</th><th>Audit Status</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Slot 1 to 3</td><td><span class="pill-badge-green" style="padding:3px 10px; font-size:0.7rem;">PASSED</span></td></tr>
                        <tr><td>Slot 4</td><td><span class="pill-badge-blue" style="padding:3px 10px; font-size:0.7rem;">PDA RISK</span></td></tr>
                        <tr><td>Slot 5 (Live)</td><td><span class="pill-badge-red" style="padding:3px 10px; font-size:0.7rem;">PDA RISK BREACH</span></td></tr>
                    </tbody>
                </table>

                <div style="font-size: 0.95rem; font-weight: 700; color: #f8fafc; margin-top: 16px; margin-bottom: 8px;">Data Provenance</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b; line-height: 1.6; background: rgba(15, 23, 42, 0.7); padding: 12px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    Source: ATE_STREAM_A17.csv<br>
                    Checksum: SHA256-59159cf7...<br>
                    Monitored: 50 Sockets (BIB-50-A)<br>
                    Chamber: THERMAL-B04 (125°C)<br>
                    Standard: MIL-STD-883 Class-S
                </div>
            </div>
        </div>

        <div class="main-dashboard" id="mainDashboard">
            
            <div class="glass-card top-navbar-single">
                <div class="header-left-cluster">
                    <button class="reopen-sidebar-btn" id="reopenSidebarBtn" onclick="toggleSidebar()">
                        <i class="fa-solid fa-chevron-right"></i> Lot Summary
                    </button>
                    <span class="pill-badge-blue">PS 26170</span>
                    <span style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.3px;">
                        Burn-In & Screening Dashboard
                    </span>
                    <div class="header-meta-chip">
                        Lot: <strong style="color: #f8fafc;">LOT-2026-A17</strong>
                    </div>
                </div>
                <div class="header-right-cluster">
                    <div class="pill-badge-green"><div class="pulse-dot"></div> OFFLINE MODE</div>
                    <div class="pill-badge-red">5 DEVICE(S) AT REJECT RISK (PDA: 11.4%)</div>
                </div>
            </div>

            <div class="progress-grid">
                <div class="glass-card progress-box">
                    <div class="progress-header">
                        <span>Burn-In Stress Progression (125°C Chamber)</span>
                        <span style="color: #38bdf8; font-family: 'JetBrains Mono', monospace;">57% (96h / 168h Reached)</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" style="width: 57%;"></div>
                    </div>
                </div>
                <div class="glass-card progress-box">
                    <div class="progress-header">
                        <span>Electrical Screening Verification</span>
                        <span style="color: #38bdf8; font-family: 'JetBrains Mono', monospace;">88% (44 of 50 Sockets Ingested)</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" style="width: 88%;"></div>
                    </div>
                </div>
            </div>

            <div class="glass-card milestone-stepper">
                <div class="milestone-step done">
                    <i class="fa-solid fa-circle-check"></i>
                    <div>
                        <div style="font-size: 0.72rem; color: #94a3b8;">STAGE 01</div>
                        <div>0h Pre-Stress Baseline</div>
                    </div>
                    <div class="tooltip-card">
                        <strong style="color:#00F59B;">STAGE 01 (0h Pre-Stress)</strong><br>
                        • Baseline Telemetry Captured<br>
                        • 50 DUT Sockets Ingested<br>
                        • Gate Check: PASSED (100%)
                    </div>
                </div>
                <i class="fa-solid fa-chevron-right milestone-arrow"></i>
                <div class="milestone-step done">
                    <i class="fa-solid fa-circle-check"></i>
                    <div>
                        <div style="font-size: 0.72rem; color: #94a3b8;">STAGE 02</div>
                        <div>24h Dynamic Intermediate</div>
                    </div>
                    <div class="tooltip-card">
                        <strong style="color:#00F59B;">STAGE 02 (24h Intermediate)</strong><br>
                        • Slope Delta Analysis Completed<br>
                        • Process Variance Normalized<br>
                        • Gate Check: PASSED (100%)
                    </div>
                </div>
                <i class="fa-solid fa-chevron-right milestone-arrow"></i>
                <div class="milestone-step active">
                    <i class="fa-solid fa-satellite-dish fa-spin" style="--fa-animation-duration: 4s;"></i>
                    <div>
                        <div style="font-size: 0.72rem; color: #38bdf8;">STAGE 03 [LIVE]</div>
                        <div>96h Active Diagnostic Scan</div>
                    </div>
                    <div class="tooltip-card">
                        <strong style="color:#38bdf8;">STAGE 03 (96h Active Scan)</strong><br>
                        • SLOT-5 Live Ingest Active<br>
                        • 5 Latent Breakdown Risks Found<br>
                        • PDA Threshold: 11.4% (Critical)
                    </div>
                </div>
                <i class="fa-solid fa-chevron-right milestone-arrow"></i>
                <div class="milestone-step pending">
                    <i class="fa-regular fa-circle"></i>
                    <div>
                        <div style="font-size: 0.72rem; color: #64748b;">STAGE 04</div>
                        <div>168h Lot Qualification</div>
                    </div>
                    <div class="tooltip-card">
                        <strong style="color:#94a3b8;">STAGE 04 (168h Final Qual)</strong><br>
                        • Scheduled Qualification State<br>
                        • Thermal Soak Completion<br>
                        • Status: IN-QUEUE
                    </div>
                </div>
            </div>

            <!-- Top 4 Parameter Cards -->
            <div class="metrics-grid">
                <div class="glass-card metric-card">
                    <div class="metric-title">Quiescent Current (I<sub>ddq</sub>)</div>
                    <div class="metric-number">14.30 <span style="font-size: 0.95rem; color: #94a3b8;">µA</span></div>
                    <div class="metric-delta" style="color: #00F59B;">↑ Baseline: 12.80 µA</div>
                    <div class="tooltip-card">
                        <strong style="color:#00F59B;">Quiescent Current (I<sub>ddq</sub>)</strong><br>
                        • Population Mean: 14.30 µA<br>
                        • Static Limit: 22.00 µA<br>
                        • Health Status: PASSED
                    </div>
                </div>

                <div class="glass-card metric-card">
                    <div class="metric-title">Leakage Current (I<sub>leak</sub>)</div>
                    <div class="metric-number">2.05 <span style="font-size: 0.95rem; color: #94a3b8;">nA</span></div>
                    <div class="metric-delta" style="color: #00F59B;">↑ +0.04 nA Normal Drift</div>
                    <div class="tooltip-card">
                        <strong style="color:#00F59B;">Leakage Current (I<sub>leak</sub>)</strong><br>
                        • Mean Leakage: 2.05 nA<br>
                        • Limit Ceiling: 4.00 nA<br>
                        • Barrier Integrity: PASSED
                    </div>
                </div>

                <div class="glass-card metric-card">
                    <div class="metric-title">Threshold Voltage (V<sub>t</sub> / V<sub>th</sub>)</div>
                    <div class="metric-number">0.72 <span style="font-size: 0.95rem; color: #94a3b8;">V</span></div>
                    <div class="metric-delta" style="color: #00F59B;">↑ Within Spec Floor</div>
                    <div class="tooltip-card">
                        <strong style="color:#00F59B;">Threshold Voltage (V<sub>t</sub> / V<sub>th</sub>)</strong><br>
                        • Nominal Mean: 0.72 V<br>
                        • Floor Limit: 0.50 V<br>
                        • Gate Integrity: PASSED
                    </div>
                </div>

                <div class="glass-card metric-card">
                    <div class="metric-title">Propagation Delay (T<sub>pd</sub>)</div>
                    <div class="metric-number">3.36 <span style="font-size: 0.95rem; color: #94a3b8;">ns</span></div>
                    <div class="metric-delta" style="color: #00F59B;">↑ Within 3.5 ns Spec</div>
                    <div class="tooltip-card">
                        <strong style="color:#00F59B;">Propagation Delay (T<sub>pd</sub>)</strong><br>
                        • Nominal Mean: 3.36 ns<br>
                        • Maximum Ceiling: 4.80 ns<br>
                        • Timing Margin: PASSED
                    </div>
                </div>

                <div class="glass-card donut-highlight-card">
                    <div style="height: 125px; width: 125px; position: relative; flex-shrink: 0;">
                        <canvas id="yieldDonut"></canvas>
                    </div>
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-size: 0.82rem; font-weight: 800; color: #f8fafc; margin-bottom: 4px;">Lot Yield (PDA: 11.4%)</div>
                        <div style="font-size: 0.68rem; color: #00F59B; font-weight: 700; margin-bottom: 2px; white-space: nowrap;">● 62% Flight Ready (PASSED)</div>
                        <div style="font-size: 0.68rem; color: #FFB800; font-weight: 700; margin-bottom: 2px; white-space: nowrap;">● 16% Retest Required (RETEST)</div>
                        <div style="font-size: 0.68rem; color: #FF2A5F; font-weight: 700; margin-bottom: 2px; white-space: nowrap;">● 10% Critical (REJECTED)</div>
                        <div style="font-size: 0.68rem; color: #FFFFFF; font-weight: 700; white-space: nowrap;">● 12% In-Queue (IN-QUEUE)</div>
                    </div>
                </div>
            </div>

            <div class="glass-card panel-container">
                <div class="section-header">
                    <div>
                        <span>Live Lot Analytics: Parametric Trajectories (Control Chart)</span>
                        <div style="font-size: 0.78rem; font-weight: 500; color: #64748b; margin-top: 4px;">All 50 Components Screened Against Dynamic Drift & Spec Limits over Burn-In Checkpoints (0h to 168h)</div>
                    </div>
                    <div style="width: 340px;">
                        <select id="paramSelect" onchange="switchParamData(this.value)">
                            <option value="Iddq">1. Quiescent Current (I<sub>ddq</sub> - µA)</option>
                            <option value="Leakage">2. Leakage Current (I<sub>leak</sub> - nA)</option>
                            <option value="Vth">3. Threshold Voltage (V<sub>t</sub> / V<sub>th</sub> - V)</option>
                            <option value="Tpd">4. Propagation Delay (T<sub>pd</sub> - ns)</option>
                            <option value="Supply">5. Supply Current (I<sub>dd</sub> - mA)</option>
                            <option value="Frequency">6. Operating Frequency (f - MHz)</option>
                        </select>
                    </div>
                </div>
                <div style="height: 350px; width: 100%;">
                    <canvas id="controlChart"></canvas>
                </div>
            </div>

            <div class="glass-card panel-container">
                <div class="section-header">
                    <div>
                        <span>Batch Anomaly Map (50 Sockets Burn-In Board Matrix)</span>
                    </div>
                </div>
                <div class="matrix-grid" id="matrixGrid"></div>
            </div>

            <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 24px; margin-bottom: 24px;">
                
                <div class="glass-card panel-container">
                    <div class="section-header" style="flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span>Forensic Diagnostics:</span>
                            <select id="dutDropdown" onchange="selectDUT(this.value)" style="width: 200px; padding: 7px 12px; font-size: 0.82rem;">
                            </select>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div class="filter-btn-group">
                                <button class="filter-btn active" onclick="filterDropdown('ALL', this)">ALL</button>
                                <button class="filter-btn" onclick="filterDropdown('PASSED', this)">PASSED</button>
                                <button class="filter-btn" onclick="filterDropdown('RETEST', this)">RETEST</button>
                                <button class="filter-btn" onclick="filterDropdown('REJECTED', this)">REJECTED</button>
                                <button class="filter-btn" onclick="filterDropdown('IN-QUEUE', this)">IN-QUEUE</button>
                            </div>
                            <span id="selectedStatusTag" class="pill-badge-yellow">RETEST</span>
                        </div>
                    </div>

                    <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                        <span id="forensicCmpTitle">CMP-1004</span>
                        <span style="color: #64748b; font-weight: 400;">|</span>
                        <span>STATUS:</span>
                        <span id="forensicStatusTitle" style="color: #FFB800;">RETEST</span>
                    </div>

                    <div id="verdictBox" style="border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.1);">
                        <div id="verdictTitle" style="font-weight: 700; font-size: 0.88rem; margin-bottom: 4px;"></div>
                        <div id="verdictDesc" style="font-size: 0.8rem; line-height: 1.5;"></div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.06); padding: 14px; border-radius: 14px;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Quiescent Current (I<sub>ddq</sub>)</div>
                            <div style="font-size: 1.45rem; font-weight: 800; color: #f8fafc;" id="fIddq">16.48 µA</div>
                            <div style="font-size: 0.72rem; font-family: 'JetBrains Mono';" id="fIddqBase">↑ Baseline: 12.80 µA</div>
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.06); padding: 14px; border-radius: 14px;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Leakage Current (I<sub>leak</sub>)</div>
                            <div style="font-size: 1.45rem; font-weight: 800; color: #f8fafc;" id="fLeak">2.28 nA</div>
                            <div style="font-size: 0.72rem; font-family: 'JetBrains Mono';" id="fLeakBase">↑ Nominal Barrier</div>
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.06); padding: 14px; border-radius: 14px;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Threshold Voltage (V<sub>t</sub> / V<sub>th</sub>)</div>
                            <div style="font-size: 1.45rem; font-weight: 800; color: #f8fafc;" id="fVth">0.72 V</div>
                            <div style="font-size: 0.72rem; font-family: 'JetBrains Mono';" id="fVthBase">↑ Floor > 0.50 V</div>
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.06); padding: 14px; border-radius: 14px;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Propagation Delay (T<sub>pd</sub>)</div>
                            <div style="font-size: 1.45rem; font-weight: 800; color: #f8fafc;" id="fTpd">3.49 ns</div>
                            <div style="font-size: 0.72rem; font-family: 'JetBrains Mono';" id="fTpdBase">↑ Spec < 3.5 ns</div>
                        </div>
                    </div>
                </div>

                <div class="glass-card panel-container">
                    <div class="section-header">
                        <span>Flight Quality Assurance & Lot Disposition Sign-Off</span>
                    </div>
                    
                    <div style="margin-bottom: 12px;">
                        <label style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; display: block; margin-bottom: 8px;">Select QA Disposition Vector:</label>
                        <div class="radio-option selected" onclick="setRadio(this, 'Class-S Flight Qualified (PASSED)')">
                            <i class="fa-solid fa-circle-dot" style="color: #38bdf8;"></i> Class-S Flight Qualified (PASSED)
                        </div>
                        <div class="radio-option" onclick="setRadio(this, 'Override: Lot Acceptance (PASSED)')">
                            <i class="fa-regular fa-circle"></i> Override: Lot Acceptance (PASSED)
                        </div>
                        <div class="radio-option" onclick="setRadio(this, 'Override: Thermal Retest (+24h Stress: RETEST)')">
                            <i class="fa-regular fa-circle"></i> Override: Thermal Retest (+24h Stress: RETEST)
                        </div>
                        <div class="radio-option" onclick="setRadio(this, 'Override: Lot Quarantine (REJECTED)')">
                            <i class="fa-regular fa-circle"></i> Override: Lot Quarantine (REJECTED)
                        </div>
                    </div>

                    <div>
                        <label style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; display: block; margin-bottom: 6px;">Mission Assurance & Engineering Justification Audit Record:</label>
                        <textarea id="qaComment" rows="4" style="min-height: 125px; resize: vertical;" placeholder="Enter formal engineering disposition rationale for qualification audit compliance..."></textarea>
                    </div>

                    <button class="btn-action" onclick="openCommitModal()">
                        <i class="fa-solid fa-satellite"></i> Authorize & Sign Off Lot Disposition (MIL-STD-883 Class-S)
                    </button>
                </div>
            </div>

            <div class="glass-card bottom-export-bar">
                <div>
                    <strong style="color:#f8fafc; font-size:0.92rem;">Audit Report & Lot Telemetry Export</strong>
                    <div style="font-size:0.75rem; color:#64748b; margin-top:2px;">Download certified screening record containing all 50 socket measurements and signed dispositions.</div>
                </div>
                <button class="btn-download-csv" onclick="downloadTelemetryCSV()">
                    <i class="fa-solid fa-file-csv"></i> Export Signed Screening Report (CSV)
                </button>
            </div>

        </div>
    </div>

    <div class="modal-overlay" id="confirmModal">
        <div class="modal-box">
            <div class="modal-icon">
                <i class="fa-solid fa-check"></i>
            </div>
            <h3 style="font-size: 1.35rem; font-weight: 800; color: #f8fafc; margin-bottom: 8px;">Disposition Authorized!</h3>
            <p style="font-size: 0.84rem; color: #94a3b8; line-height: 1.6; margin-bottom: 20px;">
                The QA disposition record has been verified and committed to the flight audit log.
            </p>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; text-align: left; margin-bottom: 20px; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">
                <div>RECORD ID: <span style="color:#38bdf8;" id="modalDut">CMP-1004</span></div>
                <div>DISPOSITION: <span style="color:#00F59B;" id="modalAction">Class-S Flight Qualified (PASSED)</span></div>
                <div>TIMESTAMP: <span style="color:#cbd5e1;">2026-09-07 02:54:12</span></div>
            </div>
            <button class="btn-action" style="margin-top:0;" onclick="closeModal()">Close & Return</button>
        </div>
    </div>

    <script>
        function toggleSidebar() {
            const panel = document.getElementById('sidebarPanel');
            const reopenBtn = document.getElementById('reopenSidebarBtn');
            panel.classList.toggle('collapsed');
            if (panel.classList.contains('collapsed')) {
                reopenBtn.style.display = 'inline-flex';
            } else {
                reopenBtn.style.display = 'none';
            }
        }

        const ctxDonut = document.getElementById('yieldDonut').getContext('2d');
        new Chart(ctxDonut, {
            type: 'doughnut',
            data: {
                labels: ['PASSED', 'RETEST', 'REJECTED', 'IN-QUEUE'],
                datasets: [{
                    data: [31, 8, 5, 6],
                    backgroundColor: ['#00F59B', '#FFB800', '#FF2A5F', '#FFFFFF'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                cutout: '66%',
                responsive: true,
                maintainAspectRatio: false,
                devicePixelRatio: 2,
                plugins: { legend: { display: false } }
            }
        });

        const checkpoints = ['0h Baseline', '24h Checkpoint', '96h Active Scan', '168h Qualification'];
        const critList = [7, 22, 30, 44, 48];
        const warnList = [3, 10, 14, 18, 26, 34, 37, 42];
        const pendList = [39, 43, 45, 46, 47, 49];

        const paramConfigs = {
            Iddq: { 
                ucl: 22.0, 
                yTitle: 'Quiescent Current (i<sub>ddq</sub> - µA)', 
                specLabel: 'Static Spec Ceiling Limit (22.0 µA)',
                yMin: 10.0, yMax: 32.0,
                baseMean: 12.8,
                unit: 'µA',
                generate: (b0, type) => {
                    if (type === 'crit') return [b0, b0 + 0.3, 22.5 + (b0 - 12.8)*1.2, 28.5 + (b0 - 12.8)*1.5];
                    if (type === 'warn') return [b0, b0 + 0.2, 16.5 + (b0 - 12.8)*0.8, 17.8 + (b0 - 12.8)*0.9];
                    if (type === 'pend') return [b0, b0 + 0.1, null, null];
                    return [b0, b0 + 0.1, 13.1 + (b0 - 12.8)*0.3, 13.3 + (b0 - 12.8)*0.3];
                }
            },
            Leakage: { 
                ucl: 4.0, 
                yTitle: 'Leakage Current (i<sub>leak</sub> - nA)', 
                specLabel: 'Static Spec Ceiling Limit (4.0 nA)',
                yMin: 1.2, yMax: 5.2,
                baseMean: 1.80,
                unit: 'nA',
                generate: (b0, type) => {
                    if (type === 'crit') return [b0, b0 + 0.04, 3.65 + (b0 - 1.80)*0.8, 4.45 + (b0 - 1.80)*1.0];
                    if (type === 'warn') return [b0, b0 + 0.02, 2.30 + (b0 - 1.80)*0.5, 2.50 + (b0 - 1.80)*0.6];
                    if (type === 'pend') return [b0, b0 + 0.01, null, null];
                    return [b0, b0 + 0.01, 1.84 + (b0 - 1.80)*0.2, 1.86 + (b0 - 1.80)*0.2];
                }
            },
            Vth: { 
                ucl: 0.50, 
                yTitle: 'Threshold Voltage (v<sub>t</sub> / v<sub>th</sub> - V)', 
                specLabel: 'Lower Static Spec Floor (0.50 V)',
                yMin: 0.25, yMax: 0.85,
                baseMean: 0.72,
                unit: 'V',
                generate: (b0, type) => {
                    if (type === 'crit') return [b0, b0 - 0.01, 0.48 + (b0 - 0.72)*0.4, 0.36 + (b0 - 0.72)*0.3];
                    if (type === 'warn') return [b0, b0 - 0.005, 0.62 + (b0 - 0.72)*0.5, 0.58 + (b0 - 0.72)*0.5];
                    if (type === 'pend') return [b0, b0 - 0.002, null, null];
                    return [b0, b0 - 0.002, 0.70 + (b0 - 0.72)*0.3, 0.69 + (b0 - 0.72)*0.3];
                }
            },
            Tpd: { 
                ucl: 4.8, 
                yTitle: 'Propagation Delay (t<sub>pd</sub> - ns)', 
                specLabel: 'Static Spec Ceiling Limit (4.8 ns)',
                yMin: 2.8, yMax: 5.4,
                baseMean: 3.20,
                unit: 'ns',
                generate: (b0, type) => {
                    if (type === 'crit') return [b0, b0 + 0.05, 4.75 + (b0 - 3.20)*0.5, 4.40 + (b0 - 3.20)*0.3];
                    if (type === 'warn') return [b0, b0 + 0.04, 3.80 + (b0 - 3.20)*0.6, 3.65 + (b0 - 3.20)*0.4];
                    if (type === 'pend') return [b0, b0 + 0.01, null, null];
                    return [b0, b0 + 0.01, 3.24 + (b0 - 3.20)*0.2, 3.23 + (b0 - 3.20)*0.1];
                }
            },
            Supply: { 
                ucl: 65.0, 
                yTitle: 'Supply Current (i<sub>dd</sub> - mA)', 
                specLabel: 'Static Spec Ceiling Limit (65.0 mA)',
                yMin: 35.0, yMax: 95.0,
                baseMean: 45.0,
                unit: 'mA',
                generate: (b0, type) => {
                    if (type === 'crit') return [b0, b0 + 1.2, 64.0 + (b0 - 45.0)*1.5, 82.0 + (b0 - 45.0)*2.0];
                    if (type === 'warn') return [b0, b0 + 0.8, 52.0 + (b0 - 45.0)*1.0, 56.5 + (b0 - 45.0)*1.1];
                    if (type === 'pend') return [b0, b0 + 0.4, null, null];
                    return [b0, b0 + 0.3, 45.7 + (b0 - 45.0)*0.4, 46.2 + (b0 - 45.0)*0.4];
                }
            },
            Frequency: { 
                ucl: 50.0, 
                yTitle: 'Operating Frequency (f - MHz)', 
                specLabel: 'Lower Spec Floor (50.0 MHz)',
                yMin: 30.0, yMax: 120.0,
                baseMean: 95.0,
                unit: 'MHz',
                generate: (b0, type) => {
                    if (type === 'crit') return [b0, b0 - 2.0, 48.0 - (95.0 - b0)*0.5, 38.0 - (95.0 - b0)*0.8];
                    if (type === 'warn') return [b0, b0 - 1.0, 72.0 - (95.0 - b0)*0.3, 64.0 - (95.0 - b0)*0.4];
                    if (type === 'pend') return [b0, b0 - 0.5, null, null];
                    return [b0, b0 - 0.2, 94.5 - (95.0 - b0)*0.1, 94.2 - (95.0 - b0)*0.1];
                }
            }
        };

        let currentActiveParam = 'Iddq';

        function generate50Traces(paramKey) {
            currentActiveParam = paramKey;
            const conf = paramConfigs[paramKey];
            const datasets = [];

            datasets.push({
                label: conf.specLabel,
                data: [conf.ucl, conf.ucl, conf.ucl, conf.ucl],
                borderColor: '#FF2A5F',
                borderWidth: 2.0,
                borderDash: [6, 6],
                pointRadius: 0,
                pointHoverRadius: 0,
                fill: false
            });

            for(let i = 0; i < 50; i++) {
                const devId = `CMP-${1001 + i}`;
                let col, width, pts;

                const offset = ((i % 7) - 3) * 0.015 * conf.baseMean;
                const b0 = conf.baseMean + offset;

                if(critList.includes(i)) {
                    col = '#FF2A5F';
                    width = 2.4;
                    pts = conf.generate(b0, 'crit');
                } else if(warnList.includes(i)) {
                    col = '#FFB800';
                    width = 2.0;
                    pts = conf.generate(b0, 'warn');
                } else if(pendList.includes(i)) {
                    col = '#FFFFFF';
                    width = 1.2;
                    pts = conf.generate(b0, 'pend');
                } else {
                    col = 'rgba(0, 245, 155, 0.45)';
                    width = 1.2;
                    pts = conf.generate(b0, 'nom');
                }

                datasets.push({
                    label: devId,
                    data: pts,
                    borderColor: col,
                    borderWidth: width,
                    tension: 0.45,
                    pointRadius: 3.5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: col,
                    fill: false
                });
            }
            return datasets;
        }

        const ctxControl = document.getElementById('controlChart').getContext('2d');
        let controlChart = new Chart(ctxControl, {
            type: 'line',
            data: {
                labels: checkpoints,
                datasets: generate50Traces('Iddq')
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                devicePixelRatio: 2,
                interaction: {
                    mode: 'nearest',
                    intersect: true
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(15, 23, 42, 0.96)',
                        titleColor: '#38bdf8',
                        bodyColor: '#f8fafc',
                        borderColor: 'rgba(56, 189, 248, 0.35)',
                        borderWidth: 1.5,
                        padding: 10,
                        titleFont: { family: 'JetBrains Mono', size: 12, weight: 'bold' },
                        bodyFont: { family: 'JetBrains Mono', size: 11 },
                        callbacks: {
                            title: function(context) {
                                return `Component: ${context[0].dataset.label}`;
                            },
                            label: function(context) {
                                if (context.datasetIndex === 0) return null;
                                const val = context.parsed.y;
                                const unit = paramConfigs[currentActiveParam].unit;
                                if (val === null) return ' Telemetry: Awaiting Scan';
                                return ` Telemetry: ${val.toFixed(2)} ${unit} against ${context.label}`;
                            }
                        },
                        filter: function(item) {
                            return item.datasetIndex !== 0;
                        }
                    }
                },
                scales: {
                    x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', font: { family: 'Inter' } } },
                    y: { 
                        min: paramConfigs.Iddq.yMin,
                        max: paramConfigs.Iddq.yMax,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }, 
                        ticks: { color: '#94a3b8', font: { family: 'Inter' } },
                        title: { display: true, text: 'Quiescent Current (i_ddq - µA)', color: '#94a3b8', font: { family: 'Inter' } }
                    }
                }
            }
        });

        function switchParamData(param) {
            const conf = paramConfigs[param];
            controlChart.data.datasets = generate50Traces(param);
            let cleanTitle = conf.yTitle.replace(/<\/?sub>/g, '').replace(/<\/?th>/g, '');
            controlChart.options.scales.y.title.text = cleanTitle;
            controlChart.options.scales.y.min = conf.yMin;
            controlChart.options.scales.y.max = conf.yMax;
            controlChart.update();
        }

        const matrixGrid = document.getElementById('matrixGrid');
        const dutDropdown = document.getElementById('dutDropdown');
        const deviceDB = {};

        for(let i = 0; i < 50; i++) {
            const devId = `CMP-${1001 + i}`;
            let status = "PASSED";
            let chipClass = "chip-pass";
            let pillText = "PASSED +2%";
            let iddq = "13.02 µA", drift = "+2.0%", zscore = "-0.12σ", leak = "1.84 nA", tpd = "3.20 ns";

            if (critList.includes(i)) {
                status = "REJECTED";
                chipClass = "chip-fail";
                pillText = "REJECTED +55%";
                iddq = "28.40 µA"; drift = "+121.5%"; zscore = "+5.42σ"; leak = "3.85 nA"; tpd = "4.12 ns";
            } else if (warnList.includes(i)) {
                status = "RETEST";
                chipClass = "chip-warn";
                pillText = "RETEST +25%";
                iddq = "16.48 µA"; drift = "+25.0%"; zscore = "+54.21σ"; leak = "2.28 nA"; tpd = "3.49 ns";
            } else if (pendList.includes(i)) {
                status = "IN-QUEUE";
                chipClass = "chip-pend";
                pillText = "IN-QUEUE";
                iddq = "Pending"; drift = "Pending"; zscore = "N/A"; leak = "Pending"; tpd = "Pending";
            }

            deviceDB[devId] = { status, iddq, drift, zscore, leak, tpd, chipClass };

            const div = document.createElement('div');
            div.className = `socket-chip ${chipClass}`;
            div.innerHTML = `
                <div class="socket-id">${devId}</div>
                <div class="socket-pill">${pillText}</div>
                <div class="tooltip-card">
                    <div style="font-weight:700; color:#f8fafc; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:4px; margin-bottom:4px;">
                        ${devId} [${status}]
                    </div>
                    <div>• Quiescent Current (i<sub>ddq</sub>): <strong>${iddq}</strong></div>
                    <div>• Temporal Drift: <strong>${drift}</strong></div>
                    <div>• Leakage Current (i<sub>leak</sub>): <strong>${leak}</strong></div>
                    <div>• Propagation Delay (t<sub>pd</sub>): <strong>${tpd}</strong></div>
                </div>
            `;
            div.onclick = () => selectDUT(devId);
            matrixGrid.appendChild(div);
        }

        function renderDropdownOptions(filter = 'ALL') {
            dutDropdown.innerHTML = '';
            for(let i = 0; i < 50; i++) {
                const devId = `CMP-${1001 + i}`;
                const st = deviceDB[devId].status;

                let match = false;
                if(filter === 'ALL') match = true;
                else if(filter === st) match = true;

                if(match) {
                    const opt = document.createElement('option');
                    opt.value = devId;
                    opt.innerText = `${devId} — [${st}]`;
                    dutDropdown.appendChild(opt);
                }
            }
        }

        function filterDropdown(category, btn) {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderDropdownOptions(category);
            if(dutDropdown.options.length > 0) {
                selectDUT(dutDropdown.options[0].value);
            }
        }

        function selectDUT(id) {
            dutDropdown.value = id;
            const d = deviceDB[id];
            
            const tag = document.getElementById('selectedStatusTag');
            tag.innerText = d.status;

            document.getElementById('forensicCmpTitle').innerText = id;
            const fStatusTitle = document.getElementById('forensicStatusTitle');
            fStatusTitle.innerText = d.status;

            const vBox = document.getElementById('verdictBox');
            const vTitle = document.getElementById('verdictTitle');
            const vDesc = document.getElementById('verdictDesc');

            const elIddqBase = document.getElementById('fIddqBase');
            const elLeakBase = document.getElementById('fLeakBase');
            const elZScore = document.getElementById('fZScore');
            const elTpdBase = document.getElementById('fTpdBase');

            let chipColor = '#00F59B';

            if(d.status === "REJECTED") {
                tag.className = "pill-badge-red";
                fStatusTitle.style.color = "#FF2A5F";
                vBox.style.background = "rgba(255, 42, 95, 0.14)";
                vBox.style.borderColor = "rgba(255, 42, 95, 0.4)";
                vTitle.style.color = "#FF2A5F";
                vTitle.innerText = "CORE VERDICT: CRITICAL ANOMALY (Latent Oxide Breakdown: REJECTED)";
                vDesc.innerText = "Fixed ceiling limit falsely passes this part, but dynamic time-drift detects impending thermal runaway.";
                chipColor = "#FF2A5F";
            } else if(d.status === "RETEST") {
                tag.className = "pill-badge-yellow";
                fStatusTitle.style.color = "#FFB800";
                vBox.style.background = "rgba(255, 184, 0, 0.14)";
                vBox.style.borderColor = "rgba(255, 184, 0, 0.4)";
                vTitle.style.color = "#FFB800";
                vTitle.innerText = "CORE VERDICT: MARGINAL DRIFT (+24h Thermal Retest Required: RETEST)";
                vDesc.innerText = "Drift slope exceeds nominal process variance. Extended thermal stress required to verify stability.";
                chipColor = "#FFB800";
            } else if(d.status === "PASSED") {
                tag.className = "pill-badge-green";
                fStatusTitle.style.color = "#00F59B";
                vBox.style.background = "rgba(0, 245, 155, 0.14)";
                vBox.style.borderColor = "rgba(0, 245, 155, 0.4)";
                vTitle.style.color = "#00F59B";
                vTitle.innerText = "CORE VERDICT: NOMINAL STABILIZATION (Flight Qualified: PASSED)";
                vDesc.innerText = "Telemetry parameters remain tightly clustered within historical 1-sigma distribution.";
                chipColor = "#00F59B";
            } else {
                tag.className = "pill-badge-white";
                fStatusTitle.style.color = "#FFFFFF";
                vBox.style.background = "rgba(148, 163, 184, 0.12)";
                vBox.style.borderColor = "rgba(148, 163, 184, 0.35)";
                vTitle.style.color = "#FFFFFF";
                vTitle.innerText = "CORE VERDICT: IN-QUEUE (Awaiting Next ATE Diagnostic Scan: IN-QUEUE)";
                vDesc.innerText = "Component pre-conditioned in chamber; awaiting scan data.";
                chipColor = "#FFFFFF";
            }

            elIddqBase.style.color = chipColor;
            elLeakBase.style.color = chipColor;
            elZScore.style.color = chipColor;
            elTpdBase.style.color = chipColor;

            document.getElementById('fIddq').innerText = d.iddq;
            document.getElementById('fDrift').innerText = d.drift;
            document.getElementById('fZScore').innerText = `↑ Z-Score: ${d.zscore}`;
            document.getElementById('fLeak').innerText = d.leak;
            document.getElementById('fTpd').innerText = d.tpd;
        }

        renderDropdownOptions('ALL');
        selectDUT("CMP-1004");

        let selectedAction = "Class-S Flight Qualified (PASSED)";
        function setRadio(elem, action) {
            document.querySelectorAll('.radio-option').forEach(el => {
                el.classList.remove('selected');
                el.querySelector('i').className = "fa-regular fa-circle";
                el.querySelector('i').style.color = "";
            });
            elem.classList.add('selected');
            elem.querySelector('i').className = "fa-solid fa-circle-dot";
            elem.querySelector('i').style.color = "#38bdf8";
            selectedAction = action;
        }

        function openCommitModal() {
            document.getElementById('modalDut').innerText = dutDropdown.value.split(' — ')[0];
            document.getElementById('modalAction').innerText = selectedAction;
            document.getElementById('confirmModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('confirmModal').classList.remove('active');
        }

        function downloadTelemetryCSV() {
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Device_ID,Status,IDDQ_uA,Leakage_Current_nA,Temporal_Drift_Rate_Pct,Propagation_Delay_ns\\n";

            for(let i = 0; i < 50; i++) {
                const devId = `CMP-${1001 + i}`;
                const d = deviceDB[devId];
                csvContent += `${devId},${d.status},${d.iddq.replace(' µA','')},${d.leak.replace(' nA','')},${d.drift},${d.tpd.replace(' ns','')}\\n`;
            }

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "ISRO_MIL_STD_883_SCREENING_REPORT.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=1520, scrolling=True)