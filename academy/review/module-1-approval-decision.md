# Module 1 — owner-authorized release decision

26 October 2026 (Asia/Kolkata).

## Current decision: GO for publication, authorized by the owner

The owner stated in this conversation: “Great consultant approved the module 1 Now u can publish it or do next scheduled task”. This supersedes the earlier preview-only/no-merge instruction and authorizes publication of Module 1.

Approval basis: owner-reported consultant approval of the reviewed Module 1 candidate `eab9e508061286bd784a3b3909e64688cf76be5b`, plus explicit owner authorization to publish. Consultant identity, review scope, dated report and signatures were not supplied in this conversation. No independent reviewer signature, WCAG certification, legal clearance or regulatory approval is inferred or fabricated. Earlier technical evidence and its stated limitations remain accurate; the release decision is the owner's decision based on reported consultant approval.

Release preparation changes are limited to publishing metadata/course discovery, learner-facing preview wording, public asset exclusions and this record. Lesson narration, captions, visuals, assessment content and player behavior remain the reviewed version.

Deployment route: merge PR #1 into `main`; Cloudflare Workers Builds deploys `valistera-website` from `main`. Confirm the exact merged commit's successful production build, then check the live course and media.

Rollback reference: pre-release main `9b4ec003312f9d951399368ffea88624f76350d2`. If a release regression occurs, revert the release merge through a new commit and confirm its production build; do not rewrite shared history.

## Historical pre-authorization record

The following unsigned checklist is retained as history. Its blank signatures must not be presented as completed independent approvals.

# ValiStera Academy — Module 1 Release Decision Record

**DRAFT / NO-GO pending required reviews. Not an authorization to publish.**

Course and version / commit: __________________
Internal GMP reviewer and dated decision: __________________
External independent GMP reviewer and dated decision: __________________
Finding log location and open Critical/Major counts: __________________
Corrected content and re-review evidence: __________________

## Release prerequisites
- [ ] Internal reviewer completed independent full-module assessment and signed PASS.
- [ ] External reviewer completed independent full-module assessment and signed PASS.
- [ ] All Critical and Major findings closed with documented re-review; remaining Minor/Editorial items explicitly assessed.
- [ ] Manual caption/audio accuracy, screen-reader/keyboard and real-device accessibility checks accepted.
- [ ] Rights for narration, images, diagrams, fonts and media documented.
- [ ] Privacy/terms, browser-local progress limitations, support and public claims reviewed.
- [ ] Exact preview commit frozen for release and production rollback approach recorded.

## Owner decision
[ ] **NO-GO** — remain on preview.
[ ] **GO for production deployment** — requires separate explicit owner authorization in the deployment workflow; selecting a checkbox here alone does not initiate a merge.

Decision rationale: __________________
Owner name / signature / date: __________________
Release approver: __________________
Production release commit (only after authorization): __________________
Rollback reference: __________________

**Current decision: NO-GO. Production main branch must not be changed without explicit owner instruction.**
