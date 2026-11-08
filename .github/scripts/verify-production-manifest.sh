#!/usr/bin/env bash
# Fail closed on Access/WAF denial; do not weaken Cloudflare security to pass QA.
set -euo pipefail

module="${1:?Module number required}"
expected="${2:?Expected commit SHA required}"
base="${3:-https://valistera.com}"
case "$module" in 3|4) ;; *) echo "::error::Unsupported Academy module"; exit 2 ;; esac
if [[ ! "$expected" =~ ^[[:xdigit:]]{40}$ ]]; then
  echo "::error::Expected commit must be a 40-character SHA"
  exit 2
fi

headers="$(mktemp)"
body="$(mktemp)"
trap 'rm -f "$headers" "$body"' EXIT
served=""
for attempt in $(seq 1 40); do
  : >"$headers"
  : >"$body"
  status="$(curl --silent --show-error --max-time 15 --dump-header "$headers" \
    --output "$body" --write-out '%{http_code}' \
    "$base/assets/academy/module-$module/review/review-build.json?release=$expected")" || status="000"

  if [[ "$status" == "401" || "$status" == "403" ]]; then
    echo "::error::Production manifest access denied (HTTP $status). Inspect Cloudflare Security Events/Access with the timestamp and cf-ray; do not disable protection."
    grep -iE '^(cf-ray|content-type|server):' "$headers" || true
    exit 1
  fi

  if [[ "$status" == "200" ]]; then
    served="$(python3 - "$body" <<'PY'
import json
import sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    print(data.get("source_commit", "") if isinstance(data, dict) else "")
except (ValueError, OSError):
    print("")
PY
)"
    if [[ "$served" == "$expected" ]]; then
      echo "Production manifest verified for Module $module at commit $expected"
      exit 0
    fi
  fi

  echo "Module $module production manifest attempt $attempt: HTTP $status; matching commit not yet confirmed."
  if [[ "$attempt" -lt 40 ]]; then sleep 10; fi
done

echo "::error::Production manifest did not confirm expected commit after 40 attempts (last HTTP $status)."
exit 1
