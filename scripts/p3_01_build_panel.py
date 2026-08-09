"""
p3_01_build_panel.py  —  assemble the master state x fiscal-year panel.

Principles: standardise state names FIRST; keep MULTIPLE candidate treatment series and
both groundwater-interpolation rules (selection happens in the models, not here); never
silently impute across coverage gaps. Inherited Paper 1/2 covariates (GHI, RPO, T&D->DISCOM)
are loaded best-effort and flagged TODO where exact filenames must be confirmed.

Output: paper3/data/processed/master_panel_state_year.parquet  (+ data_dictionary.csv, coverage heatmap)
"""
from _p3_common import *
import re, glob
import matplotlib.pyplot as plt
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig  # noqa

YEARS = list(range(2014, 2025))  # FY start years 2014-15 .. 2024-25

# ---------------------------------------------------------------- source loaders
def _melt_year_cols(df, value_prefixes):
    """Long-format a wide table whose columns look like '<prefix>_<yyyy>_<yy>'."""
    rows = []
    for _, r in df.iterrows():
        for col in df.columns:
            for pref, outname in value_prefixes.items():
                m = re.match(rf"{pref}_(\d{{4}})_(\d{{2}})$", col)
                if m:
                    rows.append({"state": r["state"], "fy_start": int(m.group(1)),
                                 outname: pd.to_numeric(r[col], errors="coerce")})
    long = pd.DataFrame(rows)
    return long.groupby(["state", "fy_start"], as_index=False).first()

def load_agri_electricity():
    frames = []
    for fn in ["agri_electricity_consumption_GWh_2016-17_to_2019-20.csv",
               "agri_electricity_consumption_GWh_2020-21_to_2021-22.csv"]:
        fp = RAW / fn
        if not fp.exists():
            log(f"WARNING missing {fn}"); continue
        df = pd.read_csv(fp); df["state"] = standardize_state(df["state"])
        frames.append(_melt_year_cols(df, {"agri_GWh": "agri_grid_gwh", "total_GWh": "total_elec_gwh"}))
    if not frames: return pd.DataFrame(columns=["state", "fy_start"])
    out = pd.concat(frames).groupby(["state", "fy_start"], as_index=False).first()
    return drop_total(out)

def load_irrigation():
    fp = RAW / "net_irrigated_area_by_source_000ha_LONG_2014-15_to_2023-24.csv"
    df = pd.read_csv(fp); df["state"] = standardize_state(df["state"])
    df["fy_start"] = df["fy"].map(fy_to_int)
    keep = df[["state", "fy_start", "tubewells", "other_wells", "canal_total",
               "net_irrigated_000ha"]].copy()
    for c in ["tubewells", "other_wells", "canal_total", "net_irrigated_000ha"]:
        keep[c] = pd.to_numeric(keep[c], errors="coerce")
    return drop_total(keep)

