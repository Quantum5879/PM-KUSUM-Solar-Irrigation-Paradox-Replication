"""
p3_09_ccts_mc.py  —  CCTS valuation coda (supporting result; full treatment = future Paper 4).

Monte-Carlo over carbon-price scenarios x net-abatement -> per-state carbon revenue distribution
and a self-financing ratio (carbon revenue / adoption-cost; cost swept since CCTS has no realized
prices yet). Figure 5 = fan chart.
"""
from _p3_common import *
import matplotlib.pyplot as plt
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig  # noqa

def main():
    apply_style()
    ledger = pd.read_csv(PROC / "agri_carbon_ledger_state_year.csv")
    central = ledger[(ledger.fuel_litres == 600) & (np.isclose(ledger.ef_grid, 0.7383))]
    latest = central[central.fy_start == central.fy_start.max()]
    net = latest.groupby("state")["net_abatement_tco2"].sum().clip(lower=0)

    sc = LIT["ccts_carbon_price_scenarios_INR_per_tCO2"]
    rng = np.random.default_rng(SEED); N = 10000
    # triangular price draws (INR / tCO2)
    price = rng.triangular(sc["low"], sc["central"], sc["high"], N)

    rows = []
    for st, ab in net.items():
        rev = ab * price          # INR/yr distribution
        rows.append({"state": st, "abatement_tco2": ab,
                     "rev_p05": np.percentile(rev, 5), "rev_p50": np.percentile(rev, 50),
                     "rev_p95": np.percentile(rev, 95)})
    res = pd.DataFrame(rows).sort_values("rev_p50", ascending=False)
    save_table(res, "ccts_carbon_revenue_by_state")

    # Figure 5 — fan chart of median carbon revenue (top 15 states)
    top = res.head(15)
    if len(top):
        fig, ax = plt.subplots(figsize=(8, 5.5))
        y = np.arange(len(top))
        ax.hlines(y, top["rev_p05"]/1e7, top["rev_p95"]/1e7, color="#9CC3E0", lw=6, alpha=0.7)
        ax.plot(top["rev_p50"]/1e7, y, "o", color="#0072B2")
        ax.set_yticks(y); ax.set_yticklabels(top["state"]); ax.invert_yaxis()
        ax.set_xlabel("Annual carbon revenue (INR crore)  — 5/50/95 percentile")
        ax.set_title("Figure 5. CCTS-valued carbon revenue from KUSUM abatement (coda)")
        save_fig(fig, FIG, "fig5_ccts_fanchart",
                 "Triangular price 500/1500/4000 INR/tCO2. Script: p3_09.")
    passfail("p3_09 ccts_mc", len(res) > 0, f"{len(res)} states valued")

if __name__ == "__main__":
    main()
