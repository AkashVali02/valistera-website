"""Measured synthesis boundaries, conventional display cues, complete source traceability."""
from pathlib import Path
import json,re,textwrap,subprocess,os,hashlib,math,importlib.metadata
import numpy as np
import soundfile as sf
import onnxruntime as rt
from kokoro_onnx import Kokoro
from render import D,ASSETS,draw_scene,ROOT
from caption_display import display,speech
base=Path(os.environ.get('TTS_DIR','/tmp/module3-tts'));base.mkdir(exist_ok=True);cache=base/'phrases';cache.mkdir(exist_ok=True)
opt=rt.SessionOptions();opt.intra_op_num_threads=2;opt.inter_op_num_threads=1
session=rt.InferenceSession(str(base/'kokoro-v1.0.onnx'),sess_options=opt,providers=['CPUExecutionProvider'])
# kokoro-onnx 0.4.9 casts speed to int32 for input_ids exports, truncating 0.92.
# Preserve the configured factor and the ONNX-declared float input, without changing weights.
run_onnx=session.run
def run_with_float_speed(outputs,inputs,*args,**kwargs):
 inputs=dict(inputs)
 if 'input_ids' in inputs:
  assert next(x for x in session.get_inputs() if x.name=='speed').type=='tensor(float)'
  inputs['speed']=np.array([.92],dtype=np.float32)
 return run_onnx(outputs,inputs,*args,**kwargs)
session.run=run_with_float_speed
k=Kokoro.from_session(session,str(base/'voices-v1.0.bin'))
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02}.{n%1000:03}'
from caption_chunks import chunks
manifest=[]
for l in D['lessons']:
 i=l['id'];audio=[];cues=[];scenes=[];elapsed=0;frames=[]
 for j,s in enumerate(l['scenes']):
  img=draw_scene(l,s,j);start=elapsed
  for n,phrase in enumerate(chunks(display(s['narration']))):
   spoken=speech(phrase);wav=cache/(hashlib.sha256(spoken.encode()).hexdigest()+'.wav')
   if wav.exists():a,sr=sf.read(wav,dtype='float32')
   else:a,sr=k.create(spoken,voice='af_heart',speed=.92,lang='en-us');sf.write(wav,a,sr)
   dur=len(a)/sr;required=max(2.0,len(phrase)/17)
   if dur<required:
    slow=cache/f'{i}-{j}-{n}-slow.wav';subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(wav),'-af',f'atempo={max(.5,dur/required)}',str(slow)],check=True);a,sr=sf.read(slow,dtype='float32');dur=len(a)/sr
   if dur<required:
    a=np.pad(a,(0,max(0,math.ceil((required-dur)*sr))));dur=len(a)/sr
   cues.append(dict(start=round(elapsed,3),end=round(elapsed+dur,3),text=phrase,spoken=spoken,scene=j+1));audio.extend([a,np.zeros(round(sr*.12),dtype='float32')]);elapsed+=dur+.12
  audio.append(np.zeros(round(sr*.5),dtype='float32'));elapsed+=.5
  scenes.append(dict(start=round(start,3),end=round(elapsed,3),title=s['title']));frames.append(f"file '{img}'\nduration {elapsed-start:.6f}\n")
 full=base/f'lesson-{i}.wav';sf.write(full,np.concatenate(audio),sr);timeline=base/f'lesson-{i}.txt';timeline.write_text(''.join(frames)+f"file '{img}'\n")
 out=ASSETS/f'lesson-{i}.mp4';subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(timeline),'-i',str(full),'-t',str(elapsed),'-vf','fps=10','-c:v','libx264','-preset','veryfast','-crf','27','-pix_fmt','yuv420p','-c:a','aac','-b:a','80k','-movflags','+faststart',str(out)],check=True)
 (ASSETS/f'lesson-{i}.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{n}\n{stamp(c["start"])} --> {stamp(c["end"])}\n'+'\n'.join(textwrap.wrap(c['text'],42)) for n,c in enumerate(cues,1))+'\n')
 (ASSETS/f'lesson-{i}-timing.json').write_text(json.dumps(dict(duration=elapsed,scenes=scenes,cues=cues),indent=2))
 manifest.append(dict(lesson=i,duration=elapsed,cues=len(cues),bytes=out.stat().st_size));print('COMPLETE',manifest[-1],flush=True)
(ASSETS/'media-manifest.json').write_text(json.dumps(manifest,indent=2))
provenance={'voice':'af_heart','runtime_version':importlib.metadata.version('kokoro-onnx'),'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [base/'kokoro-v1.0.onnx',base/'voices-v1.0.bin']},'source':'https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1','scope':'Observed downloaded toolchain hashes, not an independent upstream rights audit.'}
(ROOT/'academy/review/module-3/voice-provenance.json').write_text(json.dumps(provenance,indent=2))
print('ALL_COMPLETE',flush=True)
(ASSETS/'media-source-sha.json').write_text(json.dumps({name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ['content.json','render.py','narrate.py','caption_display.py','caption_chunks.py']},indent=2))
