"""
=====================================================================
 BurnSight Workbench -- Single-file Streamlit app
 AI-Driven Anomaly Detection in Component Burn-In & Screening
 (ISRO SIH Problem Statement 26170)
=====================================================================

WHAT THIS IS
------------
A self-contained Streamlit app -- Module A (dynamic outlier detection)
and Module B (168h drift prediction) run IN-PROCESS, right here, with
no separate FastAPI server. This is deliberate: Streamlit Cloud runs a
single process, so for a deployed Streamlit app, bundling everything
into one file is the correct architecture, not a simplification.

HOW TO RUN LOCALLY
-------------------
    pip install streamlit pandas numpy scikit-learn openpyxl
    streamlit run app.py

HOW TO DEPLOY (Streamlit Cloud)
---------------------------------
Replace your repo's main file with this one (keep the filename your
Streamlit Cloud app already points at, e.g. app.py or streamlit_app.py),
commit, push -- Streamlit Cloud auto-redeploys.

WHAT IT DOES
------------
1. Accepts an uploaded CSV/XLSX burn-in dataset (any schema -- columns
   are auto-detected by finding the 0h/24h/96h/168h checkpoint tokens),
   OR generates a realistic demo dataset on the fly using the same
   datasheet-grounded synthetic generator validated earlier in this
   project (see PARAMETER_CONFIGS below).
2. Module A: per-lot, per-checkpoint modified z-score (median/MAD) --
   flags components that deviate abnormally from their OWN LOT, even
   if still inside an absolute datasheet limit.
3. Module B: trains a RandomForestRegressor per parameter (0h,24h ->
   168h) on a held-out split of the SAME dataset, predicts drift, and
   flags components whose projected drift severity is unsafe.
4. Combines both into a three-tier decision: REJECT / REVIEW / PASS,
   with a plain-language justification per flagged component.
5. If the dataset carries a ground-truth anomaly column, the review
   threshold is calibrated against it (recall-constrained, matching
   the methodology validated earlier in this project). Otherwise it
   falls back to a sensible unsupervised percentile-based threshold.
=====================================================================
"""

import re
from collections import defaultdict

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="BurnSight Workbench", layout="wide", page_icon="\U0001F6F0\uFE0F")

# ===========================================================================
# 1. REAL-DATASHEET-GROUNDED SYNTHETIC GENERATOR (bundled demo/fallback data)
# ===========================================================================
CHECKPOINTS = ["0h", "24h", "96h", "168h"]
CHECKPOINT_HOURS = {"0h": 0, "24h": 24, "96h": 96, "168h": 168}
MAD_SCALE = 0.6745

PARAMETER_CONFIGS = {
    "IDDQ_uA": dict(
        display="IDDQ / Standby Current", unit="uA",
        lot_baseline_range=(5.0, 15.0), start_variation=0.08,
        normal_rate_range=(0.004, 0.015), anomaly_rate_range=(0.08, 0.20),
        anomaly_accel_range=(0.0008, 0.0035), noise_normal=0.25, noise_anomaly=0.8,
        direction="increase", datasheet_limit=80.0, floor=0.1,
    ),
    "leakage_uA": dict(
        display="Leakage Current", unit="uA",
        lot_baseline_range=(2.0, 8.0), start_variation=0.08,
        normal_rate_range=(0.01, 0.05), anomaly_rate_range=(0.15, 0.35),
        anomaly_accel_range=(0.002, 0.006), noise_normal=0.3, noise_anomaly=1.0,
        direction="increase", datasheet_limit=25.0, floor=0.1,
    ),
    "Vt_V": dict(
        display="Threshold Voltage", unit="V",
        lot_baseline_range=(0.45, 0.65), start_variation=0.03,
        normal_rate_range=(0.00003, 0.00015), anomaly_rate_range=(0.0008, 0.0025),
        anomaly_accel_range=(0.00001, 0.00004), noise_normal=0.004, noise_anomaly=0.015,
        direction="increase", datasheet_limit=0.9, floor=0.1,
    ),
    "prop_delay_ns": dict(
        display="Propagation Delay", unit="ns",
        lot_baseline_range=(1.5, 4.0), start_variation=0.06,
        normal_rate_range=(0.001, 0.004), anomaly_rate_range=(0.008, 0.025),
        anomaly_accel_range=(0.0004, 0.0012), noise_normal=0.04, noise_anomaly=0.12,
        direction="increase", datasheet_limit=16.0, floor=0.2,
    ),
    "supply_current_mA": dict(
        display="Supply Current", unit="mA",
        lot_baseline_range=(20.0, 35.0), start_variation=0.06,
        normal_rate_range=(0.008, 0.04), anomaly_rate_range=(0.15, 0.4),
        anomaly_accel_range=(0.0015, 0.005), noise_normal=0.4, noise_anomaly=1.3,
        direction="increase", datasheet_limit=60.0, floor=1.0,
    ),
    "frequency_MHz": dict(
        display="Operating Frequency", unit="MHz",
        lot_baseline_range=(80.0, 120.0), start_variation=0.04,
        normal_rate_range=(-0.015, -0.004), anomaly_rate_range=(-0.30, -0.10),
        anomaly_accel_range=(-0.006, -0.002), noise_normal=0.4, noise_anomaly=1.2,
        direction="decrease", datasheet_limit=60.0, floor=10.0,
    ),
}
PARAM_ANOMALY_CORRELATION = 0.75  # partial correlation: not every parameter drifts on every anomalous part


