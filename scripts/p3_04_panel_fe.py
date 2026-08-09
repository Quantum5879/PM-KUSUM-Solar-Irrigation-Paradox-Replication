"""
p3_04_panel_fe.py  —  two-way fixed-effects baseline for each channel.

No assumed functional form: candidate outcome transforms (param_grids.feature_engineering) are
scored by BIC and the winner is logged. Inference via wild cluster bootstrap (Cameron-Gelbach-
Miller 2008) given small N. Treatment = KUSUM intensity (and robustness with log1p pumps).

ECONOMIC CONTROL — log real GDP per capita (`log_gdp_pc`, leveraged from Paper 2's panel).
Rationale: state economic development jointly drives solar-pump uptake and the energy/groundwater
outcomes, so it is a time-varying confounder that state + year fixed effects alone do not absorb
(state FE remove time-invariant level differences; year FE remove common shocks; neither removes
state-specific *trajectories* in income). Including it follows the standard two-way-FE-with-covariates
estimator of Wooldridge (2010, "Econometric Analysis of Cross Section and Panel Data", 2nd ed., MIT
Press, ch. 10). The control is partialled out alongside the FE by the Frisch–Waugh–Lovell theorem
(Frisch & Waugh 1933, Econometrica; Lovell 1963, JASA) — exactly the partialling used in the wild
cluster bootstrap below, so coefficient and inference stay mutually consistent.
"""
from _p3_common import *
import statsmodels.formula.api as smf

# Time-varying economic control(s) added to every channel equation when present with enough coverage.
ECON_CONTROLS = ["log_gdp_pc"]

def avail_controls(d, controls=ECON_CONTROLS, min_n=20):
    """Keep only controls that exist and have >= min_n non-null values on this estimation sample."""
    return [c for c in controls
            if c in d.columns and pd.to_numeric(d[c], errors="coerce").notna().sum() >= min_n]

def transform(y, kind):
    y = pd.to_numeric(y, errors="coerce")
    if kind == "level": return y
    if kind == "log":   return np.log(y.where(y > 0))
    if kind == "asinh": return np.arcsinh(y)
    if kind == "per_net_sown_ha": return y  # already a rate where relevant
    return y

def select_transform(df, ycol, treat, fe="C(state)+C(fy_start)"):
    """Pick outcome transform by BIC over the pre-registered candidate set."""
    best, best_bic = None, np.inf
    for k in PARAM_GRIDS["feature_engineering"]["outcome_transforms"]:
        d = df.copy(); d["_y"] = transform(d[ycol], k)
        d = d.dropna(subset=["_y", treat])
        if d["_y"].nunique() < 10 or len(d) < 20: continue
        try:
            m = smf.ols(f"_y ~ {treat} + {fe}", data=d).fit()
            if m.bic < best_bic: best, best_bic = k, m.bic
        except Exception:
            continue
    return best or "level"

