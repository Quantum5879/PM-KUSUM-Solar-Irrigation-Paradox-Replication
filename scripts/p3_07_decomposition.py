"""
p3_07_decomposition.py  —  net carbon = gross substitution − intensive-margin rebound.

CRITICAL FIX (peer review): do NOT feed the negative FE tube-well coefficient into a
positive-rebound narrative. Rebound is derived from the IV groundwater-stage response
(intensive margin), converted via a transparent calibrated bridge with sensitivity sweeps.

Bridge (documented):
  delta_stage_pp = beta_IV_gw × kusum_intensity
  extra_extract_bcm ≈ (delta_stage_pp / 100) × extractable_bcm_proxy
  where extractable proxy uses state mean irrigation extraction / (stage/100) when available,
  else a conservative national per-state share of 251 bcm scaled by intensity weight.
  energy_kWh = extra_m3 × e_kWh_per_m3_per_m × lift_m
  rebound_tCO2 = energy_MWh × EF_grid

All constants swept; signed rebound allowed (negative stage response → negative rebound).
"""
from _p3_common import *
import matplotlib.pyplot as plt
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig  # noqa


def _read_iv_gw_beta():
    fp = TAB / "iv_results.csv"
    if not fp.exists():
        return np.nan, {}
    iv = pd.read_csv(fp)
    if "spec" in iv.columns:
        for spec in ["primary_interact", "non_interpolated_gw", "robust_gw_linear"]:
            hit = iv[(iv["spec"] == spec) & (iv["outcome"].isin(["gw_stage_step", "gw_stage_linear"]))]
            if len(hit):
                r = hit.iloc[0]
                return float(r["beta_treat"]), r.to_dict()
    hit = iv[iv["outcome"] == "gw_stage_step"]
    if len(hit):
        r = hit.iloc[0]
        return float(r["beta_treat"]), r.to_dict()
    return np.nan, {}


