"""
Applies the 7 approved minor fixes to FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx,
editing exact runs in place so no formatting/styles are disturbed.
"""
from docx import Document

PATH = 'FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx'
doc = Document(PATH)
p = doc.paragraphs

def show(idx, label):
    print(f'--- {label} (para {idx}) BEFORE ---')
    print(p[idx].text)
    print()

# ------------------------------------------------------------------
# Fix 1 & 2: Abstract (paragraph 2)
# ------------------------------------------------------------------
ab = p[2]
assert ab.runs[10].text.startswith('The extraction of groundwater'), ab.runs[10].text[:60]
ab.runs[10].text = (
    "The extraction of groundwater from wells or boreholes (IV estimation) has "
    "also shown a causal groundwater stage increase of +0.10 percentage points "
    "per intensity unit (first-stage F = 20.6, above conventional weak-instrument "
    "thresholds), concentrated in the standalone diesel-replacement pumps "
    "(Component B, F = 54.3). The positive sign withstood the leave-one-out and "
    "regional-exclusion tests with heav"
)
assert ab.runs[21].text == 'needs'
ab.runs[21].text = 'need'

# ------------------------------------------------------------------
# Fix 8a: Introduction en dashes + rewording (paragraph 5)
# ------------------------------------------------------------------
intro = p[5]
assert 'benefits –' in intro.runs[4].text
intro.runs[4].text = intro.runs[4].text.replace(
    'focuses on public investments on just these benefits – ',
    'focuses on public investments on just these benefits: '
)
assert 'if it can be called that –' in intro.runs[6].text
intro.runs[6].text = intro.runs[6].text.replace(
    'The water cost, if it can be called that – the cost of pumping the same amount ',
    'The water cost (if it can be called that: the cost of pumping the same amount '
)
assert 'hardly priced by energy policy –' in intro.runs[8].text
intro.runs[8].text = intro.runs[8].text.replace(
    'hardly priced by energy policy – remains a mystery.',
    'hardly priced by energy policy) remains a mystery.'
)

# ------------------------------------------------------------------
# Fix 8b: Section 5.3 curly apostrophe (paragraph 88)
# ------------------------------------------------------------------
sec53 = p[88]
assert sec53.runs[11].text == '\u2019s'
sec53.runs[11].text = "'s"

# ------------------------------------------------------------------
# Fix 3: Section 6.2 duplicate sentence (paragraph 128)
# ------------------------------------------------------------------
sec62 = p[128]
assert sec62.runs[7].text == 'Solarises'
assert sec62.runs[8].text == ' grid connected pumps and feeders in component'
assert sec62.runs[9].text == ' C'
assert sec62.runs[10].text == '. Component C '
sec62.runs[7].text = ''
sec62.runs[8].text = ''
sec62.runs[9].text = ''
sec62.runs[10].text = 'Component C '
# runs[11] 'solarises' and runs[12] ' grid-connected pumps and feeders. It changes...' stay as-is

# ------------------------------------------------------------------
# Fix 4: Section 6.4 heading typo (paragraph 131)
# ------------------------------------------------------------------
heading64 = p[131]
assert heading64.runs[3].text == 'mean'
heading64.runs[3].text = 'means'

# ------------------------------------------------------------------
# Fix 5: Section 5.8 lowercase "table 6" (paragraph 118)
# ------------------------------------------------------------------
sec58a = p[118]
assert sec58a.runs[2].text == ' in table'
sec58a.runs[2].text = ' in Table'

# ------------------------------------------------------------------
# Fix 6: Section 5.8 stray double period (paragraph 123)
# ------------------------------------------------------------------
sec58b = p[123]
assert sec58b.runs[12].text == '.'
sec58b.runs[12].text = ''

doc.save(PATH)
print('All 7 fixes applied and saved.')
