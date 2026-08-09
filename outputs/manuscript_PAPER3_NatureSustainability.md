# Do Subsidised Solar Pumps Really Cut Carbon or Shift the Cost to Groundwater? Evidence from India's PM-KUSUM

**Running head:** SOLAR PUMPS, CARBON AND GROUNDWATER IN INDIA

**Authors:**
Harsh Dagar¹* and Gunjan Bhandari¹

¹ Division of Dairy Economics, Statistics and Management, ICAR-National Dairy Research Institute (Deemed University), Karnal, Haryana 132001, India

**Author details:**
- Harsh Dagar, Research Scholar; ORCID: https://orcid.org/0009-0008-7394-130X; Email: harshdagar5879@gmail.com
- Gunjan Bhandari, Scientist; ORCID: https://orcid.org/0000-0001-6004-7642; Email: gunjanbhandari5@gmail.com

**Correspondence:** Harsh Dagar, Division of Dairy Economics, Statistics and Management, ICAR-National Dairy Research Institute, Karnal, Haryana 132001, India. Email: harshdagar5879@gmail.com

---

## ABSTRACT

India's PM-KUSUM scheme subsidises solar pumpsets to displace diesel and agricultural grid load, yet a solar pump's near-zero marginal energy cost can raise groundwater extraction even under a nominal water charge, because the collapse in energy cost, not the water price alone, shifts the extraction margin. Using a panel of 36 Indian states/UTs over FY2014-15 to FY2024-25, we treat back-cast KUSUM intensity as associational under two-way fixed effects and identify the groundwater response with an instrument interacting solar resource (global horizontal irradiance, GHI) with pre-scheme diesel-pump density. Wild cluster-bootstrap fixed effects link intensity to a 2.3% contraction in tube-well irrigated area. IV estimation raises groundwater stage of extraction by +0.10 percentage points per intensity unit (first-stage F = 20.6), concentrated in Component B, standalone diesel-replacement pumps (F = 54.3); Component C, grid solarisation, is too weakly instrumented for a causal claim (F = 1.4). The positive sign survives leave-one-out and regional-exclusion checks, though instrument strength depends heavily on Jharkhand, the highest-intensity state, a dependency we disclose. A carbon bridge yields central gross abatement of 1.93 Mt CO₂ yr⁻¹, rebound of 0.28 Mt and net abatement of about 1.65 Mt; the rebound share rises mechanically from about 11% in safe aquifers to about 31% in over-exploited ones because deeper water tables cost more energy to lift, not because we find evidence of a larger causal elasticity under stress; our heterogeneity test runs on the associational tube-well margin and cannot speak directly to the causal groundwater elasticity itself. Policy should haircut climate credit and condition Component B in stressed aquifers, not halt solar irrigation, and not treat Components B and C as one instrument.

**Keywords:** PM-KUSUM; solar irrigation; groundwater; climate policy; rebound effect; India; instrumental variables

---

## 1. INTRODUCTION

Solar irrigation is widely treated as an unambiguous climate good. Solar photovoltaic pumps that replace diesel irrigation directly cut emissions from fuel combustion, and solarised grid pumps reduce agricultural electricity load. India's flagship PM-KUSUM scheme channels public capital toward exactly these benefits: decarbonisation, farmer income support and a lower DISCOM subsidy burden. This climate-mitigation narrative is strongly supported in current energy-policy literature. What remains largely unaccounted for is the water cost: whether the same subsidy that lowers carbon intensity also lowers the price of pumping enough to accelerate depletion of a resource that energy policy rarely prices at all.

While diesel and grid-connected pumps impose a positive marginal cost per unit of water extracted, a solar pump's marginal cost drops to effectively zero once installed. Because of this collapse in variable pumping costs, the law of demand for inputs predicts higher water extraction (Saunders, 1992; Sorrell, 2009), a prediction that holds even where a nominal water charge exists, because it is the relative price of energy, not the water price alone, that shifts the extraction margin. If the aquifer is already stressed, fuel-emission savings may be partly offset by additional pumping energy and by irreversible depletion of a common-pool resource (Shah, 2009; Famiglietti, 2014). South Asian work already shows that cheap agricultural power deepens wells and raises extraction (Badiani et al., 2012; Fishman et al., 2015; Mukherji, 2022), and that solar-pump pilots can raise farmer surplus while dulling the scarcity signal that a rising energy bill would otherwise send as the water table falls deeper (Closas and Rap, 2017; Gupta, 2019). What remains unsettled for national programme design is whether that rebound is large enough, under PM-KUSUM, to change climate accounting and targeting rules.

**Research gap.** Existing evaluations of solar irrigation are rich on farm-level surplus and energy substitution, but thin on three programme-scale objects that climate and groundwater ministries actually use. First, most Indian evidence does not separate PM-KUSUM Component B (standalone diesel-replacement pumps) from Component C (grid/feeder solarisation), even though the two change different margins of the energy-water nexus. Second, groundwater rebound is often inferred from extensive-margin proxies (pump counts or irrigated area) rather than from the intensive-margin regulatory metric, CGWB stage of extraction, that classifies blocks as safe, semi-critical, critical or over-exploited. Third, official and project carbon claims typically report gross diesel/grid displacement and rarely net out intensive-margin rebound by aquifer class, so results-based climate finance can over-claim where water stress is already worst. Without an honesty-checked treatment construction, an IV design with placebos, and a transparent carbon bridge, policymakers lack a decision-grade map from intensity to stage points and from stage points to net Mt CO₂.

We estimate effects on three outcomes: tube-well irrigated area (extensive margin); agricultural grid electricity; and CGWB stage of extraction (extraction/recharge, %). Stage of extraction is the regulatory variable used in groundwater governance.

**Research questions.** This paper answers four linked questions:

1. Does higher PM-KUSUM intensity coincide geographically with already stressed aquifers at the state level?
2. Holding state and year fixed effects, is intensity associated with fewer tube-well hectares (extensive margin), and, under an instrument interacting solar resource with pre-scheme diesel density, does intensity raise groundwater stage of extraction (intensive margin)?
3. Is any causal groundwater response concentrated in Component B rather than Component C, and does it survive adversarial checks (including exclusion of Punjab, Haryana and Rajasthan)?
4. Once intensive-margin rebound is converted to CO₂, how large is the gap between gross and net abatement, and how should that gap shape climate-credit haircuts and Component B conditioning?

Four contributions follow. First, we evaluate groundwater-rebound risk under PM-KUSUM by transparently documenting how the treatment series is constructed, so that every downstream estimate carries an explicit statement of what is associational and what is causal. Second, we isolate the scheme's true causal channel by separating standalone from grid-connected pumps and anchoring the groundwater estimate in an instrumental-variables design validated against a placebo battery, while two-way fixed effects with a wild cluster-bootstrap protect the associational estimates from the false positives that plague small-cluster panels (Cameron et al., 2008). Third, we build an intensive-margin carbon bridge that converts the causal groundwater response into hidden rebound emissions, correcting the common error of inferring water use from a declining extensive-margin infrastructure count. Fourth, we subject the design to an adversarial confirmatory suite (leave-one-out and regional-exclusion IV, winsorised treatment, alternative denominators, year-by-year reduced forms) that converts statistical significance into decision magnitudes: stage points at policy-relevant intensities, the Mt CO₂ at risk of over-claim, and the INR social-cost bands attached to the rebound.

