"""Compare all encoded scene midpoints with their intended diagram PNGs."""
from pathlib import Path
import subprocess,json,hashlib,io
from PIL import Image,ImageChops,ImageStat
R=Path(__file__).resolve().parents[2];A=R/'assets/academy/module-3';rows=[]
for i in range(1,11):
 video=A/f'lesson-{i}.mp4';timing=json.loads((A/f'lesson-{i}-timing.json').read_text())
 for j,scene in enumerate(timing['scenes'],1):
  midpoint=(scene['start']+scene['end'])/2;png=A/f'lesson-{i}-scene-{j}.png'
  raw=subprocess.check_output(['ffmpeg','-loglevel','error','-ss',str(midpoint),'-i',str(video),'-frames:v','1','-f','image2pipe','-vcodec','png','-threads','1','-'])
  actual=Image.open(io.BytesIO(raw)).convert('RGB');expected=Image.open(png).convert('RGB')
  error=sum(ImageStat.Stat(ImageChops.difference(actual,expected)).mean)/3
  rows.append(dict(lesson=i,scene=j,midpoint=midpoint,mean_rgb_error=error,passed=error<8,png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest()))
result=dict(checks=len(rows),failures=[r for r in rows if not r['passed']],maximum_rgb_error=max(r['mean_rgb_error'] for r in rows),rows=rows)
(R/'academy/review/module-3/frame-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='rows'}));assert not result['failures']