def load_groundwater():
    fp = RAW / "groundwater_resources_LONG_2020_2022_2023_2024.csv"
    df = pd.read_csv(fp); df["state"] = standardize_state(df["state"])
    df = drop_total(df).rename(columns={"assessment_year": "gw_year"})
    for c in ["extractable_bcm", "extraction_irrigation_bcm", "extraction_total_bcm", "stage_of_extraction_pct"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def interpolate_groundwater(gw):
    """Two rules (both kept): step carry-forward and linear, mapped onto FY YEARS."""
    out = []
    for st, g in gw.groupby("state"):
        # dedupe to one value per assessment year (avoids duplicate-index reindex error)
        s = g.groupby("gw_year")["stage_of_extraction_pct"].mean().sort_index()
        allidx = sorted(set(YEARS) | set(s.index))
        ser = s.reindex(allidx).sort_index()
        step = ser.ffill().bfill().reindex(YEARS)
        lin  = ser.interpolate(method="index").ffill().bfill().reindex(YEARS)
        for y in YEARS:
            out.append({"state": st, "fy_start": y,
                        "gw_stage_step": step.get(y), "gw_stage_linear": lin.get(y),
                        "gw_interpolated": int(y not in set(s.index))})
    return pd.DataFrame(out)

def load_diesel_baseline():
    fp = RAW / "kusum_statewise_diesel_vs_standalonesolar_pumps_as31Oct2022.csv"
    df = pd.read_csv(fp); df["state"] = standardize_state(df["state"])
    df = drop_total(df)
    df["diesel_pumps_2016_17"] = pd.to_numeric(df["diesel_pumps_AISI_2016_17"], errors="coerce")
    return df[["state", "diesel_pumps_2016_17", "standalone_solar_pumps_installed"]]

def load_kusum_treatment(net_sown_proxy):
    """Back-cast KUSUM treatments: pooled B+C (primary), B-only, C-only, and equal-growth alternative.

    Primary rule: national cumulative additions × latest state share (mechanical; used with IV).
    Alternatives retained for confirmatory sweeps in p3_13.
    """
    nat = pd.read_csv(RAW / "kusum_national_physical_progress_2019-20_to_2024-25.csv")
    nat["fy_start"] = nat["year"].map(fy_to_int)
    nat["add_B"] = pd.to_numeric(nat["componentB_pumps"], errors="coerce").fillna(0)
    nat["add_C"] = pd.to_numeric(nat["componentC_pumps"], errors="coerce").fillna(0)
    nat["add_pumps"] = nat["add_B"] + nat["add_C"]
    nat = nat.sort_values("fy_start")
    nat["cum_pumps_nat"] = nat["add_pumps"].cumsum()
    nat["cum_B_nat"] = nat["add_B"].cumsum()
    nat["cum_C_nat"] = nat["add_C"].cumsum()

    snap = pd.read_csv(RAW / "kusum_statewise_progress_components_as30Jun2025.csv")
    snap["state"] = standardize_state(snap["state"]); snap = drop_total(snap)
    snap["cum_B"] = pd.to_numeric(snap.get("compB_installed_no"), errors="coerce").fillna(0)
    snap["cum_C"] = pd.to_numeric(snap.get("compC_installed_IPS_FLS"), errors="coerce").fillna(0)
    snap["cum_installed"] = snap["cum_B"] + snap["cum_C"]
    tot = snap["cum_installed"].sum()
    tot_B = snap["cum_B"].sum(); tot_C = snap["cum_C"].sum()
    snap["share_pool"] = snap["cum_installed"] / tot if tot else 0.0
    snap["share_B"] = snap["cum_B"] / tot_B if tot_B else 0.0
    snap["share_C"] = snap["cum_C"] / tot_C if tot_C else 0.0

    # equal-growth alternative: allocate each year's national addition by same terminal shares
    # (identical path shape to primary under constant shares — kept as explicit column for audit)
    rows = []
    for _, s in snap.iterrows():
        for _, n in nat.iterrows():
            rows.append({
                "state": s["state"], "fy_start": int(n["fy_start"]),
                "kusum_cum_pumps": s["share_pool"] * n["cum_pumps_nat"],
                "kusum_cum_B": s["share_B"] * n["cum_B_nat"],
                "kusum_cum_C": s["share_C"] * n["cum_C_nat"],
                "kusum_share_pool": s["share_pool"],
                "kusum_share_B": s["share_B"],
                "kusum_share_C": s["share_C"],
                # cross-section dose (no time path): terminal cumulative only, repeated
                "kusum_dose_terminal": s["cum_installed"],
                "kusum_dose_B_terminal": s["cum_B"],
                "kusum_dose_C_terminal": s["cum_C"],
            })
    k = pd.DataFrame(rows)
    k = k.merge(net_sown_proxy, on="state", how="left")
    den = k["net_irr_kha_latest"].replace(0, np.nan)
    k["kusum_intensity_per_kha"] = k["kusum_cum_pumps"] / den
    k["kusum_intensity_B_per_kha"] = k["kusum_cum_B"] / den
    k["kusum_intensity_C_per_kha"] = k["kusum_cum_C"] / den
    k["kusum_dose_per_kha"] = k["kusum_dose_terminal"] / den
    k["kusum_log1p_pumps"] = np.log1p(k["kusum_cum_pumps"])
    # pre-scheme zero pad: years before first national addition stay 0 after outer merge
    return k

def load_single_year_covariates():
    cov = None
    fp = RAW / "total_foodgrains_area_production_productivity_2024-25.csv"
    if fp.exists():
        f = pd.read_csv(fp); f["state"] = standardize_state(f["state"]); f = drop_total(f)
        cov = f[["state", "production_total_lakh_tonne", "area_total_lakh_ha"]].rename(
            columns={"production_total_lakh_tonne": "foodgrain_prod_lakh_t_2024",
                     "area_total_lakh_ha": "cropped_area_lakh_ha_2024"})
    fp = RAW / "irrigation_pumpsets_energised_statewise_as31Mar2023.csv"
    if fp.exists():
        p = pd.read_csv(fp); p["state"] = standardize_state(p["state"]); p = drop_total(p)
        p = p[["state", "pumpsets_total_31Mar2023"]]
        cov = p if cov is None else cov.merge(p, on="state", how="outer")
    return cov

def load_gsdp():
    """data (17).xls -> gsdp_statewise_raw.csv. The real year header is NOT the CSV header row:
    rows 1-2 are a title + '(Rs. in Crore)' banner, and the row whose first cell == 'States/UTs'
    carries the fiscal-year labels. Locate that row, use it as the header, parse data below it."""
    fp = RAW / "gsdp_statewise_raw.csv"
    if not fp.exists():
        log("WARNING gsdp_statewise_raw.csv absent -> gsdp column will be NaN (run p3_00).")
        return pd.DataFrame(columns=["state", "fy_start", "gsdp_cr"])
    try:
        raw = pd.read_csv(fp, header=None, dtype=str)
        hdr = raw.index[raw[0].astype(str).str.strip().str.lower() == "states/uts"]
        if len(hdr) == 0:
            log("WARNING GSDP 'States/UTs' header row not found -> gsdp NaN"); 
            return pd.DataFrame(columns=["state", "fy_start", "gsdp_cr"])
        h = int(hdr[0])
        years = raw.iloc[h].tolist()
        data = raw.iloc[h + 1:].copy()
        data.columns = ["state"] + years[1:]
        data["state"] = standardize_state(data["state"])
        data = drop_total(data.dropna(subset=["state"]))
        long = []
        for col in data.columns[1:]:
            m = re.search(r"(\d{4})", str(col))
            if not m: continue
            yr = int(m.group(1))
            if 2014 <= yr <= 2024:
                tmp = data[["state", col]].copy()
                tmp["fy_start"] = yr; tmp["gsdp_cr"] = pd.to_numeric(tmp[col], errors="coerce")
                long.append(tmp[["state", "fy_start", "gsdp_cr"]])
        if not long:
            return pd.DataFrame(columns=["state", "fy_start", "gsdp_cr"])
        out = pd.concat(long)
        # collapse source rows that map to one canonical state (e.g. DNH + Daman&Diu -> one UT):
        # GSDP is a level, so the combined-territory value is the sum.
        return out.groupby(["state", "fy_start"], as_index=False)["gsdp_cr"].sum(min_count=1)
    except Exception as e:
        log(f"WARNING GSDP parse failed: {e}"); return pd.DataFrame(columns=["state", "fy_start", "gsdp_cr"])

def load_ghi():
    """NASA observed-only annual GHI (kWh/m2/day), 20 states. Kept as a robustness column
    `ghi_annual_obs`; the PRIMARY `ghi_annual` comes from Paper 2 (wider coverage, see
    load_paper2_covariates). Time-invariant climate endowment."""
    fp = INHERIT_OPEN / "statewise_annual_GHI_solar_irradiance_and_coordinates.csv"
    if not fp.exists():
        log("WARNING GHI file absent -> ghi_annual_obs NaN"); 
        return pd.DataFrame(columns=["state", "ghi_annual_obs"])
    df = pd.read_csv(fp); df["state"] = standardize_state(df["state"]); df = drop_total(df)
    out = df[["state", "annual_ghi"]].rename(columns={"annual_ghi": "ghi_annual_obs"})
    out = out.dropna(subset=["state"]).groupby("state", as_index=False)["ghi_annual_obs"].mean()
    log(f"GHI (NASA observed-only) merged: {out['state'].nunique()} states -> ghi_annual_obs")
    return out

def load_rpo():
    """RPO total compliance % (FY2021-22). Only one fiscal year exists in the source, so it enters
    as a TIME-INVARIANT institutional/policy covariate (assigned to every panel year per state)."""
    fp = INHERIT_PROC / "MASTER_statewise_RPO_compliance_solar_nonsolar_FY2021-22.csv"
    if not fp.exists():
        log("WARNING RPO file absent -> rpo_compliance NaN"); 
        return pd.DataFrame(columns=["state", "rpo_compliance"])
    df = pd.read_csv(fp); df["state"] = standardize_state(df["state"]); df = drop_total(df)
    df["rpo_compliance"] = pd.to_numeric(df["total_compliance_pct"], errors="coerce")
    out = df[["state", "rpo_compliance"]].dropna(subset=["state"]).groupby(
        "state", as_index=False)["rpo_compliance"].mean()
    log(f"RPO merged: {out['state'].nunique()} states (FY2021-22 -> time-invariant)")
    return out

def load_discom_health():
    """ROBUSTNESS DISCOM measure = 1 - T&D_loss%/100 (Paper-1 definition), state x FY panel
    (FY2013-14..FY2022-23). The PRIMARY `discom_health` is Paper 2's AT&C-based index (wider/more
    recent coverage, see load_paper2_covariates); this T&D version is carried as `discom_health_td`.
    Two known data quirks handled: (1) a phantom 2nd row that repeats the year labels as data;
    (2) footnote digits appended to some state names (e.g. 'Andhra Pradesh1')."""
    fp = ROOT / "data" / "raw_indiastat" / "power_losses" / \
         "statewise_TD_loss_percent_panel_FY2013-14_to_FY2022-23.csv"
    if not fp.exists():
        log("WARNING T&D loss panel absent -> discom_health_td NaN"); 
        return pd.DataFrame(columns=["state", "fy_start", "discom_health_td"])
    df = pd.read_csv(fp)
    df = df[df["state"].astype(str).str.strip().str.lower() != "states/uts"].copy()  # drop phantom header row
    df["state"] = df["state"].astype(str).str.replace(r"\d+$", "", regex=True)        # strip footnote digits
    df["state"] = standardize_state(df["state"]); df = drop_total(df)
    rows = []
    for col in df.columns:
        m = re.match(r"losses_pct_(\d{4})-\d{2}$", col)
        if not m: continue
        yr = int(m.group(1))
        tmp = df[["state", col]].copy(); tmp["fy_start"] = yr
        tmp["td_loss_pct"] = pd.to_numeric(tmp[col], errors="coerce")
        rows.append(tmp[["state", "fy_start", "td_loss_pct"]])
    long = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["state", "fy_start", "td_loss_pct"])
    # collapse source rows that map to one canonical state (e.g. DNH + Daman&Diu -> one UT):
    # T&D loss is a rate (%), so the combined value is the mean.
    long = long.groupby(["state", "fy_start"], as_index=False)["td_loss_pct"].mean()
    long["discom_health_td"] = 1 - long["td_loss_pct"] / 100.0
    log(f"DISCOM health (T&D robustness) merged: {long['state'].nunique()} states x {long['fy_start'].nunique()} years")
    return long

