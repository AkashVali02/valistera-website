import ast,re,os,subprocess,textwrap,math
from PIL import Image,ImageDraw,ImageFont
from kokoro_onnx import Kokoro
import soundfile as sf
source=ast.parse(open('/home/user/make_lesson.py').read())
d={node.targets[0].id:ast.literal_eval(node.value) for node in source.body if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('S','T')}
S,T=d['S'],d['T']
B='/home/user/premium_full';os.makedirs(B,exist_ok=True)
NAVY='#0a1930';DARK='#101f39';CARD='#152d49';CYAN='#55d8e7';BLUE='#238dd3';WHITE='#f6fbff';MUT='#a7bfd1';GREEN='#55d5b1';GOLD='#f3bd6b'
f='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def ft(n,b=False):return ImageFont.truetype(fb if b else f,n)
def tx(d,x,y,s,n=22,c=WHITE,b=False):d.text((x,y),s,font=ft(n,b),fill=c)
def panel(d,rect):d.rounded_rectangle(rect,radius=20,fill=CARD,outline='#315371',width=2)
def lines(d,x,y,s,w=43,n=22,c=WHITE,limit=4):
 for j,line in enumerate(textwrap.wrap(s,w)[:limit]):tx(d,x,y+j*(n+13),line,n,c)
def get_scenes():
 scenes=[]
 for idx,(title,speech) in enumerate(zip(T,S)):
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',speech)
  # three narration-led scenes, each with related sentence group
  chunks=[[],[],[]]
  for j,s in enumerate(sentences):chunks[min(2,int(j*3/max(1,len(sentences))))].append(s)
  for j,c in enumerate(chunks):
   if c:scenes.append((idx,j,title,' '.join(c)))
 return scenes
