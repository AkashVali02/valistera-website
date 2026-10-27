/* Module 2: no third-party requests; optional, isolated browser progress. */
(() => {
'use strict';
const KEY='valistera_module2_v1';
let state={enabled:false,studied:[],passed:[],score:null};
const status=document.getElementById('storage-status');
try {
 const saved=JSON.parse(localStorage.getItem(KEY)||'null');
 if(saved?.enabled===true)state={enabled:true,studied:Array.isArray(saved.studied)?saved.studied.filter(n=>Number.isInteger(n)&&n>=1&&n<=10):[],passed:Array.isArray(saved.passed)?saved.passed.filter(n=>Number.isInteger(n)&&n>=1&&n<=10):[],score:Number.isInteger(saved.score)&&saved.score>=0&&saved.score<=20?saved.score:null};
}catch(_){status.textContent='Device storage is unavailable or unreadable. Learning still works.';}
const saveBox=document.getElementById('save-progress');saveBox.checked=state.enabled;
function save(){if(!state.enabled)return false;try{localStorage.setItem(KEY,JSON.stringify(state));return true;}catch(_){status.textContent='Progress could not be saved on this device. Learning still works.';return false;}}
function refresh(){
 const n=new Set(state.studied).size,p=new Set(state.passed).size;
 const el=document.getElementById('progress-text');if(el)el.textContent=`${n} of 10 lessons marked studied · ${p} of 10 checks passed`;
 const bar=document.getElementById('progress-bar');if(bar)bar.value=n;
 const a=document.getElementById('assessment-status');if(a)a.textContent=state.score===null?'Final assessment not completed.':`Latest final score: ${state.score}/20. ${state.score>=16?'Practice target reached.':'Review explanations and retry.'}`;
 const st=document.getElementById('studied-status');if(st)st.textContent=state.studied.includes(Number(document.body.dataset.lesson))?'Marked studied. This is a self-study indicator.':'';
}
saveBox.addEventListener('change',()=>{state.enabled=saveBox.checked;if(state.enabled){if(save())status.textContent='Device saving enabled. Workbook answers are not saved.';}else{try{localStorage.removeItem(KEY);status.textContent='Device saving disabled; saved Module 2 data removed.';}catch(_){status.textContent='Could not remove stored data. Use browser site-data settings.';}}});
document.getElementById('clear-progress').addEventListener('click',()=>{state={enabled:false,studied:[],passed:[],score:null};saveBox.checked=false;try{localStorage.removeItem(KEY);status.textContent='Module 2 progress cleared. Device saving is off.';}catch(_){status.textContent='Could not clear device storage. Use browser site-data settings.';}refresh();});
const load=document.getElementById('load-media'),video=document.getElementById('video'),mediaStatus=document.getElementById('media-status');
if(load&&video){
 load.addEventListener('click',()=>{load.hidden=true;video.hidden=false;video.src=video.dataset.src;video.preload='metadata';video.load();mediaStatus.textContent='Starting lesson…';video.focus();video.play().catch(()=>{if(!video.error)mediaStatus.textContent='Use the player’s play button to continue.';});});
 video.addEventListener('playing',()=>{mediaStatus.textContent='';});
 video.addEventListener('error',()=>{mediaStatus.textContent='Video unavailable. Retry or read the complete lesson below.';load.querySelector('.academy-play-label').textContent='Retry lesson';load.setAttribute('aria-label','Retry lesson video');load.hidden=false;video.hidden=true;if(document.activeElement===video)load.focus();});
}
document.getElementById('mark-studied')?.addEventListener('click',()=>{const id=Number(document.body.dataset.lesson);if(!state.studied.includes(id))state.studied.push(id);save();refresh();});
for(const form of document.querySelectorAll('form.quiz')){form.querySelector('button[type=submit]').disabled=false;form.addEventListener('submit',event=>{
 event.preventDefault();if(!form.reportValidity())return;
 let correct=0;const fields=[...form.querySelectorAll('fieldset')];
 fields.forEach(field=>{const chosen=Number(field.querySelector('input:checked').value),answer=Number(field.dataset.answer);const right=chosen===answer;if(right)correct++;
 field.querySelector('.feedback').textContent=(right?'Correct. ':'Review this answer. ')+field.dataset.feedback;
 });
 const result=form.querySelector('.quiz-result');result.textContent=`${correct}/${fields.length} correct. `+(correct/fields.length>=.8?'Practice target reached.':'Review the explanations and try again.');
 if(form.dataset.final){state.score=correct;result.focus();}
 else if(correct===fields.length){const id=Number(form.dataset.lesson);if(!state.passed.includes(id))state.passed.push(id);}
 save();refresh();
});}
const risk=document.getElementById('risk-score');
if(risk){const fields=['severity','occurrence','detection'].map(id=>document.getElementById(id));const update=()=>{const v=fields.map(f=>Number(f.value));risk.textContent=`${v.join(' × ')} = ${v.reduce((a,b)=>a*b,1)}`;document.getElementById('risk-context').textContent=(v[0]===3?'Higher severity needs explicit attention. ':'')+'This score is not a release decision. Review severity, uncertainty and control effectiveness.';};fields.forEach(f=>f.addEventListener('change',update));update();}
const limit=document.getElementById('data-limit');if(limit)limit.addEventListener('input',()=>{const n=limit.valueAsNumber;const result=document.getElementById('data-result');if(!Number.isFinite(n)||n<0||n>2){result.textContent='Enter a limit from 0 to 2 °C for this exercise.';return;}const data=[.1,.2,.1,.3,.2,.4,.3,.5,.4,.6];result.textContent=`Mean ${(data.reduce((a,b)=>a+b,0)/data.length).toFixed(2)} °C · Range ${(Math.max(...data)-Math.min(...data)).toFixed(2)} °C · ${data.filter(v=>Math.abs(v)>n+1e-12).length} of 10 above ${n.toFixed(2)} °C.`;});
document.getElementById('print-workbook')?.addEventListener('click',()=>window.print());
refresh();
})();
