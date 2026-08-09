import re

text = open('scripts/_manuscript_docx_text_v2.txt', encoding='utf-8').read()

em = text.count('\u2014')
en = text.count('\u2013')
lq = text.count('\u201c')
rq = text.count('\u201d')
apo = text.count('\u2019')
print('em:', em, 'en:', en, 'curly_lq:', lq, 'curly_rq:', rq, 'curly_apo:', apo)
print()

# Abstract check
m = re.search(r'Abstract\n(.+?)\nKeywords', text, re.DOTALL)
abstract = m.group(1).strip()
print('ABSTRACT (', len(abstract.split()), 'words ):')
print(abstract)
print()

# grammar fix check
print('"needs to haircut" still present:', 'needs to haircut' in text)
print('"need to haircut" present:', 'need to haircut' in text)
print()

# 6.2 duplicate check
print('6.2 duplicate phrase gone:', 'Solarises grid connected pumps and feeders in component C. Component C solarises' not in text)
idx = text.find('Component B deploys stand-alone')
print(text[idx:idx+700])
print()

# 6.4 heading check
print('"What this mean for policy" gone:', 'What this mean for policy' not in text)
print('"What this means for policy" present:', 'What this means for policy' in text)
print()

# table 6 check
print('"in table 6" (lowercase) gone:', 'in table 6' not in text)
print('"in Table 6" present:', 'in Table 6' in text)
print()

# double period check
print('double period ".." gone:', '..' not in text)
