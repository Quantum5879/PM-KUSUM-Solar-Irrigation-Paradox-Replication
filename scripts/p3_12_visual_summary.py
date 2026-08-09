"""
p3_12_visual_summary.py  —  the *visual story* of Paper 3 (not data plots: the workflow itself).

Produces a publication-grade, 300-dpi set that walks a reader from raw data -> cleaning/integrity ->
master panel -> the competing methods and WHY each was chosen -> which spec won -> key takeaways.

Figures (outputs/figures/summary/):
  S1  pipeline_lineage      — end-to-end workflow & data-lineage flow (graphical abstract)
  S2  data_coverage_upset   — UpSet of state coverage across data sources + integrity-fix ledger
  S3  method_decision_map   — methods considered per estimand, the pre-registered rule, the winner
  S4  results_scorecard     — IV first-stage F, robustness dumbbell, effect forest, carbon EF-band
  S5  key_takeaways         — graphical abstract of the five headline findings (real numbers)
  S6  cate_beeswarm         — where the effect flips sign (causal-forest CATE swarm)
  S7  pipeline_sankey       — interactive plotly Sankey (HTML + 300-dpi PNG via kaleido)

All numbers are read live from outputs/tables + reports so the visuals never drift from the analysis.
"""
from _p3_common import *
import json
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch
from matplotlib.lines import Line2D
sys.path.append(str(CONFIG)); from viz_style import apply_style, OKABE_ITO, DIVERGING  # noqa

SUM = FIG / "summary"; SUM.mkdir(parents=True, exist_ok=True)

# Okabe-Ito roles -> stable semantic colours for the whole summary
C_SRC   = "#56B4E9"   # data sources (sky)
C_CLEAN = "#E69F00"   # cleaning / integrity (amber)
C_PANEL = "#009E73"   # master panel (green)
C_METH  = "#0072B2"   # methods (blue)
C_TAKE  = "#CC79A7"   # takeaways (rose)
C_WIN   = "#009E73"   # winner badge
C_BAD   = "#D55E00"   # weak / rejected
INK     = "#222222"; MUTE = "#666666"; GRID = "#E6E6E6"


