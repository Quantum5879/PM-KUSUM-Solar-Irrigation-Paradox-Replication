import subprocess, tempfile, zipfile
from pathlib import Path

eqs = [
r"g(Y_{st}) = \beta \cdot \text{KUSUM}_{st} + \gamma \log(\text{GDPpc})_{st} + \alpha_s + \lambda_t + \varepsilon_{st}",
r"Y_{st} = \alpha_s + \lambda_t + \sum_{e \notin \{-1,\infty\}} \delta_e \, \mathbb{1}\{t - E_s = e\} + \gamma \log(\text{GDPpc})_{st} + \varepsilon_{st}",
r"\text{First stage:} \qquad \text{KUSUM}_{st} = \pi_0 + \pi_1 (\text{GHI}_s \times \text{Diesel}_{s,2016}) + \alpha_s + \lambda_t + \nu_{st}",
r"\text{Second stage:} \qquad Y_{st} = \beta^{IV}\, \widehat{\text{KUSUM}}_{st} + \alpha_s + \lambda_t + \mu_{st}",
r"Y^{pre}_{st} = \phi\,(\text{GHI}_s \times \text{Diesel}_{s,2016}) + \gamma \log(\text{GDPpc})_{st} + \alpha_s + \lambda_t + \omega_{st} \qquad \forall\, t \le 2018",
r"\text{Canal}_{st} = \psi\,(\text{GHI}_s \times \text{Diesel}_{s,2016}) + \gamma \log(\text{GDPpc})_{st} + \alpha_s + \lambda_t + \upsilon_{st} \qquad (\text{all years})",
r"\tau(x) = \mathbb{E}[Y_i(1) - Y_i(0) \mid X_i = x]",
r"Y_{st} = \beta_1 \,\text{KUSUM}_{st} + \beta_2\,(\text{KUSUM}_{st} \times \text{Covariate}_{st}) + \alpha_s + \lambda_t + \varepsilon_{st}",
r"\Delta V_{st} = \left(\frac{\beta^{IV} \cdot \text{KUSUM}_{st}}{100}\right) \times \overline{\text{Extractable}}_s",
r"\text{Rebound}_{CO_2} = \sum_s \left(\Delta V_{st} \times \rho_{\text{lift}} \times \eta_{\text{energy}} \times \theta_{\text{grid}}\right)",
r"\text{Net}_{CO_2} = \text{Gross}_{CO_2} - \text{Rebound}_{CO_2}",
r"Y_{st} = \beta^{IV(-j)}\, \widehat{\text{KUSUM}}_{st} + \alpha_s + \lambda_t + \mu_{st} \qquad \forall\, j \in S",
r"Y_{st} = \beta_B\, \text{KUSUM}_{B,st} + \beta_C\, \text{KUSUM}_{C,st} + \alpha_s + \lambda_t + \mu_{st}",
r"Y_s = \gamma\, \text{KUSUM}_{s,2025} + X_s'\theta + \epsilon_s",
]

with tempfile.TemporaryDirectory() as td:
    for i, eq in enumerate(eqs):
        md_path = Path(td) / f"eq{i}.md"
        docx_path = Path(td) / f"eq{i}.docx"
        md_path.write_text(f"$${eq}$$", encoding="utf-8")
        try:
            r = subprocess.run(["pandoc", str(md_path), "-o", str(docx_path)], capture_output=True, text=True, timeout=15)
            if r.returncode != 0:
                print(f"EQ {i} FAILED: {r.stderr[:300]}")
                continue
            with zipfile.ZipFile(docx_path) as z:
                xml = z.read("word/document.xml").decode("utf-8")
            has_omath = "oMath" in xml
            print(f"EQ {i}: OK, has_omath={has_omath}, len={len(xml)}")
        except Exception as e:
            print(f"EQ {i} EXCEPTION: {e}")
