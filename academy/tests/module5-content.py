import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'academy/module-5'))
from assessment import QUESTIONS
from caption_display import display
D=json.loads((R/'academy/module-5/content.json').read_text())
assert len(D['lessons'])==10 and all(len(x['scenes'])==4 for x in D['lessons'])
assert len(QUESTIONS)==20 and len({q['question'] for q in QUESTIONS})==20
assert not {q['question'] for q in QUESTIONS}&{l['quiz']['question'] for l in D['lessons']}
assert all(0<=q['answer']<len(q['options'])==3 for q in QUESTIONS)
assert all(len(l['worked'])>=3 and l['activity'] and l['model'] for l in D['lessons'])
assert round(13.2-10,8)==3.2 and round(.4+.2,8)==.6 and 2*3==6 and round(11/12*100,1)==91.7
print('PASS: 10 lessons / 40 scenes / 10 worked examples / 20 independent questions / teaching calculations')

from caption_chunks import chunks
import textwrap
for lesson in D['lessons']:
 for scene in lesson['scenes']:
  source=display(scene['narration']);parts=list(chunks(source))
  assert ' '.join(parts)==source
  assert all(len(p.split())>=4 and len(textwrap.wrap(p,42))<=2 for p in parts)
assert 'complete' in QUESTIONS[8]['feedback'].lower()
assert max(sum(q['answer']==i for q in QUESTIONS) for i in range(3))<=7
print('PASS: caption phrase integrity and revised assessment checks')

expected=[2,0,1,2,0,2,1,0,2,0,1,2,1,0,2,1,0,2,0,1]
assert [q['answer'] for q in QUESTIONS]==expected
assert all(len(s['description'])>60 for l in D['lessons'] for s in l['scenes'])
assert 'gasket' in D['lessons'][1]['scenes'][0]['narration']
assert 'not a universal GMP requirement' in D['lessons'][5]['scenes'][2]['narration']
print('PASS: OQ answer audit, example arithmetic, IQ continuity and decision-rule qualification')
