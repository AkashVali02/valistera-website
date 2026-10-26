import os,subprocess,math,random
from PIL import Image,ImageDraw
src=open('/home/user/premium_full.py').read().split("k=Kokoro(")[0]
exec(src)
OUT='/home/user/visual_enhanced';os.makedirs(OUT,exist_ok=True)
# Redesigned visual panel on every scene: schematic, analytical graph, quality-risk matrix, sampling distribution, decision workflow.
def draw_visual(idx,part,title,speech,num):
 path=draw(idx,part,title,speech,num)
 im=Image.open(path).convert('RGB');d=ImageDraw.Draw(im)
 d.rounded_rectangle((793,258,1216,610),radius=22,fill='#102942',outline='#3c6079',width=2)
 x0,y0=820,295
 def t(x,y,s,size=17,c=WHITE,b=False):tx(d,x,y,s,size,c,b)
 def node(x,y,label,fill='#214963',w=155):
  d.rounded_rectangle((x,y,x+w,y+48),radius=11,fill=fill,outline='#3e7a9b',width=2)
  t(x+12,y+13,label,15,WHITE,True)
 def arrow(x1,y1,x2,y2,c=CYAN):
  d.line((x1,y1,x2,y2),fill=c,width=4)
  a=math.atan2(y2-y1,x2-x1)
  d.polygon([(x2,y2),(x2-11*math.cos(a-.5),y2-11*math.sin(a-.5)),(x2-11*math.cos(a+.5),y2-11*math.sin(a+.5))],fill=c)
 def schematic():
  t(820,280,'CONTROLLED MANUFACTURING SYSTEM',15,CYAN,True)
  node(827,331,'PEOPLE');node(1032,331,'EQUIPMENT')
  node(925,438,'PROCESS',BLUE)
  arrow(902,380,968,435);arrow(1100,380,1027,435)
  node(925,523,'QUALITY', '#146d6a');arrow(1000,489,1000,519)
 def chart():
  t(820,280,'ILLUSTRATIVE QUALITY TREND',16,CYAN,True)
  t(820,308,'Fictional values • not actual results',13,GOLD)
  x,y,w,h=845,370,326,163
  for j in range(4):
   yy=y+j*h/3;d.line((x,yy,x+w,yy),fill='#34546d',width=1)
  vals=[.42,.48,.45,.54,.51,.62,.58,.66,.61,.7,.63,.75]
  pts=[(x+i*w/11,y+h-v*h) for i,v in enumerate(vals)]
  d.line(pts,fill=CYAN,width=4)
  for px,py in pts:d.ellipse((px-4,py-4,px+4,py+4),fill=GREEN)
  t(846,550,'Time  →',15,MUT);t(820,582,'Trend ≠ evidence of compliance',14,GOLD)
 def risk():
  t(821,280,'QUALITY RISK MATRIX',16,CYAN,True)
  left,top=874,341
  colors=['#1e7b69','#248575','#a7843b','#248575','#a7843b','#bc6c3d','#a7843b','#bc6c3d','#b94e52']
  for row in range(3):
   for col in range(3):
    xx=left+col*94;yy=top+row*65
    d.rounded_rectangle((xx,yy,xx+84,yy+56),radius=8,fill=colors[row*3+col])
    t(xx+32,yy+15,str((row+1)*(col+1)),17,WHITE,True)
  t(892,550,'Likelihood  →',15,MUT);t(822,584,'Illustrative • not a scoring standard',13,GOLD)
 def sample():
  t(820,281,'BATCH SAMPLING EXAMPLE',16,CYAN,True)
  for j in range(80):
   xx=839+(j%10)*35;yy=334+(j//10)*26
   fill=GOLD if j in (17,42,68) else (GREEN if j in (0,1,2,3,4) else '#44728d')
   d.rounded_rectangle((xx,yy,xx+24,yy+16),radius=3,fill=fill)
  t(823,556,'Green = sample  •  Amber = defect',13,MUT)
  t(823,582,'Fictional illustration only',13,GOLD)
 def decision():
  t(820,281,'RISK-BASED DECISION PATH',16,CYAN,True)
  node(917,323,'OBSERVATION',BLUE)
  arrow(995,374,995,408)
  node(917,410,'IMPACT REVIEW')
  arrow(995,462,995,497)
  node(917,502,'ACTION / CAPA','#146d6a')
  t(831,575,'Follow approved site procedures',13,MUT)
 def vessel():
  t(822,281,'EQUIPMENT READINESS',16,CYAN,True)
  d.ellipse((927,350,1091,386),outline=CYAN,width=5)
  d.rounded_rectangle((927,369,1091,510),radius=29,outline='#8cbfd3',width=5)
  d.line((1010,348,1010,316),fill=CYAN,width=5)
  d.line((957,510,957,534),fill=CYAN,width=5);d.line((1060,510,1060,534),fill=CYAN,width=5)
  t(830,347,'ID',16,GREEN,True);arrow(859,361,924,383)
  t(1105,393,'CAL',15,GOLD,True);arrow(1105,417,1094,421)
  t(828,561,'Illustrative vessel schematic',14,MUT)
 def docs():
  t(822,282,'DATA TRACEABILITY',16,CYAN,True)
  for j,(a,b) in enumerate([('SOP','INSTRUCTION'),('RECORD','EVIDENCE'),('REVIEW','DECISION')]):
   yy=326+j*86
   node(835,yy,a,BLUE,129);t(986,yy+13,b,16,MUT)
   if j<2:arrow(898,yy+50,898,yy+80)
 def steps():
  t(821,281,'PROCESS CONTROL FLOW',16,CYAN,True)
  labels=['INPUT','PROCESS','MONITOR','REVIEW']
  for j,l in enumerate(labels):
   yy=325+j*65;node(909,yy,l,BLUE if j==1 else '#214963',172)
   if j<3:arrow(994,yy+49,994,yy+62)
  t(826,581,'Documented quality controls',14,MUT)
 kind={0:[schematic,steps,decision],1:[risk,sample,schematic],2:[schematic,vessel,docs],3:[schematic,risk,decision],4:[steps,chart,sample],5:[schematic,steps,docs],6:[vessel,schematic,chart],7:[docs,steps,decision],8:[steps,chart,decision],9:[risk,decision,steps],10:[vessel,chart,decision],11:[schematic,steps,decision]}[idx][part]
 kind()
 im.save(f'{OUT}/scene_{num:02}.png')
 return f'{OUT}/scene_{num:02}.png'
parts=[]
for num,(idx,part,title,speech) in enumerate(scenes,1):
 print('SCENE',num,'/',len(scenes),flush=True)
 img=draw_visual(idx,part,title,speech,num)
 wav=f'/home/user/premium_full/audio_{num:02}.wav'
 out=f'{OUT}/part_{num:02}.mp4'
 # reuse identical approved narration, scene timings remain matched to the spoken text
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.75[a]','-map','0:v','-map','[a]','-shortest','-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
open(f'{OUT}/concat.txt','w').write(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{OUT}/concat.txt','-c','copy','-movflags','+faststart',f'{OUT}/full.mp4'],check=True)
print('DONE',flush=True)
