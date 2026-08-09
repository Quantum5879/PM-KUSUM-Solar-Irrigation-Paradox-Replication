# Paper 3 — Integrity Report

## SHA-256 of raw sources
- `agri_electricity_consumption_GWh_2016-17_to_2019-20.csv`: `f5c9b42acb36d328…`
- `agri_electricity_consumption_GWh_2020-21_to_2021-22.csv`: `786f15b3b2455113…`
- `CGWB_groundwater_statewise_2024_opencity_OPENSOURCE.csv`: `b0fa4974e63584ce…`
- `groundwater_resources_LONG_2020_2022_2023_2024.csv`: `b1a682f78d08b30d…`
- `gsdp_statewise_raw.csv`: `3b8b4c3547be072d…`
- `irrigation_pumpsets_energised_statewise_as31Mar2023.csv`: `0aac8b90484a6d5c…`
- `kusum_national_physical_progress_2019-20_to_2024-25.csv`: `b6b097656ddc6ffe…`
- `kusum_statewise_CO2_emission_reduction_as31Oct2022.csv`: `5a22481311b67a53…`
- `kusum_statewise_diesel_vs_standalonesolar_pumps_as31Oct2022.csv`: `88ad7d6b408df525…`
- `kusum_statewise_progress_components_as30Jun2025.csv`: `92f40d368838195e…`
- `kusum_statewise_solarpumps_sanctioned_installed_as31Dec2024.csv`: `95b88f823d287cf7…`
- `net_irrigated_area_by_source_000ha_2023-24.csv`: `066ebc544e9728c3…`
- `net_irrigated_area_by_source_000ha_LONG_2014-15_to_2023-24.csv`: `40e43bad790b4a45…`
- `total_foodgrains_area_production_productivity_2024-25.csv`: `efc7cf629a8125c1…`

## Groundwater cross-check (Indiastat vs open CKAN, 2024)
- states matched: 37; max |diff| in stage-of-extraction = 0.005 pp -> PASS

## Expected outputs
- [ok] fig1_paradox_scatter.png
- [ok] fig2_event_studies.png
- [ok] fig3_decomposition_waterfall.png
- [ok] fig4_signflip_surface.png
- [ok] fig5_ccts_fanchart.png
- [ok] fig6_district_mechanism.png