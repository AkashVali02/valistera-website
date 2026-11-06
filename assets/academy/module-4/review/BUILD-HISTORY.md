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

## Recovered final R1 evidence (superseded by R2)
The final R1 candidate was 2430dea418b60fabb776c20236200644c713c26a, not 2e90a00. Workflow 42185500710 started from 634bf7b8b28afc6fc368af90db94c74d6f19be54 and persisted 2430dea. Artifact 13486998967 contains hosted-delivery-results.json explicitly recording tested_commit=2430dea, 147 matching comparisons and zero failures, plus hosted-browser-results.json with 433 checks and zero failures. Recovered on 6 November 2026. The earlier counts were not sufficient public traceability; F1 correctly identified this publication gap.

## R2 evidence publication
R2 changes retention teaching, assessment choices/order, display notation, caption pacing/phrasing and scene descriptions/relationship panels. All media is rebuilt when its source fingerprints change. Local media/frame/browser results accompany the candidate; post-save hosted results are published separately on academy-module-4-evidence, keyed by the full tested candidate SHA. This avoids modifying the tested lesson commit merely to append its own post-deployment evidence. The review page links directly to that public record. Until that record exists and matches the served SHA, hosted verification is pending. Never reuse R1 results as proof for R2.

### Intermediate R2 run 42190497362
Source 48aa91e saved bc16c7c10146518a3bebfa70590bff14fe9044ae. Media (150), frame (40) and local browser (435) checks passed. Hosted delivery failed 9 of 147 byte comparisons even though the manifest matched; hosted browser checks were skipped. This run is NOT final acceptance. Artifact 13489991413 retains failures. A subsequent run corrects three visual descriptions and allows three bounded full delivery attempts, retaining every attempt; a persistent mismatch still fails the workflow. Edge propagation is a possible explanation, not an established root cause.
