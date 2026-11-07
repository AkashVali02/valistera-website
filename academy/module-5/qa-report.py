from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];P=R/'academy/review/module-5'
rows=['# Module 5 automated QA evidence','', 'Edition M5-20261107-R1. Review candidate, not human GMP approval or release authorization.','']
for name in ['media-results.json','frame-results.json','browser-results.json','hosted-delivery-results.json','hosted-browser-results.json']:
 p=P/name
 if not p.exists():
  rows.append(f'- {name}: PENDING in this pre-deployment snapshot. Use the workflow artifact for post-deployment results; require its tested_commit to match the served footer.');continue
 d=json.loads(p.read_text());fails=d.get('failures',[]);checks=d.get('checks',d.get('requests',[]));count=len(checks) if isinstance(checks,list) else checks
 rows.append(f'- {name}: {count} checks; {len(fails)} failures; completed={d.get("completed","see evidence scope")}.')
rows += ['', 'Post-deployment evidence: workflow artifacts linked from the review page.', '', 'Read individual JSON evidence for scope and exact failure details. Build identity is in review-build.json; workflow start and final media commit can differ because generated assets are saved after testing.','', 'Not independently verified by automated checks: full human listening/pronunciation, clinical/site applicability, physical devices, manual screen-reader and zoom acceptance, upstream voice-data rights and hosting log retention. Independent GMP consultant review and owner authorization are mandatory.']
(P/'QA-REPORT.md').write_text('\n'.join(rows)+'\n')
