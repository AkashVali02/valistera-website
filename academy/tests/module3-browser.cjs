const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs');
const BASE=process.env.BASE_URL||'http://127.0.0.1:8092';
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chromium',args:['--no-sandbox']});
 const result={base:BASE,browser:browser.version(),checks:[],failures:[]};
 const resultPath=process.env.RESULT_PATH||'/home/user/module3-browser-results.json';
 const persist=()=>fs.writeFileSync(resultPath,JSON.stringify(result,null,2));
 process.on('uncaughtException',e=>{result.failures.push(String(e));persist();process.exit(1)});
 process.on('unhandledRejection',e=>{result.failures.push(String(e));persist();process.exit(1)});
 const check=(name,pass,detail)=>{result.checks.push({name,pass,...(detail?{detail}:{})});if(!pass)result.failures.push(name);persist()};
 const context=await browser.newContext({viewport:{width:390,height:844}});

 const page=await context.newPage();page.setDefaultTimeout(20000);page.setDefaultNavigationTimeout(30000);let external=[];page.on('request',r=>{if(!r.url().startsWith(BASE)&&!r.url().startsWith('blob:'+new URL(BASE).origin+'/'))external.push(r.url())});
 const names=['academy-module-3.html','academy-module-3-workbook.html','academy-module-3-assessment.html','academy-module-3-sources.html','academy-module-3-review.html',...Array.from({length:10},(_,i)=>`academy-lesson-3-${i+1}.html`)];
 for(const name of names){
  await page.goto(BASE+'/'+name);
  check(name+' landmarks',await page.evaluate(()=>!!document.querySelector('body>header')&&!!document.querySelector('body>footer')&&!document.querySelector('main header,main footer')));
  await page.locator('.skip').focus();await page.keyboard.press('Enter');
  check(name+' skip focuses learning content',await page.evaluate(()=>document.activeElement.id==='main'));
  check(name+' heading',(await page.locator('h1').count())===1);
  check(name+' noindex',(await page.locator('meta[name=robots]').getAttribute('content')).includes('noindex'));
  for(const width of [320,390,768,1280]){await page.setViewportSize({width,height:900});check(name+' reflow '+width,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}
  await page.setViewportSize({width:390,height:844});
  await page.addScriptTag({path:process.env.AXE_PATH||'/home/user/module1-media/axe.min.js'});
  const violations=await page.evaluate(async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})).violations.map(v=>({id:v.id,nodes:v.nodes.length})));
  check(name+' axe',violations.length===0,violations);if(violations.length)console.error('AXE_FAILURE',name,JSON.stringify(violations));
  await page.addStyleTag({content:'*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}'});
  check(name+' text-spacing reflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 }
 await page.goto(BASE+'/academy-lesson-3-4.html');check('Worked DQ example',await page.getByRole('heading',{name:'Worked example'}).isVisible());
 await page.goto(BASE+'/academy-module-3-assessment.html');check('Open-book disclosure',(await page.locator('main').innerText()).includes('open-book'));
 check('No external subresource requests',external.length===0,external);
 for(let i=1;i<=10;i++){
  await page.goto(`${BASE}/academy-lesson-3-${i}.html`);
  check('Lesson '+i+' has four diagram disclosures',(await page.locator('.scene-explanation').count())===4);
  check('Lesson '+i+' no duplicate timeline',(await page.locator('.seek-controls,input[type=range]').count())===0);
  for(let j=0;j<4;j++){
   const disclosure=page.locator('.scene-explanation').nth(j), content=disclosure.locator('.technical-content');
   check('Lesson '+i+' diagram '+(j+1)+' entirely collapsed',!(await content.isVisible())&&!(await disclosure.locator('img').isVisible()));
   await disclosure.locator('summary').focus();await page.keyboard.press('Enter');
   check('Lesson '+i+' diagram '+(j+1)+' expands with information',await content.isVisible()&&await disclosure.locator('img').isVisible()&&(await disclosure.locator('summary').innerText()).includes('View Technical Explanation'));
   await page.keyboard.press('Enter');
   check('Lesson '+i+' diagram '+(j+1)+' closes again',!(await content.isVisible()));
  }
  check('Lesson '+i+' subtitle toggle present',(await page.locator('#toggle-captions').count())===1);
  check('Lesson '+i+' poster aspect ratio',await page.locator('#load-media img').evaluate(im=>Math.abs(im.getBoundingClientRect().width/im.getBoundingClientRect().height-16/9)<.02));
  check('Lesson '+i+' media deferred',await page.locator('video').evaluate(v=>!v.src&&v.hidden));
  await page.locator('#load-media').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>{const v=document.querySelector('video');return v.readyState>=2&&v.currentTime>.1&&!v.paused},null,{timeout:20000});
  check('Lesson '+i+' native playback',true);
  const info=await page.locator('video').evaluate(v=>({duration:v.duration,cues:v.textTracks[0]?.cues?.length||0,source:v.currentSrc,downloadSource:v.dataset.src}));
  check('Lesson '+i+' captions loaded',info.cues>0,info);
  await page.locator('video').evaluate(v=>{v.currentTime=v.duration*.65;});
  await page.waitForFunction(()=>{const v=document.querySelector('video');return Math.abs(v.currentTime/v.duration-.65)<.04});
  check('Lesson '+i+' media API seek',true); // This checks media capability, not a physical native-control tap.
  await page.waitForFunction(()=>!document.querySelector('video').seeking&&document.querySelector('video').readyState>=2);
  await page.locator('#toggle-captions').click();
  check('Lesson '+i+' captions off',await page.locator('#toggle-captions').getAttribute('aria-pressed')==='false');
  await page.locator('#toggle-captions').click();
  check('Lesson '+i+' captions on',await page.locator('#toggle-captions').getAttribute('aria-pressed')==='true');
  await page.locator('video').evaluate(v=>v.pause());
  await page.locator('video').hover();
  const session=await context.newCDPSession(page);await session.send('DOM.enable');
  for(const fraction of [.25,.75]){
   const doc=await session.send('DOM.getDocument',{depth:-1,pierce:true});
   const find=n=>n.attributes?.includes('-webkit-media-controls-timeline')?n:[...(n.children||[]),...(n.shadowRoots||[])].map(find).find(Boolean);
   const timeline=find(doc.root);if(!timeline)throw Error('Native timeline unavailable');
   const {model}=await session.send('DOM.getBoxModel',{nodeId:timeline.nodeId});const box=model.content;
   await page.mouse.click(box[0]+(box[2]-box[0])*fraction,(box[1]+box[5])/2);
   await page.waitForFunction(f=>{const v=document.querySelector('video');return !v.seeking&&Math.abs(v.currentTime/v.duration-f)<.06},fraction,{timeout:15000});
   check('Lesson '+i+' native timeline pointer '+fraction,true,{actualSeconds:await page.locator('video').evaluate(v=>v.currentTime),duration:info.duration});
  }
  await session.detach();
  const answer=await page.locator('fieldset').getAttribute('data-answer');
  await page.locator(`input[type=radio][value="${answer}"]`).check();await page.locator('form button').click();
  check('Lesson '+i+' correct answer feedback',(await page.locator('.quiz-result').innerText()).includes('1/1'));
  await page.locator(`input[type=radio][value="${(Number(answer)+1)%3}"]`).check();await page.locator('form button').click();
  check('Lesson '+i+' wrong answer feedback',(await page.locator('.quiz-result').innerText()).includes('0/1'));
 }
 await page.goto(BASE+'/academy-lesson-3-3.html');
 check('Error sum default',(await page.locator('#error-result').innerText()).includes('0.60 °C. Exceeds'));
 await page.locator('#error-1').fill('0.1');check('Error equality boundary',(await page.locator('#error-result').innerText()).includes('0.50 °C. Does not exceed'));
 await page.locator('#error-2').fill('0.1');check('Error lower sum',(await page.locator('#error-result').innerText()).includes('0.40 °C. Does not exceed'));
 await page.locator('#error-3').fill('-1');check('Reject negative bound',(await page.locator('#error-result').innerText()).includes('Enter each bound'));
 await page.goto(BASE+'/academy-lesson-3-10.html');
 for(const n of ['0','8','10']){await page.locator('#covered').fill(n);check('Coverage '+n,(await page.locator('#coverage-result').innerText()).includes(`${Number(n)*10}% coverage`));}
 await page.locator('#covered').fill('8.5');check('Coverage rejects fractional count',(await page.locator('#coverage-result').innerText()).includes('whole number'));
 await page.goto(BASE+'/academy-lesson-3-1.html');
 check('Storage defaults off',await page.evaluate(()=>localStorage.getItem('valistera_module3_v1')===null));
 await page.locator('#save-progress').check();await page.locator('#mark-studied').click();
 await page.goto(BASE+'/academy-module-3.html');check('Stored progress survives navigation',(await page.locator('#progress-text').innerText()).startsWith('1 of 10'));
 await page.evaluate(()=>localStorage.setItem('unrelated-qa','preserve'));
 await page.locator('#clear-progress').click();check('Clear isolates module',await page.evaluate(()=>localStorage.getItem('unrelated-qa')==='preserve'&&localStorage.getItem('valistera_module3_v1')===null));
 check('Clear disables saving',!(await page.locator('#save-progress').isChecked()));
 check('Clear resets session markers',(await page.locator('#progress-text').innerText()).startsWith('0 of 10'));
 await page.locator('#save-progress').check();
 await page.goto(BASE+'/academy-lesson-3-1.html');
 await page.locator('#mark-studied').click();
 await page.locator('#save-progress').uncheck();
 await page.goto(BASE+'/academy-module-3.html');
 check('Opt-out resets session markers',(await page.locator('#progress-text').innerText()).startsWith('0 of 10'));
 check('Opt-out removes saved key',await page.evaluate(()=>localStorage.getItem('valistera_module3_v1')===null));
 await page.goto(BASE+'/academy-module-3-assessment.html');
 await page.locator('form button').click();check('Unanswered assessment not scored',(await page.locator('.quiz-result').innerText())==='');
 const fields=page.locator('fieldset');for(let i=0;i<20;i++){const f=fields.nth(i);const a=await f.getAttribute('data-answer');await f.locator(`input[value="${a}"]`).check();}
 await page.locator('form button').click();check('Full assessment score',(await page.locator('.quiz-result').innerText()).startsWith('20/20'));
 for(const score of [16,17]){
  for(let i=0;i<20;i++){const f=fields.nth(i),a=Number(await f.getAttribute('data-answer'));await f.locator(`input[value="${i<score?a:(a+1)%3}"]`).check();}
  await page.locator('form button').click();const feedback=await page.locator('.quiz-result').innerText();
  check('85 percent practice boundary '+score,feedback.startsWith(`${score}/20`)&&feedback.includes('Practice target reached.')===(score>=17));
 }
 for(let i=0;i<20;i++){const f=fields.nth(i);const a=Number(await f.getAttribute('data-answer'));await f.locator(`input[value="${(a+1)%3}"]`).check();}
 await page.locator('form button').click();check('Wrong assessment score',(await page.locator('.quiz-result').innerText()).startsWith('0/20'));
 await page.goto(BASE+'/academy-module-3-workbook.html');await page.locator('#work-1').fill('Training note');await page.reload();check('Workbook text not persisted',(await page.locator('#work-1').inputValue())==='');
 // Simulate failed MP4 response and verify keyboard retry without losing transcript.
 await page.route('**/*.mp4*',route=>route.abort());await page.goto(BASE+'/academy-lesson-3-1.html');await page.locator('#load-media').click();await page.waitForFunction(()=>document.querySelector('#load-media').textContent.includes('Retry'));
 check('Media retry fallback',await page.locator('#load-media').isVisible()&&await page.locator('#transcript').isVisible());
 await page.unroute('**/*.mp4*');
 await page.locator('#load-media').click();await page.waitForFunction(()=>document.querySelector('video').currentTime>.1);check('Media retry recovers playback',true);await page.locator('video').evaluate(v=>v.pause());
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:800}});const p2=await nojs.newPage();await p2.goto(BASE+'/academy-lesson-3-1.html');check('No-JS transcript',await p2.locator('#transcript').isVisible());check('No-JS no quiz submission',await p2.locator('form button').isDisabled());
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})});const pb=await blocked.newPage();await pb.goto(BASE+'/academy-lesson-3-1.html');await pb.locator('#save-progress').click();check('Blocked storage reported',(await pb.locator('#storage-status').innerText()).includes('could not be saved'));check('Blocked storage checkbox reset',!(await pb.locator('#save-progress').isChecked()));check('Blocked storage lesson usable',await pb.locator('#load-media').isVisible());
 await page.goto(BASE+'/academy-module-3.html');await page.screenshot({path:(process.env.SCREENSHOT_DIR||'.')+'/module3-overview.png',fullPage:false});await page.goto(BASE+'/academy-lesson-3-9.html');await page.screenshot({path:(process.env.SCREENSHOT_DIR||'.')+'/module3-lesson.png',fullPage:false});
 result.completed=true;
 fs.writeFileSync(process.env.RESULT_PATH||'/home/user/module3-browser-results.json',JSON.stringify(result,null,2));console.log(JSON.stringify({checks:result.checks.length,failures:result.failures}));await browser.close();if(result.failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);const p=process.env.RESULT_PATH||'/home/user/module3-browser-results.json';const r=fs.existsSync(p)?JSON.parse(fs.readFileSync(p)): {checks:[],failures:[]};r.completed=false;r.failures.push(String(e));fs.writeFileSync(p,JSON.stringify(r,null,2));process.exit(1)});
