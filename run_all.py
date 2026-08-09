"""
run_all.py  —  one-command reproducible pipeline for Paper 3.
Runs p3_00 ... p3_11 in order; each prints a PASS/FAIL self-check. Stops on hard crash,
continues past soft (logged) failures. Usage:  python run_all.py
"""
import subprocess, sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent / "scripts"
ORDER = [
    "p3_00_setup.py", "p3_01_build_panel.py", "p3_02_carbon_ledger.py",
    "p3_03_descriptives.py", "p3_04_panel_fe.py", "p3_05_did.py", "p3_06_iv.py",
    "p3_07_decomposition.py", "p3_08_heterogeneity.py", "p3_09_ccts_mc.py",
    "p3_10_district.py", "p3_11_integrity.py", "p3_13_confirmatory.py",
    "p3_14_critical_tests.py", "p3_15_executive_visuals.py",
]

def main():
    results = {}
    for s in ORDER:
        print("\n" + "=" * 78 + f"\n>>> {s}\n" + "=" * 78, flush=True)
        rc = subprocess.run([sys.executable, str(SCRIPTS / s)], cwd=str(SCRIPTS)).returncode
        results[s] = rc
        if rc != 0:
            print(f"[run_all] {s} exited rc={rc} (continuing; debug this stage).", flush=True)
    print("\n" + "=" * 78 + "\nSUMMARY")
    for s, rc in results.items():
        print(f"  {'OK ' if rc == 0 else 'ERR'}  {s}")
    print("=" * 78)

if __name__ == "__main__":
    main()
