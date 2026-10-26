from faster_whisper import WhisperModel
from pathlib import Path
import json,time,os
media_dir=Path(os.environ.get("MEDIA_DIR","/tmp/academy-qa"))
m=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4)
for i in range(1,11):
 p=media_dir/f'lesson-{i}.json'
 segments,info=m.transcribe(str(media_dir/f'lesson-{i}.wav'),word_timestamps=True,beam_size=5)
 out=[{'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]} for s in segments]
 p.write_text(json.dumps(out,indent=2));print(i,'done',flush=True)
