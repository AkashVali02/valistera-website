# ValiStera Solutions website

This repository contains the static website deployed to Cloudflare Workers from the `main` branch.

## Pages and assets

- The 18 public content pages use clean URLs, such as `/services` and `/training`.
- Shared styling is in `styles.css`; navigation and enquiry behavior are in `script.js`.
- `analytics.js` manages optional GA4 consent. Analytics is disabled until accepted; advertising storage and personalization remain denied.
- Photographs, responsive variants, licensed fonts and six downloadable resources are in `assets/`.
- `404.html` is served with HTTP 404 for missing addresses through `assets.not_found_handling` in `wrangler.jsonc`.
- `sitemap.xml` lists the 18 content pages; the 404 page is excluded and marked `noindex`.

## Enquiries

The contact form submits JSON to the existing `valistera-enquiry-api` Worker after browser validation and Cloudflare Turnstile verification. The API's code, mail delivery configuration and credentials are maintained separately from this static repository. Keep its endpoint and payload field names aligned with `script.js`.

Service and course links prefill the relevant enquiry fields. A confirmed successful response clears the form and restores that context. Unconfirmed or failed requests preserve the entered details. Submission is guarded against concurrent requests and times out after 30 seconds; a timeout does not prove that the server failed to receive the enquiry. The page also provides a direct email link.

## Publishing

Upload replacement files at their original paths, retaining exact filenames. Root HTML, CSS, JavaScript and configuration files belong at the repository root. Images belong in `assets/images`; fonts belong in `assets`. Extract ZIP packages before uploading; an uploaded ZIP is not automatically extracted.

Cloudflare builds the commit on `main`. Confirm the matching commit's **Workers Builds: valistera-website** check succeeds before considering an upload deployed.

## Automatic checks

`wrangler.jsonc` runs `node validate-site.cjs` before deployment. The script needs only Node.js, makes no network requests and requires no credentials. A failed check exits with a nonzero status so the deployment stops for review.

It checks local links and anchors, required landmarks and image attributes, canonical and sitemap consistency, structured-data JSON, fingerprinted assets and browser-script syntax. Run the same command locally when needed. These structural checks complement interaction and visual testing; they do not measure PageSpeed, verify external websites or send enquiries.

## Maintenance

- Keep canonical URLs, visible breadcrumbs, structured metadata and sitemap entries consistent.
- Social image metadata must describe the referenced image and use its actual dimensions.
- Preserve the width descriptors, sizes, dimensions and fallback handlers on responsive images.
- `_headers` grants immutable caching only to fingerprinted assets. Use a new filename and update its exact header rule when replacing one.
- Original assets remain available as fallbacks; do not delete them while referenced.
- `.assetsignore` excludes repository configuration, development directories and ZIP archives from the public deployment.
- Careers lists no confirmed open vacancy. Technical resources require review and adaptation before operational use. Website references to regulatory frameworks or ISO 9001:2015 are not a guarantee of an outcome or a certification claim.

Public contact: contact@valistera.com · +91 84088 24025 · Pune, Maharashtra, India.