def _generate_param_trajectory(rng, cfg, lot_baseline, is_anomaly):
    start = max(cfg["floor"], rng.normal(lot_baseline, lot_baseline * cfg["start_variation"]))
    if is_anomaly:
        rate = rng.uniform(*cfg["anomaly_rate_range"])
        accel = rng.uniform(*cfg["anomaly_accel_range"])
        noise_scale = cfg["noise_anomaly"]
    else:
        rate = rng.uniform(*cfg["normal_rate_range"])
        accel = 0.0
        noise_scale = cfg["noise_normal"]
    values = {}
    for cp in CHECKPOINTS:
        t = CHECKPOINT_HOURS[cp]
        drift = rate * t + accel * (t ** 1.5)
        noise = rng.normal(0, noise_scale)
        val = start + drift + noise
        if cfg["direction"] == "increase":
            val = min(val, cfg["datasheet_limit"] * 0.98)
            val = max(val, cfg["floor"])
        else:
            val = max(val, cfg["datasheet_limit"] * 1.02)
        values[cp] = round(float(val), 4)
    return values


def generate_demo_dataset(num_lots: int, parts_per_lot: int, anomaly_rate: float, seed: int = 42) -> pd.DataFrame:
    """Datasheet-grounded synthetic burn-in dataset, wide format:
    one row per component, columns '<Param>_<checkpoint>' plus Lot_ID,
    Component_ID, Anomaly_GroundTruth (kept for optional calibration/scoring).
    Every ground-truth anomaly is guaranteed to manifest on at least one
    parameter (the fix found necessary during earlier large-scale testing)."""
    rng = np.random.default_rng(seed)
    rows = []
    for lot_i in range(num_lots):
        lot_id = f"L{lot_i:04d}"
        lot_baselines = {p: rng.uniform(*cfg["lot_baseline_range"]) for p, cfg in PARAMETER_CONFIGS.items()}
        for part_i in range(parts_per_lot):
            is_anomaly = rng.random() < anomaly_rate
            param_anomalous = {p: (is_anomaly and rng.random() < PARAM_ANOMALY_CORRELATION) for p in PARAMETER_CONFIGS}
            if is_anomaly and not any(param_anomalous.values()):
                forced = rng.choice(list(PARAMETER_CONFIGS.keys()))
                param_anomalous[forced] = True

            row = {"Component_ID": f"{lot_id}_P{part_i:04d}", "Lot_ID": lot_id, "Anomaly_GroundTruth": int(is_anomaly)}
            for param, cfg in PARAMETER_CONFIGS.items():
                traj = _generate_param_trajectory(rng, cfg, lot_baselines[param], param_anomalous[param])
                for cp in CHECKPOINTS:
                    row[f"{param}_{cp}"] = traj[cp]
            rows.append(row)
    return pd.DataFrame(rows)


# ===========================================================================
# 2. SCHEMA AUTO-DETECTION -- works with any wide burn-in CSV, any naming
#    convention, as long as each parameter has a column per checkpoint with
#    a recognizable 0h/24h/96h/168h token somewhere in the column name.
# ===========================================================================
_CHECKPOINT_RE = re.compile(r"(?<![A-Za-z0-9])(0h|24h|96h|168h)(?![A-Za-z0-9])")
_AGGREGATE_PREFIXES = ("lotmean", "lotstd", "lotmedian", "lotmad", "mean_", "std_", "avg_", "median_")


