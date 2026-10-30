"""Display standard abbreviations/numbers without changing the spoken audio."""
import re,json,textwrap
from pathlib import Path
REPLACEMENTS={'V two zero one':'V-201','U R S zero one':'URS-01','V M P':'VMP','U R S':'URS','F M E A':'FMEA','Annex Fifteen':'Annex 15','ICH Q Nine revision one':'ICH Q9(R1)','Module Two':'Module 2','zero point three one':'0.31','zero point one':'0.1','zero point two':'0.2','zero point three':'0.3','zero point four':'0.4','zero point five':'0.5','zero point six':'0.6','three point one':'3.1','ninety percent':'90%'}
def display(text):
 for a,b in REPLACEMENTS.items():text=text.replace(a,b)
 text=re.sub(r'(\d(?:\.\d+)?) degrees\b',r'\1 °C',text)
 return text

def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02}.{n%1000:03}'
def rebuild():
 A=Path(__file__).resolve().parents[2]/'assets/academy/module-2'
 for i in range(1,11):
  p=A/f'lesson-{i}-timing.json';t=json.loads(p.read_text())
  # Preserve original measured speech chunks to allow repeatable regeneration.
  t.setdefault('spoken_cues',t['cues'])
  cues=[dict(c,text=display(c['text'])) for c in t['spoken_cues']]
  k=0
  while k<len(cues):
   c=cues[k]
   if len(c['text'].split())<=2 and k>0 and cues[k-1]['scene']==c['scene']:
    prev=cues[k-1];merged=prev['text']+' '+c['text']
    if len(textwrap.wrap(merged,42))<=2 and c['end']-prev['start']<=8:
     prev['text']=merged;prev['end']=c['end'];cues.pop(k);continue
   k+=1
  t['cues']=cues;t['display_policy']='Conventional abbreviations and numerals; spoken_cues preserve original synthesized phrases. Short trailing cues merged where two-line/8-second limits allow.'
  p.write_text(json.dumps(t,indent=2))
  (A/f'lesson-{i}.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{n}\n{stamp(c["start"])} --> {stamp(c["end"])}\n'+ '\n'.join(textwrap.wrap(c['text'],42)) for n,c in enumerate(cues,1))+'\n')
if __name__=='__main__':rebuild()
