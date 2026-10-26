/* Run from repository root. Requires playwright and axe-core (or AXE_PATH).
 * Browser routes serve repository bytes locally: this is not a deployed HTTP test.
 */
const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),assert=require('assert');
async function media(route,file,type){const bytes=fs.readFileSync(file);const range=route.request().headers()['range'];if(range){const m=/bytes=(\d+)-(\d*)/.exec(range);if(m){const start=Number(m[1]),end=m[2]?Math.min(Number(m[2]),bytes.length-1):bytes.length-1;return route.fulfill({status:206,contentType:type,headers:{'Accept-Ranges':'bytes','Content-Range':`bytes ${start}-${end}/${bytes.length}`},body:bytes.subarray(start,end+1)})}}return route.fulfill({status:200,contentType:type,headers:{'Accept-Ranges':'bytes'},body:bytes})}
const root=process.cwd(),out='academy/review/evidence-2026-10-26';
(async()=>{
const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
const rows=[],failures=[];
for(const file of (process.env.ONLY_PAGE?[process.env.ONLY_PAGE]:['academy-gmp-foundations.html','academy-player-preview.html',...Array.from({length:9},(_,i)=>`academy-lesson-1-${i+2}.html`),'academy-gmp-assessment.html'])){
 const context=await browser.newContext();const p=await context.newPage();const errors=[],requests=[],videoRequests=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(new URL(r.url()).hostname!=='academy.test')requests.push(r.url());if(new URL(r.url()).pathname.endsWith('.mp4'))videoRequests.push(r.url())});
 await p.route('http://academy.test/**',async route=>{const name=new URL(route.request().url()).pathname;const f=path.join(root,name);if(name.endsWith('.mp4')&&process.env.MEDIA_FIXTURE)return media(route,process.env.MEDIA_FIXTURE,'video/webm');if(!fs.existsSync(f))return route.fulfill({status:404});if(name.endsWith('.mp4'))return media(route,f,'video/mp4');await route.fulfill({status:200,contentType:name.endsWith('.html')?'text/html':name.endsWith('.js')?'application/javascript':name.endsWith('.css')?'text/css':name.endsWith('.vtt')?'text/vtt':name.endsWith('.mp4')?'video/mp4':'application/octet-stream',body:fs.readFileSync(f)})});
 // Test against downloaded original bytes if MEDIA_DIR is supplied; never contact external host.
 await p.route('https://*.cloudfront.net/**',async route=>{const i=file==='academy-player-preview.html'?1:Number(file.match(/1-(\d+)/)?.[1]);if(process.env.MEDIA_FIXTURE)return media(route,process.env.MEDIA_FIXTURE,'video/webm');const f=path.join(process.env.MEDIA_DIR||'/nonexistent',`lesson-${i}.mp4`);if(fs.existsSync(f))return media(route,f,'video/mp4');return route.abort()});
 const row={file,checks:[]};const check=(name,pass)=>{row.checks.push({name,pass});if(!pass)failures.push(file+': '+name)};
 await p.goto('http://academy.test/'+file);await p.addScriptTag({path:process.env.AXE_PATH||require.resolve('axe-core/axe.min.js')});const axe=await p.evaluate(()=>window.axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}}));row.axeViolations=axe.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}));row.axeIncomplete=axe.incomplete.map(v=>v.id);check('axe automated AA rules: no detected violations',!row.axeViolations.length);
 check('no external request before load',requests.length===0);check('no MP4 request before learner action',videoRequests.length===0);
 for(const width of [320,390,768,1280]){await p.setViewportSize({width,height:900});check('no horizontal overflow at '+width,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}
 await p.setViewportSize({width:390,height:844});await p.keyboard.press('Tab');check('skip link first keyboard stop',await p.locator('.skip-link').evaluate(e=>e===document.activeElement));await p.keyboard.press('Enter');check('skip link moves focus to main',await p.locator('main').evaluate(e=>e===document.activeElement));
 if(await p.locator('video').count()){
  check('radio group named',await p.locator('fieldset legend').count()===1);
  await p.locator('#check, #checkanswer').click();check('unanswered quiz feedback',/choose/i.test(await p.locator('#feedback, #quizfeedback').innerText()));
  for(const answer of ['a','c']){await p.locator(`input[value=${answer}]`).check();await p.locator('#check, #checkanswer').click();check('wrong answer '+answer+' rejected',/not quite/i.test(await p.locator('#feedback, #quizfeedback').innerText()));}
  await p.locator('input[value=b]').check();await p.locator('#check, #checkanswer').click();check('canonical correct answer accepted',/^Correct/.test(await p.locator('#feedback, #quizfeedback').innerText()));
  await p.locator('.academy-transcript summary').focus();await p.keyboard.press('Enter');check('transcript keyboard expands',await p.locator('.academy-transcript').evaluate(e=>e.open));
  await p.locator('#load-media').click();await p.waitForFunction(()=>document.querySelector('video').readyState>=1,{},{timeout:20000}).catch(()=>{});
  check('video metadata decodes',await p.locator('video').evaluate(v=>v.readyState>=1));
  if(await p.locator('video').evaluate(v=>v.readyState>=1)){
   await p.waitForFunction(()=>document.querySelector('video').textTracks[0]?.cues?.length>0,{},{timeout:5000}).catch(()=>{});
   if(['academy-lesson-1-4.html','academy-lesson-1-5.html'].includes(file)){
    const lesson=Number(file.match(/1-(\d+)/)[1]);const scenes=JSON.parse(fs.readFileSync(path.join(out,`revised-narration-1-${lesson}.json`),'utf8'));
    for(let j=0;j<scenes.length;j++){
     await p.locator('video').evaluate((v,t)=>{v.currentTime=t;v.dispatchEvent(new Event('timeupdate'))},scenes[j][0]+1);
     await p.waitForFunction(()=>!document.querySelector('video').seeking,null,{timeout:10000});
     check('revised key explanation follows scene '+(j+1),await p.evaluate(j=>document.getElementById('keytext').textContent===keys[j],j));
    }
   }
   check('native caption track parses',await p.locator('video').evaluate(v=>v.textTracks[0]?.cues?.length>0));
   await p.locator('#cc').click();check('caption toggle off',await p.locator('video').evaluate(v=>v.textTracks[0].mode==='disabled'));await p.locator('#cc').click();check('caption toggle on',await p.locator('video').evaluate(v=>v.textTracks[0].mode==='showing'));
   await p.locator('video').evaluate(v=>{v.preload='auto';v.currentTime=65});await p.waitForFunction(()=>!document.querySelector('video').seeking,{},{timeout:5000}).catch(()=>{});await p.locator('video').evaluate(v=>v.dispatchEvent(new Event('timeupdate')));
   row.savedBeforeReload=await p.evaluate(()=>({...localStorage}));await p.goto('http://academy.test/'+file+'?resume=1');await p.locator('#load-media').click();await p.waitForFunction(()=>document.querySelector('video').currentTime>=64,{},{timeout:10000}).catch(()=>{});row.savedAfterReload=await p.evaluate(()=>({...localStorage}));check('resume 65s remains paused',await p.locator('video').evaluate(v=>Math.abs(v.currentTime-65)<1&&v.paused));
  }
 }
 if(file==='academy-gmp-assessment.html'){
  await p.evaluate(()=>items.forEach((q,i)=>document.querySelector(`input[name=q${i}][value="${q[4]}"]`).click()));await p.locator('#submit').click();check('assessment 15/15',/15 \/ 15.*100%/.test(await p.locator('#score').innerText()));check('results focus',await p.locator('#results').evaluate(e=>e===document.activeElement));await p.locator('#reset').click();check('reset removes old result',await p.evaluate(()=>localStorage.getItem('valistera_gmp_module1_assessment_result')===null));check('reset enables choices',await p.locator('input:disabled').count()===0);
  await p.evaluate(()=>items.forEach((q,i)=>document.querySelector(`input[name=q${i}][value="${(q[4]+1)%3}"]`).click()));await p.locator('#submit').click();check('assessment 0/15',/0 \/ 15.*0%/.test(await p.locator('#score').innerText()));
 }
 await p.evaluate(()=>{localStorage.setItem('unrelated_test','keep');localStorage.setItem('valistera_gmp_110_quiz','passed');});await p.locator('#clear-academy-progress').click();check('clear removes Module 1 only',await p.evaluate(()=>localStorage.getItem('unrelated_test')==='keep'&&localStorage.getItem('valistera_gmp_110_quiz')===null));
 check('no external requests throughout interaction',requests.length===0);row.externalRequests=requests;row.videoRequests=videoRequests;check('no uncaught JavaScript errors',errors.length===0);row.errors=errors;
 if(file==='academy-player-preview.html')await p.screenshot({path:out+'/lesson1-mobile.png',fullPage:true});
 await context.close();rows.push(row);
}
fs.writeFileSync(out+(process.env.MEDIA_FIXTURE?'/browser-fixture-results.json':'/browser-results.json'),JSON.stringify({browser:browser.version(),routeServed:true,syntheticMediaFixture:!!process.env.MEDIA_FIXTURE,rows,failures},null,2));console.log(JSON.stringify({pages:rows.length,checks:rows.reduce((n,r)=>n+r.checks.length,0),failures}));await browser.close();process.exitCode=failures.length?1:0;
})();