def load_paper2_covariates():
    """Leverage Paper 2's analytic_panel.parquet (same project, same states, overlapping years
    FY2016-17..FY2024-25). Brings in higher-quality versions of the institutional/climate/economic
    covariates and KEEPS the imputation/source flags so every imputed cell stays auditable:
      - discom_health  : AT&C-loss-based index (PRIMARY; 100% coverage to FY2024-25) + discom_source
      - rpo_target_pct : time-varying national RPO target trajectory (11.5% -> 29.91%)
      - rpo_compliance_score : Paper 2's sparse state compliance score
      - ghi_annual     : 32-state GHI (PRIMARY) + ghi_imputed flag
      - log_gdp, log_gdp_pc, population (+ gdp_imputed) : economic denominators
    """
    fp = INHERIT_PROC / "analytic_panel.parquet"
    if not fp.exists():
        log("WARNING Paper2 analytic_panel.parquet absent -> Paper2 covariates skipped")
        return pd.DataFrame(columns=["state", "fy_start"])
    a = pd.read_parquet(fp)
    a["state"] = standardize_state(a["state"])
    a["fy_start"] = a["fiscal_year"].map(fy_to_int)
    a = drop_total(a.dropna(subset=["state", "fy_start"]))
    rename = {
        "discom_health_index": "discom_health",      # PRIMARY (AT&C-based)
        "discom_health_source": "discom_source",
        "dhi_uday": "dhi_uday",
        "rpo_target_pct": "rpo_target_pct",
        "rpo_compliance_score": "rpo_compliance_score",
        "ghi_annual_mean": "ghi_annual",             # PRIMARY (32-state)
        "ghi_imputed": "ghi_imputed",
        "log_gdp": "log_gdp", "log_gdp_pc": "log_gdp_pc",
        "population": "population", "gdp_imputed": "gdp_imputed",
    }
    cols = [c for c in rename if c in a.columns]
    out = a[["state", "fy_start"] + cols].rename(columns={k: rename[k] for k in cols})
    # collapse merged-UT duplicates (Paper 2 keeps DNH & Daman&Diu separate -> one canonical UT here):
    # numeric -> mean, flags/source -> first.
    num = out.select_dtypes("number").columns.difference(["fy_start"]).tolist()
    agg = {c: ("mean" if c in num else "first") for c in out.columns if c not in ("state", "fy_start")}
    out = out.groupby(["state", "fy_start"], as_index=False).agg(agg)
    log(f"Paper 2 covariates merged: {out['state'].nunique()} states x {out['fy_start'].nunique()} years "
        f"(AT&C discom primary, rpo_target trajectory, 32-state ghi, gdp/pop; flags carried)")
    return out