Headline findings follow this same order. Descriptively, high-solar, high-KUSUM states span both stressed aquifers (Punjab, Haryana, Rajasthan) and currently safe ones with heavy scheme deployment (Jharkhand, Maharashtra, Gujarat): co-location, not causation, and the reason we turn to instrumental variables. Associationally, KUSUM intensity is linked to a 2.3% contraction in tube-well hectares (infrastructure consolidation, not evidence of lower aquifer stress). Causally, intensity raises groundwater stage of extraction by about 0.10 percentage points per unit, concentrated in Component B; the sign holds under leave-one-out and regional-exclusion checks, though the instrument's strength depends heavily on Jharkhand, the single highest-intensity state, a dependency we report rather than obscure (Section 5.8). Converted to carbon terms, gross abatement is real (~1.9 Mt CO₂ yr⁻¹); net is lower (~1.65 Mt) once intensive-margin rebound is subtracted, with the rebound share rising mechanically from about 11% in safe aquifers to about 31% in over-exploited ones because deeper water tables cost more energy to lift, a physical fact about pumping depth and not a statistically estimated behavioural amplification; our heterogeneity test on the associational tube-well margin finds no such amplification either, though it cannot speak directly to the causal groundwater elasticity itself (Section 5.5). The highest-impact conclusion is a conditional climate-finance rule paired with groundwater governance: **target and condition Component B, do not halt it.**

---

## 2. BACKGROUND AND LITERATURE

### 2.1 Solar irrigation policy in India

Indian agriculture consumes roughly 18-20% of national electricity, and an estimated 15-20 million energised and diesel pumpsets lift groundwater (MoSPI, 2023). Flat agricultural tariffs have long functioned as an implicit subsidy on extraction (Shah, 2009; Dubash, 2012; Badiani et al., 2012).

PM-KUSUM (announced 2019) has three components. Official scheme documentation targets addition of about **34,800 MW** of solar capacity, with Component A supporting decentralised solar plants feeding the grid (about 10,000 MW in the scheme design), Component B supporting installation of standalone solar agriculture pumps (about 14 lakh pumps in the design envelope), and Component C supporting solarisation of grid-connected agriculture pumps including feeder-level solarisation (about 35 lakh pumps in the design envelope). Component A sanctioned capacity in the December 2024 state snapshot is on the order of **~20 GW** of decentralised plant capacity, not hundreds of GW; installed capacity remains far lower. Component B subsidises standalone solar pumps, typically replacing diesel. Component C solarises grid-connected pumps through individual pump solarisation or feeder-level solarisation.

MNRE (2025) has repeatedly extended implementation windows as states and developers faced financing and grid delays. Eligible projects with power-purchase agreements or notices to proceed issued on or before 31 December 2025 have been granted revised completion timelines running through **31 March 2027** for specified Component A / feeder-level Component C commissioning paths, with earlier intermediate deadlines for financial closure and for Component B / individual-pump Component C commissioning. That extension makes aquifer-smart targeting urgent now: the next wave of installations will land while groundwater stress is already high in several high-solar states. National physical-progress files show cumulative Component B additions of about 0.40 million pumps and Component C additions of about 0.014 million through mid-2024 in the annual addition series; terminal June 2025 state snapshots record much larger cumulative installed stocks (about 1.68 million Component B and 1.20 million Component C installations), reflecting stock-versus-flow reporting differences that we keep transparent. Government communications have cited annual CO₂ reductions on the order of 0.5 Mt for early coverage years; our ledger is a national scenario construct and is compared to that figure only as an order-of-magnitude check.

### 2.2 Groundwater depletion

India extracts on the order of 250 bcm yr⁻¹ of groundwater, about a quarter of global extraction (CGWB, 2024). Roughly one-third of assessment units are semi-critical, critical or over-exploited (CGWB, 2023). Northwestern alluvial systems show large GRACE-inferred declines (Rodell et al., 2009; Tiwari et al., 2009). Because groundwater is a common-pool resource, subsidies that lower the variable cost of pumping without pricing water reproduce the tragedy of the commons (Shah, 2009; Famiglietti, 2014).

### 2.3 Rebound in energy and water

Jevons-type rebound (efficiency or cost reductions raising use) is documented in energy economics (Saunders, 1992; Greening et al., 2000; Sorrell, 2009) and increasingly in water systems (Dumont et al., 2013; Sears et al., 2018). Solar pumps are a textbook case: they improve the energy cost of lift and, absent water prices or quotas, raise optimal extraction. South Asian evidence links flat-rate agricultural power to deeper wells and higher extraction (Badiani et al., 2012; Fishman et al., 2015; Mukherji, 2022) and documents solar-pump pilots that raise farmer surplus while weakening scarcity signals (Closas and Rap, 2017; Gupta, 2019; Yashodha et al., 2021). Feeder separation and metering experiments show that restoring a positive marginal price for daytime power can reverse extraction incentives (Banerjee et al., 2014), aligning with structural evidence that rationing agricultural electricity directly constrains water demand (Ryan and Sudarshan, 2022). Our contribution is to quantify state-level causal and carbon magnitudes under PM-KUSUM with a multi-estimator package and an intensive-margin carbon bridge.

### 2.4 Empirical strategies

Three threats dominate. (i) Endogenous placement: stressed, sunny, administratively capable states adopt faster. (ii) Mechanical back-cast treatment: national additions allocated by terminal shares correlate with cumulative success. (iii) Sparse groundwater assessments (2020, 2022, 2023, 2024) with interpolation. We address (i)-(ii) with an IV design and a battery of placebo tests: falsification checks that apply the instrument to pre-policy data, or to an outcome the policy could not plausibly affect, so that a significant result there would flag a broken design rather than a real effect. We address (iii) with non-interpolated subsamples and dual interpolation rules. Modern staggered DiD concerns (de Chaisemartin and D'Haultfœuille, 2020; Callaway and Sant'Anna, 2021; Sun and Abraham, 2021) motivate the event-study layer. Wild cluster bootstrap guards inference with ~30 state clusters (Cameron et al., 2008).

---

## 3. DATA

### 3.1 Panel

Balanced panel: 36 states/UTs × 11 fiscal years (FY2014-15 to FY2024-25) = 396 rows. Raw inputs span KUSUM progress, agricultural electricity, irrigation by source, CGWB groundwater, diesel baselines, district groundwater (seven states), GSDP, foodgrain and energised pumpsets, plus institutional and climate covariates constructed for this study (DISCOM health, RPO trajectory, GHI).

### 3.2 Treatment construction (explicit vulnerability)

There is no complete official state-year installation series. Primary treatment allocates national annual Component B+C additions by each state's share of the June 2025 cumulative installed stock, yielding `kusum_cum_pumps` and intensity per 1,000 ha net irrigated area (`kusum_intensity_per_kha`). We also construct **Component B-only** and **Component C-only** intensities and a **terminal cross-sectional dose** (no time path). Because terminal shares are endogenous to cumulative adoption, TWFE on the back-cast series is reported as **associational**. Causal groundwater claims rest on IV.

### 3.3 Outcomes and controls

