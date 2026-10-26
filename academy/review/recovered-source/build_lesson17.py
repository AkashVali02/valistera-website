import os,subprocess,ast
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
source=Path('/home/user/premium_full.py').read_text().split('k=Kokoro(')[0]
source=source.replace("B='/home/user/premium_full'","B='/home/user/lesson17'")
source=source.replace("tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2)","tx(d,59,120,'LESSON 1.7  /  TOPIC '+str(idx+1).zfill(2)")
source=source.replace("tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)","tx(d,62,643,'VALISTERA ACADEMY  •  PHARMACEUTICAL QUALITY',15,CYAN,True)")
source=source.replace("excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)","excerpt='';lines(d,62,672,excerpt,94,14,MUT,1)")
source=source.replace("if idx in (0,1,2,3,4,8,9,11):","if idx in (0,1,2,3,4,5,6,7):")
source=source.replace("labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]","labels={0:['DEFINE','IMPLEMENT','REVIEW'],1:['LEADERSHIP','PROCESS','OVERSIGHT'],2:['ASSESS','CONTROL','REVIEW'],3:['RECORD','INVESTIGATE','VERIFY'],4:['PLAN','EVALUATE','APPROVE'],5:['INSTRUCT','RECORD','REVIEW'],6:['ATTRIBUTE','PROTECT','RETRIEVE'],7:['OBSERVE','DOCUMENT','ESCALATE']}[idx]")
exec(compile(source,'lesson17_draw','exec'))
T=['QUALITY CONTROL AND GMP TESTING', 'SPECIFICATIONS AND TEST METHODS', 'SAMPLING AND REPRESENTATIVENESS', 'LABORATORY INSTRUMENT CONTROLS', 'OUT-OF-SPECIFICATION RESULTS', 'LABORATORY DATA INTEGRITY', 'BATCH REVIEW AND RELEASE DECISIONS', 'PRACTICAL OOS SCENARIO']
S=['Quality control helps determine whether materials and products meet approved quality requirements. It includes appropriate sampling, specifications, testing, documentation and review. Quality cannot be assured by final testing alone, so laboratory controls work alongside manufacturing controls. Quality control activities should be independent where required by the applicable quality system and regulations.', 'A specification describes tests, analytical procedures and acceptance criteria for a material or product. Approved methods should be suitable for their intended use, with validation or verification as appropriate. Analysts must use current controlled procedures and suitable reference standards. Results should be compared against the actual approved specification, not an assumed industry-wide number.', 'Sampling plans should consider the material, process, risk and intended test. Samples must be appropriately identified, collected, handled and stored to preserve integrity. A result from a poorly selected or compromised sample may not represent the batch. Sampling procedures and any required environmental controls should be defined and followed. Traceability links each sample to its source and analysis.', 'Laboratory instruments must be suitable for their intended measurements. Qualification, calibration, maintenance and system suitability checks may be needed depending on the equipment and method. Analysts should verify instrument status before use and preserve relevant records. A successful system suitability check does not automatically excuse overdue calibration or missing qualification evidence.', 'An out-of-specification result, often called O O S, occurs when a result falls outside an established acceptance criterion. Such results require timely, documented evaluation under applicable procedures. A laboratory investigation may examine potential analytical errors, while the wider assessment considers manufacturing and product impact where appropriate. Retesting must follow justified approved procedures and must not be used simply to obtain a passing result.', 'Laboratory data must be attributable, legible, contemporaneous, original and accurate, with additional expectations for completeness, consistency, endurance and availability. Electronic raw data, audit trails, calculations and relevant metadata should be controlled according to risk and applicable requirements. Transcribing a final number without retaining required underlying data may undermine traceability and review.', 'Batch disposition decisions rely on more than a passing laboratory result. Authorized personnel should evaluate relevant manufacturing records, deviations, testing results, specifications and other required evidence. Responsibilities and legal release requirements vary by jurisdiction and product. A laboratory analyst should not independently declare a batch releasable merely because a single test passed.', 'Imagine a finished-product assay result outside its approved specification. The analyst should preserve the original data and promptly report the result according to the laboratory procedure. Authorized personnel should conduct an appropriate investigation and assess possible batch impact. The result must not be deleted, averaged away or replaced by an unjustified repeat test. The documented outcome informs the final quality decision.']
topics=[[(h,b)]*3 for h,b in [('TEST AND REVIEW', 'Testing complements process controls'), ('APPROVED LIMITS', 'Use approved specifications and methods'), ('REPRESENTATIVE SAMPLE', 'Trace sample to source and analysis'), ('INSTRUMENT STATUS', 'Check qualification and calibration'), ('INVESTIGATE OOS', 'Investigate before any justified retest'), ('COMPLETE RAW DATA', 'Retain audit trails and original evidence'), ('AUTHORIZED DECISION', 'Review the whole batch quality record'), ('PRESERVE AND ESCALATE', 'Do not discard failing assay results')]]
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
  label(97,281,'QUALITY CONTROL FLOW',20,'#56c8e0')
  for j,t in enumerate(['SAMPLE','ANALYZE','REVIEW']):card(94+j*220,355,188,90,t)
  arrow(286,399,310,399);arrow(506,399,530,399)
  label(105,510,'Testing supports—but does not replace—GMP controls',19)
 elif idx==1:
  label(97,281,'SPECIFICATION CONTROL',19,'#56c8e0')
  for j,t in enumerate(['METHOD','TEST','CRITERIA']):card(95+j*218,345,190,82,t)
  arrow(285,384,313,384);arrow(505,384,531,384)
  card(205,474,406,75,'COMPARE AGAINST APPROVED LIMITS','#d6a454')
 elif idx==2:
  label(97,281,'SAMPLING CHAIN OF CUSTODY',21,'#56c8e0')
  for j,t in enumerate(['IDENTIFY SAMPLE','CONTROL HANDLING','TRACE ANALYSIS']):
   card(103,335+j*84,515,67,t)
  for j in range(3):label(645,349+j*84,'✓',29,'#53c8a3')
 elif idx==3:
  label(97,281,'LAB INSTRUMENT READINESS',20,'#56c8e0')
  for j,(x,t) in enumerate([(110,'CALIBRATION'),(325,'SUITABILITY'),(540,'RECORDS')]):
   d.ellipse((x,360,x+110,470),outline='#56c8e0',width=5)
   label(x+11,395,str(j+1),30,'#eaf3ff');label(x-6,491,t,17)
  arrow(221,415,320,415);arrow(435,415,535,415)
 elif idx==4:
  label(97,281,'DATA INTEGRITY LAYERS',21,'#56c8e0')
  card(278,322,250,67,'RAW DATA')
  card(278,420,250,67,'METADATA')
  card(278,516,250,60,'REVIEW TRAIL')
  d.line((400,389,400,420),fill='#56c8e0',width=4);d.line((400,487,400,516),fill='#56c8e0',width=4)
 elif idx==5:
  label(97,281,'OUT-OF-SPECIFICATION RESPONSE',20,'#56c8e0')
  card(104,347,220,88,'OOS RESULT')
  card(462,347,220,88,'INVESTIGATE')
  arrow(325,392,456,392)
  label(114,490,'Preserve original result and assess potential impact',16)
  label(114,537,'Retest only under justified approved procedure',19,'#f1b767')
 elif idx==6:
  label(97,281,'BATCH DISPOSITION EVIDENCE',20,'#56c8e0')
  for j,t in enumerate(['RECORDS','TESTING','DEVIATIONS','RELEASE']):card(91+j*165,357,151,106,t)
  for j in range(3):arrow(245+j*165,411,255+j*165,411)
  label(105,518,'Authorized review integrates multiple evidence sources',18)
 elif idx==7:
  label(97,281,'FAILED ASSAY: DECISION PATH',19,'#56c8e0')
  for j,t in enumerate(['PRESERVE DATA','REPORT OOS','INVESTIGATE','DECIDE']):
   card(100+j*158,360,146,108,t,'#d6a454' if j==0 else '#56c8e0')
  for j in range(3):arrow(246+j*158,416,257+j*158,416)
  label(106,520,'Never replace a result just to obtain a pass',19,'#f1b767')
 im.save(img)

 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.7;times.append((round(elapsed,2),round(elapsed+dur,2),speech));elapsed+=dur
 out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
Path(f'{B}/concat.txt').write_text(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/lesson17.mp4'],check=True)
import json
Path(f'{B}/timings.json').write_text(json.dumps(times))
print('DONE',round(elapsed,1),flush=True)