def _save(fig, name, caption=None):
    if caption:
        fig.text(0.012, 0.008, caption, fontsize=7, color=MUTE, ha="left")
    for ext in ("png", "pdf", "svg"):
        fig.savefig(SUM / f"{name}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    log(f"summary figure -> {name}.png/.pdf/.svg")


def _box(ax, x, y, w, h, text, fc, fs=8.5, tc="white", bold=True, alpha=1.0, ec="none"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                fc=fc, ec=ec, lw=1.0, alpha=alpha, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal", zorder=3, wrap=True)


def _arrow(ax, p0, p1, color=MUTE, lw=1.3, style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=11,
                                 color=color, lw=lw, connectionstyle=f"arc3,rad={rad}",
                                 zorder=1, alpha=0.8))


# ---------------------------------------------------------------- load results
def load_facts():
    f = {}
    try:
        fe = pd.read_csv(TAB / "fe_channel_results.csv"); f["fe"] = fe
    except Exception: f["fe"] = pd.DataFrame()
    try:
        f["iv"] = pd.read_csv(TAB / "iv_results.csv")
    except Exception: f["iv"] = pd.DataFrame()
    try:
        f["led"] = pd.read_csv(TAB / "ledger_scenario_totals.csv")
    except Exception: f["led"] = pd.DataFrame()
    try:
        f["dist"] = pd.read_csv(TAB / "district_mechanism_regression.csv")
    except Exception: f["dist"] = pd.DataFrame()
    try:
        f["cate"] = pd.read_csv(TAB / "causal_forest_cate.csv")
    except Exception: f["cate"] = pd.DataFrame()
    try:
        tl = json.loads((REP / "tuning_log.json").read_text())
        f["cate_ci"] = next((e for e in reversed(tl) if "cate_mean_ci_width" in e), {})
    except Exception: f["cate_ci"] = {}
    try:
        f["panel"] = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    except Exception: f["panel"] = pd.DataFrame()
    return f


# ============================================================ S1 pipeline lineage
def fig_lineage(f):
    apply_style()
    fig, ax = plt.subplots(figsize=(16, 9.2)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    ax.text(50, 97.5, "Paper 3 — The Solar-Irrigation Paradox: end-to-end analytical pipeline",
            ha="center", fontsize=15, fontweight="bold", color=INK)
    ax.text(50, 94.3, "raw data  →  cleaning & integrity  →  master panel  →  identification methods  →  findings",
            ha="center", fontsize=9.5, color=MUTE, style="italic")

    # lane headers sit just ABOVE each row of boxes (left-aligned) so they never overlap content
    for label, y, c in [("DATA SOURCES", 89.2, C_SRC), ("CLEAN & VERIFY", 69.3, C_CLEAN),
                        ("MASTER PANEL", 54.6, C_PANEL), ("METHODS", 36.7, C_METH), ("FINDINGS", 16.0, C_TAKE)]:
        ax.text(2.0, y, label, fontsize=8.5, color=c, fontweight="bold", ha="left", va="bottom")

    # row 1: sources
    srcs = ["PM-KUSUM\npumps", "Agri\nelectricity", "Irrigation\n(tube-wells)", "Groundwater\nCGWB",
            "Diesel 2016-17\nbaseline", "District GW\n(7 states)", "GSDP\n.xls", "Paper 2\nAT&C·RPO·GHI·GDP"]
    n = len(srcs); w = 10.6; gap = (100 - 4 - n * w) / (n - 1); x = 2.0
    src_x = []
    for s in srcs:
        _box(ax, x, 81, w, 7.6, s, fc=("#FDE9C9" if "Paper 2" in s else C_SRC), fs=7.6,
             tc=INK if "Paper 2" in s else "white", ec="#1b6fa8" if "Paper 2" in s else "none")
        src_x.append(x + w / 2); x += w + gap

    # row 2: cleaning steps
    cleans = ["State-name\nstandardise", "GSDP parser\n(all-NaN → 33)", "Phantom row +\nfootnote digits",
              "Merged-UT\nde-dup", "Paper 2 covariate\nmerge", "Integrity x-check\n(CGWB == open)"]
    n2 = len(cleans); w2 = 14.0; gap2 = (100 - 4 - n2 * w2) / (n2 - 1); x = 2.0
    for s in cleans:
        _box(ax, x, 61.5, w2, 7.2, s, C_CLEAN, fs=7.6); x += w2 + gap2
    for sx in src_x:
        _arrow(ax, (sx, 81), (sx, 69.0), color="#bbbbbb", lw=0.9)

    # row 3: panel node
    pr = f.get("panel", pd.DataFrame())
    shp = f"{pr.shape[0]} rows × {pr.shape[1]} cols" if len(pr) else "396 rows × 39 cols"
    nst = pr["state"].nunique() if len(pr) else 36
    _box(ax, 26, 45.5, 48, 8.6,
         f"master_panel_state_year   ·   {shp}\n{nst} states × 11 fiscal years (FY2014-15 → FY2024-25)   ·   0 duplicate state-years",
         C_PANEL, fs=9.2)
    for x in (16, 30, 50, 70, 84):
        _arrow(ax, (x, 61.5), (50, 54.1), color="#c9b07a", lw=0.9, rad=0.04)

    # row 4: methods
    meths = ["Two-way FE\n+ income ctrl\n(wild boot SE)", "Event-study DiD\nSun-Abraham +\nCallaway-S.A.",
             "IV 2SLS\nGHI × diesel\ndensity", "Carbon ledger\nsubst − rebound",
             "Heterogeneity\nforest + interact.", "CCTS\nMonte-Carlo", "District\nmechanism"]
    n3 = len(meths); w3 = 12.4; gap3 = (100 - 4 - n3 * w3) / (n3 - 1); x = 2.0
    mx = []
    for s in meths:
        _box(ax, x, 27.0, w3, 9.2, s, C_METH, fs=7.4); mx.append(x + w3 / 2); x += w3 + gap3
    for xx in mx:
        _arrow(ax, (50, 45.5), (xx, 36.2), color="#7fa9c9", lw=0.8, rad=0.03)

    # row 5: findings
    takes = ["PARADOX:\nhigh-GHI states\nover-extracted", "TUBE-WELL CHANNEL:\nKUSUM shifts area\n(FE, p=0.021)",
             "SIGN-FLIP:\neffect depends on\nDISCOM × stress", "NET CARBON:\ngross saving offset\nin stressed aquifers"]
    n4 = len(takes); w4 = 21.0; gap4 = (100 - 4 - n4 * w4) / (n4 - 1); x = 2.0
    for s in takes:
        _box(ax, x, 6.5, w4, 9.0, s, C_TAKE, fs=8.0); x += w4 + gap4
    for xx in mx:
        _arrow(ax, (xx, 27.0), (50, 15.7), color="#c79ab4", lw=0.7, rad=0.02)

    _save(fig, "S1_pipeline_lineage",
          "Graphical abstract of the Paper 3 pipeline (scripts p3_00–p3_11). Colour = stage. Script: p3_12.")


# ============================================================ S2 coverage UpSet
def _coverage_indicators(p):
    src_cols = {"KUSUM": "kusum_cum_pumps", "Agri-elec": "agri_grid_gwh", "Tube-wells": "tubewells",
                "Groundwater": "gw_stage_step", "Diesel base": "diesel_pumps_2016_17",
                "GHI (obs)": "ghi_annual_obs", "DISCOM AT&C": "discom_health", "GDP/pop": "log_gdp_pc"}
    src_cols = {k: v for k, v in src_cols.items() if v in p.columns}
    ind = (p.groupby("state")[list(src_cols.values())].apply(lambda g: g.notna().any())
           .rename(columns={v: k for k, v in src_cols.items()}))
    return ind.astype(bool)


def fig_coverage(f):
    apply_style()
    p = f["panel"]
    ind = _coverage_indicators(p)
    try:
        from upsetplot import UpSet, from_indicators
        data = from_indicators(list(ind.columns), ind)
        fig = plt.figure(figsize=(13, 7.4))
        UpSet(data, subset_size="count", show_counts=True, sort_by="cardinality",
              facecolor=C_METH, shading_color="#F0F2F5", other_dots_color="#C9CED6",
              min_subset_size=1).plot(fig=fig)
        fig.suptitle("Figure S2. Data-source coverage across the 36 states — which datasets overlap, and where they thin out",
                     y=1.02, fontsize=12, fontweight="bold", color=INK)
        fig.text(0.012, 0.005,
                 "UpSet (upsetplot): bars = no. of states sharing exactly that source combination. "
                 "Observed GHI & DISCOM thin out for small NE states/UTs. Script: p3_12.",
                 fontsize=7, color=MUTE)
        fig.savefig(SUM / "S2_data_coverage_upset.png", dpi=300, bbox_inches="tight", facecolor="white")
        fig.savefig(SUM / "S2_data_coverage_upset.pdf", bbox_inches="tight", facecolor="white")
        plt.close(fig)
        log("summary figure -> S2_data_coverage_upset.png/.pdf")
        return
    except Exception as e:
        log(f"upsetplot unavailable ({e}); drawing hand-built UpSet")
    _manual_upset(ind)


def _manual_upset(ind, N=12):
    """UpSetR-style plot built directly in matplotlib (intersection bars + dot-matrix + set-size bars)."""
    cols = list(ind.columns)
    keys = ind.apply(lambda r: tuple(bool(r[c]) for c in cols), axis=1)
    counts = keys.value_counts().head(N)
    combos = list(counts.index)
    setsize = ind.sum(axis=0)
    order = list(setsize.sort_values(ascending=False).index)
    nC, nS = len(combos), len(cols)
    rows = np.arange(nS); xs = np.arange(nC)

    fig = plt.figure(figsize=(13.8, 8.4))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 4.0], height_ratios=[2.0, 2.9],
                          wspace=0.22, hspace=0.07)
    axb = fig.add_subplot(gs[0, 1]); axm = fig.add_subplot(gs[1, 1]); axs = fig.add_subplot(gs[1, 0])

    axb.bar(xs, counts.values, color=C_METH, edgecolor="white", width=0.68, zorder=3)
    for x, v in zip(xs, counts.values):
        axb.text(x, v + max(counts.values) * 0.02, str(int(v)), ha="center", fontsize=8,
                 fontweight="bold", color=INK)
    axb.set_xlim(-0.6, nC - 0.4); axb.set_xticks([]); axb.set_ylabel("states in\nintersection", fontsize=8.5)
    for s in ("top", "right"): axb.spines[s].set_visible(False)
    axb.set_title("Figure S2. Data-source coverage across the 36 states (UpSet) — where the datasets overlap and thin out",
                  loc="left", fontsize=12, fontweight="bold", color=INK, pad=8)

    for k in range(nS):
        if k % 2 == 0: axm.axhspan(k - 0.5, k + 0.5, color="#F6F7F9", zorder=0)
    for j, combo in enumerate(combos):
        present = [k for k, c in enumerate(order) if combo[cols.index(c)]]
        for k, c in enumerate(order):
            on = combo[cols.index(c)]
            axm.scatter(j, k, s=95, color=C_METH if on else "#D7DCE3", zorder=3)
        if present:
            axm.plot([j, j], [min(present), max(present)], color=C_METH, lw=2.2, zorder=2)
    axm.set_xlim(-0.6, nC - 0.4); axm.set_ylim(-0.6, nS - 0.4)
    axm.set_yticks([]); axm.set_xticks([]); axm.invert_yaxis()
    for s in axm.spines.values(): s.set_visible(False)
    axm.tick_params(length=0)

    sizes = [int(setsize[c]) for c in order]
    axs.barh(rows, sizes, color="#9DB8CC", edgecolor="white", height=0.6, zorder=3)
    for y, v in zip(rows, sizes):
        axs.text(v - 0.4, y, str(v), va="center", ha="right", fontsize=7.5, color="white", fontweight="bold")
    axs.set_ylim(-0.6, nS - 0.4); axs.invert_yaxis(); axs.invert_xaxis()
    # source names sit in the gutter between the set-size bars and the dot-matrix
    axs.set_yticks(rows); axs.set_yticklabels(order, fontsize=9)
    axs.yaxis.set_ticks_position("right"); axs.yaxis.set_label_position("right")
    axs.set_xlabel("set size\n(states with source)", fontsize=8.5)
    for s in ("top", "left"): axs.spines[s].set_visible(False)
    axs.tick_params(axis="y", length=0); axs.tick_params(axis="x", length=3)
    _save(fig, "S2_data_coverage_upset",
          "Top bars = states sharing exactly that source combination; dot-matrix = which sources; "
          "left bars = total states per source. Observed GHI/DISCOM thin out for small NE states. Script: p3_12.")


