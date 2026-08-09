# Paper 3 — full folder context (handoff brief)

Use this to brief a collaborator, co-author, or another agent. Everything lives under:

`…/04-Collaborations/neha sanyasi/paper3/`

(The parent folder name is historical; **authors are Harsh Dagar + Gunjan Bhandari, ICAR–NDRI Karnal** — not Neha.)

---

## 1. What this project is

**One-line claim:** Subsidised solar pumps under India’s **PM-KUSUM** can cut carbon and still raise groundwater stress, because near-zero marginal pumping cost expands extraction on the intensive margin.

**Locked title:**  
*Do Subsidised Solar Pumps Really Cut Carbon or Shift the Cost to Groundwater? Evidence from India's PM-KUSUM*

**Journal target:** *Energy Policy* (Elsevier). *Nature Sustainability* was an earlier stretch target; packaging is now Energy Policy–ready.

**Design in one sentence:** State–year panel → associational TWFE on tube-wells → causal IV on groundwater stage → intensive-margin carbon bridge → soft policy (condition Component B / haircut credits; do **not** halt B).

---

## 2. Headline empirics (current truth)

| Object | Number |
|--------|--------|
| Panel | 36 states/UTs × 11 FY (2014–15 → 2024–25) |
| TWFE tube-well area (associational) | ≈ **−0.0229** (~2.3% fewer ha per intensity unit) |
| IV groundwater stage | ≈ **+0.102** pp per intensity unit; first-stage **F ≈ 20.6** |
| Component B IV | Strong (**F ≈ 54.3**); drives the causal GW claim |
| Component C IV | Weak (**F ≈ 1.4**); do not pool with B |
| Survives drop of PB+HR+RJ | Yes (β ≈ 0.10) |
| Gross CO₂ abatement | ≈ **1.93 Mt**/yr |
| Intensive-margin rebound | ≈ **0.28 Mt** |
| Net | ≈ **1.65 Mt** |
| Rebound share of gross | ~**7%** safe vs ~**32%** over-exploited |
| Policy punchline | Condition B + haircut climate credit; don’t halt pumps |

Honesty constraints baked into the paper: treatment is **back-cast** (national additions × terminal state shares) → TWFE is **associational**; causal GW claims rest on **IV + placebos**; carbon rebound is a **calibrated bridge**, not structural microdata.

---

## 3. How the folder is arranged

```
paper3/
├── README.md                 ← pipeline quickstart
├── CONTEXT.md                ← this handoff brief
├── run_all.py                ← one-command: p3_00 → p3_15
├── requirements.txt
├── VISUAL_SUMMARY.svg        ← pipeline map graphic
│
├── config/                   ← NO hardcoded knobs in scripts
│   ├── param_grids.json      ← CV / BIC search grids
│   ├── literature_defaults.json  ← EF, fuel, lift constants
│   ├── state_map.json        ← state-name standardisation
│   └── viz_style.py
│
├── data/
│   ├── raw/                  ← official/admin CSVs (KUSUM, GW, irrigation, agri power…)
│   │   └── district_groundwater_2024/  ← district CSVs (descriptive only)
│   └── processed/
│       ├── master_panel_state_year.parquet   ← THE analysis panel
│       ├── agri_carbon_ledger_state_year.csv
│       ├── data_dictionary.csv
│       └── groundwater_assessment_years.csv
│
├── scripts/                  ← analysis + document builders
├── docs/                     ← analysis plan / extracted notes
├── outputs/                  ← results + master manuscript
│   ├── figures/              ← analysis figs + executive/ + summary/
│   ├── tables/                ← every results CSV
│   ├── reports/               ← integrity, peer review, devil’s advocate
│   └── manuscript_PAPER3_NatureSustainability.md  ← ★ MASTER TEXT (edit this)
│
├── FINAL_SUBMISSION_PACKAGE/ ← ★ SUBMIT THIS PACK (title page, highlights, manuscript,
│                                cover letter, SI, figures/, tables/, manuscript_source.md)
│
└── _archive/                 ← old reviews / superseded docs (don’t use for submission)
```

