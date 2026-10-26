# ValiStera Academy Module 1 — consolidated final technical QA

**26 October 2026 · academy-player-preview · production NO-GO**

This report supersedes the earlier same-day final report, retained as [the pre-continuation record](module-1-qa-before-continuation-2026-10-26.md). It consolidates the original remediation and the subsequent feasible work in audiovisual quality, recorded content, accessibility, and rights/hosting. The final player implementation is commit `83c546f6bf512fae8e073382a1616173b19199d7`; the extended layout/accessibility run used `e99c5c91d6e012ab5d8851a580afac333c6b5a8a` with identical layout and media; the following evidence/report commit completes this package. No production deployment or merge was performed.

## Delivered changes

- **Captions/transcripts:** all ten lessons have native VTT captions, matching embedded cue arrays and static transcripts. Earlier work corrected Lesson 1.1 timing drift, split long cues, balanced lines and checked questionable ASR phrases. The new 1.4/1.5 recordings have fresh base.en word-timestamp ASR, source-script comparison, new timing and updated transcripts. Final structural checks find no overlap, nonpositive cue or media-duration overflow; zero cues exceed the 20.05 characters/second tolerance and all use at most two authored lines. This is a readability heuristic, not a WCAG rule or human synchronization sign-off.
- **Actual recorded corrections:** Lesson 1.4 scene 8 now describes an overdue measuring instrument used with a vessel. Lesson 1.5 scene 3 now states required independent dispensing checks, EU material/weight-or-volume checking, US second-person requirements with defined automated-equipment exceptions, and that local risk assessment cannot waive applicable requirements. Original diagrams and all other per-scene source audio were reused. Key-explanation start times were updated to the revised scene durations; static checks and 16 scene-level browser assertions cover those transitions. The revised videos are stored with the preview repository. The earlier Lesson 1.8 root-cause heading/action correction remains in place.
- **Accessible visual alternatives:** every lesson now includes a readable HTML guide describing the main diagram relationships in presentation order, alongside its transcript and companion reading. The guides explain illustrative risk scoring, status conflicts, investigation paths, reconciliation and other dense graphics without relying on colour. Ten scene contact sheets were inspected when authoring them. The changed 1.4/1.5 video frames were also inspected at full resolution. This does not establish every-frame equivalence or human audio-description acceptance.
- **Accessibility fixes and retest:** enlarged layout/text testing exposed overflow in the overview and several lesson pages. Flexible grids, wrapping headings/buttons/links and responsive padding fixed those findings. Earlier contrast, keyboard focus, skip-link, quiz legend, assessment semantics and reduced-motion fixes remain. Actual H.264/AAC playback is now verified in the connected media environment; the previous local codec limitation is no longer the sole playback evidence.
- **Privacy/storage:** earlier scoped localStorage clearing, complete notices, no-referrer, opt-in video loading, retry/transcript fallback, assessment reset and resume-overwrite fixes remain. Lessons 1.4, 1.5 and 1.8 use same-origin video files; seven lessons still use their original external hosting. No new analytics or paid generation API was used.
- **Source/provenance recovery:** recovered original Kokoro scripts, model/voice identities and diagram-generation code. Nine original MP4s match workspace renders byte-for-byte. Lesson 1.1's decoded audio matches the recovered premium render; its final video assembly lacks a whole-file match. Stock `af_heart`, Pillow drawings and DejaVu font usage are documented, with publisher licensing links and observed file hashes. This narrows the rights gap; it does not invent legal clearance.

## Final executed evidence

| Test | Result | Evidence |
|---|---|---|
| Actual-media player, keyboard, quizzes, assessment, axe, storage clearing and responsive layout | **251/251 checks passed across 12 pages**; zero detected scoped axe violations | `browser-h264-results.json` |
| Real muted video playback at 5%, 50%, 95%; increasing decoded frames; accessibility-tree roles/names; 2x/4x CSS layout zoom; text spacing at 320/1280 px | **112/112 checks passed across 12 pages** | `extended-accessibility.json` |
| Ten final caption tracks | **All pass**; zero speed flags; maximum two authored lines | `caption-structure.json` |
| Complete video-stream decode and scene-change diagnostic | **10/10 decode successfully**; no more than one detected change per rolling second at the selected threshold | `full-decode-scene-scan.json` |
| Website validation | **Passed:** 31 HTML pages, 1,029 local references, sitemap, JSON, fingerprints and JS syntax | `node validate-site.cjs` |
| Patch whitespace validation | **Passed** | `git diff --check` |
| Denied localStorage regression from original remediation | **12/12 pages without uncaught errors**; implementation unchanged in continuation | `storage-denied.json` |

