import zipfile
import re

with zipfile.ZipFile('FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx') as z:
    styles_xml = z.read('word/styles.xml').decode('utf-8')

m = re.search(r'<w:style [^>]*w:styleId="ListBullet"[^>]*>.*?</w:style>', styles_xml, re.DOTALL)
if m:
    print(m.group(0)[:800])
else:
    print('ListBullet style block not found by that id, searching by name')
    m2 = re.search(r'<w:style [^>]*>(?:(?!</w:style>).)*?List Bullet(?:(?!</w:style>).)*?</w:style>', styles_xml, re.DOTALL)
    print(m2.group(0)[:800] if m2 else 'not found')