**Mental model:**  
`data/raw` → `scripts/p3_*` → `data/processed` + `outputs/tables|figures` → markdown master → DOCX builders → `FINAL_SUBMISSION_PACKAGE/`.

---

## 4. Analysis pipeline (what each script does)

Run: `python run_all.py` (from `paper3/`). Seed **1502** everywhere.

| Script | Job |
|--------|-----|
| `p3_00_setup` | Scaffold, ingest/copy raws |
| `p3_01_build_panel` | Build master state×year panel + back-cast KUSUM intensity (B/C) |
| `p3_02_carbon_ledger` | Gross substitution abatement (EF × fuel sweep) |
| `p3_03_descriptives` | Summary/balance + paradox scatter |
| `p3_04_panel_fe` | TWFE channels + wild cluster bootstrap |
| `p3_05_did` | Sun–Abraham event study (+ CS ATT for tube-wells) |
| `p3_06_iv` | IV = GHI × pre-scheme diesel density; placebos; B vs C |
| `p3_07_decomposition` | Gross − intensive-margin rebound = net (IV bridge) |
| `p3_08_heterogeneity` | Causal forest + interactions |
| `p3_09_ccts_mc` | Carbon-revenue Monte Carlo coda |
| `p3_10_district` | District hydro correlation (**not** KUSUM causal) |
| `p3_11_integrity` | Hashes + devil’s-advocate report |
| `p3_12_visual_summary` | Extra summary visuals (optional / older layer) |
| `p3_13_confirmatory` | Standard confirmation battery |
| `p3_14_critical_tests` | Adversarial suite (LOO, drop NW, winsor, alt denominators, policy magnitudes) |
| `p3_15_executive_visuals` | SI tables S1–S3 + memorable V1–V10 @ 400 dpi |

Shared helpers: `scripts/_p3_common.py`.

**Document builders (not in `run_all`):**

| Script | Produces |
|--------|----------|
| `build_energy_policy_pack.py` | Full submission folder `FINAL_SUBMISSION_PACKAGE/` (project root) |
| `build_si_docx.py` | SI DOCX (tables then figures); called by the pack builder too |
| `build_manuscript_docx.py` / `build_energy_policy_docx.py` | Older/partial MS builders (prefer the pack) — stale, kept for reference |
| `build_report_docx.py` | Long internal methods/results report |

---

## 5. Manuscripts & what to open

| File | Role |
|------|------|
| `outputs/manuscript_PAPER3_NatureSustainability.md` | **Master source of truth** (edit this; rebuild DOCX from it) |
| `FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx` | Anonymised submission MS: TNR, justified, double-spaced, line numbers, **Figures 1–4 embedded** |
| `FINAL_SUBMISSION_PACKAGE/01_Title_Page.docx` | Authors, ORCID, CRediT, declarations |
| `FINAL_SUBMISSION_PACKAGE/02_Highlights.docx` | 5 bullets ≤85 chars |
| `FINAL_SUBMISSION_PACKAGE/04_Cover_Letter.docx` | Submission letter |
| `FINAL_SUBMISSION_PACKAGE/05_Supplementary_Information.docx` | Tables S1–S3 + Figures S1–S10 |
| `FINAL_SUBMISSION_PACKAGE/figures/` `/tables/` | PNG+PDF visuals @ 400 dpi and SI table CSVs |
| `FINAL_SUBMISSION_PACKAGE/manuscript_source.md` | Reference copy of the master markdown |
| `outputs/manuscript_PAPER3_SupplementaryInformation.docx` | Same SI (source copy, also feeds the pack) |
| `_archive/superseded_docs/` | Old `EnergyPolicy_READY/` pack + stale manuscript DOCX — **don't submit those** |

Rebuild pack anytime (writes into `FINAL_SUBMISSION_PACKAGE/` at the project root):

```bash
python scripts/build_energy_policy_pack.py
```

Portal note in pack: https://www.editorialmanager.com/jepo/

---

## 6. Figures story (main vs SI)

**Main text (Figures 1–4)** — pulled from executive set:

1. **V2** geographic alignment (intensity vs stress maps)  
2. **V4** paradox scales (extensive −2.3% vs intensive +0.10 pp)  
3. **V5** component meters (B F=54.3 vs C F=1.4)  
4. **V9** carbon balance (1.93 / 0.28 / 1.65; 7% vs 32%)