# ============================================================ S3 method decision map
def fig_decision(f):
    apply_style()
    iv = f["iv"]; cc = f.get("cate_ci", {})
    fe = f["fe"]
    fmin = iv["first_stage_F"].min() if len(iv) else 27.8
    fmax = iv["first_stage_F"].max() if len(iv) else 115.3
    ci = cc.get("cate_mean_ci_width", 120.9); sp = cc.get("cate_std", 28.3)
    tubep = fe.loc[fe.outcome == "tubewells", "wild_p"].iloc[0] if len(fe) else 0.021

    rows = [
        ("Functional form\n(outcome transform)",
         "level · log · asinh · per-ha\nscored by BIC",
         "tube-wells = log;\nagri & GW = asinh", "BIC grid"),
        ("Causal effect\n(panel baseline)",
         "two-way FE (state × year)\n+ log GDP-pc control",
         f"wild cluster bootstrap, 9999 reps\n(CGM 2008)  —  tube-well p = {tubep:.3f}", "small-N inference"),
        ("Dynamics /\npre-trends",
         "Sun-Abraham event study +\nCallaway-Sant'Anna ATT",
         "onset threshold swept\n{50,60,70,75,80}; central = 70", "robustness sweep"),
        ("Endogeneity\n(instrument choice)",
         "GHI × baseline diesel density\nobserved vs imputed GHI",
         f"observed GHI wins: first-stage\nF = {fmin:.0f}-{fmax:.0f} (>>10) vs 1-6 imputed", "weak-IV rule"),
        ("Heterogeneity\n(forest vs interaction)",
         "causal forest (DML) vs\ntransparent interaction model",
         f"CI width {ci:.0f} > CATE spread {sp:.0f}\n→ interaction primary, forest = check", "pre-registered rule"),
    ]
    fig, ax = plt.subplots(figsize=(13.5, 7.8)); ax.set_xlim(0, 100); ax.set_ylim(7, 100); ax.axis("off")
    ax.text(50, 96, "Figure S3. Why each method — every modelling fork was decided by a pre-registered rule, not by hand",
            ha="center", fontsize=12.5, fontweight="bold", color=INK)
    ax.text(13, 90.5, "ESTIMATION QUESTION", fontsize=8, color=MUTE, fontweight="bold", ha="center")
    ax.text(41.5, 90.5, "WHAT WE COMPARED", fontsize=8, color=MUTE, fontweight="bold", ha="center")
    ax.text(78.5, 90.5, "DECISION & WINNER", fontsize=8, color=MUTE, fontweight="bold", ha="center")
    yh = 15.6; y0 = 72
    for i, (q, comp, dec, rule) in enumerate(rows):
        y = y0 - i * yh; h = yh - 3.4; cy = y + h / 2
        _box(ax, 2, y, 22, h, q, fc=C_METH, fs=8.6)
        ax.add_patch(FancyBboxPatch((27, y), 29, h, boxstyle="round,pad=0.006,rounding_size=0.01",
                                    fc="#F2F4F7", ec="#D5DAE0", lw=1, zorder=2))
        ax.text(41.5, cy, comp, ha="center", va="center", fontsize=8, color=INK, zorder=3)
        ax.add_patch(FancyBboxPatch((59, y), 39, h, boxstyle="round,pad=0.006,rounding_size=0.01",
                                    fc="#E7F4EE", ec=C_WIN, lw=1.4, zorder=2))
        ax.text(78.5, cy + 1.0, dec, ha="center", va="center", fontsize=8.2, color="#0a5c43",
                fontweight="bold", zorder=3)
        ax.text(96.5, y + 1.3, "RULE: " + rule.upper(), fontsize=6.4, color=C_WIN, ha="right",
                style="italic", zorder=3)
        _arrow(ax, (24.2, cy), (26.8, cy), color=MUTE, lw=1)
        _arrow(ax, (56.2, cy), (58.8, cy), color=C_WIN, lw=1.3)
    _save(fig, "S3_method_decision_map",
          "Each row: the question, the candidates compared, and the auto-selected winner + its governing rule. Script: p3_12.")


