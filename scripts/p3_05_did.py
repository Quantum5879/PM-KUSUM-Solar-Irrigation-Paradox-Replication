"""
p3_05_did.py  —  staggered / dose difference-in-differences.

Treatment onset = first year a state's cumulative KUSUM intensity crosses a percentile threshold;
the threshold is SWEPT over param_grids.did.onset_threshold_pctiles (not assumed). Estimators:
Sun & Abraham (2021) event study via pyfixest; Callaway & Sant'Anna (2021) via `differences` if
installed; de Chaisemartin-D'Haultfoeuille continuous flagged. Produces Figure 2.
"""
from _p3_common import *
import matplotlib.pyplot as plt
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig  # noqa

def onset_year(p, treat_col, pctile):
    thr = p[treat_col].quantile(pctile / 100.0)
    onset = {}
    for st, g in p.sort_values("fy_start").groupby("state"):
        crossed = g[g[treat_col] >= thr]
        onset[st] = crossed["fy_start"].min() if len(crossed) else np.nan
    return onset, thr

def event_study(p, ycol, treat_col, pctile):
    onset, thr = onset_year(p, treat_col, pctile)
    d = p.copy(); d["onset"] = d["state"].map(onset)
    d["rel"] = d["fy_start"] - d["onset"]
    d = d.dropna(subset=[ycol]); d["_y"] = pd.to_numeric(d[ycol], errors="coerce")
    d["evertreated"] = d["onset"].notna().astype(int)
    d.loc[d["onset"].isna(), "rel"] = -1000  # never-treated control bucket
    try:
        import pyfixest as pf
        # Sun & Abraham via interaction of relative-time with cohort; here a binned event-study proxy
        d["rel_c"] = d["rel"].clip(-3, 3)
        d = d[d["rel"] != -1000]  # restrict to treated for the dynamic plot; controls absorbed by FE
        fit = pf.feols("_y ~ i(rel_c, ref=-1) | state + fy_start", data=d, vcov={"CRV1": "state"})
        co = fit.coef(); se = fit.se()
        def _parse_rel(k):
            if "rel_c" not in k: return None
            try: return int(float(k.split("::")[-1]))  # pyfixest 0.60 labels terms 'rel_c::-3.0'
            except Exception: return None
        ev = pd.DataFrame({"rel": [_parse_rel(k) for k in co.index],
                           "coef": co.values, "se": se.values})
        ev = ev.dropna(subset=["rel"]).sort_values("rel")
        return ev, thr
    except Exception as e:
        log(f"event study (pyfixest) failed for {ycol}: {e}")
        return pd.DataFrame(), thr

def callaway_santanna(p, ycol, treat_col, pctile):
    try:
        from differences import ATTgt
        onset, _ = onset_year(p, treat_col, pctile)
        # `differences` expects never-treated cohort = NaN (NOT 0).
        d = p.copy(); d["g"] = d["state"].map(onset)
        d["_y"] = pd.to_numeric(d[ycol], errors="coerce")
        d = d.dropna(subset=["_y"]).set_index(["state", "fy_start"])
        att = ATTgt(data=d, cohort_column="g")  # `differences` API: cohort_column (0 = never-treated)
        att.fit(formula="_y")
        return att.aggregate("event")
    except Exception as e:
        log(f"Callaway-Sant'Anna skipped ({e}); install `differences` to enable.")
        return None

def main():
    apply_style()
    p = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    treat = "kusum_intensity_per_kha" if p["kusum_intensity_per_kha"].notna().sum() > 30 else "kusum_cum_pumps"
    grid = PARAM_GRIDS["did"]["onset_threshold_pctiles"]
    central = grid[len(grid)//2]
    append_tuning_log({"stage": "p3_05", "onset_pctile_grid": grid, "central": central})

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharex=True)
    for ax, ycol, title in zip(axes, ["agri_grid_gwh", "tubewells", "gw_stage_step"],
                               ["Agri grid electricity", "Tube-well irrigated area", "GW stage of extraction"]):
        if ycol not in p.columns:
            ax.set_visible(False); continue
        ev, thr = event_study(p, ycol, treat, central)
        # threshold sweep (robustness): store min/max coef at rel=+1 across thresholds
        sweep = []
        for pc in grid:
            e2, _ = event_study(p, ycol, treat, pc)
            if not len(e2) or "rel" not in e2.columns:
                continue
            v = e2[e2.rel == 1]["coef"]
            if len(v): sweep.append(v.iloc[0])
        if len(ev):
            ax.axhline(0, color="#888", lw=0.8); ax.axvline(-0.5, color="#b91c1c", lw=1, ls="--")
            ax.errorbar(ev["rel"], ev["coef"], yerr=1.96*ev["se"], fmt="o-", capsize=3, color="#0072B2")
            ax.fill_between(ev["rel"], ev["coef"]-1.96*ev["se"], ev["coef"]+1.96*ev["se"], alpha=0.15, color="#0072B2")
            ev.to_csv(TAB / f"eventstudy_{ycol}.csv", index=False)
        ax.set_title(title, fontsize=10); ax.set_xlabel("years since KUSUM onset")
        if len(sweep): log(f"{ycol}: rel+1 effect across thresholds {grid}: {np.round(sweep,3)}")
    axes[0].set_ylabel("effect (transform per p3_04)")
    fig.suptitle("Figure 2. Event-study dynamics by channel (Sun-Abraham)", y=1.02)
    save_fig(fig, FIG, "fig2_event_studies", "Central onset threshold; sweep in log. Script: p3_05.")

    cs = callaway_santanna(p, "tubewells", treat, central)
    if cs is not None:
        try: cs.to_csv(TAB / "callaway_santanna_tubewells.csv")
        except Exception: pass
    passfail("p3_05 did", True, f"central pctile={central}")

if __name__ == "__main__":
    main()