The final H.264 browser was **Chromium 153.0.8010.12**; axe was **4.10.3**. The tests served repository bytes through Playwright routes with byte-range handling. They did not test a deployed site's HTTP headers, CDN or physical devices. Tests used real media, not the earlier synthetic WebM fixture. Playback was muted and sampled at three positions; this is decode/control evidence, not a full listening review.

CSS layout zoom is not physical-device/browser-menu zoom. Accessibility-tree inspection is not an NVDA, JAWS, VoiceOver or TalkBack session. Zero axe findings is not WCAG 2.2 AA certification. The full-stream scene-change heuristic can miss localized or low-amplitude flashes and is not a validated photosensitive-epilepsy test. Historical `browser-results.json` and `browser-fixture-results.json` retain the earlier local failures/fixture run; do not confuse them with the new H.264 evidence.

The initial supported-browser run found one same-origin-video resume failure caused by the test route's missing range response. The harness was corrected to serve byte ranges for repository MP4s; all ten real-video resume tests then passed. The initial extended run found six failing checks (five 4x layout overflows and one text-spacing overflow); CSS corrections passed the final retest.

| Lesson | Final cues | Candidate duration (seconds) |
|---|---:|---:|
| 1.1 | 146 | 527.74 |
| 1.2 | 56 | 234.99 |
| 1.3 | 65 | 262.33 |
| 1.4 | 49 | 230.07 |
| 1.5 | 52 | 247.30 |
| 1.6 | 52 | 216.81 |
| 1.7 | 53 | 222.66 |
| 1.8 | 50 | 214.12 |
| 1.9 | 60 | 219.42 |
| 1.10 | 60 | 236.79 |

New narration ASR supports both corrected passages. Unmatched source words mostly involve compounds/acronym segmentation; they remain diagnostic entries rather than automatic text replacements. Caption boundary balancing extended five cue ends by 0.001–0.551 seconds to meet the reading-speed target; adjusted boundaries are recorded in `revised-caption-boundaries.json`. Human timing acceptance remains open. Original captions for unchanged lessons and revised source narration for 1.4/1.5 are checked independently by the static test.

## Regulatory and rights disposition

The [official-source cross-check](module-1-regulatory-crosscheck-2026-10-26.md) remains the clause-level record. It covers applicable EU human-medicinal-product GMP and US finished-pharmaceutical provisions, including Annex 15, EU Chapter 5 and 21 CFR 211.101/211.68. The two previously written-only corrections are now recorded. Companion detail still exceeds narration in places and must be evaluated as a combined course. Framework signposts do not establish detailed compliance in every jurisdiction or product category.

The [rights/hosting/privacy report](module-1-rights-hosting-privacy-2026-10-26.md) and [recovered-source notes](recovered-source/README.md) distinguish publisher licences from legal clearance. The observed local model/voice files are identified by hash, not misrepresented as independently verified upstream release checksums. Source paths show no music input. Operational access to the connected workspace does not prove legal ownership or control of its underlying CDN. Official public hosting terms were reviewed; they do not supply an Academy-specific retention/logging schedule or availability commitment.

## Remaining external acceptance gates

1. **Human audiovisual acceptance:** final listening review of pronunciation, unclear original ASR words, timing, reading comfort and narration/companion differences; real-device readability and evaluation of the text alternatives. No human review signature was fabricated.
2. **Full accessibility acceptance:** actual assistive-technology operation, physical devices/browser-menu zoom, native controls and any required audio-description alternative; validated flashing analysis if required by the release process. The automated checks above are complete within their stated scope.
3. **Rights/hosting/privacy acceptance:** review recovered provenance and licence conditions, resolve the final Lesson 1.1 visual assembly provenance, confirm commercial distribution/branding rights and approve durable hosting with known retention/logging and deletion controls. Seven external media URLs remain a dependency.
4. **Independent GMP/privacy sign-offs and owner release decision:** remain unsigned. AI technical execution does not satisfy those independent approvals.

**Decision:** the feasible continuation is implemented and tested. The two recorded-content correction blockers are technically resolved; human acceptance, legal/hosting decisions and independent sign-offs are still open. Production remains **NO-GO**. Owner release authorization is not requested for this candidate. Keep the package on `academy-player-preview`.

## Package links

- [Evidence directory](evidence-2026-10-26/)
- [Test reproduction instructions](../tests/README.md)
- [Recovered source and build evidence](recovered-source/)
- [Independent approval record](module-1-approval-decision.md)