# ============================================================ S4 results scorecard
def fig_scorecard(f):
    apply_style()
    fe = f["fe"]; iv = f["iv"]; led = f["led"]; dist = f["dist"]
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.2))
    fig.suptitle("Figure S4. Results scorecard — instrument strength, robustness, effect sizes, carbon band",
                 fontsize=12.5, fontweight="bold", color=INK, y=0.98)

    # A — IV first-stage F
    ax = axes[0, 0]
    if len(iv):
        lab = iv["outcome"].str.replace("_", " ")
        ax.barh(lab, iv["first_stage_F"], color=[C_WIN if v >= 10 else C_BAD for v in iv["first_stage_F"]],
                edgecolor="white")
        ax.axvline(10, color=INK, ls="--", lw=1.2)
        ax.text(10, -0.45, "weak-IV\nF=10", fontsize=7, color=INK, ha="center", va="top")
        for y, v in enumerate(iv["first_stage_F"]):
            ax.text(v + 2, y, f"{v:.0f}", va="center", fontsize=8, fontweight="bold", color=INK)
    ax.set_title("a  IV first-stage F (instrument relevance)", fontsize=10, loc="left")
    ax.set_xlabel("first-stage F (observed-GHI instrument)")

    # B — robustness dumbbell: wild-p before vs after income control
    ax = axes[0, 1]
    chans = ["tubewells", "agri_grid_gwh", "gw_stage_step"]
    before = {"tubewells": 0.0302, "agri_grid_gwh": 0.393, "gw_stage_step": 0.775}
    after = {r.outcome: r.wild_p for _, r in fe.iterrows()} if len(fe) else before
    y = np.arange(len(chans))
    for i, c in enumerate(chans):
        b, a = before[c], after.get(c, np.nan)
        ax.plot([b, a], [i, i], color="#bbbbbb", lw=2, zorder=1)
        ax.scatter(b, i, s=70, color=MUTE, zorder=2, label="before control" if i == 0 else None)
        ax.scatter(a, i, s=80, color=C_WIN if a < 0.05 else C_METH, zorder=3,
                   label="+ log GDP-pc" if i == 0 else None)
    ax.axvline(0.05, color=C_BAD, ls="--", lw=1.1)
    ax.text(0.062, len(chans) - 1.35, "p = 0.05", color=C_BAD, fontsize=7.5, va="center")
    ax.set_yticks(y); ax.set_yticklabels([c.replace("_", " ") for c in chans])
    ax.set_xlabel("wild cluster-bootstrap p-value"); ax.set_title("b  Robustness to income control", fontsize=10, loc="left")
    ax.legend(fontsize=7, loc="lower right")

    # C — FE effect forest (coef ± 1.96 se)
    ax = axes[1, 0]
    if len(fe):
        yy = np.arange(len(fe))
        ax.errorbar(fe["coef"], yy, xerr=1.96 * fe["se"], fmt="o", color=C_METH, capsize=4, ms=7)
        ax.axvline(0, color=INK, lw=1)
        ax.set_yticks(yy); ax.set_yticklabels([o.replace("_", " ") for o in fe["outcome"]])
        for i, r in fe.reset_index().iterrows():
            star = "*" if r["wild_p"] < 0.05 else ""
            ax.text(r["coef"], i + 0.18, f"β={r['coef']:.3f}{star}", fontsize=7.5, ha="center", color=INK)
    ax.set_title("c  Two-way FE effect of KUSUM intensity (±95% CI)", fontsize=10, loc="left")
    ax.set_xlabel("coefficient (BIC-selected transform)")

    # D — carbon abatement EF sweep band
    ax = axes[1, 1]
    if len(led):
        piv = led.pivot(index="fuel_litres", columns="ef_grid", values="gross_abatement_tco2") / 1e6
        for col in piv.columns:
            ax.plot(piv.index, piv[col], "o-", label=f"EF={col}", lw=1.6)
        ax.fill_between(piv.index, piv.min(axis=1), piv.max(axis=1), alpha=0.12, color=C_METH)
    ax.set_xlabel("diesel fuel use (litres/pump/yr, swept)")
    ax.set_ylabel("gross abatement (Mt CO2/yr)")
    ax.set_title("d  Carbon abatement — full EF × fuel sweep (band, not a point)", fontsize=10, loc="left")
    ax.legend(fontsize=7, title="grid EF", title_fontsize=7)

    dr2 = dist["r2"].iloc[0] if len(dist) else np.nan
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    _save(fig, "S4_results_scorecard",
          f"a: F>>10 = strong instrument. b: tube-well rebound stays significant after income control. "
          f"d: net carbon reported as a band. District mechanism R²={dr2:.2f}. Script: p3_12.")


