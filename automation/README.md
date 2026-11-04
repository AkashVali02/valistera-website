# ValiStera AI Operations Platform — Foundation (draft)

**Status:** Source-controlled foundation only. No autonomous backend, scheduler, credential vault, social publishing integration or production deployment is claimed.

## Architecture
1. **Controller**: receives tasks, validates agent/action and owner approvals via `policy.mjs`, writes durable task state, routes to workers.
2. **Workers**: Sales (HubSpot), Marketing (Canva and approved publishing APIs), Website (GitHub), Backend (Cloudflare), Academy, GMP Quality.
3. **Durable execution**: Cloudflare Queues or a suitable workflow engine with retries, idempotency keys, encrypted secrets and dead-letter handling. Select after verifying cost and service access.
4. **Audit**: append-only task events (request, policy decision, tool action, result, review), redact personal information and credentials.
5. **Approval**: owner approval must bind task ID, exact action and current artifact version; backend must independently authenticate approval identity. This local policy module alone is NOT a security boundary.

## Initial workflows
| Trigger | Agent | Action | Release gate |
| --- | --- | --- | --- |
| Weekly planning | Marketing | Draft technical post + design brief | Human review before public publishing |
| New validated enquiry | Backend / Sales | CRM contact sync, dedupe, internal qualification | Verified consent and secure Worker integration |
| GitHub change | Website | Static checks, draft PR | Human approval before merging/deploying |
| Academy module update | Academy / Quality | Content, assessment and accessibility pre-review | Consultant/owner sign-off for release |
| Scheduled pipeline review | Sales | Internal HubSpot review | No fabricated prospects or outbound messages |

## Configuration contract (no real credentials here)
- `HUBSPOT_PRIVATE_APP_TOKEN`: secret only in Cloudflare backend, least-privilege scopes
- `OPENAI_API_KEY`: secret only in backend; set model budget and token ceiling
- Social platform credentials: per-platform scoped secrets, only after approved API access
- `APPROVAL_SIGNING_KEY`: secret to validate authentic approvals, not in website JavaScript
- `DATABASE` / `QUEUE`: durable state and retry infrastructure (not provisioned)

## Security and business rules
- Never publish, message prospects, spend money, deploy production, or create externally visible commitments without owner authorization.
- No false ISO certifications, clients, case studies or invented GMP records.
- Do not send client-sensitive records to model providers without lawful basis and approved controls.
- Separate enquiry response consent from marketing subscription opt-in.
- Require provenance for every regulatory claim; qualified human approval remains mandatory.
- Do not claim tasks executed simply because source code or a PR exists.

## Verification and next milestones
Run `node --test automation/policy.test.mjs` using Node 20+; test has not yet been executed by the assistant. Then configure CI, durable storage and a real controller, verify connected service scopes, implement staging with synthetic test records, and test end-to-end before production.

## Controller implementation status (4 Nov 2026)
- `controller.mjs` provides injected transactional-store contract, duplicate task admission, atomic claims, state transitions, and handler isolation.
- `controller.test.mjs` covers single execution, duplicate submissions, verified approval, unavailable handlers, failure redaction, and GMP human-only gates.
- `MemoryTaskStore` is **test-only** and not durable across restarts or safe across multiple workers.
- Approval verifier defaults to denial; production must authenticate signatures, identities, task/artifact version and expiry. The example callback accepting all approvals is for isolated tests only.
- No external adapters, durable database, retry scheduler, queue, or deployed API exist yet. Tests are authored but not verified as executed.
