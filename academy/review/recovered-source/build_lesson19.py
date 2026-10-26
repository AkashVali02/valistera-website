import os,subprocess,ast
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
source=Path('/home/user/premium_full.py').read_text().split('k=Kokoro(')[0]
source=source.replace("B='/home/user/premium_full'","B='/home/user/lesson19'")
source=source.replace("tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2)","tx(d,59,120,'LESSON 1.9  /  TOPIC '+str(idx+1).zfill(2)")
source=source.replace("tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)","tx(d,62,643,'VALISTERA ACADEMY  •  PHARMACEUTICAL QUALITY',15,CYAN,True)")
source=source.replace("excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)","excerpt='';lines(d,62,672,excerpt,94,14,MUT,1)")
source=source.replace("if idx in (0,1,2,3,4,8,9,11):","if idx in (0,1,2,3,4,5,6,7):")
source=source.replace("labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]","labels={0:['DEFINE','IMPLEMENT','REVIEW'],1:['LEADERSHIP','PROCESS','OVERSIGHT'],2:['ASSESS','CONTROL','REVIEW'],3:['RECORD','INVESTIGATE','VERIFY'],4:['PLAN','EVALUATE','APPROVE'],5:['INSTRUCT','RECORD','REVIEW'],6:['ATTRIBUTE','PROTECT','RETRIEVE'],7:['OBSERVE','DOCUMENT','ESCALATE']}[idx]")
exec(compile(source,'lesson19_draw','exec'))
T=['GMP CHANGE CONTROL', 'IDENTIFY AND PROPOSE CHANGE', 'ASSESS QUALITY AND REGULATORY IMPACT', 'RISK ASSESSMENT AND PLANNING', 'APPROVAL BEFORE IMPLEMENTATION', 'EXECUTION AND VERIFICATION', 'POST-IMPLEMENTATION REVIEW', 'PRACTICAL HVAC CHANGE SCENARIO']
S=['Change control is a structured quality system process for evaluating proposed changes before they affect pharmaceutical operations. Changes may involve equipment, facilities, utilities, processes, methods, materials or computerized systems. The goal is to maintain a controlled state and avoid unintended effects on product quality. The appropriate scope of review depends on risk, intended use and applicable regulatory commitments.', 'A change request should clearly describe the current state, proposed state, rationale and affected systems. Examples include replacing a critical sensor, revising a cleaning procedure or changing an equipment component. The request should identify relevant documents, equipment and product families. Clear scope helps reviewers recognize dependencies before implementation rather than discovering them after the change.', 'Quality impact assessment considers whether a change could affect identity, strength, purity, safety or other critical quality attributes. The review may need input from quality, engineering, manufacturing, validation, regulatory affairs and other functions. Regulatory submission or notification implications depend on the market, product and type of change. A technically small modification can still have important quality consequences.', 'Risk assessment considers credible failure modes, existing controls and the uncertainty associated with the proposed change. It can help determine required qualification, validation, testing, training and monitoring activities. Risk tools should support scientific decision-making, not replace it. Acceptance criteria and verification plans must be appropriate to the actual system, product and process.', 'Implementation should proceed through the authorization steps established in the site change control procedure. Relevant prerequisites may include approved specifications, impact assessments, plans, procurement controls and training. Emergency changes may require a defined expedited process, but urgency does not remove the need for documented quality oversight. Unapproved informal modifications can compromise the validated state.', 'After authorization, the change should be executed according to the approved plan. Verification may include installation checks, functional testing, qualification, process validation or document updates depending on impact. Any departures should be evaluated and recorded. The evidence should demonstrate that required activities were completed and that affected systems remain suitable for their intended use.', 'Closing a change requires appropriate review of implementation evidence, open actions and residual risks. Some changes may require enhanced monitoring or effectiveness checks after implementation. The site should update procedures, drawings, training and other controlled records as needed. A change should not be considered complete simply because the new hardware or software has been installed.', 'Consider a proposed replacement of a differential pressure transmitter serving a critical pharmaceutical manufacturing area. The team should evaluate instrument range, accuracy, location, alarms, monitoring records and potential effects on environmental control. An approved plan may require calibration, functional verification, documentation updates and impact assessment of affected operations. The exact checks depend on the system and its qualified state.']
topics=[[(h,b)]*3 for h,b in [('CONTROLLED LIFECYCLE', 'Propose, assess, approve, execute, close'), ('DEFINE SCOPE', 'Describe current and proposed state'), ('MULTIDISCIPLINARY REVIEW', 'Quality, validation and regulatory impacts'), ('RISK-BASED PLAN', 'Define proportionate verification activities'), ('AUTHORIZE FIRST', 'Document approvals and prerequisites'), ('VERIFY IMPLEMENTATION', 'Test affected functions and update records'), ('CLOSE WITH EVIDENCE', 'Review evidence and residual actions'), ('TRANSMITTER REPLACEMENT', 'Check calibration, alarms and impact')]]
scenes=[(i,0,T[i],S[i]) for i in range(len(T))]
k=Kokoro('/home/user/kokoro-v1.0.onnx','/home/user/voices-v1.0.bin')
parts=[];times=[];elapsed=0
for number,(idx,part,title,speech) in enumerate(scenes,1):
 print('SCENE',number,flush=True)
 img=draw(idx,part,title,speech,number)
 # Replace the generic left text panel with purpose-built diagrams and illustrated flows.
 from PIL import Image,ImageDraw
 im=Image.open(img);d=ImageDraw.Draw(im)
 d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
 def label(x,y,text,sz=18,color='#eaf3ff'):
  tx(d,x,y,text,sz,color,True)
 def card(x,y,w,h,text,accent='#42bfd9'):
  d.rounded_rectangle((x,y,x+w,y+h),radius=13,fill='#1d4160',outline=accent,width=2)
  label(x+15,y+h//2-12,text,18)
 def arrow(x1,y1,x2,y2):
  d.line((x1,y1,x2,y2),fill='#56c8e0',width=5)
  d.polygon([(x2,y2),(x2-12,y2-7),(x2-12,y2+7)],fill='#56c8e0')
 if idx==0:
  label(97,281,'CHANGE CONTROL LIFECYCLE',20,'#56c8e0')
  for j,t in enumerate(['PROPOSE','ASSESS','CLOSE']):card(94+j*220,355,188,90,t)
  arrow(286,399,310,399);arrow(506,399,530,399)
  label(105,510,'Evaluate change before affecting GMP operations',19)
 elif idx==1:
  label(97,281,'CHANGE REQUEST SCOPE',19,'#56c8e0')
  for j,t in enumerate(['CURRENT','PROPOSED','RATIONALE']):card(95+j*218,345,190,82,t)
  arrow(285,384,313,384);arrow(505,384,531,384)
  card(205,474,406,75,'IDENTIFY AFFECTED SYSTEMS','#d6a454')
 elif idx==2:
  label(97,281,'IMPACT ASSESSMENT',21,'#56c8e0')
  for j,t in enumerate(['PRODUCT QUALITY','VALIDATION STATE','REGULATORY STATUS']):
   card(103,335+j*84,515,67,t)
  for j in range(3):label(645,349+j*84,'✓',29,'#53c8a3')
 elif idx==3:
  label(97,281,'RISK-BASED VERIFICATION',20,'#56c8e0')
  for j,(x,t) in enumerate([(110,'FAILURE'),(325,'CONTROL'),(540,'VERIFY')]):
   d.ellipse((x,360,x+110,470),outline='#56c8e0',width=5)
   label(x+11,395,str(j+1),30,'#eaf3ff');label(x-6,491,t,17)
  arrow(221,415,320,415);arrow(435,415,535,415)
 elif idx==4:
  label(97,281,'APPROVAL GATES',21,'#56c8e0')
  card(278,322,250,67,'ASSESSMENT')
  card(278,420,250,67,'AUTHORIZATION')
  card(278,516,250,60,'EXECUTION')
  d.line((400,389,400,420),fill='#56c8e0',width=4);d.line((400,487,400,516),fill='#56c8e0',width=4)
 elif idx==5:
  label(97,281,'IMPLEMENTATION EVIDENCE',20,'#56c8e0')
  card(104,347,220,88,'EXECUTE')
  card(462,347,220,88,'VERIFY')
  arrow(325,392,456,392)
  label(114,490,'Complete qualification and updates as needed',16)
  label(114,537,'Document evidence and deviations',19,'#f1b767')
 elif idx==6:
  label(97,281,'CHANGE CLOSURE',20,'#56c8e0')
  for j,t in enumerate(['RECORDS','TRAINING','MONITOR','CLOSE']):card(91+j*165,357,151,106,t)
  for j in range(3):arrow(245+j*165,411,255+j*165,411)
  label(105,518,'Review actions, evidence and residual risk',18)
 elif idx==7:
  label(97,281,'HVAC SENSOR CHANGE PATH',19,'#56c8e0')
  for j,t in enumerate(['PRESERVE DATA','REPORT OOS','VERIFY','DECIDE']):
   card(100+j*158,360,146,108,t,'#d6a454' if j==0 else '#56c8e0')
  for j in range(3):arrow(246+j*158,416,257+j*158,416)
  label(106,520,'Replacement must maintain qualified function',19,'#f1b767')
 im.save(img)

 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.7;times.append((round(elapsed,2),round(elapsed+dur,2),speech));elapsed+=dur
 out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
Path(f'{B}/concat.txt').write_text(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/lesson19.mp4'],check=True)
import json
Path(f'{B}/timings.json').write_text(json.dumps(times))
print('DONE',round(elapsed,1),flush=True)