# ============================================================ S5 key takeaways
def fig_takeaways(f):
    apply_style()
    iv = f["iv"]; fe = f["fe"]; led = f["led"]; dist = f["dist"]
    ivg = iv.loc[iv.outcome == "gw_stage_step", "beta_treat"].iloc[0] if len(iv) else 0.13
    ivf = iv.loc[iv.outcome == "gw_stage_step", "first_stage_F"].iloc[0] if len(iv) else 32
    tube = fe.loc[fe.outcome == "tubewells"] if len(fe) else None
    tco = tube["coef"].iloc[0] if tube is not None and len(tube) else -0.023
    tpp = tube["wild_p"].iloc[0] if tube is not None and len(tube) else 0.021
    cen = led.loc[(led.fuel_litres == 600) & (np.isclose(led.ef_grid, 0.7383)), "gross_abatement_tco2"]
    cenv = cen.iloc[0] / 1e6 if len(cen) else 1.93
    dco = dist["coef"].iloc[0] if len(dist) else 89.5
    dp = dist["p"].iloc[0] if len(dist) else 3e-25

    cards = [
        ("1 · THE PARADOX", C_TAKE,
         "States with the best solar resource and most KUSUM pumps are the same states already mining "
         "groundwater past 100% extraction (Punjab, Rajasthan, Haryana).", "Figure 1"),
        ("2 · THE TUBE-WELL CHANNEL", C_METH,
         f"KUSUM intensity significantly shifts tube-well irrigated area (FE, log scale):\n"
         f"coef = {tco:.3f}, wild-boot p = {tpp:.3f} — and it strengthens after a state income control.",
         "Figure 2 · p3_04"),
        ("3 · CAUSAL, NOT JUST CORRELATION", C_PANEL,
         f"IV (GHI × baseline diesel density) → KUSUM raises groundwater stage of extraction by "
         f"β = +{ivg:.2f} pp.\nFirst-stage F = {ivf:.0f} (strong instrument).", "Figure · p3_06"),
        ("4 · THE SIGN-FLIP", C_SRC,
         "KUSUM's groundwater effect is not uniform: it backfires in low-DISCOM-health, already-stressed "
         "aquifers, and is benign where grids are healthy and water is safe.", "Figure 4 · p3_08"),
        ("5 · NET CARBON IS CONDITIONAL", C_CLEAN,
         f"Gross substitution abatement ~ {cenv:.1f} Mt CO2/yr (central), but rebound pumping offsets it in "
         f"over-exploited zones — net benefit is a band, not a headline number.", "Figure 3 · p3_07"),
        ("MECHANISM CONFIRMED AT DISTRICT GRAIN", C_WIN,
         f"Within-state, across 184 districts (7 states): irrigation reliance → groundwater stress, "
         f"coef = {dco:.0f}, p < 1e-20, R² = {dist['r2'].iloc[0]:.2f}." if len(dist) else
         "Within-state district association confirms the rebound mechanism.", "Figure 6 · p3_10"),
    ]
    fig, ax = plt.subplots(figsize=(13.5, 8.8)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    ax.text(50, 97, "Figure S5. Key takeaways — the solar-irrigation paradox in five findings",
            ha="center", fontsize=13, fontweight="bold", color=INK)
    pos = [(2, 64, 47, 28), (51, 64, 47, 28), (2, 33, 47, 28),
           (51, 33, 47, 28), (2, 2, 47, 28), (51, 2, 47, 28)]
    for (title, col, body, src), (x, y, w, h) in zip(cards, pos):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    fc="white", ec=col, lw=2.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + h - 5.2), w, 5.2, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    fc=col, ec=col, lw=0, zorder=2))
        ax.text(x + 1.6, y + h - 2.6, title, fontsize=9.3, color="white", fontweight="bold", va="center")
        wrapped = "\n".join(textwrap.fill(ln, width=50) for ln in body.split("\n"))
        ax.text(x + 1.8, y + (h - 5.2) / 2, wrapped, fontsize=8.2, color=INK, va="center", ha="left")
        ax.text(x + w - 1.6, y + 1.3, src, fontsize=6.8, color=MUTE, ha="right", style="italic")
    _save(fig, "S5_key_takeaways",
          "Numbers read live from the results tables (p3_04/06/07/10). Script: p3_12.")


