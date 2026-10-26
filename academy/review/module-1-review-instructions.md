# ValiStera Academy — Module 1 Independent Review Instructions

**Status:** Draft for review; no approval implied. **Scope:** Pharmaceutical GMP Foundations, ten lessons and final assessment.
**Preview:** https://academy-player-preview-valistera-website.gadadeakash72.workers.dev/academy-gmp-foundations.html
**Source branch:** `academy-player-preview`. **Production release prohibited without separate explicit owner authorization.**

## Reviewer assignments and independence
**Reviewer A — Internal senior GMP consultant:** Evaluate scientific/technical accuracy, operational practicality, terminology, real-world GMP examples, video narration, diagrams, caption content and lesson quizzes. Record evidence, corrections and an independent decision.

**Reviewer B — External independent GMP specialist:** Review the same complete module independently; scrutinize jurisdiction-specific regulatory statements, potentially misleading interpretations, omissions, risks and final assessment validity. Do not simply countersign Reviewer A's conclusions.

**Owner / release authority:** Assign reviewers, track findings, ensure corrections and independent re-review, confirm rights/privacy/accessibility reviews, and make a separate documented go/no-go decision. Do not merge to production without express approval.

## Reviewer workflow
1. Enter reviewer name, professional role, relevant experience, review date, jurisdiction(s) assessed and the exact preview commit/version.
2. Independently play **every** lesson from beginning to end; inspect all captions, illustrations and key explanations, complete the lesson quiz and evaluate its answer explanation.
3. Review all 15 final assessment items and the scoring and completion disclosures. The 80% threshold is an educational target, not a regulatory acceptance criterion.
4. Record each issue in `module-1-finding-log.csv` (copy it to a private controlled workspace if it contains reviewer names or client data). Cite lesson, timestamp, exact wording and evidence; do not invent regulation clauses.
5. Classify **Critical** (unsafe/misleading patient/product risk or material regulatory error), **Major** (substantive technical inaccuracy, incorrect answer, material omission), **Minor** (limited clarity or caption issue), **Editorial** (style/format). These are internal triage categories, not regulatory classifications.
6. For each finding: propose correction, assign owner, implement on preview branch, record commit, and request **independent re-review** of affected content. Do not mark resolved merely because code changed.
7. Each reviewer completes `module-1-reviewer-signoff-template.md` with Pass / Conditional / Reject. Conditional is **not** approval for launch; all Critical/Major findings must be resolved and independently verified before consideration for release.
8. Owner reconciles both reviewers' conclusions in `module-1-approval-decision.md`, confirms accessibility, caption/audio, media licensing, privacy and support checks, and decides **GO / NO-GO**. GO is not automatic deployment.

## Official source entry points (verify applicable current editions before clause-level claims)
- European Commission EU GMP Volume 4: https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en
- ICH Quality Guidelines including Q9(R1): https://www.ich.org/page/quality-guidelines
- FDA 21 CFR Part 211: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211

## Completion criteria
- Two distinct named reviewers independently completed the full module and documented decisions.
- All findings have documented dispositions; no unresolved Critical or Major findings.
- Affected content has been corrected and re-reviewed by both reviewers as appropriate.
- Media rights, accessibility, privacy and learner-facing claims have been checked.
- Owner issues a separate explicit production release authorization. No sign-off means no release.

**Confidentiality:** Keep identifiable reviewer details, proprietary notes and signed records in an access-controlled location. This repository contains blank working templates, not executed evidence.
