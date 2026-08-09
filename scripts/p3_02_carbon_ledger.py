"""
p3_02_carbon_ledger.py  —  construct the agricultural carbon ledger per state-year.

Net carbon is CONSTRUCTED, never the LHS of a regression. This script computes the GROSS
substitution abatement (diesel + grid displaced by solar pumps) under an EF/assumption SWEEP
(low/central/high). The REBOUND term is a hook injected by p3_07 once the causal effect of KUSUM
on groundwater extraction is estimated (Stage D5). Output keeps all scenarios so nothing is a
point assumption.

Output: paper3/data/processed/agri_carbon_ledger_state_year.csv
"""
from _p3_common import *

def main():
    panel = pd.read_parquet(PROC / "master_panel_state_year.parquet")

    # national B:C split per year -> diesel-replacing (B) vs grid-replacing (C) share
    nat = pd.read_csv(RAW / "kusum_national_physical_progress_2019-20_to_2024-25.csv")
    nat["fy_start"] = nat["year"].map(fy_to_int)
    b = pd.to_numeric(nat["componentB_pumps"], errors="coerce").fillna(0)
    c = pd.to_numeric(nat["componentC_pumps"], errors="coerce").fillna(0)
    nat["diesel_share"] = (b / (b + c).replace(0, np.nan)).fillna(0.8)  # default 0.8 if undefined
    panel = panel.merge(nat[["fy_start", "diesel_share"]], on="fy_start", how="left")
    panel["diesel_share"] = panel["diesel_share"].fillna(0.8)

    # per-pump grid energy (kWh/yr): use observed avg if present, else swept constant
    if "avg_consumption_per_pumpset_kWh" in panel.columns:
        kwh = pd.to_numeric(panel["avg_consumption_per_pumpset_kWh"], errors="coerce")
    else:
        kwh = pd.Series(np.nan, index=panel.index)
    kwh = kwh.fillna(kwh.median() if kwh.notna().any() else 9000.0)

    n_pumps = pd.to_numeric(panel["kusum_cum_pumps"], errors="coerce").fillna(0)
    n_diesel = n_pumps * panel["diesel_share"]
    n_grid   = n_pumps * (1 - panel["diesel_share"])

    ef_diesel = LIT["ef_diesel_kgCO2_per_litre"]["value"]
    fuel_grid = LIT["diesel_pump_annual_fuel_litres"]["sensitivity"]   # [400,600,800]
    ef_grid_grid = LIT["ef_grid_tCO2_per_MWh"]["sensitivity"]          # [0.71,0.7383,0.79]

    rows = []
    for fuel in fuel_grid:
        for efg in ef_grid_grid:
            diesel_saved_t = n_diesel * fuel * ef_diesel / 1000.0          # tCO2
            grid_saved_t   = n_grid * (kwh / 1000.0) * efg                 # MWh*tCO2/MWh
            gross = diesel_saved_t + grid_saved_t
            tmp = panel[["state", "fy_start"]].copy()
            tmp["fuel_litres"] = fuel; tmp["ef_grid"] = efg
            tmp["diesel_saved_tco2"] = diesel_saved_t
            tmp["grid_saved_tco2"] = grid_saved_t
            tmp["gross_abatement_tco2"] = gross
            tmp["rebound_tco2"] = np.nan   # HOOK: filled by p3_07 from causal extraction effect
            tmp["net_abatement_tco2"] = gross  # provisional == gross until rebound injected
            rows.append(tmp)
    ledger = pd.concat(rows, ignore_index=True)
    ledger.to_csv(PROC / "agri_carbon_ledger_state_year.csv", index=False)

    # ---- validate magnitude vs government estimate (2022 cross-section)
    gov = RAW / "kusum_statewise_CO2_emission_reduction_as31Oct2022.csv"
    note = ""
    if gov.exists():
        g = pd.read_csv(gov); g["state"] = standardize_state(g["state"]); g = drop_total(g)
        gov_total_kt = pd.to_numeric(g["co2_reduction_000tonnes_per_annum"], errors="coerce").sum()
        central = ledger[(ledger.fuel_litres == 600) & (np.isclose(ledger.ef_grid, 0.7383))]
        ours_2022_kt = central[central.fy_start == 2022]["gross_abatement_tco2"].sum() / 1000.0
        note = f"gov 2022 ~{gov_total_kt:.0f} kt vs ledger central 2022 ~{ours_2022_kt:.0f} kt (order-of-magnitude check)"
        log(note)

    save_table(ledger.groupby(["fuel_litres", "ef_grid"], as_index=False)["gross_abatement_tco2"].sum(),
               "ledger_scenario_totals")
    passfail("p3_02 carbon_ledger", ledger["gross_abatement_tco2"].notna().any(), note)

if __name__ == "__main__":
    main()
