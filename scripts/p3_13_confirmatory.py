"""
p3_13_confirmatory.py  —  assumption stress-tests and confirmatory analyses.

Addresses peer-review CRITICAL/MAJOR items with EXISTING data:
  1. Cross-sectional dose design (no back-cast time path)
  2. Component B vs C separate FE
  3. Continuous KUSUM × gw_stage / DISCOM interactions (interpretable units)
  4. Pre-trend / placebo summaries
  5. Non-interpolated GW FE
  6. Assumption hit-list JSON for manuscript honesty table
"""
from _p3_common import *
import json


def _ols_cluster(df, formula, cluster_col="state"):
    import statsmodels.formula.api as smf
    d = df.copy()
    m = smf.ols(formula, data=d).fit(cov_type="cluster", cov_kwds={"groups": d[cluster_col]})
    return m


def main():
    p = pd.read_parquet(PROC / "master_panel_state_year.parquet").copy()
    rows = []
    assumptions = []

    # ----- 1. Cross-sectional dose (latest year, no back-cast dynamics) -----
    last_yr = int(p.loc[p["kusum_dose_per_kha"].fillna(0) > 0, "fy_start"].max()) if "kusum_dose_per_kha" in p.columns else int(p["fy_start"].max())
    cs = p[p["fy_start"] == last_yr].dropna(subset=["gw_stage_step"]).copy()
    if "kusum_dose_per_kha" in cs.columns and cs["kusum_dose_per_kha"].notna().sum() > 15:
        try:
            m = _ols_cluster(cs.dropna(subset=["kusum_dose_per_kha", "log_gdp_pc"]),
                             "gw_stage_step ~ kusum_dose_per_kha + log_gdp_pc")
            rows.append({
                "test": "cross_section_dose_gw",
                "beta": float(m.params["kusum_dose_per_kha"]),
                "se": float(m.bse["kusum_dose_per_kha"]),
                "pvalue": float(m.pvalues["kusum_dose_per_kha"]),
                "n": int(m.nobs),
                "note": f"FY{last_yr} terminal dose; no back-cast path",
            })
        except Exception as e:
            log(f"CS dose fail: {e}")

    # ----- 2. Component B vs C FE (pooled years) -----
    for tr, lab in [("kusum_intensity_B_per_kha", "FE_component_B_tubewells"),
                    ("kusum_intensity_C_per_kha", "FE_component_C_tubewells"),
                    ("kusum_intensity_B_per_kha", "FE_component_B_gw"),
                    ("kusum_intensity_C_per_kha", "FE_component_C_gw")]:
        if tr not in p.columns:
            continue
        y = "tubewells" if "tubewells" in lab else "gw_stage_step"
        d = p.dropna(subset=[y, tr, "log_gdp_pc"]).copy()
        if y == "tubewells":
            d = d[d[y] > 0]
            d["_y"] = np.log(d[y])
        else:
            d["_y"] = d[y]
        if len(d) < 40:
            continue
        try:
            m = _ols_cluster(d, f"_y ~ {tr} + log_gdp_pc + C(state) + C(fy_start)")
            rows.append({
                "test": lab, "beta": float(m.params[tr]), "se": float(m.bse[tr]),
                "pvalue": float(m.pvalues[tr]), "n": int(m.nobs),
                "note": "TWFE with income; component-separated treatment",
            })
        except Exception as e:
            log(f"{lab} fail: {e}")

    # ----- 3. Continuous interactions (interpretable) -----
    d = p.dropna(subset=["tubewells", "kusum_intensity_per_kha", "gw_stage_step", "discom_health", "log_gdp_pc"]).copy()
    d = d[d["tubewells"] > 0]
    d["log_tw"] = np.log(d["tubewells"])
    d["kusum_x_gw"] = d["kusum_intensity_per_kha"] * d["gw_stage_step"]
    d["kusum_x_discom"] = d["kusum_intensity_per_kha"] * d["discom_health"]
    try:
        m = _ols_cluster(d, "log_tw ~ kusum_intensity_per_kha + kusum_x_gw + kusum_x_discom + log_gdp_pc + C(state) + C(fy_start)")
        for term in ["kusum_intensity_per_kha", "kusum_x_gw", "kusum_x_discom"]:
            rows.append({
                "test": f"continuous_interaction_{term}",
                "beta": float(m.params[term]), "se": float(m.bse[term]),
                "pvalue": float(m.pvalues[term]), "n": int(m.nobs),
                "note": "continuous gw_stage and discom interactions (not sparse category)",
            })
    except Exception as e:
        log(f"continuous interaction fail: {e}")

    # ----- 4. Non-interpolated GW FE -----
    if "gw_interpolated" in p.columns:
        d = p[(p["gw_interpolated"] == 0)].dropna(subset=["gw_stage_step", "kusum_intensity_per_kha", "log_gdp_pc"])
        try:
            m = _ols_cluster(d, "gw_stage_step ~ kusum_intensity_per_kha + log_gdp_pc + C(state) + C(fy_start)")
            rows.append({
                "test": "FE_gw_non_interpolated",
                "beta": float(m.params["kusum_intensity_per_kha"]),
                "se": float(m.bse["kusum_intensity_per_kha"]),
                "pvalue": float(m.pvalues["kusum_intensity_per_kha"]),
                "n": int(m.nobs),
                "note": "assessment years only (2020/22/23/24)",
            })
        except Exception as e:
            log(f"non-interp FE fail: {e}")

    # ----- 5. Parallel FE on canal (placebo channel) -----
    d = p.dropna(subset=["canal_total", "kusum_intensity_per_kha", "log_gdp_pc"]).copy()
    d = d[d["canal_total"] > 0]
    d["log_canal"] = np.log(d["canal_total"])
    try:
        m = _ols_cluster(d, "log_canal ~ kusum_intensity_per_kha + log_gdp_pc + C(state) + C(fy_start)")
        rows.append({
            "test": "placebo_FE_canal",
            "beta": float(m.params["kusum_intensity_per_kha"]),
            "se": float(m.bse["kusum_intensity_per_kha"]),
            "pvalue": float(m.pvalues["kusum_intensity_per_kha"]),
            "n": int(m.nobs),
            "note": "canal area should be weakly related if solar-pump rebound is GW-specific",
        })
    except Exception as e:
        log(f"canal placebo fail: {e}")

    res = pd.DataFrame(rows)
    save_table(res, "confirmatory_tests")

    # ----- Assumption hit-list -----
    assumptions = [
        {"assumption": "Back-cast treatment shares are time-invariant",
         "threat": "Mechanical endogeneity with terminal adopters",
         "test": "cross_section_dose_gw + IV battery",
         "status": "PARTIAL — IV + CS dose required for causal claims"},
        {"assumption": "GHI × diesel density excludes non-KUSUM GW channels",
         "threat": "Historic free-power / wheat-rice complex",
         "test": "iv_reduced_form_placebos + instrument variants",
         "status": "STRESSED — report F and placebos; do not claim ironclad exclusion"},
        {"assumption": "FE tube-well decline implies less water",
         "threat": "Extensive vs intensive margin divergence",
         "test": "IV gw_stage positive vs FE tubewells negative",
         "status": "REJECTED as water proxy — intensive margin from IV"},
        {"assumption": "District irr_share regression identifies KUSUM",
         "threat": "No KUSUM exposure in district file",
         "test": "code review p3_10",
         "status": "REJECTED — descriptive hydro correlation only"},
        {"assumption": "Interpolated GW stage is harmless",
         "threat": "64% interpolated cells",
         "test": "FE_gw_non_interpolated + IV non_interpolated_gw",
         "status": "CHECKED — report both"},
        {"assumption": "Pooled B+C treatment is homogeneous",
         "threat": "Opposite incentive regimes",
         "test": "FE_component_B/C_*",
         "status": "CHECKED — report separately"},
        {"assumption": "Rebound carbon from FE tubewell coef",
         "threat": "Sign inconsistency (negative coef → zero rebound)",
         "test": "rebound_bridge_audit uses IV beta",
         "status": "FIXED — IV intensive-margin bridge"},
    ]
    (REP / "assumption_stress_tests.json").write_text(json.dumps(assumptions, indent=2), encoding="utf-8")
    save_table(pd.DataFrame(assumptions), "assumption_stress_tests")

    append_tuning_log({"stage": "p3_13", "n_tests": len(res)})
    passfail("p3_13 confirmatory", len(res) >= 3, f"{len(res)} tests")


if __name__ == "__main__":
    main()
