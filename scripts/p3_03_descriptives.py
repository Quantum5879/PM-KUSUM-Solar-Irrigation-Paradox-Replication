"""
p3_03_descriptives.py  —  summary stats, treatment-balance, and Figure 1 (the paradox).
"""
from _p3_common import *
import matplotlib.pyplot as plt
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig, DIVERGING  # noqa

def main():
    apply_style()
    p = pd.read_parquet(PROC / "master_panel_state_year.parquet")

    # summary stats
    num = p.select_dtypes("number")
    save_table(num.describe().T.reset_index().rename(columns={"index": "variable"}), "summary_stats")

    # balance: latest-year treated (top tercile intensity) vs rest
    latest = p[p.fy_start == p.fy_start.max()].copy()
    if latest["kusum_intensity_per_kha"].notna().sum() > 5:
        thr = latest["kusum_intensity_per_kha"].quantile(0.66)
        latest["grp"] = np.where(latest["kusum_intensity_per_kha"] >= thr, "high_KUSUM", "low_KUSUM")
        bal_cols = [c for c in ["gw_stage_step", "tubewells", "agri_grid_gwh", "gsdp_cr",
                                "diesel_pumps_2016_17"] if c in latest]
        bal = latest.groupby("grp")[bal_cols].mean().T
        save_table(bal.reset_index().rename(columns={"index": "variable"}), "balance_table")

    # Figure 1 — the paradox: KUSUM intensity vs groundwater stage of extraction
    d = p[p.fy_start == p.fy_start.max()].dropna(subset=["kusum_intensity_per_kha", "gw_stage_step"])
    if len(d) >= 8:
        fig, ax = plt.subplots(figsize=(7.2, 5.2))
        size = (d.get("net_irrigated_000ha", pd.Series(50, index=d.index)).fillna(50))
        col = d.get("gw_stage_step")
        sc = ax.scatter(d["kusum_intensity_per_kha"], d["gw_stage_step"],
                        s=20 + 0.03 * size, c=col, cmap=DIVERGING, vmin=0, vmax=160,
                        edgecolor="white", linewidth=0.5, alpha=0.9)
        ax.axhline(100, color="#b91c1c", lw=1, ls="--")
        ax.text(ax.get_xlim()[1], 101, " over-exploited (>100%)", color="#b91c1c", fontsize=8, va="bottom", ha="right")
        for st in ["Punjab", "Rajasthan", "Haryana", "Gujarat", "Tamil Nadu"]:
            r = d[d.state == st]
            if len(r):
                ax.annotate(st, (r["kusum_intensity_per_kha"].iloc[0], r["gw_stage_step"].iloc[0]),
                            fontsize=8, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("KUSUM intensity (cumulative solar pumps per 1,000 ha irrigated)")
        ax.set_ylabel("Groundwater stage of extraction (%)")
        ax.set_title("Figure 1. The solar-irrigation paradox")
        fig.colorbar(sc, ax=ax, label="GW stage of extraction (%)")
        save_fig(fig, FIG, "fig1_paradox_scatter",
                 "Bubble size = net irrigated area. Source: KUSUM + CGWB. Script: p3_03.")
        passfail("p3_03 descriptives", True, "Fig1 written")
    else:
        passfail("p3_03 descriptives", False, "too few states with both KUSUM & GW for Fig1")

if __name__ == "__main__":
    main()