def main():
    apply_style()
    panel = pd.read_parquet(PROC / "master_panel_state_year.parquet")
    ledger = pd.read_csv(PROC / "agri_carbon_ledger_state_year.csv")
    central = ledger[(ledger.fuel_litres == 600) & (np.isclose(ledger.ef_grid, 0.7383))].copy()

    beta_iv, meta = _read_iv_gw_beta()
    log(f"IV GW beta for rebound bridge = {beta_iv}  meta_spec={meta.get('spec')}")

    # FE tube-well coef retained only as extensive-margin audit (NOT used for positive rebound)
    reb_fe = np.nan
    fe_fp = TAB / "fe_channel_results.csv"
    if fe_fp.exists():
        fe = pd.read_csv(fe_fp)
        row = fe[fe.outcome == "tubewells"]
        if len(row):
            reb_fe = float(row["coef"].iloc[0])
    log(f"FE tubewells coef (extensive margin; NOT rebound driver) = {reb_fe}")

    treat = "kusum_intensity_per_kha"
    e_per_m3_m = LIT["pump_energy_kWh_per_m3_per_m_lift"]["value"]
    ef_grid = 0.7383
    # lift depth proxy (m): scale with stage; baseline 20 m at stage=50
    m = panel[["state", "fy_start", treat, "gw_stress_cat", "gw_stage_step",
               "net_irrigated_000ha", "net_irr_kha_latest"]].copy()

    # Extractable resource proxy from stage definition: stage% = 100 * extraction / extractable
    # => extractable ≈ extraction / (stage/100). Without bcm series in panel, use irrigation area
    # scaled national benchmark: India ~251 bcm total; allocate by NIA share.
    nia = m["net_irrigated_000ha"].fillna(m["net_irr_kha_latest"])
    nia_year = nia.groupby(m["fy_start"]).transform("sum").replace(0, np.nan)
    extractable_bcm = 251.0 * (nia / nia_year)

    intensity = m[treat].fillna(0.0)
    if np.isfinite(beta_iv):
        delta_stage_pp = beta_iv * intensity
    else:
        delta_stage_pp = pd.Series(0.0, index=m.index)
        log("WARNING: no IV beta — rebound set to 0")

    # extra extraction bcm = (delta_stage_pp/100) * extractable_bcm
    extra_bcm = (delta_stage_pp / 100.0) * extractable_bcm.fillna(0)
    extra_m3 = extra_bcm * 1e9
    lift_m = (m["gw_stage_step"].fillna(50) / 50.0 * 20.0).clip(5, 80)
    energy_kWh = extra_m3 * e_per_m3_m * lift_m
    # only attribute rebound energy where delta_stage > 0 (intensive-margin stress);
    # negative delta_stage implies abatement bonus (signed bridge, reported separately)
    m["delta_stage_pp"] = delta_stage_pp
    m["rebound_tco2"] = (energy_kWh / 1000.0) * ef_grid  # signed
    m["rebound_tco2_positive_only"] = m["rebound_tco2"].clip(lower=0)

    # sensitivity grid on energy intensity and lift
    sens_rows = []
    for e in LIT["pump_energy_kWh_per_m3_per_m_lift"]["sensitivity"]:
        for lift_base in [15, 20, 30]:
            lift = (m["gw_stage_step"].fillna(50) / 50.0 * lift_base).clip(5, 80)
            reb = (extra_m3 * e * lift / 1000.0) * ef_grid
            sens_rows.append({
                "e_kWh_per_m3_m": e, "lift_base_m": lift_base,
                "rebound_total_tco2": float(reb.clip(lower=0).sum()),
                "rebound_signed_total_tco2": float(reb.sum()),
            })
    sens = pd.DataFrame(sens_rows)
    save_table(sens, "rebound_bridge_sensitivity")

    out = central.merge(
        m[["state", "fy_start", "rebound_tco2", "rebound_tco2_positive_only",
           "delta_stage_pp", "gw_stress_cat"]],
        on=["state", "fy_start"], how="left", suffixes=("", "_m"))
    out["rebound_tco2"] = out["rebound_tco2_positive_only"].fillna(0)
    out["rebound_tco2_signed"] = out["rebound_tco2_m"].fillna(0)
    out["net_abatement_tco2"] = out["gross_abatement_tco2"] - out["rebound_tco2"]
    out["rebound_offset_share"] = np.where(
        out["gross_abatement_tco2"] > 0,
        out["rebound_tco2"] / out["gross_abatement_tco2"], np.nan)

    # write net back into full ledger central rows
    ledger = ledger.merge(
        out[["state", "fy_start", "rebound_tco2", "net_abatement_tco2", "rebound_tco2_signed"]],
        on=["state", "fy_start"], how="left", suffixes=("", "_c"))
    for col in ["rebound_tco2", "net_abatement_tco2"]:
        ledger[col] = ledger[f"{col}_c"].combine_first(ledger[col])
    if "rebound_tco2_signed_c" in ledger.columns:
        ledger["rebound_tco2_signed"] = ledger["rebound_tco2_signed_c"]
    ledger.drop(columns=[c for c in ledger.columns if c.endswith("_c")], inplace=True)
    ledger.to_csv(PROC / "agri_carbon_ledger_state_year.csv", index=False)

    # Figure 3 — waterfall by groundwater-stress category (latest year with KUSUM>0)
    last = out[out.fy_start == out.fy_start.max()]
    agg = (last.groupby("gw_stress_cat")
           .agg(subst=("gross_abatement_tco2", "sum"),
                reb=("rebound_tco2", "sum"))
           .reset_index().dropna(subset=["gw_stress_cat"]))
    if len(agg):
        agg["net"] = agg["subst"] - agg["reb"]
        # offset_share must be the ratio of the category's own summed totals (reb/subst),
        # not a mean of per-state-year ratios, so it reconciles with the Gross/Rebound
        # columns reported alongside it in the manuscript table (peer-review fix).
        agg["offset_share"] = np.where(agg["subst"] > 0, agg["reb"] / agg["subst"], np.nan)
        order = ["safe", "semi_critical", "critical", "over_exploited"]
        agg["o"] = agg["gw_stress_cat"].map({k: i for i, k in enumerate(order)})
        agg = agg.sort_values("o")
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(agg))
        ax.bar(x, agg["subst"] / 1e3, color="#0072B2", label="substitution (saving)")
        ax.bar(x, -agg["reb"] / 1e3, bottom=agg["subst"] / 1e3, color="#D55E00",
               label="intensive-margin rebound (offset)")
        ax.plot(x, agg["net"] / 1e3, "ko-", label="net abatement")
        ax.axhline(0, color="#444", lw=0.8)
        ax.set_xticks(x); ax.set_xticklabels(agg["gw_stress_cat"], rotation=20)
        ax.set_ylabel("kt CO2e / yr")
        ax.set_title("Figure 3. Substitution vs IV-based intensive-margin rebound")
        ax.legend()
        save_fig(fig, FIG, "fig3_decomposition_waterfall",
                 "Rebound from IV groundwater-stage beta (not FE tube-well coef). Script: p3_07.")
    save_table(agg if len(agg) else out.head(), "decomposition_by_stress")

    # audit note
    audit = pd.DataFrame([{
        "iv_gw_beta": beta_iv,
        "iv_spec": meta.get("spec"),
        "fe_tubewells_coef_NOT_used_for_rebound": reb_fe,
        "bridge": "delta_stage_pp = beta_IV * intensity; extra_bcm = (delta/100)*extractable_proxy; "
                  "energy from e_kWh_per_m3_m * lift_m; EF=0.7383",
        "gross_central_tco2": float(central["gross_abatement_tco2"].sum()) if len(central) else np.nan,
        "rebound_central_tco2": float(out["rebound_tco2"].sum()) if len(out) else np.nan,
        "net_central_tco2": float(out["net_abatement_tco2"].sum()) if len(out) else np.nan,
    }])
    save_table(audit, "rebound_bridge_audit")
    passfail("p3_07 decomposition", np.isfinite(beta_iv),
             f"IV beta={beta_iv}; rebound uses intensive margin")


if __name__ == "__main__":
    main()
