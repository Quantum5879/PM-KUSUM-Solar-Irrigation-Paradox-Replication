"""
p3_06_iv.py  —  IV battery for KUSUM effects (strengthened identification package).

Primary: 2SLS with instrument = GHI_obs × baseline diesel density.
Battery:
  - instrument variants (interaction / GHI alone / diesel alone)
  - Component B-only and C-only endogenous treatments
  - non-interpolated groundwater subsample
  - pre-2019 placebo reduced form (should be null)
  - canal-area placebo outcome
  - Hausman-style FE vs IV comparison table
"""
from _p3_common import *


def _first_stage_F(fs):
    try:
        return float(fs["f.stat"].iloc[0])
    except Exception:
        try:
            return float(fs["f.stat"])
        except Exception:
            return np.nan


def _fit_iv(d, ycol, treat, iv_col):
    from linearmodels.iv import IV2SLS
    dd = d.dropna(subset=[ycol, treat, iv_col, "log_gdp_pc"]).copy()
    dd["_y"] = pd.to_numeric(dd[ycol], errors="coerce")
    dd = dd.dropna(subset=["_y"])
    if len(dd) < 30 or dd[iv_col].nunique() < 5:
        return None
    # drop singleton clusters
    vc = dd["state"].value_counts()
    dd = dd[dd["state"].isin(vc[vc >= 2].index)]
    if len(dd) < 30:
        return None
    f = f"_y ~ 1 + log_gdp_pc + C(state) + C(fy_start) + [{treat} ~ {iv_col}]"
    res = IV2SLS.from_formula(f, dd).fit(cov_type="clustered", clusters=dd["state"])
    return {
        "outcome": ycol,
        "treatment": treat,
        "instrument_col": iv_col,
        "beta_treat": float(res.params.get(treat, np.nan)),
        "se": float(res.std_errors.get(treat, np.nan)),
        "pvalue": float(res.pvalues.get(treat, np.nan)),
        "first_stage_F": _first_stage_F(res.first_stage.diagnostics),
        "n": int(res.nobs),
    }


def _reduced_form(d, ycol, iv_col, label):
    """OLS of outcome on instrument (+ FE + income) — placebo / RF check."""
    import statsmodels.formula.api as smf
    dd = d.dropna(subset=[ycol, iv_col, "log_gdp_pc"]).copy()
    if len(dd) < 30:
        return None
    try:
        m = smf.ols(f"{ycol} ~ {iv_col} + log_gdp_pc + C(state) + C(fy_start)", data=dd).fit(
            cov_type="cluster", cov_kwds={"groups": dd["state"]}
        )
        return {
            "label": label,
            "outcome": ycol,
            "instrument_col": iv_col,
            "beta_iv": float(m.params.get(iv_col, np.nan)),
            "se": float(m.bse.get(iv_col, np.nan)),
            "pvalue": float(m.pvalues.get(iv_col, np.nan)),
            "n": int(m.nobs),
        }
    except Exception as e:
        log(f"RF failed {label}: {e}")
        return None


