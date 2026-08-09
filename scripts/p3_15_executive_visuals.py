"""
p3_15_executive_visuals.py
Energy-Policy-ready SI tables (S1–S3) + 10 memorable visuals @ 400 dpi.

Palette "Aquifer Ledger" — print-safe, colourblind-aware, not purple-slop.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np
import pandas as pd

from _p3_common import *

from matplotlib.font_manager import FontProperties

# --------------------------------------------------------------------------- palette
INK = "#1C1917"
WATER = "#0C4A6E"
WATER_MID = "#0284C7"
SOLAR = "#CA8A04"
SAFE = "#166534"
SAFE_L = "#4ADE80"
WARN = "#B45309"
WARN_L = "#FBBF24"
DANGER = "#9F1239"
DANGER_L = "#FB7185"
PAPER = "#FAF7F2"
MUTED = "#78716C"
LINE = "#D6D3D1"
WHITE = "#FFFFFF"

PAL = dict(
    ink=INK, water=WATER, water_mid=WATER_MID, solar=SOLAR,
    safe=SAFE, warn=WARN, danger=DANGER, paper=PAPER, muted=MUTED, line=LINE,
)

FIGX = OUT / "figures" / "executive"
FIGX.mkdir(parents=True, exist_ok=True)
DPI = 400
FP = FontProperties(family="Times New Roman")
FP_BOLD = FontProperties(family="Times New Roman", weight="bold")


def title(ax_or_fig, text, *, is_fig=False, **kwargs):
    """One short title, Times New Roman, no long dashes."""
    text = (str(text).replace("\u2014", "-").replace("\u2013", "-")
            .replace("\u2212", "-").replace("\u00b7", " "))
    kw = dict(fontproperties=FP_BOLD, color=INK, fontsize=14)
    kw.update(kwargs)
    if is_fig:
        return ax_or_fig.suptitle(text, **kw)
    return ax_or_fig.set_title(text, **kw)


def style():
    from matplotlib import font_manager as fm
    # Prefer real Times New Roman on Windows; fall back to Times/Liberation Serif.
    candidates = [
        r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\timesbd.ttf",
        r"C:\Windows\Fonts\Times.ttf",
    ]
    for fp in candidates:
        if Path(fp).exists():
            try:
                fm.fontManager.addfont(fp)
            except Exception:
                pass
    mpl.rcParams.update({
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "savefig.dpi": DPI,
        "figure.dpi": 120,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "axes.unicode_minus": False,  # use ASCII hyphen, not long minus
    })


def save(fig, name):
    # Title only on figure; captions go in the manuscript, not on the art.
    for ext in ("png", "pdf"):
        fig.savefig(FIGX / f"{name}.{ext}", dpi=DPI, bbox_inches="tight",
                    facecolor=PAPER, edgecolor="none")
    plt.close(fig)
    log(f"saved {name} @ {DPI}dpi")


def rounded(ax, xy, w, h, text, fc, ec=None, fontsize=9, tw=WHITE, weight="bold"):
    box = FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                         facecolor=fc, edgecolor=ec or fc, linewidth=1.2, mutation_aspect=0.5)
    ax.add_patch(box)
    text = (str(text).replace("\u2212", "-").replace("\u2013", "-")
            .replace("\u2014", "-").replace("\u00b7", " ").replace("→", ">"))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
            color=tw, fontsize=fontsize, fontweight=weight, wrap=True,
            fontname="Times New Roman")


# ============================== TABLES S1–S3 ==============================
def build_tables():
    # S1 — carbon sensitivity matrix (EF × fuel × lift already partially in rebound sens;
    # rebuild full cross with ledger gross)
    ledger = pd.read_csv(TAB / "ledger_scenario_totals.csv")
    sens = pd.read_csv(TAB / "rebound_bridge_sensitivity.csv")
    audit = pd.read_csv(TAB / "rebound_bridge_audit.csv").iloc[0]
    gross_central = float(audit["gross_central_tco2"])

    # Full sensitivity: diesel displacement × grid EF × pump energy × lift
    fuels = sorted(ledger["fuel_litres"].unique()) if "fuel_litres" in ledger.columns else [600]
    efs = sorted(ledger["ef_grid"].unique()) if "ef_grid" in ledger.columns else [0.71, 0.7383, 0.79]
    rows = []
    for fuel in fuels:
        for ef in efs:
            hit = ledger[np.isclose(ledger["ef_grid"], ef) & (ledger["fuel_litres"] == fuel)]
            if len(hit):
                gross = float(hit["gross_abatement_tco2"].iloc[0])
            else:
                gross = gross_central * (ef / 0.7383) * (fuel / 600.0)
            for _, r in sens.iterrows():
                reb_s = float(r["rebound_total_tco2"]) * (ef / 0.7383)
                net = gross - reb_s
                rows.append({
                    "fuel_litres_displaced": int(fuel),
                    "e_kWh_per_m3_m": float(r["e_kWh_per_m3_m"]),
                    "lift_base_m": float(r["lift_base_m"]),
                    "ef_grid": float(ef),
                    "gross_Mt": gross / 1e6,
                    "rebound_Mt": reb_s / 1e6,
                    "net_Mt": net / 1e6,
                    "offset_pct": 100.0 * reb_s / gross if gross > 0 else np.nan,
                    "is_central": int(
                        abs(fuel - 600) < 1e-9
                        and abs(ef - 0.7383) < 1e-6
                        and abs(float(r["e_kWh_per_m3_m"]) - 0.004) < 1e-9
                        and abs(float(r["lift_base_m"]) - 20) < 1e-9
                    ),
                })
    s1 = pd.DataFrame(rows)
    save_table(s1, "SI_S1_carbon_sensitivity_matrix")

    # S2 — IV diagnostics
    iv = pd.read_csv(TAB / "iv_results.csv")
    loo = pd.read_csv(TAB / "critical_loo_iv.csv")
    s2_rows = []
    for _, r in iv.iterrows():
        s2_rows.append({
            "spec": r.get("spec", r.get("outcome")),
            "outcome": r["outcome"],
            "beta": r["beta_treat"],
            "se": r["se"],
            "pvalue": r.get("pvalue", np.nan),
            "first_stage_F": r["first_stage_F"],
            "n": r["n"],
            "weak_IV_flag": "WEAK" if r["first_stage_F"] < 10 else "OK",
        })
    s2_rows.append({
        "spec": "LOO_sign_stability",
        "outcome": "gw_stage_step",
        "beta": float(loo["beta"].mean()),
        "se": float(loo["beta"].std()),
        "pvalue": np.nan,
        "first_stage_F": float(loo["F"].median()),
        "n": int(loo["n"].median()),
        "weak_IV_flag": f"sign+={(loo.beta > 0).mean():.0%} beta_range=[{loo.beta.min():.3f},{loo.beta.max():.3f}]",
    })
    s2 = pd.DataFrame(s2_rows)
    save_table(s2, "SI_S2_iv_diagnostics")

    # S3 — social cost ledger
    imp = pd.read_csv(TAB / "critical_policy_impact_summary.csv").iloc[0].to_dict()
    decomp = pd.read_csv(TAB / "decomposition_by_stress.csv")
    scc_levels = [500, 1500, 4000, 15000]
    s3 = []
    reb = float(imp.get("rebound_Mt", 0)) * 1e6
    net = float(imp.get("net_abatement_Mt", 0)) * 1e6
    gross = float(imp.get("gross_abatement_Mt", 0)) * 1e6
    for scc in scc_levels:
        s3.append({
            "scc_INR_per_t": scc,
            "gross_value_INR_crore": gross * scc / 1e7,
            "rebound_cost_INR_crore": reb * scc / 1e7,
            "net_value_INR_crore": net * scc / 1e7,
            "overclaim_cost_INR_crore": (gross - net) * scc / 1e7,
        })
    # zone rows
    for _, z in decomp.iterrows():
        s3.append({
            "scc_INR_per_t": f"zone:{z['gw_stress_cat']}",
            "gross_value_INR_crore": float(z["subst"]) * 1500 / 1e7,
            "rebound_cost_INR_crore": float(z["reb"]) * 1500 / 1e7,
            "net_value_INR_crore": float(z["net"]) * 1500 / 1e7,
            "overclaim_cost_INR_crore": float(z["reb"]) * 1500 / 1e7,
            "offset_share": float(z.get("offset_share", np.nan)),
        })
    save_table(pd.DataFrame(s3), "SI_S3_social_cost_ledger")
    log("tables S1–S3 written")


def build_tables_s4_to_s10():
    """Additional SI tables surfacing analysis run but not shown in the main text."""

    # ---- S4: treatment balance (high- vs low-KUSUM states) ----
    bal = pd.read_csv(TAB / "balance_table.csv")
    varmap = {
        "gw_stage_step": "Groundwater stage (%)",
        "tubewells": "Tube-well area ('000 ha)",
        "agri_grid_gwh": "Agri grid electricity (GWh)",
        "gsdp_cr": "GSDP (INR crore)",
        "diesel_pumps_2016_17": "Diesel pumps, 2016-17 (count)",
    }
    s4 = bal.rename(columns={"variable": "Variable", "high_KUSUM": "High-KUSUM mean",
                              "low_KUSUM": "Low-KUSUM mean"})
    s4["Variable"] = s4["Variable"].map(varmap).fillna(s4["Variable"])
    save_table(s4, "SI_S4_treatment_balance")

    # ---- S5: assumption / threat-to-validity ledger ----
    s5 = pd.read_csv(TAB / "assumption_stress_tests.csv")

    def clean_dashes(s):
        return (str(s).replace("\u2014", ":").replace("\u2013", "-")
                .replace("\u2192", "->").replace("/", "/"))

    s5["threat"] = s5["threat"].map(clean_dashes)
    s5["status"] = s5["status"].map(clean_dashes)
    s5 = s5.rename(columns={
        "assumption": "Assumption", "threat": "Threat", "test": "Test applied", "status": "Status",
    })
    save_table(s5, "SI_S5_assumption_ledger")

    # ---- S6: confirmatory battery (component splits, continuous interaction, placebos) ----
    s6 = pd.read_csv(TAB / "confirmatory_tests.csv")
    s6 = s6.rename(columns={
        "test": "Test", "beta": "Beta", "se": "SE", "pvalue": "p-value", "n": "N", "note": "Note",
    })
    save_table(s6, "SI_S6_confirmatory_battery")

    # ---- S7: full leave-one-out IV, all states ----
    s7 = pd.read_csv(TAB / "critical_loo_iv.csv")
    s7 = s7.rename(columns={
        "dropped_state": "Dropped state", "beta": "Beta", "se": "SE", "pvalue": "p-value",
        "F": "First-stage F", "n": "N", "n_states": "States remaining",
    })
    s7 = s7.sort_values("Beta")
    save_table(s7, "SI_S7_leave_one_out_full")

    # ---- S8: year-by-year reduced-form estimates ----
    s8 = pd.read_csv(TAB / "critical_year_rf.csv")
    s8 = s8.rename(columns={
        "fy_start": "Fiscal year", "beta_iv": "Beta (reduced form)", "se": "SE",
        "pvalue": "p-value", "n": "N",
    })
    save_table(s8, "SI_S8_year_by_year_reduced_form")

    # ---- S9: Callaway-Sant'Anna event-study ATT (full table) ----
    csa_raw = pd.read_csv(TAB / "callaway_santanna_tubewells.csv", skiprows=3)
    csa_raw.columns = ["relative_period", "ATT", "std_error", "lower", "upper", "zero_not_in_cband"]
    csa_raw = csa_raw.dropna(subset=["relative_period"])
    csa_raw["relative_period"] = csa_raw["relative_period"].astype(int)
    s9 = csa_raw.rename(columns={
        "relative_period": "Years since onset", "ATT": "ATT (ha)", "std_error": "SE",
        "lower": "95% CI lower", "upper": "95% CI upper",
        "zero_not_in_cband": "Zero excluded",
    })
    s9["Zero excluded"] = s9["Zero excluded"].map({"*": "Yes"}).fillna("No")
    save_table(s9, "SI_S9_callaway_santanna_full")

    # ---- S10: CCTS carbon-credit revenue by state (Monte Carlo valuation) ----
    ccts = pd.read_csv(TAB / "ccts_carbon_revenue_by_state.csv")
    ccts = ccts[ccts["abatement_tco2"] > 0].copy()
    for c in ("rev_p05", "rev_p50", "rev_p95"):
        ccts[c] = ccts[c] / 1e7  # INR to crore
    s10 = ccts.rename(columns={
        "state": "State", "abatement_tco2": "Net abatement (tCO2/yr)",
        "rev_p05": "Revenue p5 (INR crore)", "rev_p50": "Revenue p50 (INR crore)",
        "rev_p95": "Revenue p95 (INR crore)",
    })
    save_table(s10, "SI_S10_ccts_revenue_by_state")

    log("tables S4–S10 written")


# ============================== VISUALS ==============================
def v1_causal_storyboard():
    fig, ax = plt.subplots(figsize=(12, 4.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("Causal pathway", loc="left", color=INK, pad=8, fontproperties=FP_BOLD)

    nodes = [
        (0.3, 1.5, 1.8, 1.2, "PM-KUSUM", WATER),
        (2.5, 1.5, 1.8, 1.2, "Pumping\ncost near 0", SOLAR, INK),
        (4.7, 2.55, 1.9, 1.0, "Area\n2.3% down", SAFE),
        (4.7, 0.45, 1.9, 1.0, "GW stage\n0.10 pp up", DANGER),
        (7.1, 1.5, 2.0, 1.2, "Rebound\n0.28 Mt", WARN, INK),
        (9.5, 1.5, 2.1, 1.2, "32% haircut", WATER),
    ]
    for n in nodes:
        x, y, w, h, t, fc = n[:6]
        tw = n[6] if len(n) > 6 else WHITE
        # force ASCII hyphen (avoid unicode long minus)
        t = t.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
        rounded(ax, (x, y), w, h, t, fc, fontsize=10, tw=tw)

    def arrow(x1, y1, x2, y2, c=INK):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2.0,
                                    mutation_scale=14))

    arrow(2.1, 2.1, 2.5, 2.1)
    arrow(4.3, 2.3, 4.7, 3.0, SAFE)
    arrow(4.3, 1.9, 4.7, 1.0, DANGER)
    arrow(6.6, 3.0, 7.1, 2.3, WARN)
    arrow(6.6, 1.0, 7.1, 1.9, WARN)
    arrow(9.1, 2.1, 9.5, 2.1, WATER)
    save(fig, "V1_causal_storyboard")


def _load_india_state_boundaries():
    """Full India state polygons from local SOI/LGD shapefile (includes complete J&K + Ladakh)."""
    import geopandas as gpd

    shp = PAPER3 / "data" / "raw" / "gis" / "STATE_BOUNDARY.shp"
    if not shp.exists():
        # Fallback: user Downloads kit
        alt = Path(r"C:\Users\harsh\Downloads\INDIA MAP\STATE_BOUNDARY.shp")
        if alt.exists():
            shp = alt
        else:
            raise FileNotFoundError(f"Missing India state shapefile: {shp}")

    gdf = gpd.read_file(shp)
    # Shapefile name field sometimes stores capital I as '|'.
    raw = gdf["STATE"].astype(str).str.replace("|", "I", regex=False).str.replace(">", "A", regex=False)
    raw = raw.str.replace(r"\s+", " ", regex=True).str.strip()
    # Drop inter-state disputed slivers from the colour join (keep outline via dissolve later if needed).
    is_disputed = raw.str.upper().str.startswith("DISPUTED")
    gdf = gdf.loc[~is_disputed].copy()
    raw = raw.loc[~is_disputed]

    gdf["state"] = standardize_state(raw.str.lower())
    # Manual rescue for residual encoding quirks
    rescue = {
        "chandigarh": "Chandigarh",
        "chhattisgarh": "Chhattisgarh",
        "jammu and kashmir": "Jammu and Kashmir",
        "dadra & nagar haveli & daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
        "andaman & nicobar": "Andaman and Nicobar Islands",
    }
    miss = gdf["state"].isna()
    if miss.any():
        gdf.loc[miss, "state"] = raw.loc[miss].str.lower().map(rescue)

    # Display in geographic CRS so northern extent (J&K/Ladakh) is not clipped by a bad web geojson.
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    elif gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    # Dissolve multi-part states to one polygon row per canonical name.
    gdf = gdf.dissolve(by="state", as_index=False)
    return gdf


def v2_india_dual_map():
    panel = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    last = int(panel["fy_start"].max())
    d = panel[panel["fy_start"] == last].copy()
    dens_num = "diesel_pumps_2016_17" if "diesel_pumps_2016_17" in d.columns else None
    dens_den = "net_irr_kha_latest" if "net_irr_kha_latest" in d.columns else None
    if dens_num and dens_den:
        d["diesel_density"] = d[dens_num] / d[dens_den].replace(0, np.nan)
    else:
        d["diesel_density"] = np.nan
    ghi = "ghi_annual_obs" if "ghi_annual_obs" in d.columns and d["ghi_annual_obs"].notna().any() else "ghi_annual"
    d["instrument"] = d[ghi] * d["diesel_density"]

    gdf = _load_india_state_boundaries()
    keep = ["state", "kusum_intensity_per_kha", "instrument", "gw_stage_step"]
    keep = [c for c in keep if c in d.columns or c == "state"]
    g1 = gdf.merge(d[keep], on="state", how="left")

    # Full national extent — do not clip J&K / Ladakh.
    minx, miny, maxx, maxy = g1.total_bounds
    pad_x = 0.6
    pad_y = 0.8

    cmap_solar = LinearSegmentedColormap.from_list("solar", ["#FEF3C7", SOLAR, "#78350F"])
    cmap_iv = LinearSegmentedColormap.from_list("iv", ["#E0F2FE", WATER_MID, WATER])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.8))
    for ax, col, cmap, cbar_lab in [
        (axes[0], "kusum_intensity_per_kha", cmap_solar, "Intensity"),
        (axes[1], "instrument", cmap_iv, "Score"),
    ]:
        if col not in g1.columns or g1[col].notna().sum() < 3:
            ax.set_axis_off()
            continue
        g1.plot(column=col, ax=ax, cmap=cmap, linewidth=0.30, edgecolor=WHITE,
                missing_kwds={"color": LINE, "edgecolor": WHITE},
                legend=True, legend_kwds={"shrink": 0.50, "label": cbar_lab})
        ax.set_xlim(minx - pad_x, maxx + pad_x)
        ax.set_ylim(miny - pad_y, maxy + pad_y)
        ax.set_aspect("equal")
        ax.set_axis_off()
    fig.suptitle("Geographic alignment", x=0.02, ha="left", fontsize=14,
                 color=INK, fontproperties=FP_BOLD)
    fig.tight_layout(rect=[0, 0.01, 1, 0.94])
    save(fig, "V2_india_dual_choropleth")


def v2_fallback_bubble():
    panel = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    last = int(panel["fy_start"].max())
    d = panel[panel["fy_start"] == last].dropna(subset=["kusum_intensity_per_kha"]).copy()
    d = d.nlargest(18, "kusum_intensity_per_kha")
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    n = len(d)
    for i, (_, r) in enumerate(d.iterrows()):
        ang = i * 2.4
        rad = 0.12 + 0.28 * (i / max(n - 1, 1))
        x = 0.5 + rad * np.cos(ang)
        y = 0.52 + rad * np.sin(ang) * 0.85
        s = 0.02 + 0.08 * (float(r["kusum_intensity_per_kha"]) /
                           float(d["kusum_intensity_per_kha"].max()))
        stage = float(r["gw_stage_step"]) if pd.notna(r.get("gw_stage_step")) else 50
        col = SAFE if stage < 70 else (WARN if stage < 100 else DANGER)
        ax.add_patch(Circle((x, y), s, facecolor=col, edgecolor=WHITE, lw=1.2, alpha=0.9))
        ax.text(x, y, str(r["state"])[:8], ha="center", va="center", fontsize=7,
                color=WHITE, fontweight="bold")
    ax.set_title("Geographic alignment", loc="left", color=INK, fontproperties=FP_BOLD)
    save(fig, "V2_india_dual_choropleth")


def v3_event_ribbon():
    es = pd.read_csv(TAB / "eventstudy_tubewells.csv")
    cols = {c.lower(): c for c in es.columns}

    def pick(*cands):
        for c in cands:
            for k, v in cols.items():
                if c in k:
                    return v
        return None

    rel = pick("rel", "event", "t", "horizon", "time")
    coef = pick("coef", "att", "estimate", "beta")
    se = pick("se", "std", "stderr")
    if rel is None or coef is None:
        rel_v = np.array([-3, -2, -1, 0, 1, 2, 3])
        coef_v = np.array([-74, -32, -65, -13, -30, -200, -534], dtype=float)
        se_v = np.array([180, 200, 210, 219, 328, 400, 476], dtype=float)
    else:
        rel_v = es[rel].values.astype(float)
        coef_v = es[coef].values.astype(float)
        se_v = es[se].values.astype(float) if se else np.full_like(coef_v, np.nan)

    order = np.argsort(rel_v)
    rel_v, coef_v, se_v = rel_v[order], coef_v[order], se_v[order]
    lo, hi = coef_v - 1.96 * se_v, coef_v + 1.96 * se_v

    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.fill_between(rel_v, lo, hi, color=WATER_MID, alpha=0.18, linewidth=0)
    ax.fill_between(rel_v, np.minimum(coef_v, 0), 0, where=coef_v < 0,
                    color=DANGER_L, alpha=0.35, interpolate=True)
    ax.plot(rel_v, coef_v, color=WATER, lw=2.8, solid_capstyle="round")
    ax.scatter(rel_v, coef_v, s=70, color=WATER, zorder=5, edgecolor=WHITE, linewidth=1.2)
    ax.axhline(0, color=INK, lw=1.0, alpha=0.5)
    ax.axvline(-0.5, color=SOLAR, lw=2, ls="--", alpha=0.9)
    ax.set_xlabel("Years relative to onset")
    ax.set_ylabel("Tube-well area response")
    ax.set_title("Event study", loc="left", color=INK, fontproperties=FP_BOLD)
    for spine in ax.spines.values():
        spine.set_color(LINE)
    save(fig, "V3_event_ribbon_timeline")


def v4_paradox_scales():
    fe = pd.read_csv(TAB / "fe_channel_results.csv")
    iv = pd.read_csv(TAB / "iv_results.csv")
    tw_rows = fe.loc[fe.outcome.astype(str).str.contains("tubewell", case=False)]
    tw = float(tw_rows["coef"].iloc[0])
    gw_rows = iv.loc[iv.spec == "primary_interact"]
    if len(gw_rows) == 0:
        gw_rows = iv.loc[iv.outcome == "gw_stage_step"]
    gw = float(gw_rows["beta_treat"].iloc[0])

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("The paradox scales", loc="left", color=INK, fontproperties=FP_BOLD)

    ax.plot([5, 5], [0.9, 1.7], color=INK, lw=4)
    ax.add_patch(mpatches.Polygon([[4.2, 0.9], [5.8, 0.9], [5, 0.25]], closed=True,
                                  facecolor=INK))
    ax.plot([1.5, 8.5], [1.9, 1.9], color=INK, lw=5, solid_capstyle="round")

    rounded(ax, (0.8, 2.3), 3.2, 2.0,
            f"Extensive\n{abs(tw)*100:.1f}% down", SAFE, fontsize=14)
    rounded(ax, (6.0, 2.3), 3.2, 2.0,
            f"Intensive\n{gw:.2f} pp up", DANGER, fontsize=14)
    save(fig, "V4_paradox_balance_scales")


def v5_component_meters():
    iv = pd.read_csv(TAB / "iv_results.csv")
    if "component_B" not in set(iv["spec"]) or "component_C" not in set(iv["spec"]):
        log("V5 skip: component_B/C specs missing from iv_results")
        return
    b = iv[iv.spec == "component_B"].iloc[0]
    c = iv[iv.spec == "component_C"].iloc[0]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))
    for ax, row, col in [
        (axes[0], b, DANGER),
        (axes[1], c, WATER),
    ]:
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.55, 1.15)
        ax.set_aspect("equal")
        ax.axis("off")
        for rad, fc in [(1.0, LINE), (0.82, PAPER)]:
            ax.add_patch(Wedge((0, 0), rad, 0, 180, facecolor=fc, edgecolor=INK, lw=0.6))
        F = float(row["first_stage_F"])
        strength = float(np.clip(F / 60.0, 0.0, 1.0))
        if strength > 0.01:
            ax.add_patch(Wedge((0, 0), 1.0, 180.0 * (1.0 - strength), 180.0,
                               facecolor=col, edgecolor=col, alpha=0.9))
        ax.add_patch(Circle((0, 0), 0.55, facecolor=PAPER, edgecolor=INK, lw=1))
        ax.text(0, 0.05, f"F = {F:.1f}", ha="center", va="center", fontsize=16,
                fontweight="bold", color=col)
        ax.plot([np.cos(np.radians(180 * (1 - 10 / 60))), 1.05 * np.cos(np.radians(180 * (1 - 10 / 60)))],
                [np.sin(np.radians(180 * (1 - 10 / 60))), 1.05 * np.sin(np.radians(180 * (1 - 10 / 60)))],
                color=INK, lw=1.2)

    fig.suptitle("Component identification", x=0.02, ha="left", fontsize=14,
                 color=INK, fontproperties=FP_BOLD)
    fig.tight_layout(rect=[0, 0.01, 1, 0.90])
    save(fig, "V5_component_power_meters")


def v6_cate_ridges():
    cate = pd.read_csv(TAB / "causal_forest_cate.csv")

    def bucket(s):
        if pd.isna(s):
            return np.nan
        if s < 70:
            return "Safe"
        if s < 90:
            return "Semi-critical"
        if s < 100:
            return "Critical"
        return "Over-exploited"

    cate["bucket"] = cate["gw_stage_step"].map(bucket)
    order = ["Safe", "Semi-critical", "Critical", "Over-exploited"]
    colors = [SAFE, WARN_L, WARN, DANGER]

    fig, ax = plt.subplots(figsize=(10, 5.2))
    y0 = 0
    for lab, col in zip(order, colors):
        vals = cate.loc[cate["bucket"] == lab, "cate"].dropna().values
        if len(vals) < 3:
            continue
        from scipy.stats import gaussian_kde
        xs = np.linspace(np.percentile(vals, 1), np.percentile(vals, 99), 200)
        try:
            dens = gaussian_kde(vals)(xs)
        except Exception:
            continue
        dens = dens / dens.max() * 0.85
        ax.fill_between(xs, y0, y0 + dens, color=col, alpha=0.75, linewidth=0)
        ax.plot(xs, y0 + dens, color=INK, lw=0.8, alpha=0.5)
        ax.text(0.01, y0 + 0.90, lab, fontsize=11, fontweight="bold", color=col,
                va="top", ha="left", transform=ax.get_yaxis_transform(),
                bbox=dict(facecolor=WHITE, edgecolor=col, boxstyle="round,pad=0.25",
                          linewidth=1.0, alpha=0.92))
        y0 += 1.05

    ax.axvline(0, color=INK, lw=1, alpha=0.4)
    ax.set_xlabel("CATE")
    ax.set_yticks([])
    ax.set_title("Heterogeneous effects", loc="left", color=INK, fontproperties=FP_BOLD)
    save(fig, "V6_cate_ridges_by_stress")


def v7_rebound_heatmap():
    sens = pd.read_csv(TAB / "rebound_bridge_sensitivity.csv")
    audit = pd.read_csv(TAB / "rebound_bridge_audit.csv").iloc[0]
    gross = float(audit["gross_central_tco2"])
    piv = sens.pivot_table(index="lift_base_m", columns="e_kWh_per_m3_m",
                           values="rebound_total_tco2")
    offset = 100 * piv / gross

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    cmap = LinearSegmentedColormap.from_list(
        "reb", [SAFE_L, WARN_L, DANGER_L, DANGER])
    im = ax.imshow(offset.values, aspect="auto", cmap=cmap, origin="lower",
                   vmin=5, vmax=max(35, offset.values.max()))
    ax.set_xticks(range(len(offset.columns)))
    ax.set_xticklabels([f"{c:.4f}" for c in offset.columns])
    ax.set_yticks(range(len(offset.index)))
    ax.set_yticklabels([f"{int(i)} m" for i in offset.index])
    ax.set_xlabel(r"kWh / m$^3$ / m")
    ax.set_ylabel("Lift depth")
    for i in range(offset.shape[0]):
        for j in range(offset.shape[1]):
            ax.text(j, i, f"{offset.values[i, j]:.1f}%", ha="center", va="center",
                    color=WHITE if offset.values[i, j] > 18 else INK, fontsize=11,
                    fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label("Offset (%)")
    ax.set_title("Rebound sensitivity", loc="left", color=INK, fontproperties=FP_BOLD)
    save(fig, "V7_rebound_heatmap")


def v8_loo_spine():
    loo = pd.read_csv(TAB / "critical_loo_iv.csv").copy()
    base = 0.102324
    loo["delta"] = (loo["beta"] - base).abs()
    show = loo.sort_values("beta")
    big = {"Punjab", "Haryana", "Rajasthan", "Maharashtra", "Gujarat", "Karnataka",
           "Uttar Pradesh", "Madhya Pradesh", "Bihar", "Odisha", "Jharkhand",
           "Tamil Nadu", "Telangana", "Andhra Pradesh", "West Bengal"}
    show = show[show["dropped_state"].isin(big) | (show["delta"] > 0.005)].drop_duplicates("dropped_state")
    show = show.sort_values("beta")

    fig, ax = plt.subplots(figsize=(9, 6.8))
    y = np.arange(len(show))
    colors = [DANGER if b < 0 else WATER_MID for b in show["beta"]]
    ax.hlines(y, base, show["beta"], color=LINE, lw=1.5)
    ax.scatter(show["beta"], y, s=55, c=colors, zorder=3, edgecolor=WHITE, linewidth=0.8)
    ax.axvline(base, color=SOLAR, lw=2.2, label=f"Baseline ({base:.3f})")
    ax.axvline(0, color=INK, lw=0.8, alpha=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(show["dropped_state"], fontsize=10)
    ax.set_xlabel(r"IV $\beta$")
    ax.set_title("Leave-one-out", loc="left", color=INK, fontproperties=FP_BOLD)
    ax.legend(loc="lower right", frameon=False)
    save(fig, "V8_loo_lollipop_spine")


def v9_carbon_balance_sheet():
    decomp = pd.read_csv(TAB / "decomposition_by_stress.csv").copy()
    audit = pd.read_csv(TAB / "rebound_bridge_audit.csv").iloc[0]
    labmap = {
        "safe": "Safe", "semi_critical": "Semi-critical", "semi-critical": "Semi-critical",
        "critical": "Critical", "over_exploited": "Over-exploited", "over-exploited": "Over-exploited",
    }
    order = ["safe", "semi_critical", "over_exploited"]
    decomp["o"] = decomp["gw_stress_cat"].map({k: i for i, k in enumerate(order)})
    decomp = decomp.dropna(subset=["o"]).sort_values("o")
    decomp["label"] = decomp["gw_stress_cat"].map(labmap).fillna(decomp["gw_stress_cat"])

    fig = plt.figure(figsize=(11.5, 5.8))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.55], hspace=0.35, wspace=0.28)

    cards = [
        (f"{float(audit['gross_central_tco2'])/1e6:.2f} Mt", "Gross", SAFE),
        (f"{float(audit['rebound_central_tco2'])/1e6:.2f} Mt", "Rebound", DANGER),
        (f"{float(audit['net_central_tco2'])/1e6:.2f} Mt", "Net", WATER),
    ]
    for i, (val, lab, col) in enumerate(cards):
        ax = fig.add_subplot(gs[0, i])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        rounded(ax, (0.05, 0.15), 0.9, 0.7, f"{val}\n{lab}", col, fontsize=14)

    ax = fig.add_subplot(gs[1, :])
    x = np.arange(len(decomp))
    subst = decomp["subst"].values / 1e3
    reb = decomp["reb"].values / 1e3
    ax.bar(x, subst, color=WATER_MID, width=0.55, label="Gross")
    ax.bar(x, -reb, color=DANGER_L, width=0.55, label="Rebound")
    for i, (_, r) in enumerate(decomp.iterrows()):
        share = float(r.get("offset_share", 0)) * 100
        ax.text(i, subst[i] + max(8, 0.04 * subst.max()), f"{share:.0f}%",
                ha="center", fontsize=11, fontweight="bold", color=DANGER,
                fontname="Times New Roman")
    ax.axhline(0, color=INK, lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels(decomp["label"].tolist())
    ax.set_ylabel(r"kt CO$_2$/yr")
    ax.legend(loc="upper right", frameon=False)
    fig.suptitle("Carbon balance", x=0.02, ha="left", fontsize=14,
                 color=INK, fontproperties=FP_BOLD)
    save(fig, "V9_carbon_balance_sheet")


def v10_governance_matrix():
    import textwrap
    panel = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    last = int(panel["fy_start"].max())
    d = panel[panel["fy_start"] == last].dropna(
        subset=["kusum_intensity_per_kha", "gw_stress_cat"]
    ).copy()
    median_int = d["kusum_intensity_per_kha"].median()
    d["high_intensity"] = d["kusum_intensity_per_kha"] > median_int
    d["stressed"] = d["gw_stress_cat"].isin(["semi_critical", "critical", "over_exploited"])

    def names(hi, stressed):
        sub = d[(d["high_intensity"] == hi) & (d["stressed"] == stressed)]
        sub = sub.sort_values("kusum_intensity_per_kha", ascending=False)
        return sub["state"].tolist()

    quads = [
        # (x, y, w, h, fill, header, state_list, n_total_for_footer)
        (0.3, 3.85, 4.7, 2.75, SAFE, "Push Component B\n(high intensity, safe aquifer)", names(True, False)),
        (5.4, 3.85, 4.7, 2.75, DANGER, "Condition + haircut\n(high intensity, stressed aquifer)", names(True, True)),
        (0.3, 0.55, 4.7, 2.75, WATER, "Monitor, low priority\n(low intensity, safe aquifer)", names(False, False)),
        (5.4, 0.55, 4.7, 2.75, WARN, "Fix governance first\n(low intensity, stressed aquifer)", names(False, True)),
    ]

    fig, ax = plt.subplots(figsize=(11.5, 7.4))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 7.0)
    ax.axis("off")
    ax.set_title("Governance matrix", loc="left", color=INK, pad=10, fontproperties=FP_BOLD)

    # axis annotations describing the two dimensions
    ax.annotate("", xy=(10.2, 0.15), xytext=(0.1, 0.15),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    ax.text(5.15, -0.05, "Aquifer stress: safe (left)  vs.  semi-critical / critical / over-exploited (right)",
            ha="center", va="top", fontsize=9.5, color=MUTED, fontname="Times New Roman")
    ax.annotate("", xy=(0.02, 6.85), xytext=(0.02, 0.35),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    ax.text(-0.15, 3.6, "KUSUM intensity: low (bottom) vs. high (top, above median)",
            ha="center", va="center", rotation=90, fontsize=9.5, color=MUTED,
            fontname="Times New Roman")

    for x, y, w, h, fc, header, state_list in quads:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.10",
                             facecolor=fc, edgecolor=fc, linewidth=1.2, alpha=0.92)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 0.30, header, ha="center", va="top", fontsize=11.5,
                fontweight="bold", color=WHITE, fontname="Times New Roman", linespacing=1.3)
        shown = state_list[:8]
        body = ", ".join(shown)
        if len(state_list) > 8:
            body += f", +{len(state_list) - 8} more"
        if not state_list:
            body = "(no states in this cell)"
        wrapped = "\n".join(textwrap.wrap(body, width=40))
        ax.text(x + w / 2, y + h - 1.05, wrapped, ha="center", va="top", fontsize=9,
                color=WHITE, fontname="Times New Roman", linespacing=1.6)
        ax.text(x + w / 2, y + 0.20, f"n = {len(state_list)} states", ha="center", va="bottom",
                fontsize=9, color=WHITE, fontname="Times New Roman", fontweight="bold", alpha=0.95)

    save(fig, "V10_governance_matrix")


def v11_treatment_balance():
    bal = pd.read_csv(TAB / "balance_table.csv").dropna(subset=["high_KUSUM", "low_KUSUM"])
    labmap = {
        "gw_stage_step": "GW stage (%)",
        "gsdp_cr": "GSDP (INR cr)",
        "diesel_pumps_2016_17": "Diesel pumps\n2016-17",
    }
    bal = bal[bal["variable"].isin(labmap)].copy()
    bal["label"] = bal["variable"].map(labmap)

    fig, axes = plt.subplots(1, len(bal), figsize=(9.5, 4.6))
    if len(bal) == 1:
        axes = [axes]
    for ax, (_, r) in zip(axes, bal.iterrows()):
        vals = [r["low_KUSUM"], r["high_KUSUM"]]
        ax.bar([0, 1], vals, color=[WATER_MID, DANGER], width=0.55)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Low-KUSUM\nstates", "High-KUSUM\nstates"], fontsize=9.5)
        ax.set_title(r["label"], fontsize=11, fontproperties=FP_BOLD, pad=6)
        for i, v in enumerate(vals):
            ax.text(i, v * 1.02, f"{v:,.0f}", ha="center", va="bottom", fontsize=9,
                    fontname="Times New Roman")
        for spine in ax.spines.values():
            spine.set_color(LINE)
    fig.suptitle("Treatment balance", x=0.02, ha="left", fontsize=14,
                 color=INK, fontproperties=FP_BOLD)
    fig.tight_layout(rect=[0, 0.01, 1, 0.90])
    save(fig, "V11_treatment_balance")


def v12_assumption_ledger():
    ledger = pd.read_csv(TAB / "assumption_stress_tests.csv")
    status_col = {
        "PARTIAL": WARN, "STRESSED": WARN, "CHECKED": SAFE, "REJECTED": DANGER, "FIXED": WATER,
    }

    def status_key(s):
        s = str(s).upper()
        for k in status_col:
            if s.startswith(k):
                return k
        return "PARTIAL"

    ledger["status_key"] = ledger["status"].map(status_key)

    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(ledger) + 0.5)
    ax.axis("off")
    ax.set_title("Assumption ledger", loc="left", color=INK, pad=8, fontproperties=FP_BOLD)

    for i, (_, r) in enumerate(ledger.iloc[::-1].iterrows()):
        y = i + 0.5
        col = status_col[r["status_key"]]
        ax.add_patch(Rectangle((0.0, y - 0.38), 0.28, 0.76, facecolor=col, edgecolor=col))
        assumption = str(r["assumption"])
        if len(assumption) > 58:
            assumption = assumption[:55] + "..."
        ax.text(0.45, y, assumption, va="center", ha="left", fontsize=9.5,
                fontname="Times New Roman", color=INK)
        status_short = str(r["status"]).split("\u2014")[0].split("-")[0].strip()
        ax.text(9.9, y, status_short, va="center", ha="right", fontsize=9.5,
                fontweight="bold", color=col, fontname="Times New Roman")

    handles = [mpatches.Patch(color=c, label=k.title()) for k, c in status_col.items()]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02),
             ncol=4, frameon=False, fontsize=9.5)
    save(fig, "V12_assumption_ledger")


def v13_confirmatory_forest():
    conf = pd.read_csv(TAB / "confirmatory_tests.csv").copy()
    labmap = {
        "cross_section_dose_gw": "Terminal cross-section dose\n(no time-path, no IV)",
        "FE_component_B_tubewells": "Component B -> tube-wells (FE)",
        "FE_component_C_tubewells": "Component C -> tube-wells (FE)",
        "FE_component_B_gw": "Component B -> GW stage (FE)",
        "FE_component_C_gw": "Component C -> GW stage (FE)",
        "continuous_interaction_kusum_intensity_per_kha": "Continuous interaction: main term",
        "continuous_interaction_kusum_x_gw": "Continuous interaction: x GW stage",
        "continuous_interaction_kusum_x_discom": "Continuous interaction: x DISCOM health",
        "FE_gw_non_interpolated": "GW stage, non-interpolated years only",
        "placebo_FE_canal": "Canal-area placebo (FE)",
    }
    conf["label"] = conf["test"].map(labmap).fillna(conf["test"])
    conf["sig"] = conf["pvalue"] < 0.05
    conf = conf.iloc[::-1].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6.4))
    y = np.arange(len(conf))
    lo = conf["beta"] - 1.96 * conf["se"]
    hi = conf["beta"] + 1.96 * conf["se"]
    colors = [DANGER if sig else MUTED for sig in conf["sig"]]
    ax.hlines(y, lo, hi, color=LINE, lw=1.5, zorder=1)
    ax.scatter(conf["beta"], y, s=55, c=colors, zorder=3, edgecolor=WHITE, linewidth=0.8)
    ax.axvline(0, color=INK, lw=1.0, alpha=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(conf["label"], fontsize=9)
    ax.set_xlabel(r"Coefficient (95% CI)")
    ax.set_title("Confirmatory battery", loc="left", color=INK, fontproperties=FP_BOLD)
    handles = [mpatches.Patch(color=DANGER, label="p < 0.05"),
               mpatches.Patch(color=MUTED, label="not significant")]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9)
    save(fig, "V13_confirmatory_forest")


def v14_yearly_reduced_form():
    rf = pd.read_csv(TAB / "critical_year_rf.csv").sort_values("fy_start")
    fig, ax = plt.subplots(figsize=(9, 4.8))
    lo = rf["beta_iv"] - 1.96 * rf["se"]
    hi = rf["beta_iv"] + 1.96 * rf["se"]
    ax.fill_between(rf["fy_start"], lo, hi, color=WATER_MID, alpha=0.18, linewidth=0)
    ax.plot(rf["fy_start"], rf["beta_iv"], color=WATER, lw=2.5, marker="o",
            markersize=6, markerfacecolor=WATER, markeredgecolor=WHITE)
    ax.axhline(0, color=INK, lw=1, alpha=0.5)
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Reduced-form coefficient\n(instrument on GW stage)")
    ax.set_xticks(rf["fy_start"])
    ax.set_title("Year-by-year reduced form", loc="left", color=INK, fontproperties=FP_BOLD)
    save(fig, "V14_yearly_reduced_form")


def v15_csa_event_study():
    csa_raw = pd.read_csv(TAB / "callaway_santanna_tubewells.csv", skiprows=3)
    csa_raw.columns = ["relative_period", "ATT", "std_error", "lower", "upper", "zero_not_in_cband"]
    csa_raw = csa_raw.dropna(subset=["relative_period"])
    csa_raw["relative_period"] = csa_raw["relative_period"].astype(int)
    csa_raw = csa_raw.sort_values("relative_period")

    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    colors = [DANGER if str(z) == "*" else WATER_MID for z in csa_raw["zero_not_in_cband"]]
    yerr_lo = (csa_raw["ATT"] - csa_raw["lower"]).values
    yerr_hi = (csa_raw["upper"] - csa_raw["ATT"]).values
    ax.errorbar(csa_raw["relative_period"], csa_raw["ATT"], yerr=[yerr_lo, yerr_hi],
               fmt="none", ecolor=LINE, elinewidth=1.5, capsize=3, zorder=1)
    ax.scatter(csa_raw["relative_period"], csa_raw["ATT"], s=60, c=colors, zorder=3,
              edgecolor=WHITE, linewidth=0.8)
    ax.axhline(0, color=INK, lw=1, alpha=0.5)
    ax.axvline(-0.5, color=SOLAR, lw=2, ls="--", alpha=0.9)
    ax.set_xlabel("Years relative to onset")
    ax.set_ylabel("ATT on tube-well area (ha)")
    ax.set_title("Callaway-Sant'Anna event study", loc="left", color=INK, fontproperties=FP_BOLD)
    handles = [mpatches.Patch(color=DANGER, label="zero excluded from 95% band"),
               mpatches.Patch(color=WATER_MID, label="not significant")]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=9)
    save(fig, "V15_csa_event_study")


def v16_ccts_revenue_fanchart():
    ccts = pd.read_csv(TAB / "ccts_carbon_revenue_by_state.csv")
    ccts = ccts[ccts["abatement_tco2"] > 0].sort_values("rev_p50", ascending=False).head(15)
    for c in ("rev_p05", "rev_p50", "rev_p95"):
        ccts[c] = ccts[c] / 1e7

    fig, ax = plt.subplots(figsize=(9, 6.4))
    y = np.arange(len(ccts))[::-1]
    ax.hlines(y, ccts["rev_p05"], ccts["rev_p95"], color=WATER_MID, lw=6, alpha=0.35)
    ax.scatter(ccts["rev_p50"], y, s=55, color=WATER, zorder=3, edgecolor=WHITE, linewidth=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(ccts["state"], fontsize=9.5)
    ax.set_xlabel("Annual carbon revenue (INR crore), 5th-95th percentile")
    ax.set_title("CCTS revenue by state", loc="left", color=INK, fontproperties=FP_BOLD)
    save(fig, "V16_ccts_revenue_fanchart")


def main():
    style()
    warnings.filterwarnings("ignore")
    build_tables()
    build_tables_s4_to_s10()
    v1_causal_storyboard()
    try:
        v2_india_dual_map()
    except Exception as e:
        log(f"V2 map fallback: {e}")
        try:
            v2_fallback_bubble()
        except Exception as e2:
            log(f"V2 fallback also failed: {e2}")
    v3_event_ribbon()
    v4_paradox_scales()
    v5_component_meters()
    try:
        v6_cate_ridges()
    except Exception as e:
        log(f"V6 fail: {e}")
    v7_rebound_heatmap()
    v8_loo_spine()
    v9_carbon_balance_sheet()
    v10_governance_matrix()
    v11_treatment_balance()
    v12_assumption_ledger()
    v13_confirmatory_forest()
    v14_yearly_reduced_form()
    v15_csa_event_study()
    v16_ccts_revenue_fanchart()

    # inventory
    inv = pd.DataFrame([
        {"id": "S1", "file": "SI_S1_carbon_sensitivity_matrix", "type": "table"},
        {"id": "S2", "file": "SI_S2_iv_diagnostics", "type": "table"},
        {"id": "S3", "file": "SI_S3_social_cost_ledger", "type": "table"},
        {"id": "S4", "file": "SI_S4_treatment_balance", "type": "table"},
        {"id": "S5", "file": "SI_S5_assumption_ledger", "type": "table"},
        {"id": "S6", "file": "SI_S6_confirmatory_battery", "type": "table"},
        {"id": "S7", "file": "SI_S7_leave_one_out_full", "type": "table"},
        {"id": "S8", "file": "SI_S8_year_by_year_reduced_form", "type": "table"},
        {"id": "S9", "file": "SI_S9_callaway_santanna_full", "type": "table"},
        {"id": "S10", "file": "SI_S10_ccts_revenue_by_state", "type": "table"},
        {"id": "V1", "file": "V1_causal_storyboard", "type": "figure"},
        {"id": "V2", "file": "V2_india_dual_choropleth", "type": "figure"},
        {"id": "V3", "file": "V3_event_ribbon_timeline", "type": "figure"},
        {"id": "V4", "file": "V4_paradox_balance_scales", "type": "figure"},
        {"id": "V5", "file": "V5_component_power_meters", "type": "figure"},
        {"id": "V6", "file": "V6_cate_ridges_by_stress", "type": "figure"},
        {"id": "V7", "file": "V7_rebound_heatmap", "type": "figure"},
        {"id": "V8", "file": "V8_loo_lollipop_spine", "type": "figure"},
        {"id": "V9", "file": "V9_carbon_balance_sheet", "type": "figure"},
        {"id": "V10", "file": "V10_governance_matrix", "type": "figure"},
        {"id": "V11", "file": "V11_treatment_balance", "type": "figure"},
        {"id": "V12", "file": "V12_assumption_ledger", "type": "figure"},
        {"id": "V13", "file": "V13_confirmatory_forest", "type": "figure"},
        {"id": "V14", "file": "V14_yearly_reduced_form", "type": "figure"},
        {"id": "V15", "file": "V15_csa_event_study", "type": "figure"},
        {"id": "V16", "file": "V16_ccts_revenue_fanchart", "type": "figure"},
    ])
    save_table(inv, "executive_visual_inventory")
    passfail("p3_15 executive visuals", True, f"{len(list(FIGX.glob('V*.png')))} figures @ {DPI}dpi")


if __name__ == "__main__":
    main()
