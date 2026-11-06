"""Code-drawn training diagrams. No stock imagery or dimensional engineering claims."""
from pathlib import Path
import json,io,textwrap
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT/'assets/academy/module-4';ASSETS.mkdir(parents=True,exist_ok=True)
D=json.loads(Path(__file__).with_name('content.json').read_text());F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B=F.replace('.ttf','-Bold.ttf')
BG='#071526';PANEL='#112a43';WHITE='#f3f7fc';BLUE='#4c9eff';CYAN='#69dce3';MUT='#bbcedf';GOLD='#ffd18a'
MAPS=[
[['DESIGN','INSTALLED','COMPARE'],['DRAWING','WALKDOWN','CHALLENGE'],['UPSTREAM','INTERFACE','VESSEL'],['OBSERVED','UNRESOLVED','RECOMMEND']],
[['URS / DQ','DRAWINGS','PROTOCOL'],['REQUIREMENT','METHOD','RECORD'],['TRAINING','SAFE ACCESS','TOOLS'],['MEASURED','NO CRITERION','UNRESOLVED']],
[['TAG','MODEL / SERIAL','LOCATION'],['AGITATOR','OUTLET','SENSOR'],['INSTRUMENT','PATH','PIPE RACK'],['INACCESSIBLE','NOT CHECKED','FOLLOW-UP']],
[['BODY','GASKET','OUTLET'],['COMPONENT','LOT / ID','CERTIFICATE'],['BODY: LINKED','GASKET: GAP','EVIDENCE NEEDED'],['SPECIFIED','FITTED','SUITABILITY']],
[['SOURCE','ISOLATION','CONNECTION'],['CONTENTS','DIRECTION','ACTUAL ROUTE'],['CONNECTED','QUALITY DATA','READINESS'],['OLD SYSTEM','NEW BRANCH','IMPACT REVIEW']],
[['SENSOR','TRANSMITTER','DISPLAY'],['IDENTITY','COVERAGE','RESULTS'],['40.0 °C','40.4 °C','+0.4 °C'],['STATUS GAP','AFFECTED DATA','FOLLOW-UP']],
[['INSTALLED MODEL','APPLICABLE MANUAL','MAINTENANCE'],['HARDWARE','VERSION','CONFIGURATION'],['TASK','OWNER','RESOURCES'],['FACTORY DATA','IMPACT REVIEW','SITE EVIDENCE']],
[['CRITERION','OBSERVATION','ATTRIBUTION'],['SUBJECT','LOCATION','CHECK REFERENCE'],['ORIGINAL','CORRECTION','ATTRIBUTION'],['NOT APPLICABLE','NOT CHECKED','MISMATCH']],
[['REQUIRED: A','OBSERVED: B','IMPACT UNKNOWN'],['INVESTIGATE','AUTHORIZE ACTION','VERIFY'],['ORDERED ≠ CLOSED','REINSPECT','REVIEW'],['OPEN FINDING','DEFINED ACTIVITY','AUTHORIZATION']],
[['CHECKS','ATTACHMENTS','REPORT'],['9 SUPPORTED','1 OPEN','NO RELEASE RULE'],['SCOPE','RESTRICTIONS','OQ HANDOVER'],['TRACE EVIDENCE','EXPLAIN GAP','RECOMMEND']]]
def draw_scene(l,s,j):
 im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
 def text(x,y,t,size=25,color=WHITE,bold=False,anchor=None):d.text((x,y),t,font=ImageFont.truetype(B if bold else F,size),fill=color,anchor=anchor)
 def box(x,y,w,h,color=PANEL):d.rounded_rectangle((x,y,x+w,y+h),16,fill=color,outline='#345675',width=2)
 text(48,24,'Vali',32,bold=True);text(121,24,'Stera',32,BLUE,True);text(236,34,'ACADEMY',21,MUT,True)
 text(48,84,f'INSTALLATION QUALIFICATION / LESSON 4.{l["id"]} / PART {j+1}',20,CYAN,True)
 for k,line in enumerate(textwrap.wrap(s['title'],45)):text(48,124+k*46,line,38,bold=True)
 box(48,222,455,374)
 if l['id']==3 and j==2:
  text(70,240,'Maintenance envelope · plan',22,CYAN,True)
  d.ellipse((85,333,269,517),fill='#244763',outline=CYAN,width=3);text(176,425,'V-201',26,anchor='mm')
  d.rectangle((255,407,319,437),fill=BLUE);text(78,290,'Rear instrument',21)
  d.line((235,317,285,408),fill=WHITE,width=2)
  d.rectangle((384,327,421,528),fill='#745d32',outline=GOLD,width=3);text(335,288,'Pipe rack',21,GOLD)
  for x in range(326,459,18):d.line((x,422,x+10,422),fill=GOLD,width=4)
  d.polygon([(456,414),(470,422),(456,430)],fill=GOLD)
  d.line((375,402,433,442),fill='#ff9f9f',width=4);d.line((375,442,433,402),fill='#ff9f9f',width=4)
  text(74,548,'Blocked path · not to scale',22,GOLD)
 elif l['id']==6 and j==2:
  text(70,242,'Fictional error calculation',23,CYAN,True)
  text(74,306,'Reference',23);text(440,306,'40.0 °C',28,anchor='ra')
  text(74,362,'Indication',23);text(440,362,'40.4 °C',28,anchor='ra')
  d.line((75,412,470,412),fill=CYAN,width=2)
  text(74,441,'40.4 − 40.0 = +0.4 °C',28,GOLD,True)
  text(74,501,'Simple limit: ±0.5 °C',24)
  text(74,551,'Decision rule still matters',21,MUT)
 elif l['id']==10 and j==1:
  text(72,246,'Evidence coverage',27,CYAN,True)
  for n in range(10):box(76+n%5*78,310+n//5*60,60,40,CYAN if n<9 else '#745d32')
  text(76,451,'9 / 10 = 90%',38,bold=True);text(76,509,'Material gap remains',26,GOLD,True);text(76,558,'No release threshold',23,MUT)
 else:
  text(72,242,'Evidence and relationship',21,CYAN,True)
  for n,label in enumerate(MAPS[l['id']-1][j]):
   y=278+n*62;box(72,y,407,54)
   for k,line in enumerate(textwrap.wrap(label,25)):text(275,y+27+(k-(len(textwrap.wrap(label,25))-1)/2)*23,line,20,CYAN if n==0 else WHITE,True,'mm')
  relation=textwrap.wrap(s['description'],43)
  assert len(relation)<=5,(l['id'],j,relation)
  for n,line in enumerate(relation):text(72,477+n*22,line,18,MUT)
 for k,label in enumerate(s['labels']):
  y=222+k*126;box(548,y,684,110);text(576,y+55,f'{k+1:02}',28,CYAN,True,'lm')
  lines=textwrap.wrap(label,28);assert len(lines)<=2,(l['id'],j,label)
  for n,line in enumerate(lines):text(638,y+55+(n-(len(lines)-1)/2)*36,line,29,WHITE,True,'lm')
 d.line((48,624,1232,624),fill='#345675',width=2);text(48,648,'FICTIONAL TEACHING CASE · NOT AN EXECUTED GMP RECORD',21,MUT)
 p=ASSETS/f'lesson-{l["id"]}-scene-{j+1}.png';im.save(p);return p
if __name__=='__main__':
 for l in D['lessons']:
  for j,s in enumerate(l['scenes']):draw_scene(l,s,j)
