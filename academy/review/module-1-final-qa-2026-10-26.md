# ValiStera Academy Module 1 — consolidated execution and QA report

**26 October 2026 · academy-player-preview · NO-GO for production**

Reviewed starting commit: `4335a250d5f697937879c84e78f596d0b1520e64`. This report and the evidence folder belong to the correction commit that contains them; the commit is the reviewable package. No merge or production deployment was performed. This is AI-assisted technical execution, not independent human, legal or regulatory approval.

## Completed changes

1. **All ten caption tracks:** fresh base.en speech transcription with word timestamps; comparison with existing caption wording; ASR-assisted correction of accumulating Lesson 1.1 drift; long-cue splitting at matched spoken-word boundaries, fragment merging, acronym typography and balanced line breaks. No blind replacement of technical terminology with ASR guesses. Native VTT and embedded fallback arrays now agree. Static recorded-narration transcripts are available in all ten pages.
2. **Readability:** zero cues above the 20.05 CPS tolerance used for a nominal 20 CPS review threshold, maximum two authored lines, no detected overlap/nonpositive cue, and no cue beyond video duration. The threshold is a design heuristic, not a WCAG rule. Browser wrapping and human reading comfort still need real-device acceptance.
3. **Visual/media audit:** downloaded all ten MP4s, decoded every audio stream, reviewed 84 sampled authored scenes (one per scene, +2 seconds from recorded scene starts), and compared the transcript/topic content with companion readings and assessment scenarios. Corrected Lesson 1.8's misleading root-cause heading and action label in a same-origin review MP4. Inspected the corrected frame. Audio hash is unchanged. Added prominent Lesson 1.4 instrument-calibration and Lesson 1.5 US/EU dispensing clarifications. Original narration was not re-recorded.
4. **Official references:** checked the applicable published EC/EU and eCFR text, not merely link availability. Added EU Chapter 5 dispensing-check context; strengthened OOS escalation wording and linked the final May 2022 FDA guidance; clarified 211.180(e)'s product-review role versus EU self-inspection. See the linked clause-level cross-check.
5. **Accessibility:** fixed low-contrast links and CTAs, added visible keyboard focus and skip links, labelled quiz groups, added transcript disclosure controls, exposed assessment progress semantics, and respected reduced-motion styling. Retested all 12 pages.
6. **Privacy/storage:** completed notices on all 12 pages (1.9/1.10 were missing), added scoped progress clearing, delayed remote video requests until user action, added no-referrer and media-error fallback, removed stale assessment results on restart, and rejected out-of-range stored scores. Corrected a newly reproduced resume bug: loading-time zero-position events could overwrite saved progress; all ten lesson persistence handlers now reject those events and pending seeks.

## Executed evidence

| Lesson | Final cues | Original duration (s) | ASR/source-caption token similarity | CPS review flags |
|---|---:|---:|---:|---:|
| 1.1 | 146 | 527.74 | 99.60% | 0 |
| 1.2 | 56 | 234.99 | 98.32% | 0 |
| 1.3 | 65 | 262.33 | 99.34% | 0 |
| 1.4 | 55 | 225.75 | 98.50% | 0 |
| 1.5 | 62 | 229.24 | 100.00% | 0 |
| 1.6 | 52 | 216.81 | 99.44% | 0 |
| 1.7 | 53 | 222.66 | 99.32% | 0 |
| 1.8 | 50 | 214.12 | 98.76% | 0 |
| 1.9 | 60 | 219.42 | 100.00% | 0 |
| 1.10 | 60 | 236.79 | 98.49% | 0 |

Similarity is a machine diagnostic, not word-perfect transcription acceptance. US/UK spelling, spelled acronyms and brand pronunciation account for many differences. Segment-level rechecks recovered the omitted Lesson 1.10 trend-analysis phrase and supported “finding” and “from recommendations”; ambiguous ASR “manufacturer” / “a countable” remain human listening items, not grounds for changing technically sensible captions. All final caption words are preserved from the source except formatting/acronym normalization, verified by a normalized-text comparison.

