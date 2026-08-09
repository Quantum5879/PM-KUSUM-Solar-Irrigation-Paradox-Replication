import pandas as pd

panel = pd.read_parquet('data/processed/master_panel_state_year.parquet')
last = int(panel['fy_start'].max())
d = panel[panel['fy_start'] == last].dropna(subset=['kusum_intensity_per_kha', 'gw_stress_cat']).copy()
median_int = d['kusum_intensity_per_kha'].median()
print('median intensity:', median_int)
d['bucket'] = d['kusum_intensity_per_kha'].apply(lambda x: 'HIGH' if x > median_int else 'LOW')
for _, r in d.sort_values('kusum_intensity_per_kha', ascending=False).iterrows():
    print(f"{r['state']:25s} {r['kusum_intensity_per_kha']:8.2f} {r['gw_stress_cat']:15s} {r['bucket']}")
