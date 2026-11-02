/**
 * Optional server-side HubSpot adapter for the separately deployed enquiry Worker.
 * NOT deployed by this repository. Import ONLY after verified Turnstile,
 * consent, honeypot, payload validation and existing delivery handling.
 *
 * Required secret: env.HUBSPOT_PRIVATE_APP_TOKEN (never exposed to browsers).
 * Return value is intentionally narrow; do not log the raw payload or token.
 * CRM sync failure must not erase an otherwise successfully delivered enquiry.
 */
const HUBSPOT_API = "https://api.hubapi.com";
const ALLOWED_SERVICES = new Set([
  "Qualification & Validation", "GMP Compliance", "Inspection Readiness",
  "Regulatory Services / CMC", "Sterile Manufacturing",
  "Digital Quality & CSV", "Training / ValiStera Academy",
  "Other / Multi-service engagement"
]);

function clean(value, max = 255) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}
function splitName(name) {
  const words = clean(name).split(/\s+/).filter(Boolean);
  return { firstname: words.shift() || "", lastname: words.join(" ") };
}
async function hubspotRequest(token, path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(HUBSPOT_API + path, {
      ...options,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        ...(options.headers || {})
      },
      signal: controller.signal
    });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error("HubSpot request failed");
      error.status = response.status;
      throw error;
    }
    return body;
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Synchronizes a validated enquiry contact by email via HubSpot's upsert API.
 * Caller MUST establish valid consent and anti-spam checks independently.
 * Do not call on unverified browser requests.
 *
 * HubSpot private-app token needs crm.objects.contacts.write permission.
 * Marketing subscription consent is NEVER inferred from enquiry consent.
 */
export async function syncVerifiedEnquiryToHubSpot(env, enquiry) {
  const token = env?.HUBSPOT_PRIVATE_APP_TOKEN;
  if (!token) return { ok: false, reason: "not_configured" };
  if (enquiry?.privacyConsent !== true) {
    return { ok: false, reason: "consent_missing" };
  }
  const email = clean(enquiry.email, 254).toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { ok: false, reason: "invalid_email" };
  }
  const name = splitName(enquiry.name);
  const service = clean(enquiry.service);
  const properties = {
    email,
    firstname: name.firstname,
    lastname: name.lastname,
    company: clean(enquiry.organization),
    phone: clean(enquiry.phone, 60),
    country: clean(enquiry.country, 100),
    lifecyclestage: "lead"
  };
  // Never put arbitrary free-text project descriptions into CRM properties,
  // because the general form is not an approved confidential file channel.
  // Service is intentionally not sent without a verified custom property.
  void ALLOWED_SERVICES.has(service);
  try {
    const result = await hubspotRequest(
      token,
      "/crm/v3/objects/contacts/batch/upsert",
      {
        method: "POST",
        body: JSON.stringify({
          inputs: [{ id: email, idProperty: "email", properties }]
        })
      }
    );
    return { ok: true, contactId: result.results?.[0]?.id || null };
  } catch (error) {
    return {
      ok: false,
      reason: error.status === 429 ? "rate_limited" : "crm_unavailable"
    };
  }
}