def wild_cluster_boot_p(d, treat, cluster="state", controls=None, reps=None, seed=SEED):
    """Restricted wild cluster bootstrap p-value (Cameron, Gelbach & Miller 2008).

    Rademacher weights, null imposed (H0: beta_treat = 0). Two-way (state x year) FE *and any
    time-varying controls* are partialled out by Frisch-Waugh-Lovell, then the bootstrap is computed
    in closed form per cluster and fully vectorised over reps in numpy. Self-contained (no numba), so
    it is robust to the environment that breaks the `wildboottest` package's njit kernels. Returns the
    two-sided cluster-robust-t p-value.
    """
    controls = list(controls or [])
    reps = int(PARAM_GRIDS["inference"]["n_boot"]) if reps is None else int(reps)
    dd = d.dropna(subset=["_y", treat] + controls).copy()
    x = pd.to_numeric(dd[treat], errors="coerce").to_numpy(float)
    y = pd.to_numeric(dd["_y"], errors="coerce").to_numpy(float)
    ok = np.isfinite(x) & np.isfinite(y)
    dd, x, y = dd[ok], x[ok], y[ok]
    if len(dd) < 20:
        return np.nan
    FE = pd.get_dummies(dd[["state", "fy_start"]].astype(str), drop_first=True).astype(float).to_numpy()
    FE = np.column_stack([np.ones(len(dd)), FE])
    if controls:  # add time-varying controls to the partialled-out design (FWL stays exact)
        FE = np.column_stack([FE, dd[controls].apply(pd.to_numeric, errors="coerce").to_numpy(float)])
    P = FE @ np.linalg.pinv(FE.T @ FE) @ FE.T
    x = x - P @ x; y = y - P @ y                          # FWL residualisation
    sxx = float(x @ x)
    if sxx <= 0:
        return np.nan
    codes = pd.factorize(dd[cluster].to_numpy())[0]
    C = int(codes.max()) + 1
    a = np.array([x[codes == c] @ y[codes == c] for c in range(C)])   # sum_i x_i u_i  (u = restricted resid = y)
    b = np.array([x[codes == c] @ x[codes == c] for c in range(C)])   # sum_i x_i^2
    beta_hat = a.sum() / sxx
    var_hat = np.sum((a - beta_hat * b) ** 2) / sxx ** 2
    if var_hat <= 0:
        return np.nan
    t_obs = beta_hat / np.sqrt(var_hat)
    rng = np.random.default_rng(seed)
    G = rng.choice([-1.0, 1.0], size=(reps, C))
    beta_s = (G @ a) / sxx
    q = G * a[None, :] - beta_s[:, None] * b[None, :]
    var_s = np.sum(q ** 2, axis=1) / sxx ** 2
    t_s = np.divide(beta_s, np.sqrt(var_s), out=np.full(reps, np.nan), where=var_s > 0)
    t_s = t_s[np.isfinite(t_s)]
    if len(t_s) == 0:
        return np.nan
    return float((np.sum(np.abs(t_s) >= abs(t_obs)) + 1) / (len(t_s) + 1))

def run_channel(df, ycol, treat):
    k = select_transform(df, ycol, treat)
    d = df.copy(); d["_y"] = transform(d[ycol], k)
    d = d.dropna(subset=["_y", treat])
    controls = avail_controls(d)                 # e.g. ['log_gdp_pc'] when present with coverage
    if controls:
        d = d.dropna(subset=controls)            # keep one consistent control-complete sample
    ctrl_rhs = (" + " + " + ".join(controls)) if controls else ""
    res = {"outcome": ycol, "transform": k, "treat": treat,
           "controls": "+".join(controls) if controls else "none", "n": len(d)}
    append_tuning_log({"stage": "p3_04", "outcome": ycol, "chosen_transform": k, "metric": "BIC",
                       "controls": controls})
    # try pyfixest with wild cluster bootstrap; fall back to clustered OLS
    try:
        import pyfixest as pf
        fit = pf.feols(f"_y ~ {treat}{ctrl_rhs} | state + fy_start", data=d, vcov={"CRV1": "state"})
        coef = fit.coef().get(treat, np.nan); se = fit.se().get(treat, np.nan)
        try:
            wb = fit.wildboottest(param=treat, reps=PARAM_GRIDS["inference"]["n_boot"], seed=SEED)
            res["wild_p"] = float(getattr(wb, "p_value", np.nan)) if not isinstance(wb, dict) else wb.get("Pr(>|t|)", np.nan)
        except Exception as e:
            log(f"pyfixest wildboot unavailable for {ycol} ({e}); using self-contained WCB")
            res["wild_p"] = wild_cluster_boot_p(d, treat, controls=controls)
        res.update(coef=float(coef), se=float(se))
    except Exception as e:
        log(f"pyfixest unavailable/failed ({e}); using clustered OLS + self-contained WCB")
        m = smf.ols("_y ~ " + treat + ctrl_rhs + " + C(state)+C(fy_start)", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["state"]})
        res.update(coef=float(m.params.get(treat, np.nan)), se=float(m.bse.get(treat, np.nan)),
                   wild_p=wild_cluster_boot_p(d, treat, controls=controls))
    return res

def main():
    p = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    treat = "kusum_intensity_per_kha" if p["kusum_intensity_per_kha"].notna().sum() > 30 else "kusum_log1p_pumps"
    out = []
    for ycol in ["agri_grid_gwh", "tubewells", "gw_stage_step"]:
        if ycol in p.columns:
            out.append(run_channel(p, ycol, treat))
    res = pd.DataFrame(out)
    save_table(res, "fe_channel_results")
    passfail("p3_04 panel_fe", len(res) > 0, f"treat={treat}; {len(res)} channels")

if __name__ == "__main__":
    main()
