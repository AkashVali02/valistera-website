# Module 1 — production release evidence
Date: 26 October 2026 (UTC)

## Decision and deployed revision
The owner reported consultant approval and explicitly authorized publication in this conversation. No consultant identity, signature, detailed scope, regulatory approval or certification is fabricated.

PR #1 was merged as 9536bfe32ef96f7b3ecf37a0c8f9084a127b212e.
Final production commit: a0da0515034e16bba939a27f62d24eefd09d8bfe.
Production Cloudflare check: Workers Builds: valistera-website, completed / success.
Build ID: ababa0e4-e89c-44b3-b858-5e1cb7d5b8d7.
Version ID: 52389710-b13d-4682-b4c4-195eba1861f9.
Evidence source: https://api.github.com/repos/AkashVali02/valistera-website/commits/a0da0515034e16bba939a27f62d24eefd09d8bfe/check-runs

Course URL: https://valistera.com/academy-gmp-foundations

## Changes at release
- Academy landing links to the full ten-lesson module.
- Course overview has production canonical/indexing metadata and sitemap entry.
- Learner-facing preview wording changed to course wording.
- Root QA folder excluded from deployed assets. An initially broad academy exclusion was corrected to root-anchored /academy/ and /academy/** so assets/academy remains eligible for deployment.
- Media, captions, assessment content and single Play lesson interaction retain the reviewed candidate behavior.

## Testing and scope
Release preparation passed site validation: 31 HTML files and 1,050 local references; caption validation; 49 static media checks.
Reviewed player candidate evidence already stored: 305 browser checks, 112 extended checks and two retry-path checks passed. Hosted preview HTML and shared JS/CSS hashes matched the tested candidate. See the final QA report and evidence-2026-10-26 directory for detailed scope; these are not fresh production playback passes.

Production build succeeded for both the release merge and subsequent asset-exclusion correction.
Production playback smoke checks did NOT complete: the automated browser received a Cloudflare “Just a moment...” browser-verification page. No completed live ten-lesson playback or production media-availability pass is claimed. This is a limitation of the verification environment, not proof that ordinary users are blocked. Security settings were not weakened or bypassed.

## Operational status
Publication completed; production playback verification remains unconfirmed because of the challenge. User-reported consultant acceptance is recorded separately from automated evidence and historical unsigned reviewer fields.
Rollback baseline: 9b4ec003312f9d951399368ffea88624f76350d2. Revert the release and associated hotfix via new commits if required, then verify the rollback build.
