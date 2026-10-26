"""Run from repository root: python academy/tests/module1-static.py."""
import re,json,hashlib
from pathlib import Path
from html.parser import HTMLParser
root=Path('.');results=[];errors=[]
for i in range(1,11):
 path=root/f'academy-captions-1-{i}.vtt';cues=[];flags=[]
 for block in path.read_text().strip().split('\n\n')[1:]:
  ls=block.splitlines();times=re.findall(r'(\d+):(\d+):(\d+\.\d+)',ls[1]);a,b=[int(h)*3600+int(m)*60+float(s) for h,m,s in times];text=' '.join(ls[2:]);cues.append([round(a,3),round(b,3),text])
  if b<=a:errors.append(f'{i}: nonpositive cue')
  if len(text)/(b-a)>20.05:flags.append({'cue':len(cues),'cps':round(len(text)/(b-a),2)})
 for x,y in zip(cues,cues[1:]):
  if x[1]>y[0]+.001:errors.append(f'{i}: overlap at {y[0]}')
 duration=json.loads(Path('academy/review/evidence-2026-10-26/media-inventory.json').read_text())[i-1]['duration']
 if i in (4,5):duration=next(x['duration'] for x in json.loads(Path('academy/review/evidence-2026-10-26/revised-media.json').read_text()) if x['lesson']==i)
 if cues[-1][1]>duration+.001:errors.append(f'{i}: captions exceed media duration')
 original=json.loads(Path(f'academy/review/evidence-2026-10-26/source-captions-1-{i}.json').read_text())
 if i in (4,5):original=json.loads(Path(f'academy/review/evidence-2026-10-26/revised-narration-1-{i}.json').read_text())
 normalize=lambda text:re.sub('[^a-z0-9]','',text.lower().replace('+','plus'))
 if normalize(' '.join(c[2] for c in cues))!=normalize(' '.join(c[2] for c in original)):errors.append(f'{i}: caption wording changed beyond formatting')
 page=root/('academy-player-preview.html' if i==1 else f'academy-lesson-1-{i}.html');s=page.read_text();match=re.search(r'const cues=(\[.*?\]),\s*starts=',s,re.S)
 if not match or json.loads(match[1])!=cues:errors.append(f'{i}: embedded caption source differs')
 if i in (4,5):
  expected=[round(x[0],3) for x in original]
  actual=json.loads(re.search(r'starts=(\[.*?\]),keys=',s).group(1))
  if actual!=expected:errors.append(f'{i}: key-explanation scene times differ from revised recording')
 for required in ['academy-privacy-note','academy-transcript','main-content','load-media','data-src=']:
  if required not in s:errors.append(f'{i}: missing {required}')
 results.append({'lesson':i,'cue_count':len(cues),'end_seconds':cues[-1][1],'cps_over_20_05':flags,'max_lines':max(len(b.splitlines())-2 for b in path.read_text().strip().split('\n\n')[1:]),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
out={'method':'Static structural checks; CPS threshold is a review heuristic, not a WCAG criterion.','lessons':results,'failures':errors}
Path('academy/review/evidence-2026-10-26/caption-structure.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2));raise SystemExit(bool(errors))
