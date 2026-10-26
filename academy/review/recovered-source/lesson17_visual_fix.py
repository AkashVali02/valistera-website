from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
B=Path('/home/user/lesson17');times=json.loads((B/'timings.json').read_text());font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
for idx,(start,end,_) in enumerate(times,1):
 im=Image.open(B/f'scene_{idx:02}.png').convert('RGB');d=ImageDraw.Draw(im)
 def card(x,y,w,h,t):
  d.rounded_rectangle((x,y,x+w,y+h),radius=13,fill='#1d4160',outline='#56c8e0',width=2)
  d.text((x+12,y+h/2-10),t,font=font,fill='#eaf3ff')
 if idx==5:
  d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
  d.text((97,281),'OUT-OF-SPECIFICATION RESPONSE',font=font,fill='#56c8e0')
  card(100,346,180,80,'OOS RESULT');card(319,346,180,80,'INVESTIGATE');card(538,346,180,80,'ASSESS IMPACT')
  for x in (280,499):d.line((x,386,x+38,386),fill='#56c8e0',width=4)
  d.text((106,492),'Preserve original results and records',font=font,fill='#eaf3ff')
  d.text((106,532),'Retest only when justified and approved',font=font,fill='#f1b767')
 if idx==6:
  d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
  d.text((97,281),'LABORATORY DATA INTEGRITY',font=font,fill='#56c8e0')
  for j,t in enumerate(['RAW DATA','METADATA','AUDIT TRAILS']):card(160,335+j*85,460,68,t)
 if idx==8:
  d.rounded_rectangle((67,260,758,607),radius=15,fill='#102b46',outline='#31516c',width=2)
  d.text((97,281),'FAILED ASSAY: INVESTIGATION PATH',font=font,fill='#56c8e0')
  for j,t in enumerate(['PRESERVE','REPORT','INVESTIGATE','DECIDE']):card(95+j*160,365,148,93,t)
  d.text((106,518),'Do not replace a failing result without justification',font=font,fill='#f1b767')
 im.save(B/f'corrected_{idx:02}.png')
 duration=end-start
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','8','-i',str(B/f'corrected_{idx:02}.png'),'-i',str(B/f'audio_{idx:02}.wav'),'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',str(B/f'corrected_part_{idx:02}.mp4')],check=True)
 print('SCENE',idx,flush=True)
with open(B/'corrected_concat.txt','w') as f:
 for idx in range(1,9):f.write(f"file '{B}/corrected_part_{idx:02}.mp4'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(B/'corrected_concat.txt'),'-c','copy','-movflags','+faststart',str(B/'lesson17_corrected.mp4')],check=True)
print('DONE',flush=True)