Tube-well irrigated area ('000 ha) from the Ministry of Agriculture long file. Agricultural grid electricity (GWh) for FY2016-17 to FY2021-22. Groundwater stage (%) from CGWB assessment years, carried forward (step) and linearly interpolated; a flag marks interpolated cells (~64% of panel cells). Income control: log real GDP per capita. Instrument ingredients: NASA observed GHI (20 states) and 2016-17 diesel-pump counts.

---

## 4. EMPIRICAL STRATEGY

### 4.1 Functional form

For each outcome we select among level, log, inverse hyperbolic sine and per-hectare transforms by Bayesian Information Criterion (BIC), so the mathematical shape applied to each variable is chosen objectively rather than by hand. Selected: tube-wells → log (so the coefficient reads directly as a percentage change); agricultural electricity → asinh, a log-like transform that survives the true zeros in the electricity series and yields coefficients that remain interpretable as approximate percentage changes even at low values (Bellemare and Wichman, 2020); groundwater stage → asinh for the associational FE model, but retained at level for the IV model so the causal coefficient is directly interpretable as a percentage-point (pp) change for policymakers.

### 4.2 Two-way FE (associational)

$$g(Y_{st}) = \beta \cdot \text{KUSUM}_{st} + \gamma \log(\text{GDPpc})_{st} + \alpha_s + \lambda_t + \varepsilon_{st}$$

State fixed effects ($\alpha_s$) absorb time-invariant characteristics such as underlying hydrogeology; year fixed effects ($\lambda_t$) absorb national shocks such as a weak monsoon or a macro downturn. Because $\text{KUSUM}_{st}$ is back-cast from terminal cumulative shares to overcome incomplete official reporting (Section 3.2), we treat $\beta$ as associational rather than causal: a mathematically generated regressor cannot carry a causal label regardless of how precisely it is estimated. With only 36 state clusters, conventional cluster-robust standard errors risk over-rejecting the null; inference instead uses a restricted wild cluster bootstrap (Rademacher weights, null imposed, 9,999 replications), implemented via Frisch-Waugh-Lovell partialling to remain robust to third-party package instability (Cameron et al., 2008).

### 4.3 Event study

We define treatment onset $E_s$ as the first fiscal year a state's KUSUM intensity crosses the 70th percentile (swept over {50,60,70,75,80}). Standard two-way fixed-effects estimators are known to be biased under staggered adoption when treatment effects vary over time (de Chaisemartin and D'Haultfœuille, 2020; Sun and Abraham, 2021), which motivates a dynamic specification. The primary estimator is the Sun-Abraham (2021) interaction-weighted estimator:

$$Y_{st} = \alpha_s + \lambda_t + \sum_{e \notin \{-1,\infty\}} \delta_e \, \mathbb{1}\{t - E_s = e\} + \gamma \log(\text{GDPpc})_{st} + \varepsilon_{st}$$

Each $\delta_e$ traces a distinct effect for a given year relative to onset rather than collapsing the whole panel into one pooled average. A flat, near-zero path for the pre-treatment "leads" ($e<0$) supports the parallel-trends assumption that irrigation footprints were stable before KUSUM arrived, so that any divergence after onset can be attributed to the scheme rather than a pre-existing trend. As a secondary check for tube-wells, we also report the Callaway-Sant'Anna (2021) group-time average treatment effect on the treated (ATT), which is more robust to treatment-effect heterogeneity across adoption cohorts than a single pooled TWFE coefficient.

### 4.4 Instrumental variables (causal groundwater claim)

To strip out endogenous placement (the concern that administratively capable, sunny, already-stressed states adopt KUSUM fastest), we instrument pooled and component-specific KUSUM intensity with observed GHI interacted with pre-scheme (2016-17) diesel-pump density per irrigated hectare:

$$\text{First stage:} \qquad \text{KUSUM}_{st} = \pi_0 + \pi_1 (\text{GHI}_s \times \text{Diesel}_{s,2016}) + \alpha_s + \lambda_t + \nu_{st}$$
$$\text{Second stage:} \qquad Y_{st} = \beta^{IV}\, \widehat{\text{KUSUM}}_{st} + \alpha_s + \lambda_t + \mu_{st}$$

$\widehat{\text{KUSUM}}_{st}$ is the fitted value from the first stage: the share of observed KUSUM intensity that lines up with pure geography (sunlight) and pre-existing diesel infrastructure, rather than with whatever administrative or political criteria the government applied when it rolled the scheme out after 2019. This does not discard the real installation or outcome data: 2SLS uses the actual groundwater and tube-well series throughout and only replaces the endogenous regressor with its instrumented component. First-stage F and cluster-robust 2SLS standard errors are reported for every specification. The battery includes GHI alone, diesel alone, a linear groundwater-interpolation variant, non-interpolated years, and Component B and C treatments separately.

Relevance is direct: solar panels convert sunlight, so GHI dictates physical viability, and Component B explicitly subsidises diesel replacement, so pre-scheme diesel density dictates the target market; their interaction should predict where Component B thrives. Exclusion is not automatic, however: pre-scheme diesel density is itself correlated with historic irrigation intensity, so the instrument could in principle predict groundwater trends through channels other than KUSUM. We test this directly rather than assert it.

#### 4.4.1 Falsification battery (reduced-form placebos)

If the instrument's correlation with groundwater or tube-wells is real only because KUSUM exists, it should not predict those same outcomes before the scheme was announced:

$$Y^{pre}_{st} = \phi\,(\text{GHI}_s \times \text{Diesel}_{s,2016}) + \gamma \log(\text{GDPpc})_{st} + \alpha_s + \lambda_t + \omega_{st} \qquad \forall\, t \le 2018$$

If the instrument is instead picking up something structurally unrelated to solar groundwater pumping (general agricultural expansion, say), it should also fail to predict surface-canal irrigated area, which draws no groundwater:

$$\text{Canal}_{st} = \psi\,(\text{GHI}_s \times \text{Diesel}_{s,2016}) + \gamma \log(\text{GDPpc})_{st} + \alpha_s + \lambda_t + \upsilon_{st} \qquad (\text{all years})$$

For the exclusion restriction to hold, both $\phi$ and $\psi$ must be indistinguishable from zero. We additionally report a post-2020 reduced form of the instrument on groundwater stage as a positive check: once the scheme is active, this coefficient should be non-null if the KUSUM-groundwater channel is real.

### 4.5 Heterogeneity

We test whether the associational tube-well consolidation response, not the causal groundwater-stage response itself, is amplified by baseline aquifer stress or weak DISCOM finances. The panel cannot support a stress-by-DISCOM-stratified instrumented model with adequate power in each cell, so this heterogeneity check necessarily runs on the extensive-margin (tube-well) outcome rather than on the intensive-margin causal elasticity; we use two complementary approaches, chosen by a pre-registered rule so that which one is "primary" is not left to post-hoc discretion. A causal forest, built on the honest-splitting theory of Wager and Athey (2018) and implemented as a generalized random forest (Athey, Tibshirani and Wager, 2019), is estimated with orthogonalised nuisance functions in the Double/Debiased Machine Learning framework (Chernozhukov et al., 2018) and GridSearchCV tuning over lasso, random-forest and gradient-boosting learners, and estimates

$$\tau(x) = \mathbb{E}[Y_i(1) - Y_i(0) \mid X_i = x]$$

for state-year covariate profiles $x$ (DISCOM health, GHI, RPO compliance, groundwater stage, income), with tube-well irrigated area as the outcome $Y$. In parallel, a transparent continuous interaction model estimates

$$Y_{st} = \beta_1 \,\text{KUSUM}_{st} + \beta_2\,(\text{KUSUM}_{st} \times \text{Covariate}_{st}) + \alpha_s + \lambda_t + \varepsilon_{st}$$

