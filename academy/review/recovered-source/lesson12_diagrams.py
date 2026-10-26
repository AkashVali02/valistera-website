from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
B=Path('/home/user/lesson12');times=json.loads((B/'timings.json').read_text());F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=ImageFont.truetype(F,17);small=ImageFont.truetype(F,14)
for idx,(start,end,_) in enumerate(times,1):
 im=Image.open(B/f'scene_{idx:02}.png').convert('RGB');d=ImageDraw.Draw(im)
 d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
 def text(x,y,t,c='#eaf3ff',sm=False):d.text((x,y),t,font=small if sm else font,fill=c)
 def card(x,y,w,h,t,c='#56c8e0'):
  d.rounded_rectangle((x,y,x+w,y+h),radius=13,fill='#1d4160',outline=c,width=2)
  text(x+13,y+h//2-10,t)
 def arrow(x,y,x2,y2):
  d.line((x,y,x2,y2),fill='#56c8e0',width=4);d.polygon(((x2,y2),(x2-10,y2-6),(x2-10,y2+6)),fill='#56c8e0')
 headings=['PHARMACEUTICAL QUALITY SYSTEM','MANAGEMENT RESPONSIBILITY','QUALITY RISK MANAGEMENT','DEVIATION AND CAPA PATH','CHANGE CONTROL LIFECYCLE','GOOD DOCUMENTATION PRACTICES','ALCOA+ DATA INTEGRITY','EXPIRED CALIBRATION: QUALITY DECISION']
 text(95,283,headings[idx-1],'#56c8e0')
 vals={1:['PEOPLE','PROCESSES','OVERSIGHT'],2:['LEAD','RESOURCE','REVIEW'],3:['ASSESS','CONTROL','REVIEW'],4:['DOCUMENT','INVESTIGATE','VERIFY'],5:['PROPOSE','ASSESS','APPROVE'],6:['INSTRUCT','EXECUTE','RECORD'],7:['ATTRIBUTE','PRESERVE','RETRIEVE'],8:['HOLD','ASSESS','DOCUMENT']}[idx]
 for j,t in enumerate(vals):card(92+j*219,352,190,95,t,'#f1b767' if idx==8 and j==0 else '#56c8e0')
 arrow(283,400,310,400);arrow(502,400,530,400)
 subtitles=['Quality must be built into the process','Leadership provides accountability and resources','Risk effort is proportionate to product impact','CAPA effectiveness requires appropriate review','Assess impact and approve before implementation','Records reflect what actually happened','Retain complete and traceable source records','Evaluate instrument status and product impact']
 text(103,516,subtitles[idx-1],sm=True)
 im.save(B/f'diagram_{idx:02}.png')
 duration=end-start
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','8','-i',str(B/f'diagram_{idx:02}.png'),'-i',str(B/f'audio_{idx:02}.wav'),'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',str(B/f'diagram_part_{idx:02}.mp4')],check=True)
 print('SCENE',idx,flush=True)
with open(B/'diagram_concat.txt','w') as f:
 for idx in range(1,9):f.write(f"file '{B}/diagram_part_{idx:02}.mp4'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(B/'diagram_concat.txt'),'-c','copy','-movflags','+faststart',str(B/'lesson12_diagrams.mp4')],check=True)
print('DONE',flush=True)
