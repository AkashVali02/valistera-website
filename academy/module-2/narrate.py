"""Synthesize short phrases; exact audio boundaries generate captions. No ASR invented timestamps."""
from pathlib import Path
import json,re,textwrap,subprocess,os,hashlib
import numpy as np
import soundfile as sf
import onnxruntime as rt
from kokoro_onnx import Kokoro
from render import D,ASSETS,draw_scene
base=Path('/home/user');cache=base/'module2-audio';cache.mkdir(exist_ok=True)
opt=rt.SessionOptions();opt.intra_op_num_threads=2;opt.inter_op_num_threads=1
k=Kokoro.from_session(rt.InferenceSession(str(base/'kokoro-v1.0.onnx'),sess_options=opt,providers=['CPUExecutionProvider']),str(base/'voices-v1.0.bin'))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
def chunks(text):
 for sentence in re.split(r'(?<=[.!?])\s+',text):
  words=sentence.split()
  while words:
   n=min(13,len(words))
   if len(words)>13:
    candidates=[i+1 for i,w in enumerate(words[:13]) if i>=6 and w.endswith((',', ';', ':'))]
    if candidates:n=candidates[-1]
   while len(' '.join(words[:n]))>74 and n>1:n-=1
   yield ' '.join(words[:n]);words=words[n:]
manifest=[]
for l in D['lessons']:
 i=l['id'];audio=[];cues=[];scenes=[];elapsed=0;imageconcat=[]
 for j,s in enumerate(l['scenes']):
  img=draw_scene(l,s,j);start=elapsed
  for n,phrase in enumerate(chunks(s['narration'])):
   wav=cache/(hashlib.sha256(phrase.encode()).hexdigest()+'.wav')
   if wav.exists():a,sr=sf.read(wav,dtype='float32')
   else:
    a,sr=k.create(phrase,voice='af_heart',speed=.90,lang='en-us');sf.write(wav,a,sr)
   dur=len(a)/sr
   # Slow unusually fast phrases to <=18 visible characters/sec, preserving pitch.
   required=max(1.1,len(phrase)/18)
   if dur<required:
    slow=cache/f'{i}-{j}-{n}-slow.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(wav),'-af',f'atempo={max(.5,dur/required)}',str(slow)],check=True)
    a,sr=sf.read(slow,dtype='float32');dur=len(a)/sr
   cues.append(dict(start=round(elapsed,3),end=round(elapsed+dur,3),text=phrase,scene=j+1))
   audio.extend([a,np.zeros(round(sr*.15),dtype='float32')]);elapsed+=dur+.15
  audio.append(np.zeros(round(sr*.6),dtype='float32'));elapsed+=.6
  scenes.append(dict(start=round(start,3),end=round(elapsed,3),title=s['title']))
  imageconcat.append(f"file '{img}'\nduration {elapsed-start:.6f}\n")
 full=cache/f'lesson-{i}.wav';sf.write(full,np.concatenate(audio),sr)
 timeline=cache/f'lesson-{i}.txt';timeline.write_text(''.join(imageconcat)+f"file '{img}'\n")
 out=ASSETS/f'lesson-{i}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(timeline),'-i',str(full),'-t',str(elapsed),'-vf','fps=10','-c:v','libx264','-preset','veryfast','-crf','29','-pix_fmt','yuv420p','-c:a','aac','-b:a','80k','-movflags','+faststart',str(out)],check=True)
 (ASSETS/f'lesson-{i}.vtt').write_text('WEBVTT\n\n'+ '\n\n'.join(f'{n+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n'+ '\n'.join(textwrap.wrap(c['text'],42)) for n,c in enumerate(cues))+'\n')
 (ASSETS/f'lesson-{i}-timing.json').write_text(json.dumps(dict(duration=elapsed,scenes=scenes,cues=cues),indent=2))
 manifest.append(dict(lesson=i,duration=elapsed,cues=len(cues),bytes=out.stat().st_size))
 print('COMPLETE',manifest[-1],flush=True)
 # Upload each completed render before advancing; presigned destinations supplied by tool.
 uploads=json.loads((base/'module2-uploads.json').read_text())
 u=uploads[i-1]
 subprocess.run(['curl','-fsS','-X','PUT','-H','Content-Type: video/mp4','-H','If-None-Match: *','--upload-file',str(out),u['upload_url']],check=True)
(ASSETS/'media-manifest.json').write_text(json.dumps(manifest,indent=2))
print('ALL_COMPLETE',flush=True)