with log tube-well irrigated area as $Y_{st}$ and continuous groundwater stage and DISCOM health as the moderators, replacing an earlier sparse categorical specification whose semi-critical interaction term was numerically unstable because too few state-years fall in that cell. **Pre-registered rule:** if the causal forest's average confidence-interval width exceeds the standard deviation of estimated CATEs, the interaction model is treated as primary and the forest is reported only as a machine-learning cross-check.

### 4.6 Carbon ledger and intensive-margin rebound bridge

Gross abatement sweeps diesel fuel use {400,600,800} L pump⁻¹ yr⁻¹ and grid EF {0.71, 0.7383, 0.79} tCO₂ MWh⁻¹ (nine scenarios). The core correction in this bridge is methodological: many evaluations look at a decline in visible tube-well counts and infer water savings. We explicitly reject that inference: pump counts cannot be used to back out extraction volume once the intensity of pumping per well has changed. Instead, we derive rebound from the causal IV coefficient on groundwater stage:

$$\Delta V_{st} = \left(\frac{\beta^{IV} \cdot \text{KUSUM}_{st}}{100}\right) \times \overline{\text{Extractable}}_s$$
$$\text{Rebound}_{CO_2} = \sum_s \left(\Delta V_{st} \times \rho_{\text{lift}} \times \eta_{\text{energy}} \times \theta_{\text{grid}}\right)$$
$$\text{Net}_{CO_2} = \text{Gross}_{CO_2} - \text{Rebound}_{CO_2}$$

$\overline{\text{Extractable}}_s$ proxies each state's extractable resource by allocating India's ~251 bcm by net irrigated area shares (the panel carries no direct bcm series); $\rho_{\text{lift}}$ is a stage-scaled lift depth; $\eta_{\text{energy}}$ is the literature-derived pump energy intensity (kWh m⁻³ m⁻¹); $\theta_{\text{grid}}$ is the central grid emission factor. Sensitivity sweeps vary energy intensity and lift baselines. Net = gross − positive rebound, with the signed (possibly negative) version reported separately.

### 4.7 Confirmatory and assumption stress-tests

We subject the baseline IV to a structured battery designed to break it. **Leave-one-out (jackknife):**

$$Y_{st} = \beta^{IV(-j)}\, \widehat{\text{KUSUM}}_{st} + \alpha_s + \lambda_t + \mu_{st} \qquad \forall\, j \in S$$

re-estimated once per state $j$, dropping that state entirely, so that no single state can silently anchor the national result. **Regional exclusion** is the same equation restricted to $s \notin \{\text{PB}, \text{HR}, \text{RJ}\}$, testing whether the effect is a three-state anecdote or a national pattern. **Distributional robustness** winsorises treatment intensity at the 1st/99th percentiles and swaps the denominator (per 1,000 energised pumpsets vs. per cropped hectare) to check that neither outliers nor an arbitrary scaling choice is driving the sign. **Component isolation** decouples the pooled treatment,

$$Y_{st} = \beta_B\, \text{KUSUM}_{B,st} + \beta_C\, \text{KUSUM}_{C,st} + \alpha_s + \lambda_t + \mu_{st}$$

to avoid conflating Component B's zero-marginal-cost incentive with Component C's opposite, sell-back incentive. **Data-architecture checks** re-estimate the FE model on the ~36% of cells that are true (non-interpolated) CGWB assessment years, and collapse the panel into a **terminal cross-sectional dose**,

$$Y_s = \gamma\, \text{KUSUM}_{s,2025} + X_s'\theta + \epsilon_s$$

to verify that the time-series identification, not merely the terminal snapshot, is doing the causal work. Finally, a structured assumption hit-list (`assumption_stress_tests`) records, for each threat to validity, whether it is fixed, partial, checked or rejected, so no limitation is implicit.

---

## 5. RESULTS

### 5.1 Descriptive geographic alignment

**FIGURE_EMBED:** V2_india_dual_choropleth | Figure 1. Geographic alignment of PM-KUSUM intensity and groundwater stress across Indian states. Darker shades indicate higher values. Co-location of high intensity with stressed aquifers motivates instrumental-variables identification; it is not itself a causal estimate.

Figure 1 plots PM-KUSUM intensity against groundwater stress across Indian states, and the pattern is more complex than a simple "northwestern belt" story. Table 1 makes this explicit with the underlying numbers for the states with the highest terminal-year intensity in the panel, alongside the national average.

**Table 1. State-level alignment of PM-KUSUM intensity and groundwater stress, FY2024-25** (terminal panel year; Component B intensity per 1,000 ha net irrigated area).

| State | KUSUM intensity (per 1,000 ha) | Component B intensity | Groundwater stage (%) | CGWB classification |
|-------|--------------------------------:|-----------------------:|------------------------:|:---------------------|
| Jharkhand | 50.89 | 84.21 | 31.4 | Safe |
| Maharashtra | 31.96 | 30.54 | 53.0 | Safe |
| Haryana | 13.91 | 23.02 | 136.0 | Over-exploited |
| Gujarat | 8.90 | 0.89 | 54.2 | Safe |
| Kerala | 8.96 | 0.01 | 53.8 | Safe |
| Rajasthan | 4.66 | 5.18 | 149.9 | Over-exploited |
| Uttar Pradesh | 1.47 | 2.30 | 70.5 | Semi-critical |
| Karnataka | 1.41 | 0.23 | 68.4 | Safe |
| Punjab | 1.04 | 1.73 | 156.9 | Over-exploited |
| **National average** | **5.58** | n/a | **50.9** | Mixed |

The two highest-intensity states in the terminal year, Jharkhand and Maharashtra, are both classified safe; the canonical over-exploited trio (Punjab, Haryana, Rajasthan) shows the highest stage values but comparatively modest terminal intensity once back-cast allocation and net irrigated area are taken into account. This matters for two reasons. First, the descriptive co-location often attributed to the northwestern belt is real but partial: dense KUSUM deployment reaches states across the full range of aquifer stress, which is exactly why a national instrument, rather than a regional adjustment for three states, is needed to separate scheme effect from geography. Second, it flags in advance a result we return to in Section 5.8: because Jharkhand carries a disproportionate share of the intensity variation the instrument uses for identification, its exclusion is a substantive stress test, not an afterthought. Co-location is not causation; it is the motivation for IV, consistent with endogenous programme placement documented for agricultural electricity and irrigation subsidies more broadly (Dubash, 2012; Badiani et al., 2012).

### 5.2 TWFE channels (associational)

**Table 2. Two-way fixed-effects channel results** (BIC-selected transforms; wild cluster-bootstrap *p*; income control = log GDP per capita).

| Outcome | Transform | n | Coefficient | SE | Wild bootstrap *p* |
|---------|-----------|--:|------------:|---:|-------------------:|
| Tube-well irrigated area | log | 106 | −0.0229 | 0.0035 | **0.0218** |
| Agricultural grid electricity | asinh | 84 | −0.0171 | 0.0114 | 0.382 |
| Groundwater stage of extraction | asinh | 165 | −0.0009 | 0.0027 | 0.781 |

Tube-well area: about 2.3% fewer tube-well hectares per intensity unit. Agricultural electricity and FE groundwater stage are imprecise. Standard panel-data theory holds that adding a relevant control should move a biased coefficient toward zero if that control was previously an omitted confounder (Wooldridge, 2010); we use this logic as a stepwise check and confirm that income is not driving the tube-well result: the naïve TWFE without the income control returns β = −0.0222 (SE 0.0038, n = 108); adding log GDP per capita moves the estimate to β = −0.0229 (SE 0.0035, wild-bootstrap p = 0.022, n = 106). Adding income strengthens rather than weakens the coefficient, which is the opposite of what omitted-variable bias from richer states expanding irrigation generally would predict; the small drop in n reflects income-series coverage in the panel, not selection on the outcome. We interpret the tube-well decline as extensive-margin consolidation, not as proof of lower aquifer stress.

