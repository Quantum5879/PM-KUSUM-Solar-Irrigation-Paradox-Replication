import zipfile
from pathlib import Path
from docx import Document

path = Path(__file__).resolve().parents[1] / "FINAL_SUBMISSION_PACKAGE" / "03_Manuscript.docx"

# 1. Confirm python-docx (and therefore Word) can open it without error.
doc = Document(str(path))
print("Opened OK. Paragraph count:", len(doc.paragraphs))

# 2. Confirm native OMML math objects are present, and count them.
with zipfile.ZipFile(path) as z:
    xml = z.read("word/document.xml").decode("utf-8")

n_omath = xml.count("<m:oMath>") + xml.count("<m:oMath ")
n_omathpara = xml.count("<m:oMathPara>") + xml.count("<m:oMathPara ")
print("oMath count:", n_omath)
print("oMathPara count:", n_omathpara)

# 3. Confirm no leftover literal LaTeX markers or dash characters slipped through.
for marker in (r"\alpha", r"\beta", r"\text{", "$$", "\u2014", "\u2013"):
    print(f"contains {marker!r}:", marker in xml)

# 4. Spot check: locate the first block equation and print surrounding XML.
idx = xml.find("<m:oMathPara")
print()
print("First block equation context:")
print(xml[max(0, idx - 60): idx + 400])
