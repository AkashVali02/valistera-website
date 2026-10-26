> Release decision updated 26 October 2026: the owner reported consultant approval and explicitly authorized publication. See [the release decision record](module-1-approval-decision.md). The NO-GO statements below describe the pre-authorization technical QA snapshot, not the current owner decision. No technical evidence or independent signatures have been invented.

# ValiStera Academy Module 1 — consolidated final technical QA

**26 October 2026 · academy-player-preview · production NO-GO**

This report supersedes the earlier same-day final report, retained as [the pre-continuation record](module-1-qa-before-continuation-2026-10-26.md). It consolidates the original remediation and the subsequent feasible work in audiovisual quality, recorded content, accessibility, and rights/hosting. The current player implementation is commit `ef19d1e695cf70b3cc431a5317828648fb87edd4`; the following evidence/report commit completes this package. No production deployment or merge was performed.

## Delivered changes

- **Captions/transcripts:** all ten lessons have native VTT captions, matching embedded cue arrays and static transcripts. Earlier work corrected Lesson 1.1 timing drift, split long cues, balanced lines and checked questionable ASR phrases. The new 1.4/1.5 recordings have fresh base.en word-timestamp ASR, source-script comparison, new timing and updated transcripts. Final structural checks find no overlap, nonpositive cue or media-duration overflow; zero cues exceed the 20.05 characters/second tolerance and all use at most two authored lines. This is a readability heuristic, not a WCAG rule or human synchronization sign-off.
- **Actual recorded corrections:** Lesson 1.4 scene 8 now describes an overdue measuring instrument used with a vessel. Lesson 1.5 scene 3 now states required independent dispensing checks, EU material/weight-or-volume checking, US second-person requirements with defined automated-equipment exceptions, and that local risk assessment cannot waive applicable requirements. Original diagrams and all other per-scene source audio were reused. Key-explanation start times were updated to the revised scene durations; static checks and 16 scene-level browser assertions cover those transitions. The revised videos are stored with the preview repository. The earlier Lesson 1.8 root-cause heading/action correction remains in place.
- **Accessible visual alternatives:** every lesson now includes a readable HTML guide describing the main diagram relationships in presentation order, alongside its transcript and companion reading. The guides explain illustrative risk scoring, status conflicts, investigation paths, reconciliation and other dense graphics without relying on colour. Ten scene contact sheets were inspected when authoring them. The changed 1.4/1.5 video frames were also inspected at full resolution. This does not establish every-frame equivalence or human audio-description acceptance.
- **Accessibility fixes and retest:** enlarged layout/text testing exposed overflow in the overview and several lesson pages. Flexible grids, wrapping headings/buttons/links and responsive padding fixed those findings. Earlier contrast, keyboard focus, skip-link, quiz legend, assessment semantics and reduced-motion fixes remain. Actual H.264/AAC playback is now verified in the connected media environment; the previous local codec limitation is no longer the sole playback evidence.
- **Privacy/storage:** earlier scoped localStorage clearing, complete notices, no-referrer, opt-in video loading, retry/transcript fallback, assessment reset and resume-overwrite fixes remain. All ten lessons now use same-origin video files retained in the preview repository. The seven migrated originals were copied byte-for-byte and SHA-256 verified; the three reviewed derivatives remain unchanged. All twelve privacy notices now correctly describe requests to the website host. No new analytics or paid generation API was used.
- **Source/provenance recovery:** recovered original Kokoro scripts, model/voice identities and diagram-generation code. All ten original MP4s now match recovered workspace renders byte-for-byte. The final Lesson 1.1 assembly was identified as `fast_reveal/final.mp4`, and its drawing, staged-reveal and assembly scripts are retained. Stock `af_heart`, Pillow drawings and DejaVu font usage are documented, with publisher licensing links and observed file hashes. This narrows the rights gap; it does not invent legal clearance.

## Final executed evidence

| Test | Result | Evidence |
|---|---|---|
| Actual-media player, keyboard, quizzes, assessment, axe, storage clearing and responsive layout | **305/305 checks passed across 12 pages**; zero detected scoped axe violations | `browser-play-results.json` |
| Real muted video playback at 5%, 50%, 95%; increasing decoded frames; accessibility-tree roles/names; 2x/4x CSS layout zoom; text spacing at 320/1280 px | **112/112 checks passed across 12 pages** | `extended-play-results.json` |
| Ten final caption tracks | **All pass**; zero speed flags; maximum two authored lines | `caption-structure.json` |
| Complete video-stream decode and scene-change diagnostic | **10/10 decode successfully**; no more than one detected change per rolling second at the selected threshold | `full-decode-scene-scan.json` |
| Website validation | **Passed:** 31 HTML pages, 1,029 local references, sitemap, JSON, fingerprints and JS syntax | `node validate-site.cjs` |
| Patch whitespace validation | **Passed** | `git diff --check` |
| Denied localStorage regression from original remediation | **12/12 pages without uncaught errors**; implementation unchanged in continuation | `storage-denied.json` |