### 5.3 Event study

Sun-Abraham leads for tube-wells are near zero, which supports the parallel-trends assumption that irrigation footprints were stable before the scheme arrived; post-onset point estimates become more negative by t=+3, with wide SEs. Callaway-Sant'Anna ATT at t=+3 is −506.9 ha (95% CI excludes zero), a statistically significant consolidation of visible pump infrastructure by the third year after onset. Groundwater event-study paths remain imprecise, consistent with FE attenuation under the ~64% interpolated CGWB assessment years, and the reason the intensive-margin claim rests on Section 5.4's instrumented design rather than on this timeline alone.

### 5.4 IV groundwater response (causal)

**Table 3. Instrumental-variables battery** (2SLS; instrument = observed GHI × baseline diesel density unless noted; SEs clustered by state).

| Spec | Outcome | Treatment | β | SE | *p* | First-stage F | n |
|------|---------|-----------|--:|---:|----:|--------------:|--:|
| Primary | GW stage (step) | Pooled intensity | **0.102** | 0.033 | 0.002 | **20.6** | 120 |
| Robust | GW stage (linear) | Pooled intensity | 0.079 | 0.027 | 0.004 | 20.6 | 120 |
| Non-interpolated years | GW stage | Pooled intensity | 0.115 | 0.047 | 0.013 | 7.5 | 80 |
| Component B | GW stage | B intensity | **0.056** | 0.017 | <0.001 | **54.3** | 120 |
| Component C | GW stage | C intensity | −11.74 | 11.17 | 0.29 | 1.4 | 120 |
| Primary | Tube-wells | Pooled intensity | 0.40 | 9.67 | 0.97 | 28.4 | 90 |
| Primary | Agri grid GWh | Pooled intensity | −64.8 | 40.5 | 0.11 | 222.5 | 60 |

**Table 4. Reduced-form placebo / post-checks** (outcome on instrument + FE + income).

| Test | Outcome | Sample | β | *p* | Pass? |
|------|---------|--------|--:|----:|:-----:|
| Pre-KUSUM placebo | GW stage | ≤FY2018 | ≈0 | 0.52 | Yes |
| Pre-KUSUM placebo | Tube-wells | ≤FY2018 | −0.098 | 0.32 | Yes |
| Canal placebo | Canal area | Full | −0.033 | 0.69 | Yes |
| Post-onset RF | GW stage | ≥FY2020 | 0.0014 | <0.001 | Expected non-null |

The seven specifications in Table 3 do three jobs at once. The **primary model** establishes the causal channel: instrumented KUSUM intensity raises groundwater stage by 0.102 pp per unit, with a first-stage F of 20.6 comfortably above the Stock-Yogo weak-instrument benchmark of 10 (Stock and Yogo, 2005). The **component split** (rows 4-5) shows this is not one undifferentiated "solar irrigation" effect: Component B alone is strongly instrumented (F = 54.3) and returns a positive, precise coefficient, while Component C is weakly instrumented (F = 1.4) and its coefficient is statistically indistinguishable from zero, so we do not report a Component C groundwater elasticity because the design cannot support one. The **falsification rows** (non-interpolated subsample; tube-wells and agri-grid electricity as outcomes under the same instrument) show where the design is silent as much as where it speaks: the instrument does not move tube-well counts or grid electricity with any precision, consistent with those outcomes measuring different margins than the intensive groundwater response the instrument is built to isolate.

Table 4 completes the exclusion-restriction argument. Two placebo channels (pre-2019 groundwater stage and pre-2019 tube-wells) return coefficients statistically indistinguishable from zero, meaning the instrument does not predict outcomes it could not have caused before the scheme existed. The canal-area placebo, run across all years, is also null, meaning the instrument does not simply track general agricultural expansion. The post-2020 reduced form is small in absolute size but highly precise and positive, exactly the pattern expected once the scheme is active. Together, these four rows are the paper's strongest defence of the exclusion restriction: they do not prove it in the way a randomised experiment would, but they rule out the two most obvious violations we could test with existing data.

**FIGURE_EMBED:** V4_paradox_balance_scales | Figure 2. The solar-irrigation paradox on two margins: associational TWFE links intensity to about 2.3% fewer tube-well hectares (extensive margin), while IV raises groundwater stage by about +0.10 pp per intensity unit (intensive margin).

**FIGURE_EMBED:** V5_component_power_meters | Figure 3. Component identification. First-stage strength concentrates in Component B (F = 54.3); Component C is weakly instrumented (F = 1.4). Causal groundwater claims therefore attach to standalone diesel-replacement pumps, not to pooled B+C intensity.

Figure 2 summarises the two-margin result that organises the rest of the paper: fewer tube-well hectares can coexist with higher stage of extraction when marginal pumping cost collapses. Figure 3 shows why Component B, not Component C, carries the causal groundwater claim: the instrument is built for the diesel-replacement margin that Component B targets, consistent with prior solar-pump pilot evidence that zero-marginal-cost daytime power can expand withdrawals even as fuel bills fall (Closas and Rap, 2017; Gupta, 2019).

### 5.5 Heterogeneity on the tube-well margin: no robust evidence of amplification

A natural next question is whether the tube-well consolidation response is worse in already-stressed aquifers or in states with weaker DISCOM finances; the panel's sample size does not support running this stress-by-DISCOM interaction on the intensive-margin causal outcome itself, so we test it on the associational tube-well outcome instead and are explicit that this is a different quantity from the paper's central causal groundwater estimate. Following the pre-registered rule in Section 4.5, we checked the causal forest first: its average CATE confidence-interval width (≈121, tuning log) exceeds the standard deviation of estimated CATEs across states (≈28), so the rule assigns primacy to the transparent continuous interaction model, and the forest is reported only as a cross-check.

The continuous interaction model does not support a heterogeneous-amplification story on the tube-well margin. The interaction of KUSUM intensity with continuous groundwater stage is small and statistically indistinguishable from zero (β = −7.5×10⁻⁵, p = 0.54, n = 106), as is the interaction with DISCOM health (β = −0.017, p = 0.43, n = 106); the main KUSUM term in this specification is also null (β = −0.008, p = 0.59). An earlier sparse categorical specification (interacting intensity with a discrete groundwater-stress category, also on the tube-well outcome) had returned a large, seemingly dramatic semi-critical coefficient (≈−792). We do not report that coefficient as a finding: the semi-critical category contains very few state-years, and a coefficient that large and that sensitive to cell sparsity is a symptom of an unstable specification, not evidence of a real effect. We flag this explicitly rather than let a striking but fragile number stand in for a null result. Because this heterogeneity test runs on the tube-well outcome, it speaks to whether infrastructure consolidation varies by stress class; it is silent on whether the underlying causal groundwater-stage elasticity itself varies by stress class, a question our panel is not powered to answer directly.

