"""
Shared utilities for the Paper 3 pipeline.
Path resolution, config loading, state-name standardisation, logging, seeding.
Import this at the top of every p3_*.py script:  from _p3_common import *
"""
from __future__ import annotations
import json, sys, hashlib, warnings
from pathlib import Path
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------- paths
HERE    = Path(__file__).resolve().parent          # paper3/scripts
PAPER3  = HERE.parent                              # paper3
ROOT    = PAPER3.parent                            # neha sanyasi  (project root)
SRC     = ROOT / "data" / "paper3_raw"             # original source CSVs (built earlier)
SRC_K   = SRC / "kusum_extracted"
SRC_O   = SRC / "opensource_extracted"
RAW     = PAPER3 / "data" / "raw"                  # ingested copies (p3_00 fills this)
PROC    = PAPER3 / "data" / "processed"            # generated tables
CONFIG  = PAPER3 / "config"
OUT     = PAPER3 / "outputs"
FIG     = OUT / "figures"
TAB     = OUT / "tables"
REP     = OUT / "reports"
INHERIT_PROC = ROOT / "data" / "processed"         # Paper 1/2 processed data
INHERIT_OPEN = ROOT / "data" / "raw_open"          # Paper 1/2 open data

for d in (RAW, PROC, FIG, TAB, REP):
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------- config
def load_json(name):
    with open(CONFIG / name, "r", encoding="utf-8") as f:
        return json.load(f)

STATE_MAP   = load_json("state_map.json")
PARAM_GRIDS = load_json("param_grids.json")
LIT         = load_json("literature_defaults.json")
SEED        = int(PARAM_GRIDS.get("seed", 1502))
np.random.seed(SEED)

# ----------------------------------------------------------------------------- helpers
def log(msg):
    print(f"[p3] {msg}", flush=True)

def passfail(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name} {('- ' + detail) if detail else ''}", flush=True)
    return ok

def standardize_state(s: pd.Series) -> pd.Series:
    """Map any state-name variant to canonical form. Unmapped -> NaN (caught by assert)."""
    key = s.astype(str).str.strip().str.lower()
    out = key.map(STATE_MAP)
    unmapped = sorted(set(key[out.isna()]) - {"nan", ""})
    if unmapped:
        warnings.warn(f"Unmapped state names (add to state_map.json): {unmapped}")
    return out

def drop_total(df, col="state"):
    """Remove India/Grand-Total rows from a state-level table."""
    return df[df[col] != "INDIA_TOTAL"].copy()

def fy_to_int(fy):
    """'2019-20' or '2019-2020' -> start year int 2019."""
    return int(str(fy).split("-")[0])

def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()

def append_tuning_log(entry: dict):
    p = REP / "tuning_log.json"
    data = json.loads(p.read_text()) if p.exists() else []
    data.append(entry)
    p.write_text(json.dumps(data, indent=2))

def save_table(df, name):
    df.to_csv(TAB / f"{name}.csv", index=False)
    try:
        (TAB / f"{name}.tex").write_text(df.to_latex(index=False, float_format="%.3f"))
    except Exception:
        pass
    log(f"saved table -> {name}.csv")
