# Module 3 — Design Qualification: recovery and consolidated review

Preview only. Independent GMP consultant approval and owner release authorization remain mandatory. Module 1/2 approval does not approve Module 3.

## Recovered checkpoint

Branch academy-player-preview; draft PR #3. Recovered head 02dc10bda0ed94a9a398a4c1a8ef788847dd4c84. Original source 43abdb644869dbf7dc6eff5db44324abe9887f93; runtime fix 57ab0edd6fe71f8460bfa4f5e542595f413de9f1.

Run 41034790586 failed in narration; kokoro-onnx 0.4.9 supplied integer speed to an ONNX model expecting float. The committed fix preserves float32 speed 0.92. Run 41035348010 completed successfully and committed ten narrated videos and their supporting assets as 02dc10b. Artifact 12967484506 remains available. Cloudflare check 123999722368 reports successful preview deployment of that commit. The ChatGPT session becoming read-only has no established root cause.

No prior local working tree was available in this session. Exact lost edits cannot be identified. Repository inspection showed the two named visual improvements were absent: generic vessel drawings remained at cleaning pockets (3.4 parts 3/4) and maintenance access (3.6 part 2). Only these missing illustrations and their two video tracks were reconstructed. Narration was preserved, with identical compressed-audio SHA256 before/after; see visual-recovery.json. Captions and scene boundaries were retained.

## Package and corrections

Ten narrated lessons, forty original diagrams, ten worked examples, ten lesson checks, twenty distinct application assessment questions, workbook, two CSV templates, source map, rights notices and provenance. Total media duration is approximately 21.05 minutes. All media is committed; no temporary workflow output is required for playback.

Cleaning illustration now contrasts a continuous outlet with a low liquid-retaining pocket. Maintenance illustration explicitly shows a rear instrument's removal path blocked by a pipe rack. Both are qualitative, not engineering acceptance drawings. Existing white Vali / blue Stera identity and aligned key-point numbering are preserved.

All forty diagram/description groups begin collapsed behind View Technical Explanation. Native timeline controls remain the only seek bar. Deployment manifest now includes MP4, PNG and CSV bytes as well as pages/captions, enabling verification of the actual delivered media.

## Verification and evidence interpretation

Recovery local checks: content structure/calculations passed; 140 media checks passed; source/media fingerprint check passed; website validation passed (61 HTML pages). Final workflow and hosted evidence must be read by their own commit and scope; older browser-results.json must not be mistaken for new hosted results. The default local Chrome download was invalid; an official older build downloaded successfully but execution was blocked by the runtime socket restriction. Fresh browser execution therefore uses GitHub Actions. Recovery run 41060453879 passed its local browser suite before saving the corrected media. The final recovery workflow additionally waits for Cloudflare to serve its persisted commit, compares delivered bytes, and runs the same suite against that hosted preview. Read its downloadable artifact for the final outcome; workflow presence alone is not a pass.

Reviewed all 40 narration passages and all 20 assessment answers/explanations. Official EudraLex index, adopted Annex 15, Chapter 3 and Chapter 4 were retrieved on 30 October 2026. The source map distinguishes DQ from later qualification, fictional criteria from regulatory requirements, supplier evidence from site accountability, and conditional progression from routine release. This is an AI technical pre-review, not independent GMP approval.

Decoded video frames were compared against all forty intended scene PNGs at their midpoints: 40 passed, maximum mean absolute RGB difference 1.96/255 (limit 8/255). See frame-results.json. This confirms encoded scene identity, not human audio comprehension.

## Reviewer instructions and release gates

1. Check the served commit footer and review-build.json before reviewing; match them to the PR head and hosted evidence.
2. Read lessons 3.1–3.10 with transcripts; listen to every video and assess pronunciation, pacing, diagram/narration meaning and captions. Inspect the corrected outlet and access illustrations closely.
3. Complete the independent assessment and workbook; review answer rationales and fictional acceptance assumptions against source-map.md.
4. Perform real Android/iOS touch seeking and reading comfort checks, plus screen-reader/manual accessibility evaluation. Automated Chromium/axe checks do not certify WCAG conformity.
5. Independent GMP consultant must document findings and sign-off against the exact candidate commit. Owner must accept media/rights/privacy limitations and explicitly authorize production release.

No merge, production deployment, human listening acceptance, independent signature or regulatory certification is claimed. Upstream voice training-data rights and hosting log retention are not independently verified. Preview approval is not production authorization.
