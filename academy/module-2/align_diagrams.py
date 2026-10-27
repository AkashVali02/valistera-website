from pathlib import Path
import runpy
p=Path(__file__).with_name('render.py')
s=p.read_text()
old="text(574,y+28,f'{k+1:02}',28,CYAN,True)"
new="d.text((574,y+51),f'{k+1:02}',font=ImageFont.truetype(BOLD,28),fill=CYAN,anchor='lm')"
old2="for n,line in enumerate(lines):text(635,y+18+n*36,line,30,WHITE,True)"
new2="for n,line in enumerate(lines):d.text((635,y+51+(n-(len(lines)-1)/2)*36),line,font=ImageFont.truetype(BOLD,30),fill=WHITE,anchor='lm')"
assert old in s and old2 in s
p.write_text(s.replace(old,new).replace(old2,new2))
m=runpy.run_path(str(p))
for lesson in m['D']['lessons']:
 for j,scene in enumerate(lesson['scenes']):
  m['draw_scene'](lesson,scene,j)
print('Aligned all 40 diagrams')