# ---------------------------------------------------------------- assemble
def main():
    apply_style()
    log("loading sources ...")
    irr = load_irrigation()
    net_sown_proxy = (irr.sort_values("fy_start").groupby("state", as_index=False)["net_irrigated_000ha"]
                      .last().rename(columns={"net_irrigated_000ha": "net_irr_kha_latest"}))
    agri = load_agri_electricity()
    gw_raw = load_groundwater(); gw = interpolate_groundwater(gw_raw)
    diesel = load_diesel_baseline()
    kusum = load_kusum_treatment(net_sown_proxy)
    covs1 = load_single_year_covariates()
    gsdp = load_gsdp()
    ghi_obs = load_ghi()             # NASA observed-only robustness -> ghi_annual_obs (merge on state)
    rpo = load_rpo()                 # FY2021-22 state compliance, time-invariant (merge on state)
    discom_td = load_discom_health() # T&D-based robustness -> discom_health_td (merge on state + fy_start)
    p2 = load_paper2_covariates()    # PRIMARY AT&C discom, rpo trajectory, 32-state ghi, gdp (state + fy_start)

    states = sorted(set(irr["state"]) | set(agri["state"]) | set(gw["state"]) | set(kusum["state"]))
    skeleton = pd.MultiIndex.from_product([states, YEARS], names=["state", "fy_start"]).to_frame(index=False)

    panel = (skeleton
             .merge(kusum, on=["state", "fy_start"], how="left")
             .merge(agri, on=["state", "fy_start"], how="left")
             .merge(irr, on=["state", "fy_start"], how="left")
             .merge(gw, on=["state", "fy_start"], how="left")
             .merge(gsdp, on=["state", "fy_start"], how="left")
             .merge(discom_td, on=["state", "fy_start"], how="left")
             .merge(p2, on=["state", "fy_start"], how="left")
             .merge(diesel, on="state", how="left")
             .merge(ghi_obs, on="state", how="left")
             .merge(rpo, on="state", how="left"))
    if covs1 is not None:
        panel = panel.merge(covs1, on="state", how="left")

    # derived (categories only; transforms decided in models per param_grids feature_engineering)
    def cat(x):
        if pd.isna(x): return np.nan
        return ("safe" if x < 70 else "semi_critical" if x < 90 else "critical" if x < 100 else "over_exploited")
    panel["gw_stress_cat"] = panel["gw_stage_step"].map(cat)
    panel["fy"] = panel["fy_start"].map(lambda y: f"{y}-{str(y+1)[-2:]}")
    panel["kusum_treated"] = (panel["kusum_cum_pumps"].fillna(0) > 0).astype(int)

    PROC.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(PROC / "master_panel_state_year.parquet", index=False)
    gw_raw.to_csv(PROC / "groundwater_assessment_years.csv", index=False)

    # data dictionary
    dd = pd.DataFrame({"column": panel.columns,
                       "non_null": [int(panel[c].notna().sum()) for c in panel.columns],
                       "dtype": [str(panel[c].dtype) for c in panel.columns]})
    dd.to_csv(PROC / "data_dictionary.csv", index=False)

    # coverage heatmap
    cov = panel.set_index(["state", "fy_start"]).notna().groupby("fy_start").mean().T
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(cov.values, aspect="auto", cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(range(len(cov.columns))); ax.set_xticklabels(cov.columns, rotation=45)
    ax.set_yticks(range(len(cov.index))); ax.set_yticklabels(cov.index, fontsize=6)
    ax.set_title("Panel coverage (share of states non-missing) by variable x year")
    fig.colorbar(im, ax=ax, shrink=0.6); save_fig(fig, FIG, "panel_coverage_heatmap")

    log(f"panel shape={panel.shape}  states={panel.state.nunique()}  years={panel.fy_start.nunique()}")
    passfail("p3_01 build_panel", panel.shape[0] > 200 and "kusum_cum_pumps" in panel.columns,
             f"{panel.shape[0]} rows")

if __name__ == "__main__":
    main()
# end of p3_01_build_panel.py
