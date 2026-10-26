from pathlib import Path
s=Path('/home/user/build_lesson19.py').read_text().replace('lesson19','lesson110').replace('LESSON 1.9','LESSON 1.10')
a=s.index('T=[');b=s.index('topics=',a)
replacement='''T=['WHY SELF-INSPECTION MATTERS','PLANNING A RISK-BASED SELF-INSPECTION','PREPARING OBJECTIVE EVIDENCE','CONDUCTING THE INSPECTION','DOCUMENTING FINDINGS AND RISK','CORRECTIVE ACTION AND FOLLOW-UP','AUDIT READINESS AND QUALITY CULTURE','PRACTICAL AUDIT READINESS SCENARIO']
S=[
'Self-inspection is a systematic internal review of whether pharmaceutical operations follow Good Manufacturing Practice and the company quality system. It helps identify weaknesses before they affect patients or product quality. A self-inspection program should cover relevant people, premises, equipment, operations and records. The purpose is to find and correct genuine problems, not simply to produce a favorable score.',
'A useful self-inspection program defines scope, responsibilities, frequency and follow-up. Planning can consider process criticality, past deviations, previous findings and changes. Inspectors should be sufficiently knowledgeable and objective for the activity. Risk-based prioritization helps allocate attention, but it does not justify omitting required GMP controls. The plan should be documented under the site quality system.',
'Before an inspection, identify the approved procedures and records relevant to the selected area. Examples may include training records, equipment logs, cleaning records, deviations, change controls and qualification status. Inspectors should check the current approved version and whether records reflect actual work. A tidy folder alone does not demonstrate that an operation is controlled. Evidence must be reliable and traceable.',
'During the inspection, observe work, interview personnel and compare actual practices with approved requirements. Follow the process from material or personnel entry through operations and recording. Ask neutral questions and document facts, not assumptions. When a possible issue is found, capture enough objective evidence to allow fair assessment. Escalate any immediate product quality or patient safety concern through the site procedure.',
'Inspection findings should clearly describe the observed condition, applicable requirement or procedure, and supporting evidence. The organization should assess the significance and potential product impact of each finding. Classification terminology varies between quality systems and authorities; do not assign a universal severity label without an applicable framework. Reports should distinguish verified observations from recommendations and should assign accountable follow-up.',
'Appropriate corrective action should address the causes of confirmed deficiencies, not just the visible symptom. Action plans need responsible owners and justified timelines. Some issues require investigation, product impact assessment, preventive measures or training. Follow-up should verify implementation and, where appropriate, effectiveness. Closing a finding solely because a document was signed does not prove that the underlying problem is resolved.',
'Inspection readiness is sustained through routine GMP compliance, not a last-minute cleanup before an audit. Current procedures, complete records, trained personnel and equipment status controls help teams explain and demonstrate their processes. Management review and trend analysis can reveal recurring weaknesses. Personnel should answer accurately, acknowledge uncertainty and retrieve evidence through approved systems. Never fabricate or backdate records to satisfy an inspector.',
'Consider an internal inspection of a sterile manufacturing support area. An inspector notices that an equipment calibration label is expired while a nearby logbook is incomplete. The team should secure the equipment as required, verify the actual calibration and use status, and assess potential impact on operations or product quality. The observation and decisions should be documented and escalated. A new label alone is not an adequate corrective action without confirming the underlying status.'
]
'''
s=s[:a]+replacement+s[b:]
a=s.index(' # Replace the generic left text panel');b=s.index('\n audio,sr=',a)
visual=''' # The complete teaching diagram is visible from the first narrated frame.
 from PIL import Image,ImageDraw,ImageFont
 im=Image.open(img);d=ImageDraw.Draw(im)
 d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
 def label(x,y,t,size=19,color='#eaf3ff'):
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',size)
  d.text((x,y),t,font=font,fill=color)
 def card(x,y,t,color='#56c8e0'):
  d.rounded_rectangle((x,y,x+192,y+93),radius=12,fill='#1d4160',outline=color,width=2)
  label(x+12,y+33,t,15)
 def arrow(x,y):
  d.line((x,y,x+27,y),fill='#56c8e0',width=4)
  d.polygon([(x+27,y),(x+16,y-7),(x+16,y+7)],fill='#56c8e0')
 titles=['INTERNAL GMP OVERSIGHT','RISK-BASED INSPECTION PLAN','PREPARE TRACEABLE EVIDENCE','OBSERVE, ASK, VERIFY','FACT-BASED FINDING REPORT','CAPA AND EFFECTIVENESS','SUSTAIN DAILY READINESS','EXPIRED STATUS: INVESTIGATE']
 steps=[['REVIEW','IDENTIFY','IMPROVE'],['SCOPE','PRIORITIZE','ASSIGN'],['PROCEDURES','RECORDS','STATUS'],['OBSERVE','INTERVIEW','DOCUMENT'],['FACTS','IMPACT','FOLLOW-UP'],['CAUSE','ACTION','VERIFY'],['TRAIN','RECORD','REVIEW'],['SECURE','ASSESS','RESOLVE']]
 notes=['Identify gaps before quality is affected','Define scope, frequency and objectivity','Records must reflect real operations','Document evidence, not assumptions','Separate verified findings from advice','Verify actions and their effectiveness','Readiness is continuous, not cosmetic','Replacing a label alone is not enough']
 label(94,285,titles[idx],18,'#56c8e0')
 for j,t in enumerate(steps[idx]):card(91+j*220,355,t,'#f1b767' if idx==7 and j==0 else '#56c8e0')
 arrow(284,402);arrow(504,402)
 label(98,522,notes[idx],16,'#eaf3ff')
 im.save(img)
'''
s=s[:a]+visual+s[b:]
Path('/home/user/build_lesson110.py').write_text(s)
