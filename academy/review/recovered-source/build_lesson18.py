import os,subprocess,ast
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
source=Path('/home/user/premium_full.py').read_text().split('k=Kokoro(')[0]
source=source.replace("B='/home/user/premium_full'","B='/home/user/lesson18'")
source=source.replace("tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2)","tx(d,59,120,'LESSON 1.8  /  TOPIC '+str(idx+1).zfill(2)")
source=source.replace("tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)","tx(d,62,643,'VALISTERA ACADEMY  •  PHARMACEUTICAL QUALITY',15,CYAN,True)")
source=source.replace("excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)","excerpt='';lines(d,62,672,excerpt,94,14,MUT,1)")
source=source.replace("if idx in (0,1,2,3,4,8,9,11):","if idx in (0,1,2,3,4,5,6,7):")
source=source.replace("labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]","labels={0:['DEFINE','IMPLEMENT','REVIEW'],1:['LEADERSHIP','PROCESS','OVERSIGHT'],2:['ASSESS','CONTROL','REVIEW'],3:['RECORD','PREVENT','VERIFY'],4:['PLAN','EVALUATE','APPROVE'],5:['INSTRUCT','RECORD','REVIEW'],6:['ATTRIBUTE','PROTECT','RETRIEVE'],7:['OBSERVE','DOCUMENT','ESCALATE']}[idx]")
exec(compile(source,'lesson18_draw','exec'))
T=['GMP DEVIATIONS AND CAPA', 'DETECT AND CONTAIN', 'DOCUMENT AND CLASSIFY', 'PREVENT ROOT CAUSE', 'ASSESS PRODUCT IMPACT', 'CORRECTIVE AND PREVENTIVE ACTIONS', 'EFFECTIVENESS AND QUALITY TRENDS', 'PRACTICAL DEVIATION SCENARIO']
S=['Deviations are departures from approved procedures, established processes or expected conditions. A robust pharmaceutical quality system encourages prompt reporting and proportionate investigation. The purpose is to understand what happened, assess potential product impact and prevent recurrence. Corrective and preventive action, or C A P A, is one possible output of a documented investigation.', 'When an unexpected event is detected, personnel should first protect people, product and evidence as appropriate to the situation. This may require stopping an activity, segregating affected materials or placing a batch on hold under approved procedures. Immediate containment controls the potential consequences while the quality assessment continues. Personnel must not silently correct or conceal an event.', 'Deviation records should capture what happened, when and where it occurred, the affected equipment or materials, and the immediate actions taken. Classification and investigation depth should reflect risk, potential impact and site procedures. Records should distinguish observed facts from assumptions. Clear contemporaneous documentation supports reliable evaluation and later review.', 'Root cause investigation seeks to explain why a deviation occurred, not simply identify who was present. Teams may use a timeline, process mapping, the five whys or a cause-and-effect diagram when suitable. Potential causes should be tested against available evidence. Human error alone is rarely an adequate explanation if procedure design, training, equipment or working conditions contributed.', 'Product impact assessment considers the affected materials, batches, processes, time window and available supporting data. The assessment should be scientifically justified and documented by authorized personnel. It may require additional investigation or testing, but testing alone cannot always establish that a process deviation had no impact. Final disposition follows applicable procedures and regulatory requirements.', 'A correction addresses an identified problem, while a corrective action aims to remove its cause and prevent recurrence. Preventive actions may address potential problems before they occur. Actions should have clear ownership, due dates and documented implementation. Retraining may be appropriate in some cases, but should not be the default response without understanding the underlying cause.', 'CAPA effectiveness should be evaluated using measures suited to the identified cause and risk. Examples include observing process performance, reviewing repeat events or verifying that a new control works as intended. Trend analysis can identify recurring deviations that individual investigations miss. An action should not be declared effective solely because it was completed on schedule.', 'Imagine a filling-line differential pressure alarm that occurred during production and was not promptly documented. The event should be reported, relevant records preserved and the affected period assessed. Authorized personnel should investigate the alarm, the response and potential product impact. CAPA, if needed, should address the demonstrated causes, with effectiveness checks. A return to normal pressure does not erase the original deviation.']
topics=[[(h,b)]*3 for h,b in [('EVENT TO LEARNING', 'Detect, investigate and prevent recurrence'), ('CONTAIN THE RISK', 'Protect people, product and evidence'), ('RECORD THE FACTS', 'Document time, place, scope and actions'), ('TEST POSSIBLE CAUSES', 'Evidence-based root cause investigation'), ('SCIENTIFIC ASSESSMENT', 'Evaluate affected batches and process'), ('REMOVE THE CAUSE', 'Correction versus sustainable CAPA'), ('VERIFY EFFECTIVENESS', 'Check whether controls really work'), ('ESCALATE THE ALARM', 'Pressure alarm requires impact review')]]
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
  label(97,281,'DEVIATION MANAGEMENT FLOW',20,'#56c8e0')
  for j,t in enumerate(['DETECT','ASSESS','PREVENT']):card(94+j*220,355,188,90,t)
  arrow(286,399,310,399);arrow(506,399,530,399)
  label(105,510,'Learning from events strengthens process control',19)
 elif idx==1:
  label(97,281,'IMMEDIATE CONTAINMENT',19,'#56c8e0')
  for j,t in enumerate(['STOP','SEGREGATE','PRESERVE']):card(95+j*218,345,190,82,t)
  arrow(285,384,313,384);arrow(505,384,531,384)
  card(205,474,406,75,'REPORT UNDER SITE PROCEDURES','#d6a454')
 elif idx==2:
  label(97,281,'DEVIATION RECORD',21,'#56c8e0')
  for j,t in enumerate(['WHAT / WHEN / WHERE','AFFECTED MATERIAL','IMMEDIATE ACTION']):
   card(103,335+j*84,515,67,t)
  for j in range(3):label(645,349+j*84,'✓',29,'#53c8a3')
 elif idx==3:
  label(97,281,'ROOT CAUSE INVESTIGATION',20,'#56c8e0')
  for j,(x,t) in enumerate([(110,'PEOPLE'),(325,'PROCESS'),(540,'EQUIPMENT')]):
   d.ellipse((x,360,x+110,470),outline='#56c8e0',width=5)
   label(x+11,395,str(j+1),30,'#eaf3ff');label(x-6,491,t,17)
  arrow(221,415,320,415);arrow(435,415,535,415)
 elif idx==4:
  label(97,281,'PRODUCT IMPACT REVIEW',21,'#56c8e0')
  card(278,322,250,67,'BATCH SCOPE')
  card(278,420,250,67,'RISK EVIDENCE')
  card(278,516,250,60,'DISPOSITION')
  d.line((400,389,400,420),fill='#56c8e0',width=4);d.line((400,487,400,516),fill='#56c8e0',width=4)
 elif idx==5:
  label(97,281,'CAPA ACTION PATH',20,'#56c8e0')
  card(104,347,220,88,'CORRECTION')
  card(462,347,220,88,'PREVENT')
  arrow(325,392,456,392)
  label(114,490,'Implement actions against demonstrated causes',16)
  label(114,537,'Assign owners and verify implementation',19,'#f1b767')
 elif idx==6:
  label(97,281,'EFFECTIVENESS CHECKS',20,'#56c8e0')
  for j,t in enumerate(['IMPLEMENT','MONITOR','TREND','VERIFY']):card(91+j*165,357,151,106,t)
  for j in range(3):arrow(245+j*165,411,255+j*165,411)
  label(105,518,'Closure requires evidence that controls work',18)
 elif idx==7:
  label(97,281,'PRESSURE ALARM: DECISION PATH',19,'#56c8e0')
  for j,t in enumerate(['PRESERVE DATA','REPORT OOS','PREVENT','DECIDE']):
   card(100+j*158,360,146,108,t,'#d6a454' if j==0 else '#56c8e0')
  for j in range(3):arrow(246+j*158,416,257+j*158,416)
  label(106,520,'A return to normal does not erase the event',19,'#f1b767')
 im.save(img)

 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.7;times.append((round(elapsed,2),round(elapsed+dur,2),speech));elapsed+=dur
 out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
Path(f'{B}/concat.txt').write_text(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/lesson18.mp4'],check=True)
import json
Path(f'{B}/timings.json').write_text(json.dumps(times))
print('DONE',round(elapsed,1),flush=True)
