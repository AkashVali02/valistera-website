/* Module 3: no third-party requests; optional, isolated browser progress. */
(() => {
'use strict';
const KEY='valistera_module3_v1';
// Arithmetic round-off guard only, not a measurement uncertainty allowance.
function exceedsAbsoluteLimit(value, limit){return Math.abs(value)>limit+1e-12;}
let state={enabled:false,studied:[],passed:[],score:null};
const status=document.getElementById('storage-status');
try {
 const saved=JSON.parse(localStorage.getItem(KEY)||'null');
 if(saved?.enabled===true)state={enabled:true,studied:Array.isArray(saved.studied)?saved.studied.filter(n=>Number.isInteger(n)&&n>=1&&n<=10):[],passed:Array.isArray(saved.passed)?saved.passed.filter(n=>Number.isInteger(n)&&n>=1&&n<=10):[],score:Number.isInteger(saved.score)&&saved.score>=0&&saved.score<=20?saved.score:null};
}catch(_){status.textContent='Device storage is unavailable or unreadable. Learning still works.';}
const saveBox=document.getElementById('save-progress');saveBox.checked=state.enabled;
function save(){if(!state.enabled)return false;try{localStorage.setItem(KEY,JSON.stringify(state));return true;}catch(_){state.enabled=false;saveBox.checked=false;status.textContent='Progress could not be saved on this device. Device saving remains off; learning still works.';return false;}}
function refresh(){
 const n=new Set(state.studied).size,p=new Set(state.passed).size;
 const el=document.getElementById('progress-text');if(el)el.textContent=`${n} of 10 lessons marked studied · ${p} of 10 checks passed`;
 const bar=document.getElementById('progress-bar');if(bar)bar.value=n;
 const a=document.getElementById('assessment-status');if(a)a.textContent=state.score===null?'Final assessment not completed.':`Latest final score: ${state.score}/20. ${state.score>=17?'Practice target reached.':'Review explanations and retry.'}`;
 const st=document.getElementById('studied-status');if(st)st.textContent=state.studied.includes(Number(document.body.dataset.lesson))?'Marked studied. This is a self-study indicator.':'';
}
saveBox.addEventListener('change',()=>{state.enabled=saveBox.checked;if(state.enabled){if(save())status.textContent='Device saving enabled. Workbook answers are not saved.';}else{state={enabled:false,studied:[],passed:[],score:null};refresh();try{localStorage.removeItem(KEY);status.textContent='Device saving disabled; saved Module 3 data removed and this session’s progress reset.';}catch(_){status.textContent='Could not remove stored data. Use browser site-data settings.';}}});
document.getElementById('clear-progress').addEventListener('click',()=>{state={enabled:false,studied:[],passed:[],score:null};saveBox.checked=false;try{localStorage.removeItem(KEY);status.textContent='Module 3 progress cleared. Device saving is off.';}catch(_){status.textContent='Could not clear device storage. Use browser site-data settings.';}refresh();});
const load=document.getElementById('load-media'),video=document.getElementById('video'),mediaStatus=document.getElementById('media-status');
if(load&&video){
 // Static hosting may ignore byte ranges. A complete, small local Blob gives
 // native controls a genuinely seekable source without a second timeline.
 let objectUrl=null,loading=false;
 const showMediaError=()=>{mediaStatus.textContent='Video unavailable. Retry or read the complete lesson below.';load.querySelector('.academy-play-label').textContent='Retry lesson';load.setAttribute('aria-label','Retry lesson video');load.hidden=false;video.hidden=true;load.disabled=false;if(document.activeElement===video)load.focus();};
 load.addEventListener('click',async()=>{
  if(loading)return;loading=true;load.disabled=true;mediaStatus.textContent='Loading lesson video…';
  const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),60000);
  try{
   const response=await fetch(video.dataset.src,{signal:controller.signal});
   if(!response.ok)throw new Error('Media response '+response.status);
   const blob=await response.blob();if(!blob.size)throw new Error('Empty media');
   if(objectUrl)URL.revokeObjectURL(objectUrl);objectUrl=URL.createObjectURL(blob);
   load.hidden=true;video.hidden=false;video.src=objectUrl;video.preload='auto';video.load();video.focus();
   await video.play().catch(()=>{if(!video.error)mediaStatus.textContent='Use the player’s play button to continue.';});
  }catch(_){showMediaError();}finally{clearTimeout(timeout);loading=false;load.disabled=false;}
 });
 window.addEventListener('pagehide',e=>{if(!e.persisted&&objectUrl)URL.revokeObjectURL(objectUrl);});
 const captionsButton=document.getElementById('toggle-captions');
 const captionsStatus=document.getElementById('caption-status');
 if(captionsButton){
  let captionsOn=true;
  const applyCaptions=()=>{for(const track of video.textTracks)if(track.kind==='captions'||track.kind==='subtitles')track.mode=captionsOn?'showing':'disabled';captionsButton.setAttribute('aria-pressed',String(captionsOn));captionsButton.textContent='Subtitles: '+(captionsOn?'On':'Off');if(captionsStatus)captionsStatus.textContent=captionsOn?'English subtitles enabled.':'English subtitles disabled.';};
  captionsButton.addEventListener('click',()=>{captionsOn=!captionsOn;applyCaptions();});
  video.addEventListener('loadedmetadata',applyCaptions);
  video.addEventListener('loadeddata',applyCaptions);
  video.querySelector('track')?.addEventListener('load',applyCaptions);
  captionsButton.hidden=false;applyCaptions();
 }
 video.addEventListener('playing',()=>{mediaStatus.textContent='';});
 video.addEventListener('error',showMediaError);
}
document.getElementById('mark-studied')?.addEventListener('click',()=>{const id=Number(document.body.dataset.lesson);if(!state.studied.includes(id))state.studied.push(id);save();refresh();});
for(const form of document.querySelectorAll('form.quiz')){form.querySelector('button[type=submit]').disabled=false;form.addEventListener('submit',event=>{
 event.preventDefault();if(!form.reportValidity())return;
 let correct=0;const fields=[...form.querySelectorAll('fieldset')];
 fields.forEach(field=>{const chosen=Number(field.querySelector('input:checked').value),answer=Number(field.dataset.answer);const right=chosen===answer;if(right)correct++;
 field.querySelector('.feedback').textContent=(right?'Correct. ':'Review this answer. ')+field.dataset.feedback;
 });
 const result=form.querySelector('.quiz-result');result.textContent=`${correct}/${fields.length} correct. `+(correct/fields.length>=(form.dataset.final ? .85 : 1)?'Practice target reached.':'Review the explanations and try again.');
 if(form.dataset.final){state.score=correct;result.focus();}
 else if(correct===fields.length){const id=Number(form.dataset.lesson);if(!state.passed.includes(id))state.passed.push(id);}
 save();refresh();
});}
const sumInputs=[...document.querySelectorAll('[data-error-component]')];
function errorBudget(){const values=sumInputs.map(x=>x.valueAsNumber),out=document.getElementById('error-result');if(!out)return;if(values.some(x=>!Number.isFinite(x)||x<0||x>2)){out.textContent='Enter each bound from 0 to 2 °C.';return;}const sum=values.reduce((a,b)=>a+b,0);out.textContent=`Worst-case sum: ${sum.toFixed(2)} °C. ${exceedsAbsoluteLimit(sum,.5)?'Exceeds':'Does not exceed'} the fictional 0.50 °C requirement. This is not a complete uncertainty budget or approval.`;}
sumInputs.forEach(x=>x.addEventListener('input',errorBudget));errorBudget();
const coverage=document.getElementById('covered');if(coverage){const update=()=>{const n=coverage.valueAsNumber;document.getElementById('coverage-result').textContent=Number.isInteger(n)&&n>=0&&n<=10?`${n} of 10 = ${n*10}% coverage. Review important gaps and evidence; no percentage authorizes use.`:'Enter a whole number from 0 to 10.';};coverage.addEventListener('input',update);update();}
document.getElementById('print-workbook')?.addEventListener('click',()=>window.print());
refresh();
})();
