# ValiStera development readiness and production-verification runbook

Updated 2026-11-08. This is a review-stage record; no live configuration was changed by this branch.

## Evidence and verified boundaries
- Main website deployment configuration: `wrangler.jsonc` with `assets.directory: "./"`; build stamps Academy modules 2–4, then runs `node validate-site.cjs`.
- The **Workers Builds: valistera-website** check succeeded for commit `357d3b5b537db0514085c0bdac9357660c8c99b5` on 2026-11-06.
- Separate Module 3 and 4 production-verification workflows failed while requesting the hosted release manifest: they received repeated HTTP **403**. Their local content checks passed, but the hosted-delivery and browser stages did not complete. This does **not** establish that production is healthy or unhealthy.
- The frontend contact form POSTs to `https://valistera-enquiry-api.gadadeakash72.workers.dev/`. Server-side source, delivery secrets, and production logs are outside this repository, so endpoint health and mail/HubSpot outcomes are not verified.
- Draft PR #5 contains a **non-deployed** HubSpot adapter. Keep it independent until the real enquiry Worker source is accessible and an end-to-end staging test passes.
- `website_refresh` is an alternative static site whose README describes email-app form handling; it must **not** replace the current Turnstile/enquiry API implementation without design and approval.

## Proposed changes in this branch
1. Both production QA workflows call `.github/scripts/verify-production-manifest.sh`. For a 401/403, it fails immediately and records only safe headers (`cf-ray`, `content-type`, `server`); it neither bypasses security nor falsely reports success. Non-denial failures and commit mismatches continue through the existing bounded retry window.
2. `.claude/settings.json` requests approval for common push, merge, destructive Git and Wrangler deployment/secret commands, and denies direct reads of common local secret files. These rules do not replace mandatory reviews, Cloudflare secrets, branch protection or account permissions; other command forms may be outside the rule's scope.
3. `.assetsignore` excludes `.claude` configuration from the public static site.

## Cloudflare owner investigation (requires dashboard access)
1. Open Cloudflare Security Events and inspect requests to `valistera.com` at **2026-11-06 17:13–17:15 UTC**. Filter by request path `/assets/academy/module-3/review/review-build.json` and `/assets/academy/module-4/review/review-build.json`. Inspect triggered rule, request classification and Ray ID, if present.
2. Also inspect Zero Trust Access application policies (if configured) for the domain. A 403 can originate from WAF/bot rules, Access, or another intermediary; do not assume which.
3. Check whether ordinary unauthenticated visitors can load the pages and media in a normal browser. If blocked, treat as a site availability issue. If only CI is blocked, design a narrowly scoped authenticated verification path with owner review; **do not globally disable security protections** or hardcode tokens.
4. Do not merge or redeploy solely to make a check green. Re-run hosted verification after the security cause is understood; require matching commit and bytes, then browser tests.

## Enquiry Worker acceptance gates
- Read existing Worker source and runtime environment without copying secrets into repository/chat.
- Match frontend JSON: `name`, `organization`, `email`, `phone`, `country`, `service`, `projectStage`, `preferredContact`, `message`, `privacyConsent`, `website`, `turnstileToken`.
- Verify server-side Turnstile validation, consent, spam checks, mail delivery, CORS, rate limiting, retry/idempotency and privacy retention.
- Only after existing mail delivery passes, stage the HubSpot adapter; prevent duplicate CRM contacts and false success reporting; obtain explicit release approval before production.

## Local setup checks (not performed by this remote GitHub change)
- In the existing VS Code repository, use `git status` to inspect uncommitted files. Do not switch branches while changes are uncommitted.
- Use `node validate-site.cjs` for offline structural checks.
- When npm connectivity works, install/use a documented Wrangler version, then inspect `wrangler --version` and use `wrangler dev` **only for local preview**.
- In Claude Code, use `/status` to confirm the project settings were loaded after pulling this branch. Kilo Code's permission prompts require a separate review.
- No production deploy, Git push to `main`, merge or Cloudflare policy change is part of this work.

## Release gate
Keep this PR in draft until the shell/YAML changes pass review, the Cloudflare 403 root cause is diagnosed, hosted checks can run successfully, and the owner approves a merge. Do not equate a green Cloudflare build with completed post-deploy QA.