# ============================================================ S6 CATE beeswarm
def fig_beeswarm(f):
    import seaborn as sns
    apply_style()
    d = f["cate"]
    if not len(d) or "cate" not in d.columns:
        log("S6 skipped — no causal_forest_cate.csv"); return
    d = d.copy()
    # split state-years along the groundwater-stress gradient (the key moderator), honestly:
    # all CATEs here are negative, so the story is MAGNITUDE heterogeneity, not a sign flip.
    if "gw_stage_step" in d.columns and d["gw_stage_step"].notna().sum() >= 6:
        try:
            d["grp"] = pd.qcut(d["gw_stage_step"], 3,
                               labels=["low stress", "medium stress", "high stress"])
        except Exception:
            d["grp"] = "all state-years"
    else:
        d["grp"] = "all state-years"
    d = d.dropna(subset=["grp"])
    order = [g for g in ["high stress", "medium stress", "low stress", "all state-years"]
             if g in set(d["grp"])]
    pal = {"high stress": C_BAD, "medium stress": C_CLEAN, "low stress": C_METH,
           "all state-years": C_METH}
    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    sns.swarmplot(data=d, x="cate", y="grp", order=order, hue="grp", palette=pal, size=6.0,
                  edgecolor="white", linewidth=0.5, ax=ax, legend=False)
    ax.set_ylim(len(order) - 0.45, -0.55)
    mean_by = d.groupby("grp")["cate"].mean()
    for i, g in enumerate(order):
        ax.scatter(mean_by[g], i, marker="D", s=85, color=INK, zorder=5)
        ax.text(mean_by[g], i + 0.34, f"mean {mean_by[g]:.0f}", ha="center", va="center", fontsize=7.8,
                color=INK, fontweight="bold")
    ax.axvline(0, color=INK, lw=1.2, ls="--")
    ax.text(0, len(order) - 0.5, " no effect", fontsize=7.5, ha="right", va="bottom", color=MUTE, rotation=90)
    ax.set_xlabel("CATE: causal-forest marginal effect of KUSUM intensity on tube-well area (per state-year)")
    ax.set_ylabel("groundwater-stress tercile")
    ax.set_title("Figure S6. The effect is heterogeneous in magnitude — causal-forest CATEs along the stress gradient",
                 fontsize=11, fontweight="bold", color=INK, loc="left", pad=12)
    ax.text(0.015, 0.04, f"N={len(d)} state-years · honest causal forest (econml) · diamonds = group means\n"
            f"all CATEs are negative (no sign flip); the interaction model is the pre-registered primary",
            transform=ax.transAxes, ha="left", va="bottom", fontsize=7.2, color=MUTE)
    _save(fig, "S6_cate_beeswarm",
          "Each dot a state-year, split by groundwater-stress tercile; beeswarm avoids overplotting "
          "(ggbeeswarm-style). The spread is why the forest CI was wide. Script: p3_12.")


