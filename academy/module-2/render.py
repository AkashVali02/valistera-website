from pathlib import Path
import json,textwrap,math,io,os
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'assets/academy/module-2';ASSETS.mkdir(parents=True,exist_ok=True)
D=json.loads((Path(__file__).parent/'content.json').read_text())
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
BG='#071526';PANEL='#112a43';WHITE='#f3f7fc';BLUE='#4c9eff';MUT='#bbcedf';CYAN='#69dce3';ORANGE='#ffd18a'
def draw_scene(l,s,j):
 im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
 def text(x,y,t,size=30,fill=WHITE,bold=False):d.text((x,y),t,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=fill)
 def box(x,y,w,h,fill=PANEL):d.rounded_rectangle((x,y,x+w,y+h),radius=18,fill=fill,outline='#345675',width=2)
 text(48,26,'Vali',32,bold=True);text(121,26,'Stera',32,BLUE,True);text(235,35,'ACADEMY',21,MUT,True)
 text(48,92,f'MODULE 02   /   LESSON 2.{l["id"]}   /   {j+1:02} OF 04',20,CYAN,True)
 title=textwrap.wrap(s['title'],42)
 for n,line in enumerate(title):text(48,130+50*n,line,42,bold=True)
 # Original pharmaceutical system illustration, or data-specific visualization.
 box(48,235,455,355)
 if l['id']==9:
  vals=[.1,.2,.1,.3,.2,.4,.3,.5,.4,.6]
  text(72,252,'Illustrative error (°C)',25,CYAN,True)
  for n,v in enumerate(vals):
   x=87+n*39;y=538-v*330
   d.line((x,538,x,y),fill=CYAN,width=16);text(x-10,y-30,str(v),16)
  d.line((70,538,475,538),fill=MUT,width=2);text(73,552,'Observation 1 → 10',22,MUT)
 elif l['id']==7 and j==2:
  text(72,254,'Same total. Different severity.',22,CYAN,True)
  for k,nums in enumerate([[3,1,2],[1,3,2]]):
   x=90+k*210
   for n,v in enumerate(nums):d.rectangle((x+n*43,490-v*54,x+n*43+28,490),fill=[ORANGE,CYAN,BLUE][n]);text(x+n*43,500,['S','O','D'][n],20)
   text(x,542,'Score = 6',25)
 elif l['id']==10:
  text(75,260,'Project activity completed',24,CYAN,True)
  d.rounded_rectangle((77,315,470,360),12,fill='#304a62');d.rounded_rectangle((77,315,431,360),12,fill=CYAN)
  text(78,382,'90% ≠ ready for use',32,ORANGE,True)
  for k,t in enumerate(['Mixing range unresolved','Cleaning evidence missing','Alarm response unverified']):text(78,441+k*40,t,22,MUT)
 elif l['id'] in [2,3,4,5,6,8]:
  examples={2:['Programme: V-201 project','Protocol: mixing verification','Report: evaluated results'],3:['Jacket utility → vessel','Sensor → controller','Vessel → transfer hose'],4:['URS-01: contact materials','Design: compatibility basis','Verify: installed records'],5:['URS-01 → design response','Risk control → verification','Evidence → reviewed status'],6:['Agitator stops','Concentration may vary','Dose may be affected'],8:['Shared sensor signal','Controller + alarm','Common failure possible']}[l['id']]
  for k,t in enumerate(examples):
   box(72,270+k*100,405,70,'#1b3d56');text(90,290+k*100,t,21,WHITE,True)
   if k<2 and l['id']!=3:
    d.line((274,344+k*100,274,365+k*100),fill=CYAN,width=4);d.polygon([(266,358+k*100),(274,369+k*100),(282,358+k*100)],fill=CYAN)
 else:
  # Vessel with agitator, jacket, temperature instrument and transfer pathway.
  d.rounded_rectangle((155,318,347,505),40,fill='#244763',outline=CYAN,width=4)
  d.rounded_rectangle((169,330,333,492),30,outline='#86b7d6',width=2)
  d.rectangle((170,416,332,467),fill='#287f99');d.ellipse((170,401,332,432),fill='#389fb1')
  d.line((250,283,250,453),fill=WHITE,width=5);d.rounded_rectangle((218,265,282,310),8,fill=BLUE)
  d.line((213,449,286,427),fill=WHITE,width=6);d.line((213,427,286,449),fill=WHITE,width=6)
  d.line((250,505,250,544,435,544),fill=CYAN,width=5);d.polygon([(435,536),(451,544),(435,552)],fill=CYAN)
  d.line((320,355,405,355),fill=ORANGE,width=3);d.ellipse((390,328,445,382),fill=PANEL,outline=ORANGE,width=3);text(405,341,'T',23,ORANGE,True)
  text(180,365,'V-201',27,WHITE,True);text(75,560,'Mixing vessel • schematic',23,MUT)
 # Three strong takeaways; full text alternative is provided in HTML.
 for k,label in enumerate(s['labels']):
  y=235+k*120;box(548,y,684,103);d.text((574,y+51),f'{k+1:02}',font=ImageFont.truetype(BOLD,28),fill=CYAN,anchor='lm')
  lines=textwrap.wrap(label,28)
  for n,line in enumerate(lines):d.text((635,y+51+(n-(len(lines)-1)/2)*36),line,font=ImageFont.truetype(BOLD,30),fill=WHITE,anchor='lm')
 d.line((48,627,1232,627),fill='#345675',width=2)
 text(48,652,'FICTIONAL TEACHING CASE · NOT A SITE ACCEPTANCE CRITERION',20,MUT)
 p=ASSETS/f'lesson-{l["id"]}-scene-{j+1}.png';buf=io.BytesIO();im.save(buf,format="PNG",optimize=True);tmp=p.with_suffix(".tmp");tmp.write_bytes(buf.getvalue());os.replace(tmp,p)
 return p
if __name__=='__main__':
 for l in D['lessons']:
  for j,s in enumerate(l['scenes']):draw_scene(l,s,j)
 print('Rendered 40 original diagrams')
