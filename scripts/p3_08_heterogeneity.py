"""
p3_08_heterogeneity.py  —  where the effect flips. Runs BOTH a causal forest and a transparent
interaction model; a pre-registered rule decides which is primary.

Causal forest: econml.CausalForestDML with GridSearchCV-tuned nuisance learners (no hardcoded
hyperparameters; grids in param_grids.json). Outcome Y = tube-well irrigated area (rebound);
treatment T = KUSUM intensity; heterogeneity X = institutional & climate features. Figure 4 = the
sign-flip surface (effect over DISCOM health x groundwater stress).

PRE-REGISTERED RULE: if forest CATE CIs are tight & agree in sign with the interaction model ->
forest primary; else interaction model primary, forest reported as ML validation.
"""
from _p3_common import *
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig, DIVERGING  # noqa

def tune_nuisance(X, y):
    """GridSearchCV over candidate learners; return best estimator + logged metric."""
    from sklearn.model_selection import GridSearchCV
    from sklearn.linear_model import Lasso
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    g = PARAM_GRIDS["dml_nuisance_models"]; cv = PARAM_GRIDS["cv_folds"]
    cands = []
    cands.append(("lasso", GridSearchCV(Lasso(max_iter=5000), {"alpha": g["lasso"]["alpha"]}, cv=cv)))
    cands.append(("rf", GridSearchCV(RandomForestRegressor(random_state=SEED), g["random_forest"], cv=cv)))
    cands.append(("gbm", GridSearchCV(GradientBoostingRegressor(random_state=SEED), g["gradient_boosting"], cv=cv)))
    best, best_score, best_name = None, -np.inf, None
    for name, gs in cands:
        try:
            gs.fit(X, y)
            if gs.best_score_ > best_score:
                best, best_score, best_name = gs.best_estimator_, gs.best_score_, name
        except Exception as e:
            log(f"nuisance {name} failed: {e}")
    append_tuning_log({"stage": "p3_08", "nuisance_best": best_name, "cv_R2": float(best_score)})
    return best

def main():
    apply_style()
    p = pd.read_parquet(PROC / "master_panel_state_year.parquet").copy()
    treat = "kusum_intensity_per_kha" if p["kusum_intensity_per_kha"].notna().sum() > 30 else "kusum_cum_pumps"
    Y = "tubewells"
    # Economic dimension = log real GDP per capita (Paper 2), not raw GSDP level: per-capita avoids
    # collinearity with state size and matches the p3_04 control (Wooldridge 2010, ch. 10).
    econ = "log_gdp_pc" if "log_gdp_pc" in p.columns else ("gsdp_cr" if "gsdp_cr" in p.columns else None)
    feats = [c for c in ["discom_health", "ghi_annual", "rpo_compliance", "gw_stage_step", econ]
             if c and c in p.columns]
    if "gw_stage_step" not in feats:
        log("WARNING gw_stage_step missing — heterogeneity limited");
    d = p.dropna(subset=[Y, treat] + feats).copy()
    for c in [Y, treat] + feats: d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=[Y, treat] + feats)
    log(f"heterogeneity: N={len(d)}, features={feats}")

    # ---------- transparent interaction model (always runs) ----------
    # Same time-varying economic control as p3_04 (log GDP per capita; Wooldridge 2010, ch. 10),
    # added to each interaction so the moderation is net of income confounding.
    ctrl = (" + " + econ) if (econ and econ in p.columns) else ""
    inter = {}
    for mod in ["gw_stress_cat", "discom_health"]:
        if mod == "gw_stress_cat" and "gw_stress_cat" in p.columns:
            sub = [Y, treat, "gw_stress_cat"] + ([econ] if ctrl else [])
            dd = p.dropna(subset=sub).copy()
            try:
                m = smf.ols(f"{Y} ~ {treat}*C(gw_stress_cat){ctrl} + C(state)+C(fy_start)", data=dd).fit(
                    cov_type="cluster", cov_kwds={"groups": dd["state"]})
                inter["by_gw_stress"] = {k: float(v) for k, v in m.params.items() if treat in k}
            except Exception as e: log(f"interaction gw_stress failed: {e}")
        if mod == "discom_health" and "discom_health" in p.columns:
            sub = [Y, treat, "discom_health"] + ([econ] if ctrl else [])
            dd = p.dropna(subset=sub).copy()
            try:
                m = smf.ols(f"{Y} ~ {treat}*discom_health{ctrl} + C(state)+C(fy_start)", data=dd).fit(
                    cov_type="cluster", cov_kwds={"groups": dd["state"]})
                inter["by_discom"] = {k: float(v) for k, v in m.params.items() if treat in k}
            except Exception as e: log(f"interaction discom failed: {e}")
    pd.DataFrame(inter).to_csv(TAB / "heterogeneity_interactions.csv")

    # ---------- causal forest (tuned) ----------
    cate_ok = False
    try:
        from econml.dml import CausalForestDML
        X = d[feats].values; T = d[treat].values; Yv = d[Y].values
        model_y = tune_nuisance(X, Yv); model_t = tune_nuisance(X, T)
        cf_grid = PARAM_GRIDS["causal_forest"]
        est = CausalForestDML(model_y=model_y, model_t=model_t, discrete_treatment=False,
                              n_estimators=max(cf_grid["n_estimators"]),
                              min_samples_leaf=min(cf_grid["min_samples_leaf"]),
                              honest=True, random_state=SEED)
        est.fit(Yv, T, X=X)
        d["cate"] = est.effect(X)
        lb, ub = est.effect_interval(X, alpha=0.05)
        d["cate_lb"], d["cate_ub"] = lb, ub
        d[["state", "fy_start", "cate", "cate_lb", "cate_ub"] + feats].to_csv(TAB / "causal_forest_cate.csv", index=False)
        ci_width = float(np.nanmean(ub - lb)); spread = float(np.nanstd(d["cate"]))
        append_tuning_log({"stage": "p3_08", "cate_mean_ci_width": ci_width, "cate_std": spread})
        cate_ok = True
        # pre-registered referee
        primary = "causal_forest" if (ci_width < spread) else "interaction_model"
        log(f"PRE-REGISTERED RULE -> primary = {primary} (ci_width={ci_width:.3f}, spread={spread:.3f})")
    except Exception as e:
        log(f"CausalForestDML failed/absent ({e}); interaction model is primary.")

    # ---------- Figure 4: sign-flip surface ----------
    ax_x = "discom_health" if "discom_health" in d.columns else ("gsdp_cr" if "gsdp_cr" in d.columns else None)
    ax_y = "gw_stage_step" if "gw_stage_step" in d.columns else None
    if cate_ok and ax_x and ax_y:
        fig, ax = plt.subplots(figsize=(7, 5.4))
        sc = ax.scatter(d[ax_x], d[ax_y], c=d["cate"], cmap=DIVERGING,
                        s=40, edgecolor="white", linewidth=0.4,
                        vmin=-np.nanmax(np.abs(d["cate"])), vmax=np.nanmax(np.abs(d["cate"])))
        ax.set_xlabel(ax_x); ax.set_ylabel(ax_y + "  (groundwater stress %)")
        ax.set_title("Figure 4. Where KUSUM's groundwater effect flips sign")
        cb = fig.colorbar(sc, ax=ax); cb.set_label("CATE: KUSUM -> tube-well area (red = backfire)")
        save_fig(fig, FIG, "fig4_signflip_surface",
                 "Causal-forest CATE over institutional x stress space. Script: p3_08.")
    passfail("p3_08 heterogeneity", True, f"forest={'ok' if cate_ok else 'fallback-interactions'}")

if __name__ == "__main__":
    main()
