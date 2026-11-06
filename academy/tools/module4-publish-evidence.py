"""Prepare public immutable-by-convention evidence directories from original CI ZIPs.
Does not change or rerun tested lesson code. Publish output to the evidence branch.
"""
from pathlib import Path
import zipfile,json,hashlib,html,sys
archive,output,run_id,artifact_id,source=sys.argv[1:]
z=zipfile.ZipFile(archive)
def original(name,area='academy/review/module-4/'):
 matches=[n for n in z.namelist() if n.endswith(area+name)]
 assert len(matches)==1,(name,matches)
 return z.read(matches[0])
delivery=json.loads(original('hosted-delivery-results.json'));commit=delivery['tested_commit'];assert len(commit)==40
manifest=original('review-build.json','assets/academy/module-4/review/');assert json.loads(manifest)['source_commit']==commit
files={n:original(n) for n in ['media-results.json','frame-results.json','browser-results.json','hosted-delivery-results.json','hosted-browser-results.json','voice-provenance.json']}
files['review-build.json']=manifest
for name in z.namelist():
 if '/academy/review/module-4/hosted-delivery-attempt-' in name and name.endswith('.json'):
  files[name.rsplit('/',1)[-1]]=z.read(name)
for name in ['CLAUDE-FINDINGS-RESPONSE.md','PINPOINT-VERIFICATION.md','RIGHTS-PRIVACY.md','SOURCE-MAP.md']:
 try:files[name]=original(name)
 except AssertionError:pass
hashes=json.loads(manifest)['sha256']
for row in json.loads(files['media-results.json'])['rows']:
 assert hashes[f"assets/academy/module-4/lesson-{row['lesson']}.mp4"]==row['sha256']
for row in json.loads(files['frame-results.json'])['rows']:
 assert hashes[f"assets/academy/module-4/lesson-{row['lesson']}-scene-{row['scene']}.png"]==row['png_sha256']
 assert hashes[f"assets/academy/module-4/lesson-{row['lesson']}.mp4"]==row['video_sha256']
reports=[]
for name in ['media-results.json','frame-results.json','browser-results.json','hosted-delivery-results.json','hosted-browser-results.json']:
 data=json.loads(files[name]);checks=data.get('checks',data.get('requests',[]));count=len(checks) if isinstance(checks,list) else checks
 assert not data['failures'],(name,data['failures'])
 if 'completed' in data:assert data['completed']
 if name=='hosted-browser-results.json' and 'tested_commit' in data:assert data['tested_commit']==commit
 reports.append(dict(file=name,checks=count,failures=len(data['failures'])))
record=dict(tested_commit=commit,edition=json.loads(manifest)['edition'],local_browser_commit=json.loads(files['browser-results.json']).get('tested_commit'),media_and_frame_hashes_match_candidate=True,workflow_source_commit=source,workflow_run=int(run_id),workflow_url=f'https://github.com/AkashVali02/valistera-website/actions/runs/{run_id}',artifact_id=int(artifact_id),artifact_sha256=hashlib.sha256(Path(archive).read_bytes()).hexdigest(),hosted_base=delivery['base'],hosted_checked_at=delivery['checked_at'],manifest_matches=delivery['manifest_matches'],reports=reports,sha256={n:hashlib.sha256(b).hexdigest() for n,b in files.items()},provenance='Raw JSON copied byte-for-byte from the workflow artifact. Hosted delivery explicitly identifies the saved candidate. R1 browser result is associated through that same workflow artifact; R2 additionally identifies and checks the manifest before and after browser tests.',release_status='NOT APPROVED: independent GMP consultant and owner release gates remain open')
files['evidence-record.json']=(json.dumps(record,indent=2)+'\n').encode()
E=html.escape
rows=''.join(f'<tr><th scope="row"><a href="{r["file"]}">{r["file"]}</a></th><td>{r["checks"]}</td><td>{r["failures"]}</td></tr>' for r in reports)
links=''.join(f'<li><a href="{E(n)}">{E(n)}</a></li>' for n in files)
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Module 4 exact-commit QA evidence</title><style>body{{max-width:64rem;margin:2rem auto;padding:0 1rem;font:18px/1.55 system-ui;background:#071526;color:#f3f7fc}}a{{color:#69dce3}}code{{overflow-wrap:anywhere}}table{{border-collapse:collapse;width:100%}}th,td{{padding:.65rem;text-align:left;border:1px solid #6c8094;overflow-wrap:anywhere}}.brand span{{color:#4c9eff}}:focus-visible{{outline:3px solid #ffd18a;outline-offset:4px}}</style></head><body><header class="brand">Vali<span>Stera</span> Academy</header><main><h1>Module 4 exact-commit QA evidence</h1><p>Edition {E(record['edition'])}. Tested lesson commit: <code>{commit}</code></p><p>This is a separate evidence publication, not a new lesson candidate. Its deployment commit is not the tested lesson commit. Match the above SHA to the lesson preview footer and build manifest. If the preview has moved, this record is historical.</p><p><a href="{delivery['base']}/academy-module-4-review">Lesson review package</a> · <a href="{record['workflow_url']}">Original workflow</a> · <a href="https://github.com/AkashVali02/valistera-website/pull/7">Draft PR #7</a></p><p>Workflow source: <code>{source}</code>. Local browser tests precede the generated-assets save and may identify the workflow source commit. Hosted browser and delivery tests follow the save and identify the final candidate. Media/frame report hashes were cross-checked against that candidate manifest. Hosted delivery timestamp: {E(delivery['checked_at'])}. Artifact {artifact_id}; its ZIP digest and every published file digest are in evidence-record.json.</p><h2>Measured automated results</h2><table><caption>Original workflow results, not human acceptance</caption><thead><tr><th>Report</th><th>Checks</th><th>Failures</th></tr></thead><tbody>{rows}</tbody></table><h2>Readable source evidence</h2><ul>{links}</ul><h2>Scope and limitations</h2><p>Browser tests cover 320/390/768/1280 widths, automated axe checks, skip links, keyboard Enter disclosure/play activation, collapsed images and descriptions, native timeline clicks, captions, assessment boundaries, optional storage and failure/retry paths. Media and frame checks measure encoding, caption/source timing and correspondence to PNGs. They do not establish human clarity, pronunciation, physical-device behavior or regulatory compliance.</p><p>Manual audiovisual review, physical Android/iOS, screen-reader and zoom acceptance, rights/privacy acceptance, independent GMP consultant sign-off and explicit owner production authorization remain required. Module 3 approval does not authorize Module 4. No certification or release approval is claimed.</p></main></body></html>'''
files['index.html']=page.encode()
root=Path(output)/'assets/academy/module-4/evidence'/commit;root.mkdir(parents=True,exist_ok=True)
for name,b in files.items():(root/name).write_bytes(b)
print(json.dumps(dict(commit=commit,files=len(files),reports=reports,root=str(root))))