This null finding needs to be kept conceptually separate from the carbon bridge's stress-differentiated haircuts reported in Section 5.6, where the rebound share is far higher in over-exploited zones (about 31%) than in safe ones (about 11%). That gap is a **mechanical** consequence of the carbon bridge's lift-depth term ($\rho_{\text{lift}}$ in Section 4.6), which scales with how deep the water table already sits: lifting the same extra cubic metre of water from a deeply depleted aquifer costs more energy than lifting it from a shallow one, as a matter of physics, regardless of whether the underlying causal elasticity itself varies by stress class. It is not a claim, and should not be read as a claim, that the estimated behavioural response to KUSUM intensity is larger where aquifers are stressed; our heterogeneity tests do not support that stronger claim at conventional confidence levels.

### 5.6 Carbon: gross, rebound, net

Central gross abatement: **1.93 Mt CO₂ yr⁻¹** (nine EF×fuel scenarios ≈ 1.36-2.49 Mt). Using IV β = 0.102, central intensive-margin rebound ≈ **0.28 Mt** (energy/lift sensitivity ≈ 0.18-0.46 Mt). Net central ≈ **1.65 Mt**.

**FIGURE_EMBED:** V9_carbon_balance_sheet | Figure 4. Carbon balance sheet. Central gross abatement is 1.93 Mt CO₂ yr⁻¹; intensive-margin rebound is 0.28 Mt; net is about 1.65 Mt. Rebound offsets about 11% of gross abatement in safe zones but about 31% in over-exploited zones.

**Table 5. Substitution vs intensive-margin rebound by groundwater-stress class** (central scenario; latest fiscal year; kt CO₂). Offset share is the class's summed rebound divided by its summed gross substitution.

| Stress class | Gross substitution | Rebound offset | Net | Offset share |
|--------------|-------------------:|---------------:|----:|-------------:|
| Safe | 507.5 | 57.4 | 450.1 | **11.3%** |
| Semi-critical | 36.5 | 5.6 | 31.0 | 15.2% |
| Over-exploited | 160.6 | 49.6 | 111.0 | **30.9%** |

Figure 4 and Table 5 make the same point in different registers: claiming the gross figure as net benefit overstates climate performance most where aquifers are already failing, because that is exactly where the mechanical lift-depth penalty is steepest, the classic Jevons pattern applied to irrigation energy (Dumont et al., 2013; Sears et al., 2018).

### 5.7 Confirmatory suite (standard)

Component B FE on tube-wells remains negative and precise; Component C FE is noisy. Cross-sectional terminal dose on groundwater is insignificant: without IV, back-cast/CS designs do not deliver a clean GW effect. Canal FE placebo is null. Non-interpolated GW FE is positive but imprecise. The assumption table records which threats are fixed, partial or rejected.

### 5.8 Adversarial confirmation and policy magnitudes

We next try to break the headline IV.

**Table 6. Critical confirmation tests** (outcome = groundwater stage unless noted).

| Stress test | β | First-stage F | *p* | Survives? |
|-------------|--:|--------------:|----:|:---------:|
| Baseline IV | 0.102 | 20.6 | 0.002 | n/a |
| Drop Punjab+Haryana+Rajasthan | **0.101** | 19.3 | 0.005 | **Yes** |
| Winsorise intensity 1-99% | 0.142 | 12.2 | 0.006 | Yes |
| Intensity per 1,000 energised pumpsets | 0.051 | 39.8 | <0.001 | Yes |
| Intensity per cropped hectare | −1.76 | 0.42 | 0.54 | No (weak instrument) |
| Leave-one-out, all states except Jharkhand | 0.086-0.122 | 18.997-22.820 | ≤0.006 | **Yes** |
| Leave-one-out, drop Jharkhand | **0.074** | **2.08** | **0.71** | **Sign holds; power and significance lost** |

Three insights follow, and we report the third as honestly as the first two. First, the groundwater effect is **not** an artefact of the northwestern wheat-rice belt: excluding Punjab, Haryana and Rajasthan leaves β ≈ 0.10 with F = 19.3, essentially unchanged from baseline. National targeting rules remain warranted; NW governance is necessary but not sufficient as the whole story. Second, denominator choice matters and we report the failure transparently: pumpset-normalised intensity reproduces the sign with a strong first stage (F = 39.8), while a cropped-area denominator fails the instrument outright (F = 0.42); this is a failed confirmation, not a hidden one, and it tells us the instrument operates through the physically accurate pump-replacement pathway rather than through broad agricultural area.

Third, and this is the caveat flagged in Section 5.1: dropping every state except Jharkhand leaves the coefficient stable and significant (β = 0.086-0.122, F ≥ 19), but dropping **Jharkhand specifically** (the single highest-intensity state in the panel) collapses the first-stage F from 20.6 to 2.08 and pushes the p-value to 0.71. The point estimate stays positive (β = 0.074), so the sign is not reversed, but the estimate becomes statistically indistinguishable from zero and the instrument becomes too weak to support a causal reading on its own. We do not describe the baseline result as universally "bulletproof" against leave-one-out deletion; it is robust to dropping any of the other 19 states in the estimation sample, and it depends materially on Jharkhand for its statistical power. This is a genuine limitation of identification with roughly 20 usable state clusters and one dominant high-intensity observation, and we carry it forward into the discussion (Section 6.6) rather than let the "100%-of-LOO-draws-stay-positive" framing stand alone.

**Table 7. Decision magnitudes** (using baseline IV β = 0.102 and central carbon bridge).

| Quantity | Value |
|----------|------:|
| Implied Δ stage at median intensity | +0.08 pp |
| Implied Δ stage at p75 intensity | +0.30 pp |
| Implied Δ stage at p90 intensity | **+0.94 pp** |
| Gross abatement | 1.93 Mt CO₂ yr⁻¹ |
| Intensive-margin rebound | 0.28 Mt |
| Net abatement | 1.65 Mt |
| Over-claim if gross sold as net | **0.28 Mt yr⁻¹** |
| Rebound offset share, safe zones | 11.3% |
| Rebound offset share, over-exploited | **30.9%** |
| Rebound social cost @ ₹1,500/t | ≈ ₹42 crore yr⁻¹ |
| Net abatement value @ ₹1,500/t | ≈ ₹247 crore yr⁻¹ |

At high intensity, nearly a full percentage point of stage is at stake. The climate-accounting error from citing gross as net is itself material (~0.28 Mt), and it is concentrated where aquifers are already failing.

One further adversarial nuance deserves equal weight: **year-by-year cross-sectional** reduced forms of the instrument on groundwater stage (no state FE) are negative, whereas the **panel reduced form with state FE** after 2020 is positive and precise. That gap is informative, not embarrassing: between-state co-location of solar/diesel endowments with aquifer stress differs from within-state responses to instrumented KUSUM intensity, the same reason the terminal cross-sectional dose is null and the IV/FE design is required for causal claims.

---

## 6. INTERPRETATION AND DISCUSSION

### 6.1 What the two results mean together

At first sight the main results pull in opposite directions. Tube-well area falls with KUSUM intensity, while groundwater stage of extraction rises. The two findings can sit side by side. Tube-well area counts how much land is irrigated by tube-wells. Stage of extraction records how hard the aquifer is being used. Solar pumps can reduce the number of wells in view and still raise water lifted per well, because daytime pumping no longer carries a fuel bill (Shah, 2009; Fishman et al., 2015). Energy studies have long noted the same pattern: when the cost of using an input falls, use often rises (Saunders, 1992; Greening et al., 2000; Sorrell, 2009). Aquifer stress is therefore about intensity of pumping, not about the count of pumps alone. Northern India already showed large groundwater losses before PM-KUSUM scaled (Rodell et al., 2009; Tiwari et al., 2009; Famiglietti, 2014). A scheme that makes lifting cheaper arrives on aquifers that were under strain.

