/* Deployment identity comes from Workers Builds, never a hard-coded parent SHA. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const sha=process.env.WORKERS_CI_COMMIT_SHA||cp.execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
if(!/^[a-f0-9]{40}$/.test(sha))throw Error('Missing valid source commit');
const reviewed=sha;
const files=fs.readdirSync(root).filter(p=>/^academy-(module-5(?:-[\w-]+)?|lesson-5-\d+)\.html$/.test(p));
for(const f of files){const p=path.join(root,f),s=fs.readFileSync(p,'utf8');if(!s.includes('class="served-commit"'))throw Error('Missing identity slot: '+f);fs.writeFileSync(p,s.replace(/(<code class="served-commit">)[^<]*(<\/code>)/,'$1'+sha+'$2').replace(/(\/evidence\/)(BUILD_PENDING|[a-f0-9]{40})(\/index.html)/g,'$1'+reviewed+'$3'));}
const hashes={};
function add(p){hashes[p]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');}
files.forEach(add);
for(const f of fs.readdirSync(path.join(root,'assets/academy/module-5'))){if(/\.(vtt|txt|js|css|json|mp4|png|csv)$/.test(f))add('assets/academy/module-5/'+f);}
fs.writeFileSync(path.join(root,'assets/academy/module-5/review/review-build.json'),JSON.stringify({source_commit:sha,reviewed_candidate:reviewed,edition:'M5-20261107-R1',identity_source:process.env.WORKERS_CI_COMMIT_SHA?'WORKERS_CI_COMMIT_SHA':'local git HEAD (local build)',sha256:hashes},null,2)+'\n');
console.log('Stamped '+files.length+' Module 5 pages: '+sha);
