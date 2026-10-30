"""Write a parseable manifest for all 50 durable media files."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2];A=R/'assets/academy/module-2'
paths=sorted([*A.glob('lesson-*-scene-*.png'),*A.glob('lesson-*.mp4')])
assert len(paths)==50
record={str(p.relative_to(R)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths}
(R/'academy/module-2/media-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
print('Recorded SHA-256 and size for 50 media files')
