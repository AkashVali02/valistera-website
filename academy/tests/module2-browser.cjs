const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs');
const BASE=process.env.BASE_URL||'http://127.0.0.1:8092';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const result={base:BASE,browser:browser.version(),checks:[],failures:[]};
 const check=(name,pass,detail)=>{result.checks.push({name,pass,...(detail?{detail}:{})});if(!pass)result.failures.push(name)};
 const context=await browser.newContext({viewport:{width:390,height:844}});
 const page=await context.newPage();let external=[];page.on('request',r=>{if(!r.url().startsWith(BASE))external.push(r.url())});
 const names=['academy-module-2.html','academy-module-2-workbook.html','academy-module-2-assessment.html','academy-module-2-sources.html','academy-module-2-review.html',...Array.from({length:10},(_,i)=>`academy-lesson-2-${i+1}.html`)];
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
  check(name+' axe',violations.length===0,violations);
  await page.addStyleTag({content:'*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}'});
  check(name+' text-spacing reflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 }
 await page.goto(BASE+'/academy-lesson-2-4.html');check('Worked measurable URS',await page.getByRole('heading',{name:'Worked artefact: a measurable URS'}).isVisible());
 await page.goto(BASE+'/academy-module-2-assessment.html');check('Open-book disclosure',(await page.locator('main').innerText()).includes('open-book'));
 check('No external subresource requests',external.length===0,external);
 for(let i=1;i<=10;i++){
  await page.goto(`${BASE}/academy-lesson-2-${i}.html`);
  check('Lesson '+i+' media deferred',await page.locator('video').evaluate(v=>!v.src&&v.hidden));
  await page.locator('#load-media').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>{const v=document.querySelector('video');return v.readyState>=2&&v.currentTime>.1&&!v.paused},null,{timeout:20000});
  check('Lesson '+i+' native playback',true);
  const info=await page.locator('video').evaluate(v=>({duration:v.duration,cues:v.textTracks[0]?.cues?.length||0,source:v.currentSrc}));
  check('Lesson '+i+' captions loaded',info.cues>0,info);
  await page.locator('video').evaluate(v=>v.pause());
  const answer=await page.locator('fieldset').getAttribute('data-answer');
  await page.locator(`input[type=radio][value="${answer}"]`).check();await page.locator('form button').click();
  check('Lesson '+i+' correct answer feedback',(await page.locator('.quiz-result').innerText()).includes('1/1'));
  await page.locator(`input[type=radio][value="${(Number(answer)+1)%3}"]`).check();await page.locator('form button').click();
  check('Lesson '+i+' wrong answer feedback',(await page.locator('.quiz-result').innerText()).includes('0/1'));
 }
 await page.goto(BASE+'/academy-lesson-2-7.html');
 await page.selectOption('#severity','3');await page.selectOption('#occurrence','1');await page.selectOption('#detection','2');
 check('Risk arithmetic',(await page.locator('#risk-score').innerText())==='3 × 1 × 2 = 6');
 check('Risk severity warning',(await page.locator('#risk-context').innerText()).includes('Higher severity'));
 await page.goto(BASE+'/academy-lesson-2-9.html');
 check('Data default',(await page.locator('#data-result').innerText()).includes('1 of 10'));
 await page.locator('#data-limit').fill('0.3');check('Data recompute',(await page.locator('#data-result').innerText()).includes('4 of 10'));
 for(const [limit,count] of [['0.5',1],['0.30000000000000004',4],['0.499999',2],['0.500001',1]]){await page.locator('#data-limit').fill(limit);check('Data boundary '+limit,(await page.locator('#data-result').innerText()).includes(count+' of 10'));}
 await page.locator('#data-limit').fill('-1');check('Invalid data limit',(await page.locator('#data-result').innerText()).includes('Enter a limit'));
 await page.goto(BASE+'/academy-lesson-2-1.html');
 check('Storage defaults off',await page.evaluate(()=>localStorage.getItem('valistera_module2_v1')===null));
 await page.locator('#save-progress').check();await page.locator('#mark-studied').click();
 await page.goto(BASE+'/academy-module-2.html');check('Stored progress survives navigation',(await page.locator('#progress-text').innerText()).startsWith('1 of 10'));
 await page.evaluate(()=>localStorage.setItem('unrelated-qa','preserve'));
 await page.locator('#clear-progress').click();check('Clear isolates module',await page.evaluate(()=>localStorage.getItem('unrelated-qa')==='preserve'&&localStorage.getItem('valistera_module2_v1')===null));
 check('Clear disables saving',!(await page.locator('#save-progress').isChecked()));
 await page.goto(BASE+'/academy-module-2-assessment.html');
 await page.locator('form button').click();check('Unanswered assessment not scored',(await page.locator('.quiz-result').innerText())==='');
 const fields=page.locator('fieldset');for(let i=0;i<20;i++){const f=fields.nth(i);const a=await f.getAttribute('data-answer');await f.locator(`input[value="${a}"]`).check();}
 await page.locator('form button').click();check('Full assessment score',(await page.locator('.quiz-result').innerText()).startsWith('20/20'));
 for(let i=0;i<20;i++){const f=fields.nth(i);const a=Number(await f.getAttribute('data-answer'));await f.locator(`input[value="${(a+1)%3}"]`).check();}
 await page.locator('form button').click();check('Wrong assessment score',(await page.locator('.quiz-result').innerText()).startsWith('0/20'));
 await page.goto(BASE+'/academy-module-2-workbook.html');await page.locator('#work-1').fill('Training note');await page.reload();check('Workbook text not persisted',(await page.locator('#work-1').inputValue())==='');
 // Simulate failed MP4 response and verify keyboard retry without losing transcript.
 await page.route('**/*.mp4',route=>route.abort());await page.goto(BASE+'/academy-lesson-2-1.html');await page.locator('#load-media').click();await page.waitForFunction(()=>document.querySelector('#load-media').textContent.includes('Retry'));
 check('Media retry fallback',await page.locator('#load-media').isVisible()&&await page.locator('#transcript').isVisible());
 await page.unroute('**/*.mp4');
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:800}});const p2=await nojs.newPage();await p2.goto(BASE+'/academy-lesson-2-1.html');check('No-JS transcript',await p2.locator('#transcript').isVisible());check('No-JS no quiz submission',await p2.locator('form button').isDisabled());
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})});const pb=await blocked.newPage();await pb.goto(BASE+'/academy-lesson-2-1.html');await pb.locator('#save-progress').check();check('Blocked storage reported',(await pb.locator('#storage-status').innerText()).includes('could not be saved'));check('Blocked storage lesson usable',await pb.locator('#load-media').isVisible());
 await page.goto(BASE+'/academy-module-2.html');await page.screenshot({path:'/home/user/module2-overview.png',fullPage:false});await page.goto(BASE+'/academy-lesson-2-9.html');await page.screenshot({path:'/home/user/module2-lesson.png',fullPage:false});
 fs.writeFileSync(process.env.RESULT_PATH||'/home/user/module2-browser-results.json',JSON.stringify(result,null,2));console.log(JSON.stringify({checks:result.checks.length,failures:result.failures}));await browser.close();if(result.failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
