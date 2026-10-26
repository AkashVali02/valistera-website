from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
B=Path('/home/user/lesson15');times=json.loads((B/'timings.json').read_text());F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=ImageFont.truetype(F,17);small=ImageFont.truetype(F,14)
for idx,(start,end,_) in enumerate(times,1):
 im=Image.open(B/f'scene_{idx:02}.png').convert('RGB');d=ImageDraw.Draw(im)
 d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
 def text(x,y,t,c='#eaf3ff',sm=False):d.text((x,y),t,font=small if sm else font,fill=c)
 def card(x,y,w,h,t,c='#56c8e0'):
  d.rounded_rectangle((x,y,x+w,y+h),radius=13,fill='#1d4160',outline=c,width=2)
  text(x+13,y+h//2-10,t)
 def arrow(x,y,x2,y2):
  d.line((x,y,x2,y2),fill='#56c8e0',width=4);d.polygon(((x2,y2),(x2-10,y2-6),(x2-10,y2+6)),fill='#56c8e0')
 headings=['CONTROLLED MANUFACTURING','MATERIAL STATUS DECISION','DISPENSING TRACEABILITY','PRE-START LINE CLEARANCE','IN-PROCESS CONTROL LOOP','BATCH RECORD EVIDENCE','DEVIATION RESPONSE','CONFLICTING STATUS: DO NOT USE']
 text(95,283,headings[idx-1],'#56c8e0')
 if idx in (1,3,4,6,7):
  vals={1:['INSTRUCTIONS','EXECUTION','REVIEW'],3:['MATERIAL','MEASURE','RECORD'],4:['CLEAR AREA','CHECK SETUP','AUTHORIZE'],6:['OPERATIONS','IPC DATA','RECONCILE'],7:['SECURE','REPORT','ASSESS']}[idx]
  for j,t in enumerate(vals):card(92+j*219,352,190,95,t)
  arrow(283,400,310,400);arrow(502,400,530,400)
  subtitles={1:'Approved procedures + trained personnel',3:'Link source material to batch and quantity',4:'Remove prior materials and verify readiness',6:'Record actual activities and investigate gaps',7:'Preserve evidence; evaluate product impact'}
  text(104,510,subtitles[idx],sm=True)
 elif idx==2:
  for j,t in enumerate(['QUARANTINE','RELEASED','REJECTED']):card(105,336+j*80,500,63,t,'#e3b26b' if j!=1 else '#53c8a3')
  text(107,575,'Check records, not only container labels',sm=True)
 elif idx==5:
  card(97,343,205,87,'MEASURE');card(506,343,205,87,'COMPARE');arrow(305,386,503,386)
  card(268,481,270,74,'RESPOND / RECORD','#e3b26b')
  text(101,574,'Limits and frequency come from approved process',sm=True)
 else:
  card(99,337,267,88,'LABEL: RELEASED','#e3b26b');card(443,337,267,88,'SYSTEM: HOLD','#e3b26b')
  card(229,471,360,78,'HOLD AND ESCALATE','#f1b767')
  text(110,569,'Authorized review must resolve discrepancy',sm=True)
 im.save(B/f'diagram_{idx:02}.png')
 duration=end-start
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','8','-i',str(B/f'diagram_{idx:02}.png'),'-i',str(B/f'audio_{idx:02}.wav'),'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',str(B/f'diagram_part_{idx:02}.mp4')],check=True)
 print('SCENE',idx,flush=True)
with open(B/'diagram_concat.txt','w') as f:
 for idx in range(1,9):f.write(f"file '{B}/diagram_part_{idx:02}.mp4'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(B/'diagram_concat.txt'),'-c','copy','-movflags','+faststart',str(B/'lesson15_diagrams.mp4')],check=True)
print('DONE',flush=True)
