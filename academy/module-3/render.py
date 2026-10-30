from pathlib import Path
import json,textwrap,io
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT/'assets/academy/module-3';ASSETS.mkdir(parents=True,exist_ok=True)
D=json.loads(Path(__file__).with_name('content.json').read_text());F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B=F.replace('.ttf','-Bold.ttf')
BG='#071526';PANEL='#112a43';WHITE='#f3f7fc';BLUE='#4c9eff';CYAN='#69dce3';MUT='#bbcedf';GOLD='#ffd18a'
def draw_scene(l,s,j):
 im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
 def text(x,y,t,size=27,color=WHITE,bold=False):d.text((x,y),t,font=ImageFont.truetype(B if bold else F,size),fill=color)
 def box(x,y,w,h,color=PANEL):d.rounded_rectangle((x,y,x+w,y+h),16,fill=color,outline='#345675',width=2)
 def arrow(x,y,x2,y2):
  d.line((x,y,x2,y2),fill=CYAN,width=4)
  d.polygon([(x2-7,y2-10),(x2+7,y2-10),(x2,y2)],fill=CYAN)
 text(48,24,'Vali',32,bold=True);text(121,24,'Stera',32,BLUE,True);text(236,34,'ACADEMY',21,MUT,True)
 text(48,84,f'DESIGN QUALIFICATION / LESSON 3.{l["id"]} / PART {j+1}',21,CYAN,True)
 for k,t in enumerate(textwrap.wrap(s['title'],43)):text(48,124+k*48,t,40,bold=True)
 box(48,222,455,374)
 if l['id']==3:
  text(72,244,'Teaching error bounds',26,CYAN,True)
  for n,(label,value) in enumerate([('Sensor',.2),('Transmitter',.2),('Display',.2),('Sum',.6)]):
   y=306+n*64;text(72,y,label,23);d.rectangle((250,y+2,250+value*320,y+27),fill=GOLD if n==3 else BLUE);text(250+value*320+7,y,str(value),20)
  text(72,564,'Limit: 0.5 °C (fictional)',22,MUT)
 elif l['id']==10:
  text(72,246,'Evidence coverage',28,CYAN,True)
  for n in range(10):
   x=78+n%5*78;y=310+n//5*60;box(x,y,60,40,CYAN if n<8 else '#745d32')
  text(76,446,'8 / 10 = 80%',38,bold=True);text(76,507,'Gaps still matter',30,GOLD,True);text(76,556,'No release threshold',24,MUT)
 elif l['id'] in [1,4,6]:
  text(72,242,'V-201 · oral-liquid vessel',23,CYAN,True)
  d.rounded_rectangle((154,319,335,492),35,fill='#244763',outline=CYAN,width=4)
  d.line((245,284,245,448),fill=WHITE,width=5);d.rectangle((217,282,272,314),fill=BLUE)
  d.ellipse((173,411,317,458),fill='#287f99');d.line((206,449,280,424),fill=WHITE,width=5)
  d.line((246,492,246,536,444,536),fill=CYAN,width=5)
  d.line((333,351,415,351),fill=GOLD,width=3);d.ellipse((394,324,449,379),outline=GOLD,width=3);text(409,337,'T',24,GOLD,True)
  text(74,560,['Purpose → design', 'Contact path + cleaning','Utility + access'][[1,4,6].index(l['id'])],23,MUT)
 elif l['id']==5:
  box(140,275,265,64);text(166,292,'Shared sensor',26,CYAN,True)
  d.line((272,341,272,384,151,384,151,410),fill=CYAN,width=4);d.line((272,384,392,384,392,410),fill=CYAN,width=4)
  box(68,414,184,72);box(280,414,197,72);text(83,437,'Controller',25);text(319,437,'Alarm',25)
  text(79,542,'One input ≠ independence',22,GOLD,True)
 else:
  for k,label in enumerate(s['labels']):
   box(72,260+k*105,407,76)
   for n,line in enumerate(textwrap.wrap(label,27)):text(91,277+k*105+n*26,line,23,CYAN if k==0 else WHITE,True)
   if k<2:arrow(275,338+k*105,275,360+k*105)
 for k,label in enumerate(s['labels']):
  y=222+k*126;box(548,y,684,110)
  d.text((576,y+55),f'{k+1:02}',font=ImageFont.truetype(B,28),fill=CYAN,anchor='lm')
  lines=textwrap.wrap(label,28)
  for n,line in enumerate(lines):
   assert len(lines)<=2,(l['id'],j,label)
   d.text((638,y+55+(n-(len(lines)-1)/2)*36),line,font=ImageFont.truetype(B,29),fill=WHITE,anchor='lm')
 d.line((48,624,1232,624),fill='#345675',width=2)
 text(48,648,'FICTIONAL TEACHING CASE · NOT AN APPROVED SITE DESIGN',21,MUT)
 p=ASSETS/f'lesson-{l["id"]}-scene-{j+1}.png';buf=io.BytesIO();im.save(buf,format='PNG',optimize=True);tmp=p.with_suffix('.tmp');tmp.write_bytes(buf.getvalue());tmp.replace(p);return p
if __name__=='__main__':
 for l in D['lessons']:
  for j,s in enumerate(l['scenes']):draw_scene(l,s,j)
