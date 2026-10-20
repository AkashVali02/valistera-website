/* Dependency-free checks for this static site. Runs before Wrangler deployment. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const ROOT = __dirname;
const BASE = 'https://valistera.com';
const errors = [];
const check = (condition, message) => { if (!condition) errors.push(message); };
const read = file => fs.readFileSync(path.join(ROOT, file), 'utf8');
const decode = text => text.replace(/&(#x[\da-f]+|#\d+|amp|quot|apos|lt|gt);/gi, (_, value) => {
  if (value[0] === '#') return String.fromCodePoint(value[1].toLowerCase() === 'x' ? parseInt(value.slice(2), 16) : Number(value.slice(1)));
  return ({amp:'&',quot:'"',apos:"'",lt:'<',gt:'>'})[value.toLowerCase()];
});
function attrs(text) {
  const result = {};
  for (const match of text.matchAll(/([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) {
    const key = match[1].toLowerCase();
    check(!Object.hasOwn(result, key), `Duplicate attribute: ${key}`);
    result[key] = decode(match[2] ?? match[3] ?? match[4] ?? '');
  }
  return result;
}
function parsePage(file) {
  const source = read(file);
  const markup = source.replace(/<!--[\s\S]*?-->/g, '').replace(/<(script|style)\b([^>]*)>[\s\S]*?<\/\1\s*>/gi, '<$1$2></$1>');
  const tags = [...markup.matchAll(/<([a-z][\w:-]*)\b([^<>]*?)>/gi)].map(m => ({name:m[1].toLowerCase(), attrs:attrs(m[2])}));
  const ids = tags.filter(t => t.attrs.id).map(t => t.attrs.id);
  check(new Set(ids).size === ids.length, `${file}: duplicate element IDs`);
  check(tags.filter(t => t.name === 'main').length === 1, `${file}: expected one main landmark`);
  check(tags.filter(t => t.name === 'h1').length === 1, `${file}: expected one H1`);
  check(tags.some(t => t.name === 'html' && t.attrs.lang), `${file}: missing page language`);
  check(/<title>[^<]+<\/title>/i.test(source), `${file}: missing title`);
  check(!/<img\b[^>]*\/\s+\w+=/i.test(source), `${file}: malformed image attributes`);
  for (const t of tags) {
    if (t.name === 'img') check(Object.hasOwn(t.attrs, 'alt') && Number(t.attrs.width) > 0 && Number(t.attrs.height) > 0, `${file}: image needs alt and dimensions`);
    for (const key of ['aria-controls','aria-labelledby','aria-describedby']) {
      for (const id of (t.attrs[key] || '').split(/\s+/).filter(Boolean)) check(ids.includes(id), `${file}: ${key} points to missing #${id}`);
    }
  }
  for (const match of source.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (attrs(match[1]).type === 'application/ld+json') {
      try { JSON.parse(match[2]); } catch { errors.push(`${file}: invalid structured-data JSON`); }
    }
  }
  const canonical = tags.filter(t => t.name === 'link' && t.attrs.rel === 'canonical').map(t => t.attrs.href);
  const noindex = tags.some(t => t.name === 'meta' && t.attrs.name === 'robots' && /\bnoindex\b/i.test(t.attrs.content));
  if (!noindex) {
    const expected = BASE + (file === 'index.html' ? '/' : '/' + file.replace(/\.html$/, ''));
    check(canonical.length === 1 && canonical[0] === expected, `${file}: canonical URL is missing or incorrect`);
    const og = tags.filter(t => t.name === 'meta' && t.attrs.property === 'og:url');
    check(og.length === 1 && og[0].attrs.content === expected, `${file}: Open Graph URL differs from canonical`);
    check(tags.some(t => t.name === 'meta' && t.attrs.name === 'description' && t.attrs.content), `${file}: missing description`);
  }
  return {file, tags, ids:new Set(ids), canonical:canonical[0], noindex};
}

try {
  const pages = new Map(fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).map(f => [f, parsePage(f)]));
  check(pages.has('index.html') && pages.has('contact.html') && pages.has('404.html'), 'Home, Contact and 404 pages must exist');
  let localReferences = 0;
  function reference(value, page) {
    let url;
    try { url = new URL(value, BASE + (page.file === 'index.html' ? '/' : '/' + page.file)); } catch { errors.push(`${page.file}: invalid URL ${value}`); return; }
    if (url.origin !== BASE) return;
    let filename;
    try { filename = decodeURIComponent(url.pathname).replace(/^\//, '') || 'index.html'; } catch { errors.push(`${page.file}: invalid URL encoding ${value}`); return; }
    if (!fs.existsSync(path.join(ROOT, filename)) && !path.extname(filename)) filename += '.html';
    localReferences++;
    check(fs.existsSync(path.join(ROOT, filename)) && fs.statSync(path.join(ROOT, filename)).isFile(), `${page.file}: missing local file ${value}`);
    if (url.hash && pages.has(filename)) check(pages.get(filename).ids.has(decodeURIComponent(url.hash.slice(1))), `${page.file}: missing anchor ${value}`);
  }
  for (const page of pages.values()) {
    for (const tag of page.tags) {
      for (const key of ['href','src']) if (tag.attrs[key]) reference(tag.attrs[key], page);
      if (tag.attrs.srcset && !tag.attrs.srcset.startsWith('data:')) for (const candidate of tag.attrs.srcset.split(',')) reference(candidate.trim().split(/\s+/)[0], page);
      if (tag.name === 'meta' && [tag.attrs.name,tag.attrs.property].some(x => ['og:image','twitter:image'].includes(x))) reference(tag.attrs.content, page);
    }
  }
  const sitemap = [...read('sitemap.xml').matchAll(/<loc>(.*?)<\/loc>/g)].map(m => decode(m[1]));
  const expected = [...pages.values()].filter(p => !p.noindex).map(p => p.canonical);
  check(new Set(sitemap).size === sitemap.length && sitemap.length === expected.length && expected.every(u => sitemap.includes(u)), 'Sitemap must match all indexable page canonicals');
  check(pages.get('404.html')?.noindex, '404 page must be marked noindex');
  check(read('robots.txt').includes('Sitemap: '+BASE+'/sitemap.xml'), 'robots.txt must declare the sitemap');
  // Wrangler validates JSONC syntax; accept comments in its configuration here.
  check(/"not_found_handling"\s*:\s*"404-page"/.test(read('wrangler.jsonc')), 'Missing-page routing must use 404-page');
  const headerPaths = read('_headers').split(/\r?\n/).filter(line => line.startsWith('/'));
  check(headerPaths.length <= 100, 'Cloudflare _headers exceeds 100 rules');
  for (const url of headerPaths) {
    if (url.includes('*')) continue;
    const filename = url.slice(1), file = path.join(ROOT, filename);
    check(fs.existsSync(file), `Header rule references missing ${filename}`);
    const hash = filename.match(/-([a-f\d]{10})\.(?:woff2|webp|jpg)$/)?.[1];
    if (hash && fs.existsSync(file)) check(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex').startsWith(hash), `Fingerprint mismatch: ${filename}`);
  }
  for (const filename of ['script.js','analytics.js']) {
    try { new vm.Script(read(filename), {filename}); } catch (error) { errors.push(`${filename}: ${error.message}`); }
  }
  if (!errors.length) process.stdout.write(`Website checks passed: ${pages.size} HTML pages, ${localReferences} local references, sitemap, JSON data, asset fingerprints and JavaScript syntax.\n`);
} catch (error) { errors.push(error.message); }
if (errors.length) {
  process.stderr.write('Website checks failed:\n' + errors.map(e => '- '+e).join('\n') + '\n');
  process.exitCode = 1;
}