def detect_parameter_columns(columns) -> dict:
    groups = defaultdict(dict)
    for col in columns:
        m = _CHECKPOINT_RE.search(str(col))
        if not m:
            continue
        cp = m.group(1)
        base = (col[:m.start()] + col[m.end():]).strip("_").replace("__", "_")
        if not base:
            continue
        if base.lower().startswith(_AGGREGATE_PREFIXES):
            continue  # pre-computed lot-level statistic, not a raw per-component parameter
        groups[base][cp] = col
    return {base: cps for base, cps in groups.items() if all(k in cps for k in CHECKPOINTS)}


def detect_lot_column(df: pd.DataFrame):
    for candidate in ["Lot_ID", "LotID", "lot_id", "Lot", "lot"]:
        if candidate in df.columns:
            return candidate
    return None


def detect_ground_truth_column(df: pd.DataFrame):
    for candidate in ["Anomaly_GroundTruth", "GroundTruth", "is_anomaly", "Anomaly", "Label"]:
        if candidate in df.columns:
            return candidate
    return None


# ===========================================================================
# 3. MODULE A -- dynamic outlier detection (per-lot median/MAD)
# ===========================================================================
def modified_z_scores(values: np.ndarray):
    median = np.median(values)
    mad = np.median(np.abs(values - median))
    if mad == 0:
        mad = 1e-6
    return MAD_SCALE * (values - median) / mad, median, mad


def compute_module_a_signal(df: pd.DataFrame, param_groups: dict, lot_col: str):
    """Per-part MAX modified z-score across all (parameter, checkpoint),
    computed per lot. Returns (signal Series, reason Series)."""
    max_signal = pd.Series(0.0, index=df.index)
    reason = pd.Series("", index=df.index)

    if lot_col is None:
        return max_signal, reason  # Module A needs lot context; skip gracefully

    for base, cps in param_groups.items():
        for cp in CHECKPOINTS:
            col = cps[cp]
            for lot_id, group in df.groupby(lot_col):
                values = group[col].to_numpy(dtype=float)
                if len(values) < 5:
                    continue
                z, median, mad = modified_z_scores(values)
                abs_z = np.abs(z)
                idx = group.index
                improved = abs_z > max_signal.loc[idx].to_numpy()
                if improved.any():
                    upd_idx = idx[improved]
                    max_signal.loc[upd_idx] = abs_z[improved]
                    for i, v, azv in zip(upd_idx, group.loc[upd_idx, col], abs_z[improved]):
                        reason.loc[i] = f"{base}@{cp}: {v:.3f} is {azv:.1f}x lot deviation (median={median:.3f})"
    return max_signal, reason


# ===========================================================================
# 4. MODULE B -- per-parameter drift predictor (RandomForestRegressor)
# ===========================================================================
def train_module_b(df: pd.DataFrame, param_groups: dict, directions: dict, test_size: float = 0.2):
    """Trains one regressor per parameter on an 80/20 split of the
    dataset. Returns (models dict, metrics dict)."""
    models, metrics = {}, {}
    n = len(df)
    if n < 20:
        test_size = 0.0  # too small to split meaningfully

    for base, cps in param_groups.items():
        c0, c24, c168 = cps["0h"], cps["24h"], cps["168h"]
        X = np.column_stack([
            df[c0].to_numpy(float), df[c24].to_numpy(float),
            (df[c24].to_numpy(float) - df[c0].to_numpy(float)) / 24.0,
        ])
        y = df[c168].to_numpy(float)
        sign = 1.0 if directions.get(base, "increase") == "increase" else -1.0

        if test_size > 0:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        else:
            X_train, y_train = X, y
            X_test, y_test = X, y

        model = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42, min_samples_leaf=3)
        model.fit(X_train, y_train)
        pred_test = model.predict(X_test)
        mae = mean_absolute_error(y_test, pred_test)
        r2 = r2_score(y_test, pred_test) if len(set(y_test)) > 1 else float("nan")

        train_slopes = sign * (y_train - X_train[:, 1]) / (168 - 24)
        scale = max(np.percentile(np.abs(train_slopes), 95), 1e-9)

        models[base] = {"model": model, "sign": sign, "scale": scale}
        metrics[base] = {"MAE": round(float(mae), 4), "R2": round(float(r2), 4) if not np.isnan(r2) else None,
                          "n_train": len(X_train), "n_test": len(X_test)}
    return models, metrics


