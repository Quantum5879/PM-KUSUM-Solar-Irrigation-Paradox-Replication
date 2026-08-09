# -*- coding: utf-8 -*-
"""One-off script: replace every em dash in the manuscript with natural punctuation.
Each replacement is context-anchored (old -> new) to avoid accidental double-hits.
Run once, then delete.
"""
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "outputs" / "manuscript_PAPER3_NatureSustainability.md"

REPLACEMENTS = [
    ("- Harsh Dagar \u2014 Research Scholar", "- Harsh Dagar, Research Scholar"),
    ("- Gunjan Bhandari \u2014 Scientist", "- Gunjan Bhandari, Scientist"),
    ("these benefits \u2014 decarbonisation", "these benefits: decarbonisation"),
    ("Sorrell, 2009) \u2014 a prediction that holds",
     "Sorrell, 2009), a prediction that holds"),
    ("regulatory metric \u2014 CGWB stage of extraction \u2014 that classifies",
     "regulatory metric, CGWB stage of extraction, that classifies"),
    ("margin), and \u2014 under an instrument interacting solar resource with pre-scheme diesel density \u2014 does intensity",
     "margin), and, under an instrument interacting solar resource with pre-scheme diesel density, does intensity"),
    ("adversarial confirmatory suite \u2014 leave-one-out and regional-exclusion IV, winsorised treatment, alternative denominators, year-by-year reduced forms \u2014 that converts",
     "adversarial confirmatory suite (leave-one-out and regional-exclusion IV, winsorised treatment, alternative denominators, year-by-year reduced forms) that converts"),
    ("Gujarat) \u2014 co-location, not causation", "Gujarat): co-location, not causation"),
    ("tube-well hectares \u2014 infrastructure consolidation, not evidence of lower aquifer stress.",
     "tube-well hectares (infrastructure consolidation, not evidence of lower aquifer stress)."),
    ("cost more energy to lift \u2014 a physical fact about pumping depth, not a statistically estimated behavioural amplification,",
     "cost more energy to lift, a physical fact about pumping depth and not a statistically estimated behavioural amplification,"),
    ("groundwater \u2014 about a quarter of global extraction", "groundwater, about a quarter of global extraction"),
    ("Jevons-type rebound \u2014 efficiency or cost reductions raising use \u2014 is documented",
     "Jevons-type rebound (efficiency or cost reductions raising use) is documented"),
    ("battery of placebo tests \u2014 falsification checks", "battery of placebo tests: falsification checks"),
    ("endogenous placement \u2014 the concern that administratively capable, sunny, already-stressed states adopt KUSUM fastest \u2014 we instrument",
     "endogenous placement (the concern that administratively capable, sunny, already-stressed states adopt KUSUM fastest), we instrument"),
    ("outcome data \u2014 2SLS uses the actual groundwater", "outcome data: 2SLS uses the actual groundwater"),
    ("groundwater pumping \u2014 general agricultural expansion, say \u2014 it should also fail",
     "groundwater pumping (general agricultural expansion, say), it should also fail"),
    ("reject that inference \u2014 pump counts cannot be used to back out extraction volume once the intensity of pumping per well has changed \u2014 and instead derive rebound",
     "reject that inference: pump counts cannot be used to back out extraction volume once the intensity of pumping per well has changed. Instead, we derive rebound"),
    ("| **National average** | **5.58** | \u2014 | **50.9** | Mixed |",
     "| **National average** | **5.58** | n/a | **50.9** | Mixed |"),
    ("remain imprecise \u2014 consistent with FE attenuation", "remain imprecise, consistent with FE attenuation"),
    ("indistinguishable from zero \u2014 we do not report", "indistinguishable from zero, so we do not report"),
    ("Two placebo channels \u2014 pre-2019 groundwater stage and pre-2019 tube-wells \u2014 return coefficients",
     "Two placebo channels (pre-2019 groundwater stage and pre-2019 tube-wells) return coefficients"),
    ("causal groundwater claim \u2014 the instrument is built for the diesel-replacement margin",
     "causal groundwater claim: the instrument is built for the diesel-replacement margin"),
    ("categorical specification \u2014 interacting intensity with a discrete groundwater-stress category \u2014 had returned",
     "categorical specification (interacting intensity with a discrete groundwater-stress category) had returned"),
    ("already sits \u2014 lifting the same extra cubic metre of water", "already sits: lifting the same extra cubic metre of water"),
    ("lift-depth penalty is steepest \u2014 the classic Jevons pattern", "lift-depth penalty is steepest, the classic Jevons pattern"),
    ("groundwater is insignificant \u2014 without IV, back-cast/CS designs", "groundwater is insignificant: without IV, back-cast/CS designs"),
    ("| Baseline IV | 0.102 | 20.6 | 0.002 | \u2014 |", "| Baseline IV | 0.102 | 20.6 | 0.002 | n/a |"),
    ("(F = 0.42) \u2014 this is a failed confirmation", "(F = 0.42); this is a failed confirmation"),
    ("**Jharkhand specifically** \u2014 the single highest-intensity state in the panel \u2014 collapses the first-stage F",
     "**Jharkhand specifically** (the single highest-intensity state in the panel) collapses the first-stage F"),
    ("| Rebound offset share \u2014 safe zones | 7.3% |", "| Rebound offset share, safe zones | 7.3% |"),
    ("| Rebound offset share \u2014 over-exploited | **31.7%** |", "| Rebound offset share, over-exploited | **31.7%** |"),
    ("instrumented KUSUM intensity \u2014 the same reason the terminal cross-sectional dose is null",
     "instrumented KUSUM intensity, the same reason the terminal cross-sectional dose is null"),
    ("marginal pumping cost collapses \u2014 the same Jevons logic", "marginal pumping cost collapses, the same Jevons logic"),
    ("diesel-dense states \u2014 the variation the instrument is built to isolate.",
     "diesel-dense states: the variation the instrument is built to isolate."),
    ("cannot identify \u2014 an error that mirrors earlier conflations", "cannot identify, an error that mirrors earlier conflations"),
    ("lower in over-exploited states \u2014 consistent with water-rebound studies",
     "lower in over-exploited states, consistent with water-rebound studies"),
    ("flatters the worst aquifers \u2014 the opposite of an aquifer-smart carbon protocol.",
     "flatters the worst aquifers: the opposite of an aquifer-smart carbon protocol."),
    ("of stage \u2014 enough to matter for blocks near regulatory thresholds.",
     "of stage, enough to matter for blocks near regulatory thresholds."),
    ("weakens the instrument considerably \u2014 a dependency we report",
     "weakens the instrument considerably, a dependency we report"),
    ("in over-exploited zones \u2014 an over-claim of ~0.28 Mt if gross is sold as net \u2014 while our heterogeneity tests",
     "in over-exploited zones (an over-claim of ~0.28 Mt if gross is sold as net), while our heterogeneity tests"),
    ("consumption\u2014the rebound effect: a survey.", "consumption, the rebound effect: a survey."),
]


def main():
    text = PATH.read_text(encoding="utf-8")
    missing = []
    for old, new in REPLACEMENTS:
        n = text.count(old)
        if n == 0:
            missing.append(old)
            continue
        if n > 1:
            print(f"WARNING: pattern occurs {n} times, replacing all: {old[:60]}...")
        text = text.replace(old, new)
    if missing:
        print(f"{len(missing)} patterns NOT FOUND:")
        for m in missing:
            print("  -", m[:90])
    remaining_em = text.count("\u2014")
    remaining_en = text.count("\u2013")
    print(f"Remaining em dashes: {remaining_em}")
    print(f"Remaining en dashes: {remaining_en}")
    if remaining_em:
        lines = text.splitlines()
        for i, l in enumerate(lines, 1):
            if "\u2014" in l:
                print(f"  line {i}: {l[:150]}")
    PATH.write_text(text, encoding="utf-8")
    print("Wrote", PATH)


if __name__ == "__main__":
    main()
