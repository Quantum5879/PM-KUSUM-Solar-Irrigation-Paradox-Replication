from docx import Document

doc = Document('FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx')

targets = {
    'ABSTRACT': "India's PM-KUSUM scheme subsidises",
    'INTRO': 'Solar irrigation is considered an unambiguous',
    '5.3_EVENT': 'Sun-Abraham leads for tube-wells',
    '6.2_COMPONENT': 'Component B deploys stand-alone solar pumps',
    '6.4_HEADING': 'What this mean for policy',
    '5.8_TABLE6': 'As shown in table 6',
}

for label, prefix in targets.items():
    for i, p in enumerate(doc.paragraphs):
        if p.text.startswith(prefix) or prefix in p.text[:200]:
            print('===', label, '=== paragraph index:', i, 'style:', p.style.name)
            for j, r in enumerate(p.runs):
                print(j, repr(r.text))
            print()
            break
