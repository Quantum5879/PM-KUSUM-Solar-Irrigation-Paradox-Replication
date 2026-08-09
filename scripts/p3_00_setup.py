"""
p3_00_setup.py  —  scaffold the self-contained paper3/ tree and ingest raw data.
Idempotent: safe to re-run. Copies built CSVs into paper3/data/raw and parses the
GSDP .xls (HTML table) into a tidy CSV.
"""
from _p3_common import *
import shutil, glob

def copy_sources():
    n = 0
    # KUSUM + open-source state-level CSVs (flatten into raw/)
    for folder in (SRC_K, SRC_O):
        if not folder.exists():
            log(f"WARNING source folder missing: {folder}")
            continue
        for fp in folder.glob("*.csv"):
            shutil.copy2(fp, RAW / fp.name); n += 1
    # district groundwater (preserve subfolder)
    dsrc = SRC_O / "district_groundwater_2024"
    if dsrc.exists():
        ddst = RAW / "district_groundwater_2024"; ddst.mkdir(exist_ok=True)
        for fp in dsrc.glob("*.csv"):
            shutil.copy2(fp, ddst / fp.name); n += 1
    return n

def parse_gsdp():
    """data (17).xls is an HTML table; parse with read_html. Save gsdp_statewise.csv."""
    candidates = list(SRC.glob("data (17).xls")) + list(SRC.glob("*GSDP*.xls"))
    if not candidates:
        log("WARNING GSDP .xls not found (data (17).xls). Skipping; add manually if needed.")
        return
    try:
        tables = pd.read_html(str(candidates[0]))
        gsdp = max(tables, key=lambda t: t.size)
        gsdp.to_csv(RAW / "gsdp_statewise_raw.csv", index=False)
        log(f"parsed GSDP -> gsdp_statewise_raw.csv  shape={gsdp.shape} (clean cols in p3_01)")
    except Exception as e:
        log(f"WARNING could not parse GSDP xls: {e}")

def main():
    log("scaffolding paper3/ tree ...")
    n = copy_sources()
    parse_gsdp()
    files = list(RAW.glob("*.csv")) + list((RAW / "district_groundwater_2024").glob("*.csv"))
    rep = pd.DataFrame({"file": [f.name for f in files],
                        "rows": [sum(1 for _ in open(f, encoding="utf-8", errors="ignore")) - 1 for f in files]})
    rep.to_csv(REP / "ingest_report.csv", index=False)
    log(f"ingested {n} source files into {RAW}")
    passfail("p3_00 setup", len(files) >= 10, f"{len(files)} csv files in raw/")

if __name__ == "__main__":
    main()