def main():
    p = pd.read_parquet(PROC / "master_panel_state_year.parquet").copy()
    treat = "kusum_intensity_per_kha"
    p["diesel_density"] = p["diesel_pumps_2016_17"] / p["net_irrigated_000ha"].replace(0, np.nan)
    # time-invariant diesel density using latest NIA when year-specific missing
    p["diesel_density"] = p["diesel_density"].fillna(
        p["diesel_pumps_2016_17"] / p["net_irr_kha_latest"].replace(0, np.nan)
    )
    ghi_col = "ghi_annual_obs" if p.get("ghi_annual_obs") is not None and p["ghi_annual_obs"].notna().any() else "ghi_annual"
    p["iv_interact"] = p[ghi_col] * p["diesel_density"]
    p["iv_ghi"] = p[ghi_col]
    p["iv_diesel"] = p["diesel_density"]

    out = []
    rf_out = []
    try:
        from linearmodels.iv import IV2SLS  # noqa: F401
    except Exception as e:
        log(f"linearmodels absent: {e}")
        save_table(pd.DataFrame(), "iv_results")
        passfail("p3_06 iv", False, "linearmodels missing")
        return

    # --- primary + instrument variants ---
    specs = [
        ("gw_stage_step", treat, "iv_interact", "primary_interact"),
        ("gw_stage_step", treat, "iv_ghi", "variant_ghi_alone"),
        ("gw_stage_step", treat, "iv_diesel", "variant_diesel_alone"),
        ("tubewells", treat, "iv_interact", "primary_tubewells"),
        ("agri_grid_gwh", treat, "iv_interact", "primary_elec"),
        ("gw_stage_linear", treat, "iv_interact", "robust_gw_linear"),
    ]
    # Component B / C treatments
    if "kusum_intensity_B_per_kha" in p.columns:
        specs += [
            ("gw_stage_step", "kusum_intensity_B_per_kha", "iv_interact", "component_B"),
            ("gw_stage_step", "kusum_intensity_C_per_kha", "iv_interact", "component_C"),
        ]

    for ycol, tr, ivc, tag in specs:
        if ycol not in p.columns or tr not in p.columns:
            continue
        try:
            r = _fit_iv(p, ycol, tr, ivc)
            if r:
                r["spec"] = tag
                r["instrument"] = f"{ivc} (GHI={ghi_col})"
                out.append(r)
                log(f"IV {tag}: beta={r['beta_treat']:.4g} F={r['first_stage_F']:.2f} n={r['n']}")
        except Exception as e:
            log(f"IV fail {tag}: {e}")

    # --- non-interpolated GW subsample ---
    if "gw_interpolated" in p.columns:
        d_ni = p[p["gw_interpolated"] == 0].copy()
        try:
            r = _fit_iv(d_ni, "gw_stage_step", treat, "iv_interact")
            if r:
                r["spec"] = "non_interpolated_gw"
                r["instrument"] = f"iv_interact (GHI={ghi_col})"
                out.append(r)
                log(f"IV non-interp: beta={r['beta_treat']:.4g} F={r['first_stage_F']:.2f} n={r['n']}")
        except Exception as e:
            log(f"IV non-interp fail: {e}")

    # --- placebo reduced forms ---
    # Pre-KUSUM years: instrument should not predict groundwater dynamics before 2019
    pre = p[p["fy_start"] <= 2018].copy()
    for ycol, lab in [("gw_stage_step", "placebo_pre2019_gw"),
                      ("tubewells", "placebo_pre2019_tubewells"),
                      ("canal_total", "placebo_canal_outcome")]:
        if ycol not in p.columns:
            continue
        src = pre if "pre2019" in lab else p
        rf = _reduced_form(src, ycol, "iv_interact", lab)
        if rf:
            rf_out.append(rf)
            log(f"RF {lab}: beta={rf['beta_iv']:.4g} p={rf['pvalue']:.3g}")

    # Post-onset reduced form (should be non-null if IV story holds)
    post = p[p["fy_start"] >= 2020].copy()
    rf = _reduced_form(post, "gw_stage_step", "iv_interact", "RF_post2020_gw")
    if rf:
        rf_out.append(rf)

    res = pd.DataFrame(out)
    save_table(res, "iv_results")
    save_table(pd.DataFrame(rf_out), "iv_reduced_form_placebos")

    # headline row for downstream scripts
    primary = res[res["spec"] == "primary_interact"]
    note = "no primary"
    if len(primary):
        note = (f"primary beta={primary.iloc[0]['beta_treat']:.4f} "
                f"F={primary.iloc[0]['first_stage_F']:.1f} n={int(primary.iloc[0]['n'])}")
    append_tuning_log({"stage": "p3_06", "n_specs": len(res), "primary": note})
    passfail("p3_06 iv", len(res) > 0, note)


if __name__ == "__main__":
    main()