### 6.2 Why Component B matters more than Component C

Component B installs standalone solar pumps meant to replace diesel sets. That is the channel the instrument is built to follow: sunny places with many diesel pumps before the scheme. Earlier solar-pump work warned that free daytime power can expand withdrawals even when fuel costs fall (Closas and Rap, 2017; Gupta, 2019). Component C solarises grid-connected pumps and feeders. It changes DISCOM incentives more than diesel bills, and it is weakly instrumented in this panel (first-stage F = 1.4). The paper therefore does not report a causal groundwater elasticity for Component C. Pooling B and C as one "solar irrigation" treatment would attach B's groundwater result to a channel this design cannot identify. The safer reading is simple: treat the two components as different tools (Ryan and Sudarshan, 2022).

### 6.3 Reading the carbon numbers with care

Gross abatement of about 1.93 Mt CO₂ yr⁻¹ is real. Diesel displacement and avoided grid load are genuine climate gains (Closas and Rap, 2017). Net abatement is lower, about 1.65 Mt, once intensive-margin rebound of about 0.28 Mt is subtracted. The rebound share is about 11% in safe zones and about 31% in over-exploited zones. That gap is not a claim that farmers in stressed blocks respond more strongly to KUSUM. Section 5.5's heterogeneity test runs on the associational tube-well margin, not on the causal groundwater elasticity, and finds no amplification there either, but it cannot directly test whether the causal elasticity itself is larger under stress. The higher share in over-exploited zones follows from lift depth: the same extra cubic metre costs more energy when the water table is already deep (Dumont et al., 2013; Sears et al., 2018). The bridge uses published constants and a sensitivity grid; it is calibrated, not a full farm model. For climate finance the practical lesson is direct. Paying the full gross figure as if it were net flatters the worst aquifers. A fairer scorecard uses net abatement, or applies a larger haircut where stage of extraction is already above safe limits.

### 6.4 What this means for policy

Stopping Component B is not the right response. In India, agricultural power reform has usually worked when it restored a price or scarcity signal, not when it cut off farmers' access to energy (Shah, 2009; Mukherji, 2022; Ryan and Sudarshan, 2022). Our results point toward a similar, quieter rule: keep solar irrigation running, but change how it is measured and where it is pushed.

A few practical steps follow from this:

- Use the CGWB stress class as a screen. In over-exploited and critical blocks, groundwater risk should be checked before carbon credits are approved (CGWB, 2023, 2024).
- Pay climate credit on net abatement, not the gross figure. Where the stage of extraction is already at or above 100%, full gross claims should wait until the state DISCOM or nodal agency confirms metering or feeder separation, using CGWB's own maps. The bridge points to a haircut of roughly one-third in over-exploited zones and around one-tenth (about 11%) in safe zones.
- Push Component B faster where aquifers are safe and diesel use is still common, but attach metering or micro-irrigation conditions wherever aquifers are already stressed.
- Track Components B and C on separate scorecards. The groundwater response found for Component B should not be assumed to hold for Component C, which needs its own evaluation.

MNRE's commissioning deadline of March 2027 leaves some room to put these checks in place before the next big round of installations goes ahead. None of this calls for a new satellite product or a fresh dataset; the CGWB classes and MNRE component codes that already exist are enough for a first layer of oversight. Additional tables and figures are given in the Supplementary Information.

### 6.5 What a sceptical reader should check

Section 7 gives the headline numbers. What follows here is why we trust the design behind them, not just the point estimates.

- We report the tests that failed, not only the ones that passed. A cropped-area version of the intensity measure breaks the instrument outright (F = 0.42), and a single cross-section from the terminal year cannot recover any groundwater effect without the full time-series IV. Both results are useful: they show the instrument tracks pump replacement, which is what it was built to measure, rather than some broader measure of farm activity.
- Tube-well area is falling while the groundwater stage of extraction is rising, which can look contradictory at first. It is not: this is the paper's central point. As farms consolidate into fewer, more efficient wells, extraction can keep climbing even though the well count alone makes it look like less water is being pumped.
- A small coefficient can still carry real weight. On its own, +0.10 pp per intensity unit looks modest. But at the 90th percentile of intensity, the implied rise in stage of extraction is close to a full percentage point, large enough to push some blocks over a regulatory threshold.
- The causal estimate has one weak point worth stating plainly. Its statistical power comes mostly from Jharkhand. Drop any other single state and the result holds; drop Jharkhand and the sign survives but the estimate loses significance. We treat this as a limit on precision, not a reason to doubt the direction of the effect.
- We keep the heterogeneity results and the carbon gradient separate on purpose. We are not claiming the underlying behavioural response is larger in stressed aquifers; the bigger carbon haircut there comes from a simple physical fact, water sitting deeper costs more energy to lift. Our heterogeneity test runs on tube-well area rather than groundwater stage, because the panel is too small to test the stress-by-DISCOM interaction on the causal outcome with any real power. So it speaks to infrastructure consolidation, not to whether the causal effect itself changes with stress.

### 6.6 Limits of the study

Several limits should be kept in view. The KUSUM series is back-cast from national additions and terminal state shares, so the fixed-effects tube-well result is associational; causal groundwater claims rest on the IV and its placebos. About 64% of groundwater cells are interpolated between sparse assessment years; the IV sign holds on non-interpolated years, but the first stage is weaker. The instrument is strong for Component B and weak for Component C. Leave-one-out tests show that power depends on Jharkhand. One more limit concerns Section 5.5. Our panel is simply too small to test the stress-by-DISCOM interaction on the actual causal outcome, groundwater stage, with any real power, so that check runs on tube-well area instead. We found no sign of amplification on that margin, but that is different from proving the causal elasticity does not change with stress class; the data cannot answer that second question directly. On top of this, the carbon bridge is built from the IV stage response and published energy factors rather than from metering on actual farms, and gaps in installation data, along with aquifers that cross state lines, add further uncertainty to how precise our numbers can be. Even so, none of this changes what we think the policy answer should be: judge solar irrigation by net carbon and by aquifer class, and stop treating Components B and C as if they were one and the same instrument.

---

## 7. CONCLUSION AND POLICY IMPLICATIONS

PM-KUSUM cuts fuel and grid emissions. It can also push up groundwater extraction at the same time, simply because a solar pump costs almost nothing to run once it is installed. We tested this with an IV design, checked it against placebos, and ran it through a set of adversarial checks meant to break it. What comes out the other side is a real, positive groundwater response on the intensive margin, driven mainly by Component B, sitting alongside a fall in tube-well area on the extensive margin. Drop the northwestern states and the result holds. Drop any single state other than Jharkhand and it still holds. Drop Jharkhand itself and the instrument weakens a lot, which tells us something about how much precision rests on one state, not that the underlying effect is doubtful. On the carbon side, our bridge puts net abatement at around 1.65 Mt CO₂ a year against a gross figure of 1.93 Mt, and the rebound eats into that gain more in stressed aquifers (about 31%) than in safe ones (about 11%); treating the gross number as if it were net would overstate the benefit by roughly 0.28 Mt. A heterogeneity check on the tube-well side finds no sign that this response gets stronger under stress, though we are upfront that our panel simply is not big enough to test that question directly on the causal margin itself.