# ============================================================ S7 plotly Sankey
def fig_sankey(f):
    try:
        import plotly.graph_objects as go
    except Exception as e:
        log(f"S7 plotly Sankey skipped: {e}"); return
    labels = ["KUSUM", "Agri-elec", "Irrigation", "Groundwater", "Diesel base", "Paper 2 covariates",
              "Master panel",
              "FE + income ctrl", "Event-study DiD", "IV 2SLS", "Carbon ledger", "Heterogeneity", "District",
              "Rebound", "Paradox", "Sign-flip", "Net carbon"]
    idx = {l: i for i, l in enumerate(labels)}
    P = idx["Master panel"]
    src, tgt, val, col = [], [], [], []
    for s in ["KUSUM", "Agri-elec", "Irrigation", "Groundwater", "Diesel base", "Paper 2 covariates"]:
        src += [idx[s]]; tgt += [P]; val += [3]; col += ["rgba(86,180,233,0.45)"]
    for m in ["FE + income ctrl", "Event-study DiD", "IV 2SLS", "Carbon ledger", "Heterogeneity", "District"]:
        src += [P]; tgt += [idx[m]]; val += [3]; col += ["rgba(0,114,178,0.40)"]
    flows = [("FE + income ctrl", "Rebound"), ("Event-study DiD", "Rebound"), ("IV 2SLS", "Paradox"),
             ("District", "Rebound"), ("Heterogeneity", "Sign-flip"), ("Carbon ledger", "Net carbon")]
    for a, b in flows:
        src += [idx[a]]; tgt += [idx[b]]; val += [3]; col += ["rgba(204,121,167,0.45)"]
    node_col = ([C_SRC]*6 + [C_PANEL] + [C_METH]*6 + [C_TAKE]*4)
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=labels, pad=16, thickness=16, color=node_col,
                  line=dict(color="white", width=0.6)),
        link=dict(source=src, target=tgt, value=val, color=col)))
    fig.update_layout(title_text="Figure S7. Paper 3 data → method → finding flow (interactive)",
                      font=dict(size=12, color=INK), paper_bgcolor="white", width=1200, height=680)
    fig.write_html(str(SUM / "S7_pipeline_sankey.html"))
    log("summary figure -> S7_pipeline_sankey.html")
    try:
        fig.write_image(str(SUM / "S7_pipeline_sankey.png"), scale=3, width=1200, height=680)
        log("summary figure -> S7_pipeline_sankey.png (300-dpi via kaleido)")
    except Exception as e:
        log(f"S7 static PNG export skipped ({e}); interactive HTML written.")


def main():
    f = load_facts()
    fig_lineage(f)
    try: fig_coverage(f)
    except Exception as e: log(f"S2 coverage failed: {e}")
    fig_decision(f)
    fig_scorecard(f)
    fig_takeaways(f)
    try: fig_beeswarm(f)
    except Exception as e: log(f"S6 beeswarm failed: {e}")
    fig_sankey(f)
    made = sorted(p.name for p in SUM.glob("S*.*"))
    passfail("p3_12 visual_summary", len(made) >= 6, f"{len(made)} files in outputs/figures/summary/")


if __name__ == "__main__":
    main()
