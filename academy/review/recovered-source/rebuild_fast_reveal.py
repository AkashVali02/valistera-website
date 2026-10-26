import os,subprocess
B='/home/user/animated_gmp'; O='/home/user/fast_reveal';os.makedirs(O,exist_ok=True)
parts=[]
for i in range(1,37):
 wav=f'/home/user/premium_full/audio_{i:02}.wav'
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',wav],text=True).strip())+.75
 # first visual immediately; all diagram elements visible within 1.7 seconds
 a=min(.65,duration*.1);b=min(1.05,duration*.1);c=duration-a-b
 txt=f'{O}/frames_{i:02}.txt'
 with open(txt,'w') as f:
  for stage,seconds in [(0,a),(1,b),(2,c)]:f.write(f"file '{B}/frame_{i:02}_{stage}.png'\nduration {seconds:.5f}\n")
  f.write(f"file '{B}/frame_{i:02}_2.png'\n")
 out=f'{O}/part_{i:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-safe','0','-f','concat','-i',txt,'-i',wav,'-vf','fps=6,format=yuv420p,drawbox=x=38:y=625:w=1135:h=74:color=0x0a1930:t=fill','-af','apad=pad_dur=0.75','-t',str(duration),'-c:v','libx264','-preset','ultrafast','-crf','31','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out);print('DONE',i,flush=True)
with open(f'{O}/concat.txt','w') as f:
 for part in parts:f.write(f"file '{part}'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{O}/concat.txt','-c','copy','-movflags','+faststart',f'{O}/final.mp4'],check=True)
print('RENDER COMPLETE',flush=True)