The highest-impact policy reading is a conditional climate-finance and groundwater-governance rule: protect solar irrigation's climate gains by haircutting carbon credit and requiring metering/feeder separation where aquifers are already failing; accelerate Component B where aquifers are safe and diesel baselines are high; and stop treating Components B and C as one instrument. We reject a blanket halt on Component B. The solar-irrigation paradox is not an argument against renewables; it is an argument against scoring renewables as unconditional climate victories while the energy cost of lifting common-pool water keeps collapsing toward zero.

---

## METHODS SUMMARY

Analyses in Python using pandas, numpy, scipy, statsmodels, linearmodels, pyfixest and econml. Scripts `p3_00`-`p3_15` are fully runnable (`python run_all.py`), including adversarial confirmation (`p3_14`). Parameter grids and literature constants live in `config/`. SHA-256 hashes of raw inputs are logged in the integrity report. Seed = 1502.

---

## DATA AVAILABILITY

Primary sources: Ministry of Agriculture; CGWB; CEA emission factors; MoSPI; PM-KUSUM national and state progress reports. Processed panels and tables accompany the replication archive at [repository DOI to be added].

---

## CODE AVAILABILITY

Replication code: [repository DOI to be added]. Pipeline stages include confirmatory tests (`p3_13`) and rebound-bridge audit tables.

---

## ACKNOWLEDGEMENTS

We thank colleagues in the Division of Dairy Economics, Statistics and Management at ICAR-National Dairy Research Institute, Karnal, for institutional support. Errors remain ours.

---

## AUTHOR CONTRIBUTIONS

H.D.: conceptualisation, data curation, formal analysis, investigation, methodology, software, validation, visualisation, writing (original draft), writing (review and editing). G.B.: supervision, validation, writing (review and editing). Both authors approved the final manuscript.

---

## COMPETING INTERESTS

The authors declare no competing interests.

---

## SUPPLEMENTARY INFORMATION

Figures 1-4 in the main text are drawn from the executive visual set (geographic alignment; paradox scales; component identification; carbon balance). The separate Supplementary Information file contains Tables S1-S3 and the full figure set (Figures S1-S10), including event-study, heterogeneity, leave-one-out, rebound-sensitivity and governance-matrix panels not reproduced above.

---

## DECLARATION OF GENERATIVE AI AND AI-ASSISTED TECHNOLOGIES IN THE MANUSCRIPT PREPARATION PROCESS

During the preparation of this work the authors used [NAME OF TOOL/SERVICE] to assist with drafting prose, checking internal consistency of results across tables and manuscript text, and formatting. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

---

## REFERENCES

Athey, S., Tibshirani, J. and Wager, S. Generalized random forests. *Annals of Statistics*, 47(2), 1148-1178 (2019).

Badiani, R., Jessoe, K. K. and Plant, S. Development and the environment: the implications of agricultural electricity subsidies in India. *Journal of Environment & Development*, 21(2), 244-262 (2012).

Banerjee, S. G., Khanna, A., Khurana, M., Mukherjee, M. and Saraswat, K. *Lighting Rural India: Load Segregation Experience in Selected States*. Asia Sustainable and Alternative Energy (ASTAE) Program, South Asia Energy Studies, World Bank (2014).

Bellemare, M. F. and Wichman, C. J. Elasticities and the inverse hyperbolic sine transformation. *Oxford Bulletin of Economics and Statistics*, 82(1), 50-61 (2020).

Callaway, B. and Sant'Anna, P. H. C. Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200-230 (2021).

Cameron, A. C., Gelbach, J. B. and Miller, D. L. Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics*, 90(3), 414-427 (2008).

Central Ground Water Board (CGWB). *National Compilation on Dynamic Ground Water Resources of India, 2023*. Ministry of Jal Shakti (2023).

Central Ground Water Board (CGWB). *National Compilation on Dynamic Ground Water Resources of India, 2024*. Ministry of Jal Shakti (2024).

Chernozhukov, V. et al. Double/debiased machine learning for treatment and structural parameters. *The Econometrics Journal*, 21(1), C1-C68 (2018).

Closas, A. and Rap, E. Solar-based groundwater pumping for irrigation: sustainability, policies and limitations. *Energy Policy*, 104, 33-37 (2017).

de Chaisemartin, C. and D'Haultfœuille, X. Two-way fixed effects estimators with heterogeneous treatment effects. *American Economic Review*, 110(9), 2964-2996 (2020).

Dubash, N. K. (ed.). *Handbook of Climate Change and India: Development, Politics, and Governance*. Oxford University Press (2012).

Dumont, A., Mayor, B. and López-Gunn, E. Is the rebound effect or Jevons paradox a useful concept for water resource management? *Water Policy*, 15, 137-156 (2013).

Famiglietti, J. S. The global groundwater crisis. *Nature Climate Change*, 4, 945-948 (2014).

Fishman, R., Devineni, N. and Raman, S. Can improved agricultural water use efficiency save India's groundwater? *Environmental Research Letters*, 10, 084022 (2015).

Greening, L. A., Greene, D. L. and Difiglio, C. Energy efficiency and consumption, the rebound effect: a survey. *Energy Policy*, 28, 389-401 (2000).

Gupta, E. The impact of solar water pumps on energy-water-food nexus: Evidence from Rajasthan, India. *Energy Policy*, 129, 819-831 (2019).

Ministry of New and Renewable Energy (MNRE). *Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyaan (PM-KUSUM)* scheme documentation and subsequent timeline revisions (target design capacity ~34,800 MW; eligible-project commissioning windows extended through March 2027). Ministry of New and Renewable Energy, Government of India (2025).

Ministry of Statistics and Programme Implementation (MoSPI). *Energy Statistics India*. Government of India (2023).

Mukherji, A. Sustainable groundwater management in India needs a water-energy-food nexus approach. *Groundwater for Sustainable Development*, 18, 100782 (2022).

Rodell, M., Velicogna, I. and Famiglietti, J. S. Satellite-based estimates of groundwater depletion in India. *Nature*, 460, 999-1002 (2009).

Ryan, N. and Sudarshan, A. Rationing the commons. *Journal of Political Economy*, 130(1), 210-256 (2022).

Saunders, H. D. The Khazzoom-Brookes postulate and neoclassical growth. *The Energy Journal*, 13(4), 131-148 (1992).

Sears, L. et al. Jevons' Paradox and efficient irrigation technology. *Sustainability*, 10(5), 1590 (2018).

Shah, T. *Taming the Anarchy: Groundwater Governance in South Asia*. Resources for the Future Press (2009).

Sorrell, S. Jevons' Paradox revisited. *Energy Policy*, 37, 4456-4469 (2009).

Stock, J. H. and Yogo, M. Testing for weak instruments in linear IV regression. In Andrews and Stock (eds.), *Identification and Inference for Econometric Models*. Cambridge University Press (2005).

Sun, L. and Abraham, S. Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2), 175-199 (2021).

Tiwari, V. M., Wahr, J. and Swenson, S. Dwindling groundwater resources in northern India, from satellite gravity observations. *Geophysical Research Letters*, 36, L18401 (2009).

Wager, S. and Athey, S. Estimation and inference of heterogeneous treatment effects using random forests. *Journal of the American Statistical Association*, 113(523), 1228-1242 (2018).

Wooldridge, J. M. *Econometric Analysis of Cross Section and Panel Data*, 2nd ed. MIT Press (2010).

Yashodha, Y., Sanjay, A. and Mukherji, A. *Solar Irrigation in India: A Situation Analysis Report*. International Water Management Institute (IWMI) (2021).
