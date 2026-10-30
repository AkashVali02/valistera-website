const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs');
(async()=>{
 const b=await chromium.launch({channel:'chromium',headless:true,args:['--no-sandbox']});
 const c=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true});
 const p=await c.newPage();p.setDefaultTimeout(20000);
 const result={scope:'Chromium mobile emulation with synthetic touchscreen taps, not a physical device',tested_commit:process.env.TESTED_COMMIT,checks:[],failures:[]};
 for(let i=1;i<=10;i++){
  try{
   await p.goto((process.env.BASE_URL||'http://127.0.0.1:8092')+'/academy-lesson-2-'+i+'.html');
   await p.locator('#load-media').tap();await p.waitForFunction(()=>document.querySelector('video').currentTime>.1);
   await p.locator('video').evaluate(v=>v.pause());await p.locator('video').scrollIntoViewIfNeeded();await p.locator('video').focus();
   const session=await c.newCDPSession(p);await session.send('DOM.enable');
   for(const fraction of [.33,.66]){
    const doc=await session.send('DOM.getDocument',{depth:-1,pierce:true});
    const find=n=>n.attributes?.includes('-webkit-media-controls-timeline')?n:[...(n.children||[]),...(n.shadowRoots||[])].map(find).find(Boolean);
    const timeline=find(doc.root);if(!timeline)throw Error('Native timeline missing');
    const {model}=await session.send('DOM.getBoxModel',{nodeId:timeline.nodeId});const box=model.content;
    await p.touchscreen.tap(box[0]+(box[2]-box[0])*fraction,(box[1]+box[5])/2);
    await p.waitForFunction(f=>{const v=document.querySelector('video');return !v.seeking&&Math.abs(v.currentTime/v.duration-f)<.08},fraction);
    result.checks.push({lesson:i,fraction,pass:true,actualSeconds:await p.locator('video').evaluate(v=>v.currentTime)});
   }
   await session.detach();
  }catch(e){result.failures.push({lesson:i,error:String(e)});}
 }
 result.completed=true;fs.writeFileSync(process.env.RESULT_PATH||'module2-touch-results.json',JSON.stringify(result,null,2));
 console.log(JSON.stringify(result));await b.close();if(result.failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
