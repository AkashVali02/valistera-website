"""Verify exact deployed bytes on unversioned and fresh query URLs; no cache purge claim."""
import concurrent.futures,datetime,hashlib,json,pathlib,sys,uuid,subprocess,tempfile
base,expected,out=sys.argv[1:4]
root=pathlib.Path(__file__).resolve().parents[2]
manifest=json.loads((root/'assets/academy/module-2/review/review-build.json').read_text())
assert manifest['source_commit']==expected
rows=[]
def request(task):
 path,suffix,sha=task
 url=base+'/'+path+suffix
 try:
  with tempfile.TemporaryDirectory() as tmp:
   header=pathlib.Path(tmp)/'headers'
   data=subprocess.check_output(['curl','--fail','--silent','--show-error','--location','--max-time','40','-H','Cache-Control: no-cache','-D',str(header),url])
   h={k.lower():v.strip() for line in header.read_text().splitlines() if ':' in line for k,v in [line.split(':',1)]}
   cc=h.get('cache-control','');ray=h.get('cf-ray');cache=h.get('cf-cache-status')
  actual=hashlib.sha256(data).hexdigest()
  return dict(path=path,query=suffix,sha256=actual,expected=sha,match=actual==sha,no_store='no-store' in cc,cache_control=cc,cf_ray=ray,cf_cache_status=cache)
 except Exception as e:return dict(path=path,query=suffix,match=False,error=str(e))
tasks=[]
for path,sha in manifest['sha256'].items():
 variants=['','?review='+uuid.uuid4().hex,'?review='+uuid.uuid4().hex] if path.endswith('.html') else ['?review='+uuid.uuid4().hex]
 for v in variants:tasks.append((path,v,sha))
 if path.endswith('.html'):tasks.append((path[:-5],'?review='+uuid.uuid4().hex,sha))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(request,tasks))
live=json.loads(subprocess.check_output(['curl','--fail','--silent','--show-error','--max-time','40',base+'/assets/academy/module-2/review/review-build.json?review='+uuid.uuid4().hex]))
result=dict(tested_commit=expected,base=base,checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest_matches=live==manifest,requests=rows,failures=[r for r in rows if not r.get('match') or not r.get('no_store')],scope='HTTP content and headers from this network location; not global cache invalidation or browser accessibility')
pathlib.Path(out).write_text(json.dumps(result,indent=2))
print(json.dumps({'commit':expected,'requests':len(rows),'manifest_matches':result['manifest_matches'],'failures':result['failures']}))
sys.exit(bool(result['failures']) or not result['manifest_matches'])
