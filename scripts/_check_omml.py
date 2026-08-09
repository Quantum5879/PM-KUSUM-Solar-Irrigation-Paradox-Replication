import re
from docx import Document

doc = Document('FINAL_SUBMISSION_PACKAGE/03_Manuscript.docx')
xml = doc.element.xml

opens = len(re.findall(r'<m:oMathPara>', xml))
closes = len(re.findall(r'</m:oMathPara>', xml))
selfclose = len(re.findall(r'<m:oMathPara/>', xml))
print('oMathPara opens:', opens, 'closes:', closes, 'selfclose:', selfclose)

pr_tags = len(re.findall(r'<m:oMathParaPr', xml))
print('oMathParaPr tags (nested property element, substring match explains inflated count):', pr_tags)

math_opens = len(re.findall(r'<m:oMath>', xml))
math_closes = len(re.findall(r'</m:oMath>', xml))
print('oMath opens:', math_opens, 'closes:', math_closes)