**SI (S1–S10 / V1–V10):** causal storyboard, event ribbon, CATE ridges, rebound heatmap, LOO lollipop, governance matrix, plus the four above. Source PNGs/PDFs: `outputs/figures/executive/`.

Older analysis figures (`fig1`–`fig6`, `summary/S*`) still exist under `outputs/figures/` from earlier pipeline stages; the **submission narrative** uses the executive set.

---

## 7. Intellectual story the paper tells

1. **Gap:** Solar irrigation literature is strong on farm surplus / energy substitution, weak on (i) separating KUSUM **B vs C**, (ii) intensive-margin **CGWB stage**, (iii) **net** vs gross carbon by aquifer class.  
2. **RQs:** Co-location? Two margins (FE vs IV)? B vs C + adversarial survival? Gross–net carbon → policy haircuts?  
3. **Methods honesty:** Back-cast treatment → TWFE labelled associational; IV + placebos for GW; carbon bridge rebuilt from IV β (not from negative tube-well FE).  
4. **Policy:** Soft protocol — screen by CGWB class → haircut credits → condition B in stressed blocks / accelerate in safe → separate B from C → rewrite KPIs → use MNRE **2027** window. Reject “halt B.”

---

## 8. Authors / identity (locked)

- **Harsh Dagar** (corresponding) — Research Scholar, DESM, ICAR–NDRI Karnal; ORCID `0009-0008-7394-130X`; harshdagar5879@gmail.com  
- **Gunjan Bhandari** — Scientist, same affiliation; ORCID `0000-0001-6004-7642`; gunjanbhandari5@gmail.com  

Main MS is **anonymised**; identity only on title page / cover letter.

---

## 9. Quality status & open gaps

Latest simulated panel review: `outputs/reports/PEER_REVIEW_ITER4_CURRENT.md`  
**Score ~88.2/100 → Minor revision → Accept after DOI.** Honest ceiling without installation microdata ~90–92.

**Still open before formal submit:**
1. Public **repo DOI** + fill Data/Code availability links (placeholders now)  
2. Optional sentence: who verifies metering for the carbon haircut (DISCOM / CGWB / state agri)  
3. Primary MNRE guideline citations could be a bit richer  

**Structural limits (already disclosed in paper):** back-cast treatment; calibrated (not structural) energy bridge; sparse GW assessment years with interpolation.

---

## 10. How another agent should work here

1. Treat **`manuscript_PAPER3_NatureSustainability.md`** as editable master.  
2. Numbers must match **`outputs/tables/*.csv`** (esp. `iv_results`, `fe_channel_results`, `decomposition_by_stress`, `critical_*`).  
3. After text edits: `python scripts/build_energy_policy_pack.py` (writes into `FINAL_SUBMISSION_PACKAGE/`).  
4. After empirics change: `python run_all.py` (or individual `p3_*`), then rebuild pack.  
5. Don’t resurrect `_archive/` or old `EnergyPolicy_READY` as current.  
6. Don’t invent installation microdata; keep honesty labels (associational TWFE / IV causal GW / calibrated carbon).  
7. Disclose Jharkhand leave-one-out power dependency; treat 7%→32% rebound shares as mechanical lift-depth accounting unless heterogeneity supports more.

---

## 11. One-paragraph elevator for a human

This folder is a full reproducible research project on India’s PM-KUSUM solar pumps. It builds a 36×11 state–year panel, shows that KUSUM intensity is linked to fewer tube-well hectares but—under IV—raises groundwater stage of extraction, mainly via Component B. An intensive-margin carbon bridge turns that into ~1.93 Mt gross vs ~1.65 Mt net, with rebound ~32% in over-exploited zones. Code is `scripts/p3_00`–`p3_15`; submission files are in `FINAL_SUBMISSION_PACKAGE/` at the project root; master prose is the NatureSustainability-named markdown in `outputs/`. Authors are Harsh Dagar and Gunjan Bhandari (NDRI). Ready for Energy Policy once the repository DOI is filled.
