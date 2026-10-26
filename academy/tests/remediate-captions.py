from pathlib import Path
import json,re,difflib,textwrap,html
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[2];log=[]
def norm(s):return re.findall(r'[a-z0-9]+',s.lower())
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
for i in range(1,11):
 # Rebuild from original source snapshot, keeping text fidelity and ASR diagnostics separate.
 c=json.load(open(root/f'academy/review/evidence-2026-10-26/source-captions-1-{i}.json'));asr=json.load(open(root/f'academy/review/evidence-2026-10-26/asr-1-{i}.json'))
 aw=[(t,w['start'],w['end']) for s in asr for w in s['words'] for t in norm(w['word'])];cw=[(t,n) for n,x in enumerate(c) for t in norm(x[2])]
 match=difflib.SequenceMatcher(None,[w[0] for w in cw],[w[0] for w in aw],autojunk=False);mapping={}
 for a,b,size in match.get_matching_blocks():
  for z in range(size):mapping[a+z]=b+z
 offset=0;new=[]
 for n,(a,e,t) in enumerate(c):
  tokens=norm(t);ids=[mapping.get(k) for k in range(offset,offset+len(tokens))];offset+=len(tokens)
  exact=all(k is not None for k in ids) and ids[-1]-ids[0]+1==len(ids)
  # Correct accumulating L1 drift using exact word matches. Unknown brand tokens retain original boundaries.
  if i==1 and exact:a=max(0,aw[ids[0]][1]-.08);e=aw[ids[-1]][2]+.12
  # Split long blocks on a matched word boundary; retain outer bounds in lessons 2–10.
  words=t.split();split=None
  if len(t)>84 and exact:
   middle=min(range(1,len(words)),key=lambda k:abs(len(' '.join(words[:k]))-len(t)/2));left=' '.join(words[:middle]);right=' '.join(words[middle:]);count=len(norm(left));boundary=aw[ids[count]][1]-.03
   if a+.5<boundary<e-.5 and len(left)/(boundary-a)<=20 and len(right)/(e-boundary)<=20:split=[[a,boundary,left],[boundary,e,right]]
  new.extend(split or [[a,e,t]])
 # Keep starts monotonic; remove overlap without compressing a cue to an unusable flash.
 for n,x in enumerate(new[:-1]):
  if x[1]>new[n+1][0]:
   if new[n+1][0]-x[0]<.5:new[n+1][0]=x[1]
   else:x[1]=new[n+1][0]
 duration=json.load(open(root/'academy/review/evidence-2026-10-26/audio-diagnostics.json'))[i-1]['duration']
 new[-1][1]=min(duration,new[-1][1])
 for n,x in enumerate(new):
  limit=new[n+1][0] if n+1<len(new) else duration
  x[1]=min(limit,max(x[1],x[0]+len(x[2])/20))
 # Merge a fast or tiny adjacent block; don't shift outer speech boundaries.
 merged=[];j=0
 while j<len(new):
  x=new[j][:]
  if j+1<len(new):
   y=new[j+1]
   if (len(x[2])/(x[1]-x[0])>20.05 or len(y[2])<15 or x[2].endswith('C A P')) and y[0]-x[1]<.2 and len(x[2]+' '+y[2])<=112 and y[1]-x[0]<8:
    x=[x[0],y[1],x[2]+' '+y[2]];j+=1
  for a,b in [('C A P A','CAPA'),('A L C O A plus','ALCOA+'),('O O S','OOS'),('I Q','IQ'),('O Q','OQ'),('P Q','PQ')]:x[2]=x[2].replace(a,b)
  x[0]=round(x[0],3);x[1]=round(x[1],3);merged.append(x);j+=1
 # Balance at most two lines; long cues that could not be aligned remain flagged by line length.
 def wrap(t):
  if len(t)<=42:return t
  w=t.split();k=min(range(1,len(w)),key=lambda j:abs(len(' '.join(w[:j]))-len(' '.join(w[j:]))));return ' '.join(w[:k])+'\n'+' '.join(w[k:])
 (root/f'academy-captions-1-{i}.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{n}\n{stamp(a)} --> {stamp(e)}\n'+wrap(t) for n,(a,e,t) in enumerate(merged,1))+'\n')
 p=root/('academy-player-preview.html' if i==1 else f'academy-lesson-1-{i}.html');s=p.read_text();s=re.sub(r'const cues=\[.*?\],\s*starts=',lambda m:'const cues='+json.dumps(merged,separators=(',',':'))+',starts=',s,flags=re.S)
 transcript='<details class="academy-transcript"><summary>Read the recorded narration transcript</summary><p>This transcript follows the existing recording. Read the technical clarifications and companion material as well.</p>'+''.join('<p><span class="muted">'+stamp(a)[:8]+'</span> '+html.escape(t)+'</p>' for a,e,t in merged)+'</details>'
 s=re.sub(r'<details class="academy-transcript">.*?</details>',lambda _:transcript,s,flags=re.S);p.write_text(s)
 log.append({'lesson':i,'original_cues':len(c),'final_cues':len(merged),'method':'L1 exact ASR-word alignment; long-cue splits at exact ASR word matches; adjacent rapid-fragment merging; outer times preserved otherwise. Machine-assisted timing requires human acceptance.'})
(root/'academy/review/evidence-2026-10-26/caption-changes.json').write_text(json.dumps(log,indent=2))
