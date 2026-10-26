import os,subprocess,ast
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
source=Path('/home/user/premium_full.py').read_text().split('k=Kokoro(')[0]
source=source.replace("B='/home/user/premium_full'","B='/home/user/lesson110'")
source=source.replace("tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2)","tx(d,59,120,'LESSON 1.10  /  TOPIC '+str(idx+1).zfill(2)")
source=source.replace("tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)","tx(d,62,643,'VALISTERA ACADEMY  •  PHARMACEUTICAL QUALITY',15,CYAN,True)")
source=source.replace("excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)","excerpt='';lines(d,62,672,excerpt,94,14,MUT,1)")
source=source.replace("if idx in (0,1,2,3,4,8,9,11):","if idx in (0,1,2,3,4,5,6,7):")
source=source.replace("labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]","labels={0:['DEFINE','IMPLEMENT','REVIEW'],1:['LEADERSHIP','PROCESS','OVERSIGHT'],2:['ASSESS','CONTROL','REVIEW'],3:['RECORD','INVESTIGATE','VERIFY'],4:['PLAN','EVALUATE','APPROVE'],5:['INSTRUCT','RECORD','REVIEW'],6:['ATTRIBUTE','PROTECT','RETRIEVE'],7:['OBSERVE','DOCUMENT','ESCALATE']}[idx]")
exec(compile(source,'lesson110_draw','exec'))
T=['WHY SELF-INSPECTION MATTERS','PLANNING A RISK-BASED SELF-INSPECTION','PREPARING OBJECTIVE EVIDENCE','CONDUCTING THE INSPECTION','DOCUMENTING FINDINGS AND RISK','CORRECTIVE ACTION AND FOLLOW-UP','AUDIT READINESS AND QUALITY CULTURE','PRACTICAL AUDIT READINESS SCENARIO']
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
topics=[[(h,b)]*3 for h,b in [('CONTROLLED LIFECYCLE', 'Propose, assess, approve, execute, close'), ('DEFINE SCOPE', 'Describe current and proposed state'), ('MULTIDISCIPLINARY REVIEW', 'Quality, validation and regulatory impacts'), ('RISK-BASED PLAN', 'Define proportionate verification activities'), ('AUTHORIZE FIRST', 'Document approvals and prerequisites'), ('VERIFY IMPLEMENTATION', 'Test affected functions and update records'), ('CLOSE WITH EVIDENCE', 'Review evidence and residual actions'), ('TRANSMITTER REPLACEMENT', 'Check calibration, alarms and impact')]]
scenes=[(i,0,T[i],S[i]) for i in range(len(T))]
k=Kokoro('/home/user/kokoro-v1.0.onnx','/home/user/voices-v1.0.bin')
parts=[];times=[];elapsed=0
for number,(idx,part,title,speech) in enumerate(scenes,1):
 print('SCENE',number,flush=True)
 img=draw(idx,part,title,speech,number)
 # The complete teaching diagram is visible from the first narrated frame.
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

 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.7;times.append((round(elapsed,2),round(elapsed+dur,2),speech));elapsed+=dur
 out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
Path(f'{B}/concat.txt').write_text(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/lesson110.mp4'],check=True)
import json
Path(f'{B}/timings.json').write_text(json.dumps(times))
print('DONE',round(elapsed,1),flush=True)
