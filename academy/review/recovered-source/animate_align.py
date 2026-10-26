import os,subprocess,math
from PIL import Image,ImageDraw
from faster_whisper import WhisperModel
import soundfile as sf
B='/home/user/animated_gmp';os.makedirs(B,exist_ok=True)
base='/home/user/visual_enhanced'
model=WhisperModel('tiny.en',device='cpu',compute_type='int8')
def stamp(sec):
 h=int(sec//3600);m=int(sec%3600//60);s=sec%60
 return f'{h:02}:{m:02}:{s:06.3f}'.replace('.',',')
subs=[];elapsed=0.0;parts=[]
for i in range(1,37):
 print('SCENE',i,flush=True)
 wav=f'/home/user/premium_full/audio_{i:02}.wav'
 data,sr=sf.read(wav);duration=len(data)/sr
 # align subtitles to actual spoken audio, instead of text-length estimation
 segments,info=model.transcribe(wav,beam_size=1,word_timestamps=True,vad_filter=False)
 words=[]
 for seg in segments:
  for w in seg.words or []:
   if w.word.strip():words.append((w.start,w.end,w.word.strip()))
 for j in range(0,len(words),7):
  group=words[j:j+7];start=elapsed+group[0][0];end=elapsed+group[-1][1]
  subs.append((start,end,' '.join(w[2] for w in group)))
 image=Image.open(f'{base}/scene_{i:02}.png').convert('RGB')
 for stage in range(3):
  im=image.copy();d=ImageDraw.Draw(im)
  # staged visual reveal: expose first 1/3, 2/3, then full diagram
  if stage<2:
   top=int(259+352*(stage+1)/3)
   d.rounded_rectangle((794,top,1215,609),radius=10,fill='#102942')
   d.text((824,top+10),'Visual explanation continues…',fill='#6f91a7')
  im.save(f'{B}/frame_{i:02}_{stage}.png')
 dur=duration+0.75
 concat=f'{B}/frames_{i:02}.txt'
 with open(concat,'w') as f:
  for stage in range(3):
   f.write(f"file '{B}/frame_{i:02}_{stage}.png'\nduration {dur/3:.4f}\n")
  f.write(f"file '{B}/frame_{i:02}_2.png'\n")
 out=f'{B}/part_{i:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-safe','0','-f','concat','-i',concat,'-i',wav,'-vf','fps=6,format=yuv420p','-af','apad=pad_dur=0.75','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-c:a','aac','-b:a','96k',out],check=True)
 # use actual encoded scene length to track time
 actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',out],text=True))
 elapsed+=actual;parts.append(out)
with open(f'{B}/subtitles.srt','w') as f:
 for j,(start,end,caption) in enumerate(subs,1):
  f.write(f'{j}\n{stamp(start)} --> {stamp(end)}\n{caption}\n\n')
with open(f'{B}/concat.txt','w') as f:
 for p in parts:f.write(f"file '{p}'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/animated.mp4'],check=True)
# include selectable subtitle track in MKV and MP4 mov_text; MP4 players may or may not expose toggle
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{B}/animated.mp4','-i',f'{B}/subtitles.srt','-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=eng','-disposition:s:0','0','-movflags','+faststart',f'{B}/final_selectable.mp4'],check=True)
print('DONE',len(subs),'caption groups',flush=True)
