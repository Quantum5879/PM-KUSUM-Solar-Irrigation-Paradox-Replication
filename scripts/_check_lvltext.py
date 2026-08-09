import zipfile
import re

with zipfile.ZipFile('FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx') as z:
    xml = z.read('word/numbering.xml').decode('utf-8')

m = re.search(r'<w:abstractNum w:abstractNumId="10".*?</w:abstractNum>', xml, re.DOTALL)
block = m.group(0)
m2 = re.search(r'<w:lvlText w:val="(.*?)"', block)
val = m2.group(1)
print('lvlText repr:', repr(val))
print('codepoints:', [hex(ord(c)) for c in val])

# also check abstractNum 8 (numId 1, used by ListBullet style) for comparison
m3 = re.search(r'<w:abstractNum w:abstractNumId="8".*?</w:abstractNum>', xml, re.DOTALL)
block3 = m3.group(0)
m4 = re.search(r'<w:lvlText w:val="(.*?)"', block3)
val3 = m4.group(1)
print('style lvlText repr:', repr(val3))
print('codepoints:', [hex(ord(c)) for c in val3])
