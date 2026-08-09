import zipfile
import re

with zipfile.ZipFile('FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx') as z:
    xml = z.read('word/numbering.xml').decode('utf-8')

m = re.search(r'<w:num w:numId="11"[^>]*>.*?<w:abstractNumId w:val="(\d+)"', xml, re.DOTALL)
print('numId 11 -> abstractNumId', m.group(1) if m else None)
abs_id = m.group(1)
m2 = re.search(r'<w:abstractNum w:abstractNumId="' + abs_id + r'".*?</w:abstractNum>', xml, re.DOTALL)
block = m2.group(0)
m3 = re.search(r'<w:lvl w:ilvl="0".*?</w:lvl>', block, re.DOTALL)
print(m3.group(0)[:600])