The current same-origin run recorded zero external requests throughout all tested interactions, with no MP4 request before learner action. All ten videos parsed captions, decoded metadata and passed paused-resume checks.

The final H.264 browser was **Chromium 153.0.8010.12**; axe was **4.10.3**. The tests served repository bytes through Playwright routes with byte-range handling. They did not test a deployed site's HTTP headers, CDN or physical devices. Tests used real media, not the earlier synthetic WebM fixture. Playback was muted and sampled at three positions; this is decode/control evidence, not a full listening review.

CSS layout zoom is not physical-device/browser-menu zoom. Accessibility-tree inspection is not an NVDA, JAWS, VoiceOver or TalkBack session. Zero axe findings is not WCAG 2.2 AA certification. The full-stream scene-change heuristic can miss localized or low-amplitude flashes and is not a validated photosensitive-epilepsy test. Historical `browser-results.json`, `browser-fixture-results.json`, `browser-h264-results.json` and `extended-accessibility.json` retain earlier runs; use browser-play-results.json and extended-play-results.json for the current candidate.

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

The [rights/hosting/privacy report](module-1-rights-hosting-privacy-2026-10-26.md) and [recovered-source notes](recovered-source/README.md) distinguish publisher licences from legal clearance. The observed local model/voice files are identified by hash, not misrepresented as independently verified upstream release checksums. Source paths show no music input. Operational access and matching hashes establish recovery of the source renders, not independent legal clearance. The player no longer relies on that workspace CDN. Official public hosting terms were reviewed; they do not supply an Academy-specific retention/logging schedule or availability commitment.

## Remaining external acceptance gates

1. **Human audiovisual acceptance:** final listening review of pronunciation, unclear original ASR words, timing, reading comfort and narration/companion differences; real-device readability and evaluation of the text alternatives. No human review signature was fabricated.
2. **Full accessibility acceptance:** actual assistive-technology operation, physical devices/browser-menu zoom, native controls and any required audio-description alternative; validated flashing analysis if required by the release process. The automated checks above are complete within their stated scope.
3. **Rights/hosting/privacy acceptance:** review recovered provenance and licence conditions, confirm commercial distribution/branding rights and approve durable hosting with known retention/logging and deletion controls. The separate external-media dependency is removed. Website-host retention/logging, backup and deletion commitments still require an accountable hosting/privacy decision; no production configuration is asserted.
4. **Independent GMP/privacy sign-offs and owner release decision:** remain unsigned. AI technical execution does not satisfy those independent approvals.

**Decision:** the feasible continuation is implemented and tested. The two recorded-content correction blockers, final Lesson 1.1 assembly provenance and seven external-media dependencies are technically resolved; human acceptance, legal/hosting decisions and independent sign-offs are still open. Production remains **NO-GO**. Owner release authorization is not requested for this candidate. Keep the package on `academy-player-preview`.

## Package links

- [Evidence directory](evidence-2026-10-26/)
- [Test reproduction instructions](../tests/README.md)
- [Recovered source and build evidence](recovered-source/)
- [Independent approval record](module-1-approval-decision.md)

## Final same-origin package evidence

`same-origin-media.json` records the ten repository paths, file sizes, SHA-256 values and old URLs for historical traceability. `same-origin-static.json` records 49 passing checks for hashes, unchanged original bytes, same-origin paths, deferred video loading and corrected notices. The active lesson pages do not contact the old CloudFront media host. The repository now retains the media needed by the preview; no new paid hosting service or production deployment was created. Historical external copies and Git history were not deleted.

The Lesson 1.1 render hash `7c23b00967139ce5c499eb1f37ec26cfde2a45501d8352c231fa076700dddf9d` matches both `fast_reveal/final.mp4` and the repository copy. The recovered chain is `make_lesson.py` → `premium_full.py` → `visual_enhanced.py` → `animate_align.py` → `rebuild_fast_reveal.py`. This closes the previously unidentified final visual assembly; independent rights acceptance is still distinct.

## One-tap player refinement

The separate load button, long pre-player notice and blank unloaded native player were replaced with an actual lesson-frame thumbnail and one accessible “Play lesson” button on all ten lessons. Activating it by touch/click or Enter requests playback immediately; MP4 loading remains deferred until that action. The native player appears for playback. If browser playback policy rejects the request, native controls remain available with a short instruction. Failed media loading restores a labelled Retry lesson control and transcript fallback. Privacy details stay in the existing lower-page notice. Static transcripts and a no-JavaScript direct-video link remain available.

The 305-check run includes poster visibility, hidden unloaded controls, single keyboard activation starting actual playback on all ten lessons, and saved-position resume. The 112 extended checks passed again. A separate network-failure/retry test passed, and the mobile Lesson 1.6 poster was visually inspected. Hosted verification fetched all ten lesson pages plus shared player JS/CSS and compared their bytes to the tested candidate; see `hosted-play-verification.json`. No production merge or deployment action was performed.
