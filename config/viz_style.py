"""
Publication-quality matplotlib style for Paper 3 (Nature-tier).
Import and call `apply_style()` at the top of every figure script.
Palettes are colour-blind safe. Exports both 300-dpi PNG and vector PDF/SVG.
"""
from __future__ import annotations
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

# Okabe-Ito colour-blind-safe categorical palette
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]
ACCENT = "#0072B2"
# Diverging palette for the sign-flip map (zero-centred): red = backfire, blue = win
DIVERGING = "RdBu_r"
SEQUENTIAL = "viridis"


def apply_style():
    mpl.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.titlesize": 11,
        "axes.labelsize": 9.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#E6E6E6",
        "grid.linewidth": 0.6,
        "legend.frameon": False,
        "legend.fontsize": 8.5,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "figure.autolayout": False,
    })


def save_fig(fig, outdir, name, panel_caption: str | None = None):
    """Save a figure as both 300-dpi PNG and vector PDF + SVG."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    if panel_caption:
        fig.text(0.01, 0.005, panel_caption, fontsize=7, color="#666666", ha="left")
    for ext in ("png", "pdf", "svg"):
        fig.savefig(outdir / f"{name}.{ext}")
    plt.close(fig)