def compute_module_b_signal(df: pd.DataFrame, param_groups: dict, models: dict):
    max_signal = pd.Series(0.0, index=df.index)
    reason = pd.Series("", index=df.index)
    predicted_168h = {}

    for base, cps in param_groups.items():
        if base not in models:
            continue
        info = models[base]
        c0, c24 = cps["0h"], cps["24h"]
        X = np.column_stack([
            df[c0].to_numpy(float), df[c24].to_numpy(float),
            (df[c24].to_numpy(float) - df[c0].to_numpy(float)) / 24.0,
        ])
        y_pred = info["model"].predict(X)
        predicted_168h[base] = y_pred
        slope = info["sign"] * (y_pred - X[:, 1]) / (168 - 24)
        severity = np.abs(slope) / info["scale"]

        improved = severity > max_signal.to_numpy()
        if improved.any():
            idx = df.index[improved]
            max_signal.loc[idx] = severity[improved]
            for i, pv, sv in zip(idx, y_pred[improved], severity[improved]):
                reason.loc[i] = f"{base}: predicted 168h={pv:.3f}, drift severity {sv:.2f}x normal scale"
    return max_signal, reason, predicted_168h


# ===========================================================================
# 5. COMBINED SIGNAL + THRESHOLD CALIBRATION
# ===========================================================================
def calibrate_and_classify(df, combined_signal, gt_col, margin, reject_frac=0.98):
    """If ground truth is present, calibrate against it (recall-constrained,
    same method validated earlier in this project). Otherwise fall back to
    an unsupervised percentile-based threshold."""
    if gt_col is not None and df[gt_col].nunique() > 1:
        anomaly_signals = combined_signal[df[gt_col] == 1]
        if len(anomaly_signals) > 0:
            anomaly_min = anomaly_signals.min()
            reject_threshold = anomaly_min * reject_frac
            review_threshold = anomaly_min * margin
            method = "supervised (calibrated against ground truth)"
            return review_threshold, reject_threshold, method
    # Unsupervised fallback: treat the top ~1%/3% of signal as reject/review.
    reject_threshold = float(np.percentile(combined_signal, 99))
    review_threshold = float(np.percentile(combined_signal, 97))
    method = "unsupervised (percentile-based, no ground truth available)"
    return review_threshold, reject_threshold, method


def classify(signal, review_threshold, reject_threshold):
    return np.where(signal >= reject_threshold, "REJECT", np.where(signal >= review_threshold, "REVIEW", "PASS"))


# ===========================================================================
# 6. STREAMLIT UI
# ===========================================================================
st.title("\U0001F6F0\uFE0F BurnSight Workbench")
st.caption("AI-Driven Anomaly Detection in Component Burn-In & Screening \u2014 SIH Problem Statement 26170")

with st.sidebar:
    st.header("1. Data")
    uploaded = st.file_uploader("Upload burn-in dataset (CSV or XLSX)", type=["csv", "xlsx"])

    st.markdown("**No file?** Generate a realistic demo dataset:")
    demo_lots = st.slider("Demo lots", 5, 100, 20)
    demo_parts_per_lot = st.slider("Parts per lot", 20, 1000, 200)
    demo_rate = st.slider("Demo anomaly rate", 0.01, 0.30, 0.08, step=0.01)
    generate_demo = st.button("Generate demo dataset", use_container_width=True)

    st.header("2. Calibration")
    margin = st.slider(
        "Review-tier safety margin", 0.30, 0.98, 0.75, step=0.05,
        help="Lower = wider review net (fewer misses, more manual review). "
             "0.75 was the value validated earlier in this project at large scale.",
    )

if "df" not in st.session_state:
    st.session_state.df = None

if uploaded is not None:
    try:
        if uploaded.name.endswith(".xlsx"):
            st.session_state.df = pd.read_excel(uploaded)
        else:
            st.session_state.df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}")

if generate_demo:
    st.session_state.df = generate_demo_dataset(demo_lots, demo_parts_per_lot, demo_rate)

df = st.session_state.df

if df is None:
    st.info("Upload a dataset or generate a demo dataset from the sidebar to begin.")
    st.markdown(
        "**Expected format:** one row per component, with a column per parameter per checkpoint "
        "(0h / 24h / 96h / 168h somewhere in each column name -- e.g. `IDDQ_uA_0h` or `Iddq_0h_uA` both work). "
        "A `Lot_ID` column enables Module A. An optional ground-truth anomaly column enables calibrated thresholds."
    )
    st.stop()

