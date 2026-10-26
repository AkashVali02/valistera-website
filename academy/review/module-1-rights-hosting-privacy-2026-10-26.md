# Module 1 — media provenance, hosting and browser storage

26 October 2026 · review branch only · not legal clearance.

## Inventory and evidence

`evidence-2026-10-26/media-inventory.json` records the ten original URLs, durations and SHA-256 hashes plus the corrected Lesson 1.8 derivative. All originals were downloaded and decoded to mono audio; URL accessibility is not evidence of ownership or redistribution permission.

No original narration voice licence, generation receipt/account terms, music/source asset list, original graphic/font provenance or explicit commercial redistribution permission was located in the Academy review files. These remain open for every original MP4 and the derivative. Do not represent the derivative as cleared merely because it was edited here.

The web lessons use system/Arial fonts, with no added font CDN request. The repository includes `assets/font-licenses.txt` for the wider website's DM Sans/Manrope files; this does not establish the fonts used in the pre-rendered videos. The new Lesson 1.8 overlay uses DejaVu Sans Bold; the installed package's Bitstream/DejaVu notice is retained in `assets/academy/dejavu-font-notice.txt`. The overlay changes only the heading and second action label during 80.18–107.08 seconds. The decoded audio SHA-256 is identical before and after the edit.

## Hosting controls implemented

- Nine original videos remain externally hosted on the original CloudFront domain. Permanent retention, account control, commercial terms, origin access, revocation, logging retention and regional processing cannot be inferred from the URL.
- Lesson 1.8's corrected review MP4 is stored with the preview source, using a same-origin relative URL. It does not require a CloudFront request.
- `data-src` and an explicit load button prevent automatic MP4 requests before learner action. No autoplay is introduced. Load errors offer transcript/reading fallback and a retry control.
- Page-level `no-referrer` suppresses referrer disclosure. This does not conceal IP addresses from a host selected by the learner.
- All ten lessons have native captions and static recorded-narration transcripts. Companion clarifications remain distinct from the transcript.
- No new analytics, form submission, third-party script, tracking pixel or paid media-generation operation was introduced.

## Local storage

Keys are scoped to `valistera_gmp_11` through `valistera_gmp_110` for `_position`, `_watched`, `_quiz`, and `valistera_gmp_module1_assessment_draft` / `_result`. Stored values include playback seconds, completion flags, answer selections and latest score/completion date. These are self-study aids, not validated competency/training records. They can be edited by a learner and do not prove actual watch time or competence.

A complete notice is now present on all 12 module pages, including previously missing Lessons 1.9 and 1.10. It explains device/profile scope, retention until overwrite/clear/browser removal, shared-profile visibility, third-party media requests and confidentiality. It links privacy/terms/support. A clear button deletes only this module's keys, preserving unrelated localStorage. Clearing does not prevent subsequent learning activity from saving new progress; the status message explains this. Assessment restart now deletes the stale saved result as well as the draft. The overview ignores scores outside 0–15.

Browser tests cover clearing with an unrelated sentinel key and rendering with the localStorage getter forced to throw SecurityError. These tests do not establish privacy-law compliance or hosting-provider retention practices.

## Release dependencies

Original asset provenance/licensing, vendor-hosting control and retention, and an appropriate privacy/terms review remain unresolved. No external rights holder was contacted and no permission was fabricated. Keep production NO-GO pending those records and the independent review gates.