- `caption-structure.json`: all ten pass structural/source-agreement checks. The script also checks duration bounds and normalized wording preservation.
- `audio-diagnostics.json`, ten `asr-1-*.json` files and `asr-discrepancy-recheck.json`: actual machine transcript and diagnostic evidence, including original timing flags. Those flags describe the **pre-remediation** captions; they are not final sync errors.
- `browser-fixture-results.json`: **235 checks across 12 pages; zero failures**, using synthetic WebM solely for player/control testing. Includes correct/incorrect/unanswered lesson answers; assessment 15/15 and 0/15; reset; 65-second paused resume on all ten; caption-track parsing/toggles; keyboard skip/transcript controls; 320/390/768/1280 px overflow; no automatic CloudFront video request; scoped clearing; no uncaught JS errors. Axe-core 4.10.3 detected zero scoped A/AA violations. Incomplete/manual axe checks are retained, not promoted to passes.
- `browser-results.json`: original-MP4 attempt recorded **195 checks, 185 passes and 10 metadata-decode failures**. Environment diagnosis: Chromium headless shell 134.0.6998.35 returns empty support for H.264/AAC and `probably` for WebM. Therefore real MP4 playback/resume/native-caption rendering in a supported production browser remains **unverified here**. The successful fixture run is not substituted for it.
- `storage-denied.json`: all 12 pages remain functional without uncaught errors when access to localStorage throws SecurityError, with clear feedback.
- `node validate-site.cjs`: passed for 31 HTML pages, 1,029 local references, sitemap, JSON, asset fingerprints and JavaScript syntax. `git diff --check` passed.
- Browser checks served exact local repository files through Playwright routes, **not a live deployed HTTP server**. No claim is made about final deployed headers/CDN behavior. Sampled screenshots are evidence of layout only; the mobile player screenshot contains synthetic test media.

## Findings and current disposition

| ID | Finding | Disposition |
|---|---|---|
| QA-01 | Old report simultaneously claimed ASR had and had not run; counts predated last commits | Historical records marked superseded. Fresh raw ASR/test evidence is retained here. |
| QA-02 | Caption speed/line layout and Lesson 1.1 timing drift | Technical remediation and structural retest complete. Human listening/synchronization acceptance open. |
| QA-03 | Lesson 1.4 vessel/calibrated-instrument ambiguity | Prominent written clarification added. Original spoken example still requires accepted media correction or explicit combined-format approval. |
| QA-04 | Lesson 1.5 dispensing wording could imply local discretion over required checks | US/EU clarification added before video; applicable clauses verified. Spoken revision/combined-format acceptance open. |
| QA-05 | Lesson 1.8 slide says PREVENT ROOT CAUSE | Heading/action corrected in review MP4; audio preserved. Original media rights remain open. |
| QA-06 | Link/button contrast, absent quiz legend/skip controls | Fixed; automated accessibility and keyboard/reflow retests pass within tested scope. |
| QA-07 | Missing privacy notices, uncontrolled initial media contact, stale result, zero-time resume overwrite | Fixed and tested. Legal adequacy and hosting retention not certified. |
| QA-08 | Media provenance and independent acceptance evidence absent | Open; cannot be manufactured by technical execution. |

## Unresolved release dependencies

- **Human audiovisual acceptance:** listening review of all final captions, pronunciation, timing, reading speed, narration/companion differences and any unclear ASR words. The 84 scene samples do not prove absence of every transient visual defect, flashing issue or missing visual description. Small slide labels and dense diagrams need real-device readability/accessible-equivalence review.
- **Recorded content:** the written clarifications are visible, but do not rewrite the 1.4/1.5 audio. A reviewer must accept the combined learning format or request re-recording with an authorized voice/source project. No paid voice-generation or fabricated voice permission was used.
- **Full accessibility:** actual H.264-capable browser/device playback, screen-reader operation, 200%/400% zoom/text-spacing, native control behavior and audiovisual alternatives still need acceptance. Zero axe violations is not WCAG 2.2 AA certification.
- **Rights and hosting:** original voice/graphics/fonts/music provenance, commercial redistribution rights, external hosting account control and retention/logging terms remain absent. The derivative retains those dependencies. See the media inventory and rights report.
- **Independent GMP and privacy review:** established internal/external reviewer sign-offs remain blank. AI execution does not satisfy those independent signatures. No regulatory approval is claimed.
- **Owner release authorization:** not requested because the candidate is not release-ready. Production remains NO-GO. Keep work on the preview branch.

## Package index

- [Official-source cross-check](module-1-regulatory-crosscheck-2026-10-26.md)
- [Rights, hosting and privacy audit](module-1-rights-hosting-privacy-2026-10-26.md)
- [Evidence folder](evidence-2026-10-26/)
- [Reproducible test instructions](../tests/README.md)
- [Existing independent approval record](module-1-approval-decision.md)

**Decision:** feasible technical remediation is consolidated; release acceptance is incomplete. Do not merge, publish or portray this package as approved training evidence.
