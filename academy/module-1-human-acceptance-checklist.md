# ValiStera Academy — Module 1 Human Acceptance & Launch Approval

**Document type:** Internal pre-publication checklist. **Status:** DRAFT / NOT APPROVED.  
**Course:** Pharmaceutical GMP Foundations (Lessons 1.1–1.10 and 15-question final knowledge assessment).  
**Preview:** https://academy-player-preview-valistera-website.gadadeakash72.workers.dev/academy-gmp-foundations.html  
**Branch:** `academy-player-preview`; **production changes prohibited without explicit owner authorization**.

## Mobile user acceptance evidence — 26 October 2026

**User-reported results:** Video narration/playback **PASS**; caption synchronization/toggle **PASS**; Key Explanation controls **PASS**; knowledge-check quiz **PASS**. The user was directed to test Lessons 1.1 and 1.6 on an Android phone. These are **user-reported checks**, not an independent screen-reader or all-lesson accessibility audit. Exact device/browser version and per-lesson test evidence were not collected. Do not mark the all-ten-lesson, screen-reader, media-rights or GMP technical-review gates complete on this basis.

## Assigned approval route
Two separate technical assessments are required: (1) internal senior GMP consultant and (2) external independent GMP specialist. See `academy/review/module-1-review-instructions.md`, `module-1-reviewer-signoff-template.md`, `module-1-finding-log.md` and `module-1-approval-decision.md`. Both reviewer decisions remain **PENDING**; the owner's separate production authorization is also **PENDING**.

## A. Independent technical review (qualified GMP SME)
Review each lesson's spoken audio, on-screen illustrations, captions, quiz question, answer and explanation. Mark each row Pass / Rework / N/A, with reviewer initials and date. Do not mark pass based on automated website testing.

| Lesson | Subject | Audio / graphics / caption accuracy | Quiz / answer correctness | Reviewer / date | Notes |
|---|---|---|---|---|---|
| 1.1 | Introduction to GMP | Pending | Pending | | |
| 1.2 | PQS and GDP | Pending | Pending | | |
| 1.3 | Personnel, training and gowning | Pending | Pending | | |
| 1.4 | Premises, equipment and qualification | Pending | Pending | | |
| 1.5 | Manufacturing and in-process controls | Pending | Pending | | |
| 1.6 | Packaging and mix-up prevention | Pending | Pending | | |
| 1.7 | QC, laboratory testing and OOS | Pending | Pending | | |
| 1.8 | Deviations, investigations and CAPA | Pending | Pending | | |
| 1.9 | Change control | Pending | Pending | | |
| 1.10 | Self-inspection and readiness | Pending | Pending | | |
| Final | 15-question assessment and answer explanations | N/A | Pending | | |

## B. Human accessibility and mobile acceptance
- [ ] On an Android phone, play **start, middle and end** of each video with captions ON; compare visible words and timing with spoken narration.
- [ ] Switch captions OFF: no captions should remain visible; switch back ON.
- [ ] Test Key Explanation ON/OFF independently of captions.
- [ ] With a keyboard, tab through course overview, lesson player, quiz, assessment and navigation; check visible focus, logical order and no traps.
- [ ] Use TalkBack (Android) or another screen reader to test video control names, quiz radio groups, score announcement and feedback.
- [ ] Check 200% text zoom, portrait/landscape, contrast, and low-bandwidth video behavior on an actual device.
- [ ] Confirm browser refresh/resume and progress work on the intended learner device; browser-local data is not a transferable completion record.

## C. Commercial, privacy and content checks
- [ ] Confirm documented permission for commercial/public use of **each** narration voice, music, illustration, icon, font and video asset.
- [ ] Confirm all course content is original or appropriately licensed; do not claim regulatory agency approval or certification.
- [ ] Review learner-facing terms, privacy notice, browser storage explanation, support email and any third-party media requests.
- [ ] Verify the Academy wordmark, Pune headquarters and worldwide service language; do not introduce unsupported certifications or project claims.

## D. Go / no-go decision
**Go only if:** all required technical, accessibility, rights and legal checks are passed or formally resolved, and the owner explicitly authorizes production deployment.

**Decision:** NOT APPROVED (pending human checks).  
**Reviewer:** __________  **Date:** __________  
**Owner authorization:** __________  **Date:** __________  
**Release commit:** __________  **Rollback owner:** __________

## E. Deployment after authorization (not performed)
1. Capture approved preview commit and rollback reference for `main`.
2. Merge only with explicit approval; monitor Cloudflare build and production deployment.
3. Test live course overview, all ten videos/captions/quizzes, assessment, dashboard, resume and mobile layout.
4. Confirm noindex/indexing policy, analytics/privacy notices and launch communications only after live acceptance.

This is an internal review aid, **not** an executed GMP validation report or proof of staff competence.
