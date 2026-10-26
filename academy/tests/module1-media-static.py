"""Verify self-contained Module 1 media and historical-original byte identity."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[2]
evidence=root/'academy/review/evidence-2026-10-26'
manifest=json.loads((evidence/'same-origin-media.json').read_text())
originals={x['lesson']:x for x in json.loads((evidence/'media-inventory.json').read_text())}
rows=[]
for x in manifest:
 i=x['lesson'];page=root/('academy-player-preview.html' if i==1 else f'academy-lesson-1-{i}.html');s=page.read_text();p=root/x['path'];sha=hashlib.sha256(p.read_bytes()).hexdigest()
 checks={'file_hash_matches_manifest':sha==x['sha256'],'page_uses_same_origin_copy':f'data-src="/{x["path"]}"' in s,'video_not_preloaded':bool(re.search(r'<video\b[^>]*preload="none"',s)),'no_external_video_reference':'cloudfront.net' not in s}
 if i not in (4,5,8):checks['original_bytes_unchanged']=sha==originals[i]['sha256']
 rows.append({'lesson':i,'checks':checks})
for name in ['academy-gmp-foundations.html','academy-gmp-assessment.html']:
 s=(root/name).read_text();rows.append({'page':name,'checks':{'no_obsolete_external_media_notice':'third-party media host' not in s and 'CloudFront' not in s}})
result={'scope':'Static same-origin paths, hashes and deferred loading; does not verify deployed hosting configuration.','rows':rows,'failures':[r for r in rows if not all(r['checks'].values())]}
(evidence/'same-origin-static.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'checks':sum(len(r['checks']) for r in rows),'failures':result['failures']}));raise SystemExit(bool(result['failures']))
