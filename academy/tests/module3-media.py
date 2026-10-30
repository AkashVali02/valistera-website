import json,re,subprocess,hashlib,sys
sys.path.insert(0,str(__import__("pathlib").Path(__file__).resolve().parents[1]/"module-3"))
from caption_display import display
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];A=R/'assets/academy/module-3';D=json.loads((R/'academy/module-3/content.json').read_text());rows=[]
for l in D['lessons']:
 i=l['id'];p=A/f'lesson-{i}.mp4';t=json.loads((A/f'lesson-{i}-timing.json').read_text());probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');c=t['cues'];vtt=(A/f'lesson-{i}.vtt').read_text();blocks=vtt.strip().split('\n\n')[1:]
 checks={'h264':v['codec_name']=='h264','aac':a['codec_name']=='aac','resolution':v['width']==1280 and v['height']==720,'duration':abs(float(probe['format']['duration'])-t['duration'])<.2,'caption_source_match':' '.join(x['text'] for x in c)==display(' '.join(x['narration'] for x in l['scenes'])),'cue_order':all(x['start']<x['end'] and (n==0 or x['start']>=c[n-1]['end']) for n,x in enumerate(c)),'cue_bounds':c[-1]['end']<=t['duration'],'caption_2_lines':all(len(b.splitlines()[2:])<=2 for b in blocks),'caption_42_chars':all(len(line)<=42 for b in blocks for line in b.splitlines()[2:]),'caption_speed':max(len(x['text'])/(x['end']-x['start']) for x in c)<18.5,'four_scenes':len(t['scenes'])==4,'no_orphan_cues':all(len(x['text'].split())>=3 for x in c),'scene_alignment':all(t['scenes'][x['scene']-1]['start']<=x['start']<x['end']<=t['scenes'][x['scene']-1]['end'] for x in c)}
 for j in range(1,5):
  with Image.open(A/f'lesson-{i}-scene-{j}.png') as im:im.verify()
 checks['four_pngs_decode']=True
 rows.append({'lesson':i,'duration':t['duration'],'cues':len(c),'max_cps':max(len(x['text'])/(x['end']-x['start']) for x in c),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':checks})
result={'checks':sum(len(x['checks']) for x in rows),'failures':[(x['lesson'],k) for x in rows for k,v in x['checks'].items() if not v],'duration_minutes':sum(x['duration'] for x in rows)/60,'rows':rows}
(R/'academy/review/module-3/media-results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'}));assert not result['failures']
