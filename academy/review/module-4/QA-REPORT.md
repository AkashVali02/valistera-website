# Module 4 automated QA evidence

Edition M4-20261106-R1. Review candidate, not human GMP approval or release authorization.

- media-results.json: 150 checks; 0 failures; completed=see evidence scope.
- frame-results.json: 40 checks; 0 failures; completed=see evidence scope.
- browser-results.json: 433 checks; 0 failures; completed=True.
- hosted-delivery-results.json: generated after deployment and retained in the GitHub workflow artifact. See PR #7 for the exact verified commit/run; this pre-deployment report does not assert a hosted result.
- hosted-browser-results.json: generated after deployment and retained in the GitHub workflow artifact. See PR #7 for the exact verified commit/run; this pre-deployment report does not assert a hosted result.

Latest review status and hosted evidence: https://github.com/AkashVali02/valistera-website/pull/7

Read individual JSON evidence for scope and exact failure details. Build identity is in review-build.json; workflow start and final media commit can differ because generated assets are saved after testing.

Not independently verified by automated checks: full human listening/pronunciation, clinical/site applicability, physical devices, manual screen-reader and zoom acceptance, upstream voice-data rights and hosting log retention. Independent GMP consultant review and owner authorization are mandatory.
