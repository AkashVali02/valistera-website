from pathlib import Path
import json,subprocess,shutil,zipfile,hashlib
import soundfile as sf
from kokoro_onnx import Kokoro
base=Path('/home/user'); out=base/'module1-recovery';out.mkdir(exist_ok=True)
k=Kokoro(str(base/'kokoro-v1.0.onnx'),str(base/'voices-v1.0.bin'))
replacements={4:(8,"Consider a vessel needed for a scheduled manufacturing batch. A measuring instrument used with the vessel has an expired calibration due date, and its calibration records contain no current evidence of calibration. The operator should not assume that the instrument or the planned operation is acceptable. Report the finding so authorized personnel can assess the instrument status, its intended use, and any potential product impact under site procedures. Work should proceed only after appropriate documented authorization."),5:(3,"Dispensing involves selecting and measuring the correct approved materials for a defined batch. Operators should follow authorized instructions, use suitable calibrated instruments, and document quantities and material identities. Applicable independent checks must be performed. European Union GMP requires an independent check of each dispensed material and its weight or volume, with the check recorded. United States regulations specify second-person checks, with defined exceptions for qualifying automated equipment. A local risk assessment does not waive applicable requirements. Traceability connects each dispensed material to its source and the batch in which it is used.")}
for lesson,(changed,speech) in replacements.items():
 src=base/f'lesson1{lesson}'; dest=out/f'lesson1{lesson}';dest.mkdir(exist_ok=True)
 old=json.loads((src/'timings.json').read_text());new=[];elapsed=0;parts=[]
 for n,(start,end,text) in enumerate(old,1):
  wav=src/f'audio_{n:02}.wav';img=src/f'diagram_{n:02}.png'
  if n==changed:
   text=speech; audio,sr=k.create(text,voice='af_heart',speed=.95,lang='en-us');wav=dest/f'audio_{n:02}.wav';sf.write(str(wav),audio,sr)
  duration=sf.info(str(wav)).duration+.7
  part=dest/f'part_{n:02}.mp4'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','8','-i',str(img),'-i',str(wav),'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',str(part)],check=True)
  actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(part)]))
  new.append([elapsed,elapsed+actual,text]);elapsed+=actual;parts.append(part)
 (dest/'timings.json').write_text(json.dumps(new,indent=2));(dest/'concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts))
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(dest/'concat.txt'),'-c','copy','-movflags','+faststart',str(out/f'lesson-1-{lesson}-review.mp4')],check=True)
 print('RENDERED',lesson,elapsed,flush=True)
with zipfile.ZipFile(out/'module1-source-recovery.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in [base/'premium_full.py',base/'make_lesson.py']+list(base.glob('build_lesson*.py'))+list(base.glob('lesson*_diagrams.py'))+[out/'rebuild.py']:
  if p.exists():z.write(p,'source/'+p.name)
 for l in [4,5]:
  z.write(out/f'lesson1{l}/timings.json',f'lesson1{l}/timings.json')
  for p in (base/f'lesson1{l}').glob('diagram_*.png'):z.write(p,f'lesson1{l}/'+p.name)
print('DONE',flush=True)

