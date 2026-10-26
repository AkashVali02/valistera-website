/* Supplemental media/accessibility evidence; route-served preview, not device certification. */
const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox'],...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
 const root=process.cwd(),rows=[];
 const pages=['academy-gmp-foundations.html','academy-player-preview.html',...Array.from({length:9},(_,i)=>`academy-lesson-1-${i+2}.html`),'academy-gmp-assessment.html'];
 for(const file of pages){
  const p=await b.newPage({viewport:{width:1280,height:900}});let row={file,checks:[]};const check=(name,pass,detail)=>row.checks.push({name,pass,detail});
  await p.route('**/*',async r=>{
   const u=new URL(r.request().url());let f;
   if(u.hostname==='academy.test')f=path.join(root,u.pathname);
   else if(u.hostname.endsWith('cloudfront.net')){const i=file==='academy-player-preview.html'?1:Number(file.match(/1-(\d+)/)?.[1]);f=path.join(process.env.MEDIA_DIR,`lesson-${i}.mp4`);}
   else return r.abort();
   if(!fs.existsSync(f))return r.fulfill({status:404});
   const body=fs.readFileSync(f),ext=path.extname(f),type={'.html':'text/html','.js':'application/javascript','.css':'text/css','.vtt':'text/vtt','.mp4':'video/mp4'}[ext]||'application/octet-stream';
   const m=/bytes=(\d+)-(\d*)/.exec(r.request().headers().range||'');
   if(m){const a=+m[1],z=m[2]?Math.min(+m[2],body.length-1):body.length-1;return r.fulfill({status:206,contentType:type,headers:{'Content-Range':`bytes ${a}-${z}/${body.length}`,'Accept-Ranges':'bytes'},body:body.subarray(a,z+1)})}
   return r.fulfill({contentType:type,body});
  });
  await p.goto('http://academy.test/'+file);
  await p.locator('details').evaluateAll(es=>es.forEach(e=>e.open=true));
  for(const zoom of [2,4]){
   await p.evaluate(z=>{document.documentElement.style.zoom=z},zoom);
   check('CSS layout zoom '+zoom+'x: no horizontal overflow',await p.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth+1));
  }
  await p.evaluate(()=>document.documentElement.style.zoom=1);
  await p.addStyleTag({content:'*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}'});
  for(const width of [320,1280]){
   await p.setViewportSize({width,height:900});
   const result=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,clipped:[...document.querySelectorAll('p,h1,h2,h3,button,summary,label,a')].filter(e=>e.getClientRects().length&&getComputedStyle(e).overflow==='hidden'&&(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1)).map(e=>e.textContent.slice(0,80))}));
   check('text spacing at '+width,!result.overflow&&!result.clipped.length,result);
  }
  const client=await p.context().newCDPSession(p);const ax=await client.send('Accessibility.getFullAXTree');
  const nodes=ax.nodes.filter(n=>!n.ignored);check('accessibility tree exposes main landmark',nodes.some(n=>n.role?.value==='main'));
  check('named buttons in accessibility tree',nodes.filter(n=>n.role?.value==='button').every(n=>n.name?.value));
  row.axRoles=nodes.reduce((a,n)=>(a[n.role.value]=(a[n.role.value]||0)+1,a),{});
  if(await p.locator('video').count()){
   await p.setViewportSize({width:1280,height:900});await p.locator('#load-media').click();
   await p.waitForFunction(()=>document.querySelector('video').readyState>=2,null,{timeout:20000}).catch(()=>{});
   row.media=await p.locator('video').evaluate(v=>({duration:v.duration,readyState:v.readyState,codec:v.canPlayType('video/mp4; codecs="avc1.42E01E, mp4a.40.2"')}));
   check('real H264 media ready',row.media.readyState>=2);
   if(row.media.readyState>=2){
    for(const fraction of [.05,.5,.95]){
     await p.locator('video').evaluate((v,f)=>{v.muted=true;v.currentTime=v.duration*f},fraction);
     await p.waitForFunction(()=>!document.querySelector('video').seeking,null,{timeout:10000});
     const before=await p.locator('video').evaluate(v=>({time:v.currentTime,frames:v.getVideoPlaybackQuality().totalVideoFrames}));
     await p.locator('video').evaluate(v=>v.play());await p.waitForTimeout(1200);await p.locator('video').evaluate(v=>v.pause());
     const after=await p.locator('video').evaluate(v=>({time:v.currentTime,frames:v.getVideoPlaybackQuality().totalVideoFrames,captions:v.textTracks[0]?.cues?.length}));
     check('decoded frames and playback at '+fraction,after.time>before.time+.5&&after.frames>before.frames,{before,after});
    }
   }
  }
  rows.push(row);await p.close();
 }
 const result={browser:b.version(),method:'Actual H264/AAC MP4s, muted automated playback at three positions; CSS layout zoom (not OS/browser UI zoom); CDP accessibility tree (not a screen-reader session).',rows};
 fs.writeFileSync('academy/review/evidence-2026-10-26/extended-accessibility.json',JSON.stringify(result,null,2));
 console.log(JSON.stringify({pages:rows.length,checks:rows.reduce((a,r)=>a+r.checks.length,0),failures:rows.flatMap(r=>r.checks.filter(c=>!c.pass).map(c=>({file:r.file,...c})))}));await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
