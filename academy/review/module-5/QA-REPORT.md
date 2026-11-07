# Module 5 automated QA evidence

Edition M5-20261107-R1. Review candidate, not human GMP approval or release authorization.

- media-results.json: 150 checks; 0 failures; completed=see evidence scope.
- frame-results.json: 40 checks; 0 failures; completed=see evidence scope.
- browser-results.json: 435 checks; 0 failures; completed=True.
- hosted-delivery-results.json: PENDING in this pre-deployment snapshot. Use the workflow artifact for post-deployment results; require its tested_commit to match the served footer.
- hosted-browser-results.json: PENDING in this pre-deployment snapshot. Use the workflow artifact for post-deployment results; require its tested_commit to match the served footer.

Post-deployment evidence: workflow artifacts linked from the review page.

Read individual JSON evidence for scope and exact failure details. Build identity is in review-build.json; workflow start and final media commit can differ because generated assets are saved after testing.

Not independently verified by automated checks: full human listening/pronunciation, clinical/site applicability, physical devices, manual screen-reader and zoom acceptance, upstream voice-data rights and hosting log retention. Independent GMP consultant review and owner authorization are mandatory.