scenes=get_scenes()
# Content-specific micro-learning cards. All are illustrative explanatory labels, not test results.
topics=[
 [('GMP FOUNDATION','Quality throughout the lifecycle'),('CONSISTENT PROCESSES','Not just end-product testing'),('LEARNING GOAL','Connect GMP controls to patient safety')],
 [('PATIENT SAFETY','Protect product identity and quality'),('MANUFACTURING RISKS','Contamination • mix-ups • variability'),('CONTROL STRATEGY','Prevention across production')],
 [('DEFINITION','Consistently manufactured and controlled'),('CONTROL ELEMENTS','Personnel • premises • processes'),('EQUIPMENT EXAMPLE','Suitable, maintained and cleaned')],
 [('QUALITY SYSTEM','Integrated oversight and accountability'),('QUALITY RISK','Assess and manage uncertainty'),('CONTINUAL IMPROVEMENT','Investigate • act • verify')],
 [('PROCESS CONTROL','Quality is designed into operations'),('IN-PROCESS CHECKS','Monitor relevant process variables'),('TESTING LIMITATION','A sample is not the whole batch')],
 [('PERSONNEL','Role-based qualification and training'),('COMPETENCE','Training plus demonstrated capability'),('OPERATOR EXAMPLE','Cleaning procedure and records')],
 [('FACILITY DESIGN','Prevent contamination and mix-ups'),('EQUIPMENT CONTROL','Maintenance, calibration, qualification'),('UTILITIES','Water • gases • HVAC controls')],
 [('DOCUMENT TYPES','Instructions versus evidence'),('DATA INTEGRITY','Attributable • legible • contemporaneous'),('TRACEABILITY','Document actual test execution')],
 [('MANUFACTURING','Execute approved instructions'),('QUALITY CONTROL','Sample and test as appropriate'),('QUALITY OVERSIGHT','Evaluate batch records and release')],
 [('DEVIATIONS','Record and evaluate unexpected events'),('INVESTIGATION','Identify causes and product impact'),('CHANGE CONTROL','Assess change before implementation')],
 [('PRE-USE CHECK','Identity • cleaning • calibration'),('QUALITY FINDING','Overdue instrument calibration'),('DECISION PATH','Assess suitability and product impact')],
 [('REVIEW','GMP is a system of controls'),('PATIENT PROTECTION','People, process and reliable evidence'),('NEXT LESSON','PQS and Good Documentation Practices')]
]
def draw(idx,part,title,speech,number):
 im=Image.new('RGB',(1280,720),NAVY);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1280,9),fill=CYAN);d.rectangle((0,0,1280,88),fill='#071325')
 tx(d,53,27,'Vali',24,WHITE,True);tx(d,107,27,'Stera',24,BLUE,True);tx(d,250,30,'ACADEMY  /  PHARMACEUTICAL GMP',17,MUT,True)
 tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2),16,CYAN,True)
 tx(d,59,165,title.upper(),32,WHITE,True);d.line((60,219,1210,219),fill='#2c4c69',width=2)
 h,b=topics[idx][part]
 panel(d,(65,259,760,608));tx(d,99,287,h,25,CYAN,True)
 lines(d,99,348,b,34,29,WHITE,3)
 # right hand visuals tailored to topic, with real explanatory diagrams rather than text duplication
 panel(d,(795,259,1214,608))
 if idx in (0,1,2,3,4,8,9,11):
  labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]
  for k,l in enumerate(labels):
   y=295+k*95;d.rounded_rectangle((828,y,1168,y+67),radius=15,fill='#21435f')
   d.ellipse((847,y+14,884,y+51),fill=BLUE if k<2 else GREEN)
   tx(d,857,y+22,str(k+1),17,WHITE,True);tx(d,907,y+20,l,22,WHITE,True)
   if k<2:tx(d,990,y+70,'↓',16,CYAN)
 elif idx==5:
  for k,(l,s) in enumerate([('TRAIN','Approved procedure'),('DEMONSTRATE','Practical competence'),('DOCUMENT','Training evidence')]):
   y=290+k*94;tx(d,825,y,l,22,CYAN,True);tx(d,825,y+33,s,17,MUT)
 elif idx==6:
  # diagrammatic stainless steel vessel and control tags
  d.ellipse((914,320,1088,364),outline=CYAN,width=5);d.rounded_rectangle((914,340,1088,498),radius=35,outline='#8dbdd3',width=6)
  d.line((1000,315,1000,286),fill=CYAN,width=7);d.line((949,501,949,531),fill=CYAN,width=6);d.line((1053,501,1053,531),fill=CYAN,width=6)
  tx(d,833,552,'VESSEL  •  ILLUSTRATIVE',17,MUT,True)
 elif idx==7:
  for k,(l,s) in enumerate([('SOP','What to do'),('RECORD','What was done'),('REVIEW','Is evidence reliable?')]):
   y=296+k*93;d.rounded_rectangle((831,y,1168,y+70),radius=12,outline=CYAN,width=2);tx(d,846,y+11,l,19,CYAN,True);tx(d,846,y+39,s,15,WHITE)
 elif idx==10:
  tx(d,832,294,'TEMPERATURE SENSOR',21,CYAN,True);tx(d,832,349,'CALIBRATION',20,MUT,True);tx(d,832,395,'OVERDUE',40,GOLD,True)
  tx(d,832,486,'Assess before use',23,WHITE,True)
 tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)
 # On-screen caption of actual spoken segment, 2-line extract, to reduce cognitive mismatch
 excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)
 tx(d,1103,669,f'{number:02} / {len(scenes):02}',17,CYAN,True)
 p=f'{B}/scene_{number:02}.png';im.save(p);return p
k=Kokoro('/home/user/kokoro-v1.0.onnx','/home/user/voices-v1.0.bin');parts=[]
for number,(idx,part,title,speech) in enumerate(scenes,1):
 print('SCENE',number,'of',len(scenes),flush=True)
 img=draw(idx,part,title,speech,number)
 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.75;out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.75[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
open(f'{B}/concat.txt','w').write(''.join("file '"+p+"'\\n" for p in parts).replace('\\n','\n'))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/full.mp4'],check=True)
print('DONE',flush=True)
