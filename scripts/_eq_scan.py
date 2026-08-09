import re
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "outputs" / "manuscript_PAPER3_NatureSustainability.md"
text = path.read_text(encoding="utf-8")

blocks = re.findall(r"\$\$(.+?)\$\$", text, re.DOTALL)
print("block count:", len(blocks))

text_no_blocks = re.sub(r"\$\$.+?\$\$", "", text, flags=re.DOTALL)
inlines = re.findall(r"\$([^$\n]+)\$", text_no_blocks)
print("inline count:", len(inlines))
for x in inlines:
    print(repr(x))
