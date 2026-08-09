import subprocess, tempfile, zipfile
from pathlib import Path

samples = [
    r"State fixed effects ($\alpha_s$) absorb time and year fixed effects ($\lambda_t$) absorb national shocks.",
    r"Because $\text{KUSUM}_{st}$ is back-cast we treat $\beta$ as associational.",
    r"We define treatment onset $E_s$ as the first fiscal year.",
    r"Each $\delta_e$ traces a distinct effect. A flat path for the leads ($e<0$) supports parallel trends.",
    r"$\widehat{\text{KUSUM}}_{st}$ is the fitted value from the first stage.",
    r"For the exclusion restriction to hold, both $\phi$ and $\psi$ must be indistinguishable from zero.",
    r"for state-year covariate profiles $x$ (DISCOM health, GHI).",
    r"$\overline{\text{Extractable}}_s$ proxies each state's extractable resource; $\rho_{\text{lift}}$ is a stage-scaled lift depth; $\eta_{\text{energy}}$ is pump energy intensity; $\theta_{\text{grid}}$ is the grid emission factor.",
    r"re-estimated once per state $j$. Regional exclusion is restricted to $s \notin \{\text{PB}, \text{HR}, \text{RJ}\}$.",
]

with tempfile.TemporaryDirectory() as td:
    for i, s in enumerate(samples):
        md_path = Path(td) / f"s{i}.md"
        docx_path = Path(td) / f"s{i}.docx"
        md_path.write_text(s, encoding="utf-8")
        r = subprocess.run(["pandoc", str(md_path), "-o", str(docx_path)], capture_output=True, text=True, timeout=15)
        if r.returncode != 0:
            print(f"S {i} FAILED: {r.stderr[:300]}")
            continue
        with zipfile.ZipFile(docx_path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        has_omath = "<m:oMath>" in xml or "<m:oMath " in xml
        has_omathpara = "oMathPara" in xml
        print(f"S {i}: omath={has_omath} omathpara={has_omathpara}")
        print("  ", xml[xml.find("<w:body>")+8: xml.find("<w:body>")+900])
