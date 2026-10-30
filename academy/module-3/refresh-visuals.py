from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[2];A=R/'assets/academy/module-3';e=[]
# Never reuse audio if narration, captions or synthesis configuration changed.
source=json.loads((A/'media-source-sha.json').read_text())
for name in ['content.json','narrate.py','caption_display.py']:
 assert source[name]==hashlib.sha256((R/'academy/module-3'/name).read_bytes()).hexdigest(), name
render_hash=hashlib.sha256((R/'academy/module-3/render.py').read_bytes()).hexdigest()
if source['render.py']==render_hash:
 print('Visual refresh already persisted');raise SystemExit(0)
subprocess.run(['python3',str(R/'academy/module-3/render.py')],check=True)
for i in [4,6]:
 old=A/f'lesson-{i}.mp4';t=json.loads((A/f'lesson-{i}-timing.json').read_text());seq=Path(f'/tmp/m3-{i}.txt')
 seq.write_text(''.join(f"file '{A}/lesson-{i}-scene-{j+1}.png'\nduration {s['end']-s['start']:.6f}\n" for j,s in enumerate(t['scenes']))+f"file '{A}/lesson-{i}-scene-4.png'\n")
 def audiohash(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
 before=audiohash(old);new=Path(f'/tmp/m3-{i}.mp4')
 subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(seq),'-i',str(old),'-map','0:v','-map','1:a','-t',str(t['duration']),'-vf','fps=10','-c:v','libx264','-preset','veryfast','-crf','27','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(new)],check=True)
 after=audiohash(new);assert before==after
 old.write_bytes(new.read_bytes());e.append(dict(lesson=i,audio_hash_before=before,audio_hash_after=after,audio_unchanged=True,timing_and_captions_unchanged=True))
manifest=json.loads((A/'media-manifest.json').read_text())
for x in manifest:x['bytes']=(A/f'lesson-{x["lesson"]}.mp4').stat().st_size
(A/'media-manifest.json').write_text(json.dumps(manifest,indent=2))
p=A/'media-source-sha.json';d=json.loads(p.read_text());d['render.py']=hashlib.sha256((R/'academy/module-3/render.py').read_bytes()).hexdigest();p.write_text(json.dumps(d,indent=2))
(R/'academy/review/module-3/visual-recovery.json').write_text(json.dumps(e,indent=2))
print(e)
