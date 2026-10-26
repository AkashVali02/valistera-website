# ValiStera Academy Module 1 — Media and Release Evidence Addendum
Date: 2026-10-26
Branch: academy-player-preview (not production)
Status: TECHNICAL WORK IN PROGRESS — NOT RELEASE APPROVED

## Direct media verification
All ten lesson HTML pages reference reachable CloudFront MP4s. FFprobe read the actual media duration for each video. Native VTT files were retrieved from the deployed preview and parsed against actual media duration.

| Lesson | Video duration (s) | Native VTT cues | Overlaps | Cues exceeding video end | Cues >20 chars/second |
|---|---:|---:|---:|---:|---:|
| 1.1 | 527.7 | 156 | 0 | 0 | 14 |
| 1.2 | 235.0 | 49 | 0 | 0 | 0 |
| 1.3 | 262.3 | 50 | 0 | 0 | 0 |
| 1.4 | 225.8 | 47 | 0 | 0 | 1 |
| 1.5 | 229.2 | 47 | 0 | 0 | 0 |
| 1.6 | 216.8 | 44 | 0 | 0 | 0 |
| 1.7 | 222.7 | 43 | 0 | 0 | 0 |
| 1.8 | 214.1 | 44 | 0 | 0 | 1 |
| 1.9 | 219.4 | 43 | 0 | 0 | 0 |
| 1.10 | 236.8 | 48 | 0 | 0 | 0 |

The 20-character-per-second flag is a conservative review heuristic, not a universal WCAG pass/fail threshold. Retiming these cues without speech alignment could make synchronization worse; they remain flagged for audio-aligned correction. Existing videos have not been edited. Written companion reading is explicitly labeled as not necessarily narrated (verified on Lesson 1.6).

## Functional smoke tests
Automated preview checks returned HTTP 200 for 12 module pages and reported zero failures in module_release_qa.cjs. Smoke tests do not establish full WCAG compliance.

## Privacy and rights
Spot-check of overview, Lessons 1.1 and 1.6, and assessment confirmed browser localStorage usage and privacy-related text exists in each HTML page. Presence of disclosure text does not establish legal adequacy. CloudFront MP4 access is verified, but media licensing/ownership/redistribution rights cannot be inferred from accessibility.

## Unresolved release gates
1. Audio-to-VTT transcription and word-level timing verification: not performed; cue duration checks are insufficient.
2. Video narration and visual technical content compared against final written content: not performed.
3. Exact regulatory citations verified against currently effective official provisions: not completed.
4. Full WCAG 2.2 AA manual/assistive technology audit: not completed.
5. Media rights provenance and legal/privacy assessment: evidence outstanding.
6. Independent internal and external senior GMP review, and owner GO/NO-GO: not obtained.

## Decision
NO-GO for production. Continue technical remediation on preview branch only. Do not represent this addendum as independent consultant approval.
