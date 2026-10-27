"""Replace slide frames in existing MP4s while preserving original recorded audio."""
from pathlib import Path
import json, subprocess, tempfile
root=Path(__file__).resolve().parents[2]/'assets/academy/module-2'
for i in range(1,11):
    data=json.loads((root/f'lesson-{i}-timing.json').read_text())
    scenes=data['scenes']
    with tempfile.TemporaryDirectory() as td:
        timeline=Path(td)/'frames.txt'
        timeline.write_text(''.join("file '"+str((root/f'lesson-{i}-scene-{j}.png').resolve())+"'\nduration "+str(round(float(scene['end'])-float(scene['start']),6))+"\n" for j,scene in enumerate(scenes,1))+"file '"+str((root/f'lesson-{i}-scene-4.png').resolve())+"'\n")
        source=root/f'lesson-{i}.mp4'
        output=Path(td)/'rebuilt.mp4'
        subprocess.run(['ffmpeg','-y','-nostdin','-loglevel','error','-f','concat','-safe','0','-i',str(timeline),'-i',str(source),'-map','0:v:0','-map','1:a:0','-t',str(data['duration']),'-vf','fps=10','-c:v','libx264','-preset','veryfast','-crf','29','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True)
        output.replace(source)
    print('Rebuilt lesson',i,flush=True)
