# Module 4 build history
## Initial saved media candidate — 6 November 2026
- Editorial/workflow source: 938d193ebbdd980347539701edd3dd1f0d10a5d7.
- Saved media and tested preview: 2e90a00a3b2930c13bd6b6aaa68bb67f8423d69f.
- Successful workflow: https://github.com/AkashVali02/valistera-website/actions/runs/42182510538
- Evidence ZIP: https://github.com/AkashVali02/valistera-website/actions/runs/42182510538/artifacts/13485958228
- Ten saved H.264/AAC videos; 17.2089 minutes; forty PNGs, captions and timing data.
- 150 media checks, 40 encoded scene comparisons, 433 local browser checks and 433 hosted browser checks passed with zero failures.
- 147 hosted byte/header comparisons passed; exact identity and manifest matched the saved candidate.
- Build passed 76 HTML pages and 2,022 local references.
- Cloudflare preview build succeeded. Browser inspection independently confirmed review/overview identity, lesson 4.3 initially collapsed diagrams, keyboard disclosure and video playback.
- The initial source-only Cloudflare build failed before generated assets existed; the subsequent saved-media deployment succeeded. No production changes were made.

This is historical evidence for the named commit. The latest exact candidate, subsequent worksheet/player cleanup verification and final hosted evidence are linked from draft PR #7: https://github.com/AkashVali02/valistera-website/pull/7. Media generation is skipped when its source hashes match; measured media is not needlessly regenerated. A passing automation run is not independent GMP approval, full human audiovisual acceptance or release authorization.
