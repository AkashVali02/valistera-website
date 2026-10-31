from pathlib import Path
import hashlib,json,sys
S=Path(__file__).parent;A=S.parents[1]/'assets/academy/module-3'
try:
 d=json.loads((A/'media-source-sha.json').read_text())
 assert all(d.get(n)==hashlib.sha256((S/n).read_bytes()).hexdigest() for n in ['content.json','render.py','narrate.py','caption_display.py','caption_chunks.py'])
 assert all((A/f'lesson-{i}.mp4').exists() for i in range(1,11))
except Exception:sys.exit(1)
print('Media matches editorial and rendering source')
