"""
p3_10_district.py  —  district-level hydro correlation (2024 cross-section, 7 states, ~185 units).

HONEST SCOPE: no district-level KUSUM exists. This is NOT a KUSUM causal test and MUST NOT be
sold as mechanism corroboration of the scheme. It documents that, within states, districts with
higher irrigation reliance on groundwater have higher stage-of-extraction — a hydro accounting
association that motivates (but does not identify) the intensive-margin concern.
"""
from _p3_common import *
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
sys.path.append(str(CONFIG)); from viz_style import apply_style, save_fig, SEQUENTIAL  # noqa

DDIR = RAW / "district_groundwater_2024"

def load_districts():
    frames = []
    if not DDIR.exists():
        log("WARNING district folder missing"); return pd.DataFrame()
    for fp in DDIR.glob("*_district_groundwater_2024.csv"):
        st = fp.name.split("_district")[0]
        df = pd.read_csv(fp)
        df = df[df["Name of District"].astype(str).str.lower().str.contains("total") == False]
        df["state"] = st
        for c in ["Irrigation - Annual extraction", "Annual Extractable Groundwater Resource",
                  "Total Annual Extraction", "Stage of GW extraction (%)"]:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def main():
    apply_style()
    d = load_districts()
    if d.empty:
        passfail("p3_10 district", False, "no district data"); return
    d = d.rename(columns={"Stage of GW extraction (%)": "stage",
                          "Irrigation - Annual extraction": "irr_extr",
                          "Annual Extractable Groundwater Resource": "extractable"})
    d = d.dropna(subset=["stage", "irr_extr", "extractable"])
    d["irr_share"] = d["irr_extr"] / d["extractable"].replace(0, np.nan)
    d = d.dropna(subset=["irr_share"])
    log(f"district units: {len(d)} across {d.state.nunique()} states")

    try:
        m = smf.ols("stage ~ irr_share + C(state)", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["state"]})
        res = pd.DataFrame({
            "term": ["irr_share"],
            "coef": [m.params.get("irr_share")],
            "se": [m.bse.get("irr_share")],
            "p": [m.pvalues.get("irr_share")],
            "n": [int(m.nobs)],
            "r2": [m.rsquared],
            "interpretation": ["DESCRIPTIVE within-state hydro correlation; NOT a KUSUM effect"],
        })
        save_table(res, "district_mechanism_regression")
    except Exception as e:
        log(f"district regression failed: {e}")

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    sc = ax.scatter(d["irr_share"], d["stage"], c=d["stage"], cmap=SEQUENTIAL,
                    s=22, edgecolor="white", linewidth=0.3, alpha=0.85)
    ax.axhline(100, color="#b91c1c", ls="--", lw=1)
    ax.set_xlabel("Irrigation share of extractable groundwater (district)")
    ax.set_ylabel("Stage of groundwater extraction (%)")
    ax.set_title("Figure 6. District hydro correlation (not a KUSUM causal test)")
    fig.colorbar(sc, ax=ax, shrink=0.8, label="Stage %")
    save_fig(fig, FIG, "fig6_district_mechanism",
             "Within-state association only; no district KUSUM data. Script: p3_10.")
    passfail("p3_10 district", True, f"n={len(d)} descriptive")

if __name__ == "__main__":
    main()
