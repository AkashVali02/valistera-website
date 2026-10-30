/* Deployment identity comes from Workers Builds, never a hard-coded parent SHA. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const sha=process.env.WORKERS_CI_COMMIT_SHA||cp.execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
if(!/^[a-f0-9]{40}$/.test(sha))throw Error('Missing valid source commit');
const files=fs.readdirSync(root).filter(p=>/^academy-(module-2(?:-[\w-]+)?|lesson-2-\d+)\.html$/.test(p));
for(const f of files){const p=path.join(root,f),s=fs.readFileSync(p,'utf8');if(!s.includes('class="served-commit"'))throw Error('Missing identity slot: '+f);fs.writeFileSync(p,s.replace(/(<code class="served-commit">)[^<]*(<\/code>)/,'$1'+sha+'$2'));}
const hashes={};
function add(p){hashes[p]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');}
files.forEach(add);
for(const f of fs.readdirSync(path.join(root,'assets/academy/module-2'))){if(/\.(vtt|txt|js|css|json)$/.test(f))add('assets/academy/module-2/'+f);}
fs.writeFileSync(path.join(root,'assets/academy/module-2/review/review-build.json'),JSON.stringify({source_commit:sha,edition:'M2-20261030-R2',identity_source:process.env.WORKERS_CI_COMMIT_SHA?'WORKERS_CI_COMMIT_SHA':'local git HEAD (local build)',sha256:hashes},null,2)+'\n');
console.log('Stamped '+files.length+' Module 2 pages: '+sha);
