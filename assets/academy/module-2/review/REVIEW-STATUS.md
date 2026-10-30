# Module 2 continuation — 30 October 2026

Status: NOT RELEASE-APPROVED. Preview branch only; PR #2 remains unmerged.

## Recovered state and corrections
Started from 201daa44d3ca96034d7d4795d6ef886b416c4070, which contains 40 regenerated aligned diagrams and ten rebuilt videos. The ten recordings retain their original narration. Required reading remains part of the assessed learning format.

The latest duplicate push/PR workflows raced while saving media; one failed with a non-fast-forward push. The successful media commit used [skip ci], and Cloudflare reported its build skipped. These are observed causes, not a claim that the newer media had deployed.

Changes in this continuation: serialize preview QA, remove duplicate PR trigger and routine media regeneration, test the exact triggering commit, permit explicit media regeneration and save only after passing QA, remove skip-ci from generated commits, repair the manifest's literal backslash-n trailer, use a range-capable preview server, save browser evidence incrementally even on failure, preserve hidden explanations, and version media/CSS/JS URLs by content hash to avoid stale client assets. Added keyboard focus styling for scrollable tables and restored full explanations in print output.

## Evidence
Local static validation and 120 media checks pass. A fresh browser regression and hosted media/hash verification are being executed; do not infer their success from historical reports.

Historical reports remain in this package and are dated. The 225-check local report from the earlier draft is not substituted for the current version. See the forthcoming continuation report for exact commits, checks and hosted results.

## Remaining acceptance boundaries
Human pronunciation/listening, physical-device operation, actual screen-reader review, audiovisual-equivalence acceptance, rights/host-account/privacy review, independent GMP review and owner release authorization remain unsigned. Nothing here certifies WCAG, GMP compliance or legal clearance. Production is unchanged.
