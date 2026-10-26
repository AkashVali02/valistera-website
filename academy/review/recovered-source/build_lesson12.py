import os,subprocess,ast
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
source=Path('/home/user/premium_full.py').read_text().split('k=Kokoro(')[0]
source=source.replace("B='/home/user/premium_full'","B='/home/user/lesson12'")
source=source.replace("tx(d,59,120,'LESSON 1.1  /  MODULE '+str(idx+1).zfill(2)","tx(d,59,120,'LESSON 1.2  /  TOPIC '+str(idx+1).zfill(2)")
source=source.replace("tx(d,62,643,'KEY EXPLANATION',15,CYAN,True)","tx(d,62,643,'VALISTERA ACADEMY  •  PHARMACEUTICAL QUALITY',15,CYAN,True)")
source=source.replace("excerpt=' '.join(speech.split()[:18]);lines(d,62,672,excerpt,94,14,MUT,1)","excerpt='';lines(d,62,672,excerpt,94,14,MUT,1)")
source=source.replace("if idx in (0,1,2,3,4,8,9,11):","if idx in (0,1,2,3,4,5,6,7):")
source=source.replace("labels={0:['DESIGN','CONTROL','VERIFY'],1:['RISK','PREVENT','PROTECT'],2:['PEOPLE','PROCESS','RECORDS'],3:['DETECT','ASSESS','IMPROVE'],4:['PROCESS','SAMPLE','REVIEW'],8:['PRODUCE','TEST','RELEASE'],9:['OBSERVE','INVESTIGATE','CAPA'],11:['KNOW','APPLY','REVIEW']}[idx]","labels={0:['DEFINE','IMPLEMENT','REVIEW'],1:['LEADERSHIP','PROCESS','OVERSIGHT'],2:['ASSESS','CONTROL','REVIEW'],3:['RECORD','INVESTIGATE','VERIFY'],4:['PLAN','EVALUATE','APPROVE'],5:['INSTRUCT','RECORD','REVIEW'],6:['ATTRIBUTE','PROTECT','RETRIEVE'],7:['OBSERVE','DOCUMENT','ESCALATE']}[idx]")
exec(compile(source,'lesson12_draw','exec'))
T=['PHARMACEUTICAL QUALITY SYSTEM','MANAGEMENT RESPONSIBILITY','QUALITY RISK MANAGEMENT','DEVIATIONS AND CAPA','CHANGE MANAGEMENT','GOOD DOCUMENTATION PRACTICES','DATA INTEGRITY PRINCIPLES','PRACTICAL QUALITY DECISIONS']
S=[
'A pharmaceutical quality system, often called a P Q S, brings together the people, processes and management arrangements used to maintain medicine quality. Good Manufacturing Practice is a fundamental part of this system. A strong quality system defines responsibilities, establishes procedures, monitors performance and supports continual improvement. It does not rely on final product testing alone.',
'Senior management is accountable for establishing an effective pharmaceutical quality system and providing suitable resources. Responsibilities and authorities should be clearly defined. Quality units, production teams, engineering and other functions must work together, while preserving required independent quality decisions. Management review uses information about performance, problems and improvement opportunities to guide action.',
'Quality risk management provides a structured way to assess, control, communicate and review risks to product quality. The level of formality, effort and documentation should reflect the risk and available knowledge. Risk assessments are not a substitute for meeting regulatory requirements. For example, the criticality of a temperature sensor depends on its intended function and potential effect on product quality.',
'When work departs from an approved procedure or expected result, the event should be documented and evaluated through applicable quality procedures. Investigation depth should be proportionate to the potential impact. Corrective and preventive action, or C A P A, should address identified causes where appropriate. Effectiveness checks help determine whether the action achieved its intended outcome. Not every deviation requires the same investigation or C A P A.',
'Changes to equipment, processes, software, facilities or documents can affect validated status and product quality. A formal change management process evaluates proposed changes before implementation. The assessment considers technical impact, regulatory implications, validation needs, training and required approvals. After implementation, the organization verifies that the change was completed as intended and that necessary evidence is available.',
'Good documentation practices help ensure that instructions are clear and records accurately describe work performed. An approved standard operating procedure explains how to perform a defined activity. A completed record provides evidence of what actually happened. Entries should be accurate, legible, attributable and made at the time of the activity, according to applicable procedures. Corrections must preserve the original information and remain traceable.',
'Data integrity means that information is complete, consistent and accurate throughout its lifecycle. The A L C O A principles include attributable, legible, contemporaneous, original and accurate. Additional expectations often described as A L C O A plus include complete, consistent, enduring and available. These concepts apply to both paper and electronic records. Access controls, audit trails and record retention should be appropriate to the system and its risks.',
'Consider a manufacturing vessel whose critical instrument has an expired calibration status. The operator should not simply ignore the finding. The equipment suitability and potential product quality impact must be assessed under approved site procedures. The decision, rationale and any necessary corrective action should be documented. This example connects the pharmaceutical quality system, risk management and good documentation practices to a real operational decision.'
]
topics=[[(h,b)]*3 for h,b in [('QUALITY SYSTEM','Integrated processes and oversight'),('ACCOUNTABILITY','Leadership and defined responsibilities'),('RISK-BASED THINKING','Assess risks proportionately'),('DEVIATION MANAGEMENT','Investigate and verify actions'),('CONTROLLED CHANGE','Evaluate before implementation'),('DOCUMENTATION','Instructions and executed evidence'),('DATA INTEGRITY','ALCOA and ALCOA plus principles'),('QUALITY DECISIONS','Assess, document and escalate')]]
scenes=[(i,0,T[i],S[i]) for i in range(len(T))]
k=Kokoro('/home/user/kokoro-v1.0.onnx','/home/user/voices-v1.0.bin')
parts=[];times=[];elapsed=0
for number,(idx,part,title,speech) in enumerate(scenes,1):
 print('SCENE',number,flush=True)
 img=draw(idx,part,title,speech,number)
 audio,sr=k.create(speech,voice='af_heart',speed=.95,lang='en-us')
 wav=f'{B}/audio_{number:02}.wav';sf.write(wav,audio,sr)
 dur=len(audio)/sr+0.7;times.append((round(elapsed,2),round(elapsed+dur,2),speech));elapsed+=dur
 out=f'{B}/part_{number:02}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','6','-i',img,'-i',wav,'-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','31','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out],check=True)
 parts.append(out)
Path(f'{B}/concat.txt').write_text(''.join("file '"+p+"'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{B}/concat.txt','-c','copy','-movflags','+faststart',f'{B}/lesson12.mp4'],check=True)
import json
Path(f'{B}/timings.json').write_text(json.dumps(times))
print('DONE',round(elapsed,1),flush=True)
