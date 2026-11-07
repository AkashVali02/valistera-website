"""Original code-drawn OQ reasoning diagrams; values are fictional, not engineering drawings."""
from pathlib import Path
import json,textwrap
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT/'assets/academy/module-5';ASSETS.mkdir(parents=True,exist_ok=True)
D=json.loads(Path(__file__).with_name('content.json').read_text());F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B=F.replace('.ttf','-Bold.ttf')
BG='#071526';PANEL='#112a43';WHITE='#f3f7fc';BLUE='#4c9eff';CYAN='#69dce3';MUT='#bbcedf';GOLD='#ffd18a'
def draw_scene(l,s,j):
 im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
 def text(x,y,t,size=25,color=WHITE,bold=False,anchor=None):d.text((x,y),t,font=ImageFont.truetype(B if bold else F,size),fill=color,anchor=anchor)
 def box(x,y,w,h,color=PANEL):d.rounded_rectangle((x,y,x+w,y+h),14,fill=color,outline='#345675',width=2)
 def arrow(x,y,x2,y2):
  d.line((x,y,x2,y2),fill=CYAN,width=3)
  if y2>y:d.polygon([(x2-6,y2-9),(x2+6,y2-9),(x2,y2)],fill=CYAN)
  else:d.polygon([(x2-9,y2-6),(x2-9,y2+6),(x2,y2)],fill=CYAN)
 text(48,24,'Vali',32,bold=True);text(121,24,'Stera',32,BLUE,True);text(236,34,'ACADEMY',21,MUT,True)
 text(48,84,f'OPERATIONAL QUALIFICATION / LESSON 5.{l["id"]} / PART {j+1}',20,CYAN,True)
 for k,line in enumerate(textwrap.wrap(s['title'],45)):text(48,124+k*46,line,38,bold=True)
 box(48,222,455,374)
 key=(l['id'],j+1)
 if key==(3,3):
  text(72,247,'Fictional response interval',22,CYAN,True)
  arrow(95,335,456,335)
  for x,t in [(95,'START'),(380,'OUTPUT')]:
   d.line((x,320,x,350),fill=WHITE,width=3);text(x,370,t,20,anchor='mm')
  text(285,420,'Elapsed: 3.2 s',31,GOLD,True,'mm');text(285,468,'Limit: 4.0 s',27,WHITE,False,'mm');text(285,518,'Margin: 0.8 s',27,WHITE,False,'mm');text(285,565,'Clock suitability required',20,MUT,False,'mm')
 elif key==(4,3):
  text(72,245,'Fictional 2 × 3 matrix',23,CYAN,True)
  for col,v in enumerate(['LOW','NOM','HIGH']):text(195+col*103,305,v,19,WHITE,True,'mm')
  for row,label in enumerate(['LOW','HIGH']):
   text(104,363+row*76,label,18,MUT,True,'mm')
   for col in range(3):box(157+col*103,336+row*76,76,54);text(195+col*103,363+row*76,str(row*3+col+1),23,CYAN,True,'mm')
  text(280,514,'6 combinations',29,GOLD,True,'mm');text(280,558,'Selection needs justification',20,MUT,False,'mm')
 elif key==(5,1):
  text(72,247,'Two separate outputs',23,CYAN,True);box(140,294,270,55);text(275,321,'CONDITION',23,WHITE,True,'mm')
  d.line((275,350,275,376,155,376,155,405),fill=CYAN,width=3);d.line((275,376,388,376,388,405),fill=CYAN,width=3)
  box(73,405,168,65);box(301,405,175,65);text(157,438,'ALARM',22,WHITE,True,'mm');text(389,438,'ACTION',22,GOLD,True,'mm')
  text(275,515,'Check both branches',26,GOLD,True,'mm');text(275,558,'Display ≠ output evidence',21,MUT,False,'mm')
 elif key==(6,3):
  text(72,246,'Illustrative decision rule',23,CYAN,True)
  for y,a,b in [(311,'Absolute error','0.4 °C'),(365,'Uncertainty','0.2 °C'),(438,'Sum','0.6 °C'),(492,'Limit','0.5 °C')]:text(75,y,a,23);text(471,y,b,25,GOLD if y==438 else WHITE,True,'ra')
  d.line((76,412,471,412),fill=CYAN,width=2);text(275,559,'Not accepted under this rule',20,GOLD,True,'mm')
 elif key==(10,2):
  text(72,246,'Fictional test coverage',23,CYAN,True)
  for n in range(12):
   box(83+n%4*99,303+n//4*60,72,43,CYAN if n<11 else '#745d32');text(119+n%4*99,324+n//4*60,'P' if n<11 else 'F',22,BG if n<11 else WHITE,True,'mm')
  text(275,518,'11 / 12 ≈ 91.7%',30,WHITE,True,'mm');text(275,561,'Protective failure remains',21,GOLD,True,'mm')
 else:
  text(72,242,'Reasoning map',23,CYAN,True)
  for n,label in enumerate(s['labels']):
   y=285+n*66;box(76,y,397,52)
   lines=textwrap.wrap(label,28);assert len(lines)<=2,(key,label)
   for k,line in enumerate(lines):text(274,y+26+(k-(len(lines)-1)/2)*21,line,19,CYAN if n==0 else WHITE,True,'mm')
  # The caption states the relationship explicitly, avoiding invented causal arrows.
  lines=textwrap.wrap(s['description'],44);assert len(lines)<=5,(key,lines)
  for n,line in enumerate(lines):text(72,490+n*20,line,17,MUT)
 for k,label in enumerate(s['labels']):
  y=222+k*126;box(548,y,684,110);text(576,y+55,f'{k+1:02}',28,CYAN,True,'lm')
  lines=textwrap.wrap(label,28);assert len(lines)<=2,(key,label)
  for n,line in enumerate(lines):text(638,y+55+(n-(len(lines)-1)/2)*36,line,29,WHITE,True,'lm')
 d.line((48,624,1232,624),fill='#345675',width=2);text(48,648,'FICTIONAL TEACHING CASE · NOT AN EXECUTED GMP RECORD',21,MUT)
 p=ASSETS/f'lesson-{l["id"]}-scene-{j+1}.png';im.save(p);return p
if __name__=='__main__':
 for l in D['lessons']:
  for j,s in enumerate(l['scenes']):draw_scene(l,s,j)
