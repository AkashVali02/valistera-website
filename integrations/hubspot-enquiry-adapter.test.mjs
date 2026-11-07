import assert from "node:assert/strict";
import { test, mock } from "node:test";
import { syncVerifiedEnquiryToHubSpot } from "./hubspot-enquiry-adapter.mjs";

const input = {
  name: "Example Test", organization: "Example Test Company",
  email: " Test@example.com ", country: "India",
  service: "Qualification & Validation", privacyConsent: true
};

test("refuses requests without consent", async () => {
  assert.deepEqual(await syncVerifiedEnquiryToHubSpot(
    { HUBSPOT_PRIVATE_APP_TOKEN: "test-token" },
    { ...input, privacyConsent: false }
  ), { ok: false, reason: "consent_missing" });
});
test("refuses invalid email", async () => {
  const result = await syncVerifiedEnquiryToHubSpot(
    { HUBSPOT_PRIVATE_APP_TOKEN: "test-token" },
    { ...input, email: "invalid" }
  );
  assert.equal(result.reason, "invalid_email");
});
test("does not contact CRM without configured secret", async () => {
  assert.equal((await syncVerifiedEnquiryToHubSpot({}, input)).reason, "not_configured");
});
test("upserts a normalized contact without marketing consent or enquiry message", async () => {
  const oldFetch = globalThis.fetch;
  let sent;
  globalThis.fetch = async (url, options) => {
    sent = { url, options };
    return { ok: true, json: async () => ({ results: [{ id: "123" }] }) };
  };
  try {
    const result = await syncVerifiedEnquiryToHubSpot(
      { HUBSPOT_PRIVATE_APP_TOKEN: "test-token" }, { ...input, message: "PRIVATE" }
    );
    assert.equal(result.ok, true);
    assert.equal(result.contactId, "123");
    const body = JSON.parse(sent.options.body);
    assert.equal(body.inputs[0].id, "test@example.com");
    assert.equal(body.inputs[0].properties.email, "test@example.com");
    assert.equal(body.inputs[0].properties.firstname, "Example");
    assert.equal(body.inputs[0].properties.lastname, "Test");
    assert.equal(JSON.stringify(body).includes("PRIVATE"), false);
    assert.equal(JSON.stringify(body).includes("marketing"), false);
  } finally { globalThis.fetch = oldFetch; }
});
test("reports CRM outage without throwing raw error details", async () => {
  const oldFetch = globalThis.fetch;
  globalThis.fetch = async () => { throw Error("private backend diagnostic"); };
  try {
    const result = await syncVerifiedEnquiryToHubSpot(
      { HUBSPOT_PRIVATE_APP_TOKEN: "test-token" }, input
    );
    assert.deepEqual(result, { ok: false, reason: "crm_unavailable" });
  } finally { globalThis.fetch = oldFetch; }
});