st.success(f"Loaded {len(df)} components.")

param_groups = detect_parameter_columns(df.columns)
lot_col = detect_lot_column(df)
gt_col = detect_ground_truth_column(df)

if not param_groups:
    st.error(
        "No parameter columns detected. Each parameter needs four columns whose names contain "
        "0h, 24h, 96h, and 168h respectively (e.g. `Leakage_0h`, `Leakage_24h`, `Leakage_96h`, `Leakage_168h`)."
    )
    st.stop()

st.write(f"**Detected {len(param_groups)} parameters:** {', '.join(param_groups.keys())}")
st.write(f"**Lot column:** {lot_col or 'not found -- Module A will be skipped'}")
st.write(f"**Ground truth column:** {gt_col or 'not found -- using unsupervised threshold'}")

with st.expander("Parameter direction (which way is degradation?)"):
    st.caption("Most parameters get worse by increasing. Mark any that get worse by DECREASING (e.g. operating frequency).")
    directions = {}
    cols = st.columns(3)
    for i, base in enumerate(param_groups):
        default_decrease = "freq" in base.lower()
        with cols[i % 3]:
            is_decrease = st.checkbox(f"{base} decreases = worse", value=default_decrease, key=f"dir_{base}")
        directions[base] = "decrease" if is_decrease else "increase"

run = st.button("\u25B6 Run Analysis", type="primary", use_container_width=True)

if run:
    with st.spinner("Training Module B and scoring Module A..."):
        sig_a, reason_a = compute_module_a_signal(df, param_groups, lot_col)
        models, metrics = train_module_b(df, param_groups, directions)
        sig_b, reason_b, predicted_168h = compute_module_b_signal(df, param_groups, models)

        combined = pd.Series(np.maximum(sig_a.to_numpy(), sig_b.to_numpy()), index=df.index)
        review_threshold, reject_threshold, method = calibrate_and_classify(df, combined, gt_col, margin)
        tier = classify(combined.to_numpy(), review_threshold, reject_threshold)

        reason = np.where(sig_a.to_numpy() >= sig_b.to_numpy(), reason_a.to_numpy(), reason_b.to_numpy())

        results = df.copy()
        results["combined_signal"] = combined.round(3)
        results["tier"] = tier
        results["reason"] = reason

    st.session_state.results = results
    st.session_state.metrics = metrics
    st.session_state.thresholds = (review_threshold, reject_threshold, method)

if "results" in st.session_state:
    results = st.session_state.results
    metrics = st.session_state.metrics
    review_threshold, reject_threshold, method = st.session_state.thresholds

    st.divider()
    st.subheader("Results")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total components", len(results))
    c2.metric("REJECT", int((results["tier"] == "REJECT").sum()))
    c3.metric("REVIEW", int((results["tier"] == "REVIEW").sum()))
    c4.metric("PASS", int((results["tier"] == "PASS").sum()))

    st.caption(f"Threshold method: {method} \u2014 review={review_threshold:.3f}, reject={reject_threshold:.3f}")

    if gt_col is not None and results[gt_col].nunique() > 1:
        missed = int(((results["tier"] == "PASS") & (results[gt_col] == 1)).sum())
        total_anom = int((results[gt_col] == 1).sum())
        st.metric("Missed anomalies (auto-passed but ground-truth positive)", f"{missed} / {total_anom}")

    tab1, tab2, tab3 = st.tabs(["Flagged components", "All results", "Module B accuracy"])

    with tab1:
        flagged = results[results["tier"] != "PASS"].sort_values("combined_signal", ascending=False)
        st.dataframe(
            flagged[[c for c in ["Component_ID", lot_col, "tier", "combined_signal", "reason"] if c and c in flagged.columns]],
            use_container_width=True, height=420,
        )
        st.download_button("Download flagged components (CSV)", flagged.to_csv(index=False), "flagged_components.csv")

    with tab2:
        st.dataframe(results, use_container_width=True, height=420)
        st.download_button("Download full results (CSV)", results.to_csv(index=False), "burnsight_results.csv")

    with tab3:
        metrics_df = pd.DataFrame(metrics).T
        metrics_df.index.name = "parameter"
        st.dataframe(metrics_df, use_container_width=True)
        st.caption("MAE / R\u00b2 measured on a held-out 20% split of the uploaded dataset for each parameter's 168h prediction.")

    st.divider()
    st.bar_chart(results["tier"].value_counts())
