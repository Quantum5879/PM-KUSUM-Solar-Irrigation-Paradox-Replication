import re
from docx import Document

path = 'scripts/_manuscript_docx_text.txt'
text = open(path, encoding='utf-8').read()

doc = Document('FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx')
xml = doc.element.xml
print('oMath count:', xml.count('<m:oMath>') + xml.count('<m:oMath '))
print('oMathPara count:', xml.count('oMathPara'))
print("contains raw LaTeX \\alpha:", '\\alpha' in xml)
print('contains $$ marker:', '$$' in text)
print('contains \\text{ marker:', '\\text{' in xml)
print()

# Body prose word count (Intro through Conclusion, excluding refs/methods)
m = re.search(r'1\. INTRODUCTION\n(.+?)\nMETHODS SUMMARY', text, re.DOTALL)
if m:
    body = m.group(1)
    words = re.findall(r'\b[A-Za-z0-9]+\b', body)
    print('Body prose word count (Intro-Conclusion):', len(words))

# Check heading numbering sequence
headings = re.findall(r'^(\d+\.\d+(?:\.\d+)?)\s', text, re.MULTILINE)
print('Subheadings found:', headings)

# Check for duplicate/garbled text (e.g. "Solarises grid connected pumps and feeders in component C. Component C solarises...")
if 'Solarises grid connected pumps and feeders in component C. Component C solarises' in text:
    print()
    print('FOUND DUPLICATE SENTENCE IN 6.2 (component C described twice, garbled)')

# Check title case / heading with "6.4 What this mean for policy" typo
if 'What this mean for policy' in text:
    print('FOUND TYPO: "What this mean for policy" (should be "means")')

# Check for "As shown in table 6" lowercase table ref
lowercase_refs = re.findall(r'\b(table|figure) \d+', text)
print('Lowercase table/figure refs:', lowercase_refs)

# lgtm check for lists that used to be dash bullets but now are missing bullet markers
sec_64 = re.search(r'A few insights follow from this:\n(.+?)MNRE', text, re.DOTALL)
if sec_64:
    print()
    print('SECTION 6.4 LIST BLOCK:')
    print(repr(sec_64.group(1)[:600]))
