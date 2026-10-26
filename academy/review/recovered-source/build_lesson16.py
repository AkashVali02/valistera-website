import os,subprocess,ast
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
source=Path('/home/user/premium_full.py').read_text().split('k=Kokoro(')[0]
source=source.replace("B='/home/user/premium_full'","B='/home/user/lesson16'")
source=source.replace("tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2)","tx(d,59,120,'LESSON 1.6  /  TOPIC '+str(idx+1).zfill(2)")
source=source.replace("tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)","tx(d,62,643,'VALISTERA ACADEMY  •  PHARMACEUTICAL QUALITY',15,CYAN,True)")
source=source.replace("excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)","excerpt='';lines(d,62,672,excerpt,94,14,MUT,1)")
source=source.replace("if idx in (0,1,2,3,4,8,9,11):","if idx in (0,1,2,3,4,5,6,7):")
source=source.replace("labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]","labels={0:['DEFINE','IMPLEMENT','REVIEW'],1:['LEADERSHIP','PROCESS','OVERSIGHT'],2:['ASSESS','CONTROL','REVIEW'],3:['RECORD','INVESTIGATE','VERIFY'],4:['PLAN','EVALUATE','APPROVE'],5:['INSTRUCT','RECORD','REVIEW'],6:['ATTRIBUTE','PROTECT','RETRIEVE'],7:['OBSERVE','DOCUMENT','ESCALATE']}[idx]")
exec(compile(source,'lesson16_draw','exec'))
T=['PACKAGING AND LABELLING GMP', 'PRINTED MATERIAL CONTROL', 'LINE CLEARANCE BEFORE PACKAGING', 'IN-PROCESS PACKAGING CHECKS', 'SERIALIZATION AND TRACEABILITY', 'RECONCILIATION AND DISCREPANCIES', 'MIX-UP PREVENTION CONTROL STRATEGY', 'PRACTICAL WRONG-LABEL SCENARIO']
S=['Packaging and labelling operations require particular attention because a correct medicine in the wrong pack or with the wrong label can put patients at risk. Controls should protect product identity, strength, batch information and instructions. This lesson uses diagrams to illustrate material flow, checks and decisions. Specific packaging controls depend on the product, market and approved procedures.', 'Printed packaging materials should be approved, identified, stored and issued under appropriate controls. Different products, strengths and markets may have similar-looking artwork. Controlled issuance and secure storage reduce the chance of a mix-up. Obsolete or superseded printed components must be prevented from unintended use. Reconciliation and destruction practices should follow approved site procedures.', 'Before starting a packaging batch, line clearance helps verify that unrelated product, printed components, labels and documents from previous operations are removed or appropriately controlled. Equipment and area status should be confirmed. The line-clearance procedure should define responsibilities and records. A completed checklist is meaningful only when the physical checks were actually performed.', 'During packaging, checks may verify the correct product, printed component, batch number, expiry information, readability and packaging integrity. The appropriate checks, frequency and acceptance criteria must be defined by the approved process. Camera inspection or barcode verification may provide additional controls, but automated systems still require suitable qualification, maintenance and oversight.', 'Serialization can assign a unique identifier to saleable packs where required by the applicable market. Aggregation may associate packs with cartons and shippers. These systems support traceability and verification but do not replace basic GMP controls. Regulatory requirements vary by jurisdiction and product, so the site must follow the relevant market-specific rules and validated system design.', 'Packaging reconciliation compares quantities issued, used, rejected, returned and otherwise accounted for. Unexplained discrepancies, particularly involving printed materials or finished packs, should be investigated according to approved procedures. Reconciliation tolerances, if applicable, must be scientifically and procedurally justified. The illustrative diagram here shows relationships, not real batch data or acceptance limits.', 'Mix-up prevention is strongest when multiple controls work together. These can include physical segregation, material identification, approved artwork, line clearance, in-process checks, barcode systems and independent review. Each layer reduces a different failure opportunity. A single final inspection is not an adequate substitute for controlling risks throughout packaging operations.', 'Imagine that an operator notices a carton printed for a different strength at the packaging line. The operator should secure the operation and report the finding under site procedures. Authorized personnel should assess the extent of possible mix-up, affected materials and batches, and any required investigation. Packaging should resume only after the issue is appropriately resolved and documented. The goal is to protect patient safety and preserve traceability.']
topics=[[(h,b)]*3 for h,b in [('IDENTITY AND SAFETY', 'Correct medicine, pack and label'), ('ARTWORK CONTROL', 'Approve, issue, control and reconcile'), ('CLEARANCE', 'Remove prior materials before start'), ('VERIFY IN PROCESS', 'Check identity, print and integrity'), ('PACK TRACEABILITY', 'Market-specific serialization controls'), ('MATERIAL BALANCE', 'Account for printed materials and packs'), ('LAYERED CONTROLS', 'Prevent errors at multiple stages'), ('STOP AND ESCALATE', 'Wrong-strength carton requires assessment')]]
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
  label(97,281,'PACK IDENTITY CHAIN',20,'#56c8e0')
  for j,t in enumerate(['PRODUCT','CARTON','LABEL']):card(94+j*220,355,188,90,t)
  arrow(286,399,310,399);arrow(506,399,530,399)
  label(105,510,'A mismatch anywhere can affect patient safety',19)
 elif idx==1:
  label(97,281,'CONTROLLED PRINTED MATERIAL LIFECYCLE',19,'#56c8e0')
  for j,t in enumerate(['APPROVE','ISSUE','RECONCILE']):card(95+j*218,345,190,82,t)
  arrow(285,384,313,384);arrow(505,384,531,384)
  card(205,474,406,75,'OBSOLETE ARTWORK: SEGREGATE','#d6a454')
 elif idx==2:
  label(97,281,'PRE-START LINE CLEARANCE',21,'#56c8e0')
  for j,t in enumerate(['REMOVE OLD MATERIAL','VERIFY EQUIPMENT','RECORD CHECK']):
   card(103,335+j*84,515,67,t)
  for j in range(3):label(645,349+j*84,'✓',29,'#53c8a3')
 elif idx==3:
  label(97,281,'IN-PROCESS VERIFICATION POINTS',20,'#56c8e0')
  for j,(x,t) in enumerate([(110,'IDENTITY'),(325,'PRINT'),(540,'INTEGRITY')]):
   d.ellipse((x,360,x+110,470),outline='#56c8e0',width=5)
   label(x+11,395,str(j+1),30,'#eaf3ff');label(x-6,491,t,17)
  arrow(221,415,320,415);arrow(435,415,535,415)
 elif idx==4:
  label(97,281,'ILLUSTRATIVE PACK HIERARCHY',21,'#56c8e0')
  card(278,322,250,67,'SHIPPER')
  card(278,420,250,67,'CARTON')
  card(278,516,250,60,'SALEABLE PACK')
  d.line((400,389,400,420),fill='#56c8e0',width=4);d.line((400,487,400,516),fill='#56c8e0',width=4)
 elif idx==5:
  label(97,281,'ILLUSTRATIVE RECONCILIATION',20,'#56c8e0')
  card(104,347,220,88,'ISSUED')
  card(462,347,220,88,'ACCOUNTED')
  arrow(325,392,456,392)
  label(114,490,'Used + rejected + returned + other documented disposition',16)
  label(114,537,'Unexplained differences → investigate',19,'#f1b767')
 elif idx==6:
  label(97,281,'MULTIPLE BARRIERS AGAINST MIX-UPS',20,'#56c8e0')
  for j,t in enumerate(['SEGREGATE','IDENTIFY','VERIFY','REVIEW']):card(91+j*165,357,151,106,t)
  for j in range(3):arrow(245+j*165,411,255+j*165,411)
  label(105,518,'Layered controls reduce opportunities for error',18)
 elif idx==7:
  label(97,281,'WRONG-STRENGTH CARTON: DECISION PATH',19,'#56c8e0')
  for j,t in enumerate(['STOP / SECURE','REPORT','ASSESS IMPACT','AUTHORIZE RESUME']):
   card(100+j*158,360,146,108,t,'#d6a454' if j==0 else '#56c8e0')
  for j in range(3):arrow(246+j*158,416,257+j*158,416)
  label(106,520,'Do not silently discard the evidence',19,'#f1b767')
 im.save(img)

 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.7;times.append((round(elapsed,2),round(elapsed+dur,2),speech));elapsed+=dur
 out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
Path(f'{B}/concat.txt').write_text(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/lesson16.mp4'],check=True)
import json
Path(f'{B}/timings.json').write_text(json.dumps(times))
print('DONE',round(elapsed,1),flush=True)
