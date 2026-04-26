---
name: webshop-vuln-scan
description: Active vulnerability scan of webshop endpoints. Combines sqlmap (SQLi), Dalfox/XSStrike (XSS), Commix (cmd injection), plus merch-specific checks (coupon abuse, IDOR, price tampering). Authorized engagements only.
---

# Webshop Vulnerability Scan

Phase 3 of merch-pentest. Active testing — generates traffic the target will see in logs/WAF.

## ⚠️ Authorization

This phase is **active** and may trigger:
- WAF blocks
- Rate-limit bans
- Alert pager-duties
- Apparent service degradation

Confirm with engagement contact before starting. Run against staging if available.

## Inputs

- Endpoint list from `merch-recon` Phase 1
- Auth tokens if testing logged-in flows (per engagement)
- Rate-limit ceiling

## Scan layers

### Layer 1 — Generic web vulns

#### SQL injection
```bash
sqlmap -u "https://shop.example/products?id=1" \
  --batch --random-agent --level=2 --risk=1 \
  --rate-limit 5 \
  --output-dir=./sqlmap-out
```
- Start at `--level=2 --risk=1` — escalate only with permission.
- For POST/JSON: use `--data` and `--method`.
- For GraphQL: extract query params, test each variable.

#### XSS — reflected & DOM
```bash
dalfox url "https://shop.example/search?q=test" --silence -o dalfox-out.json
# or, against a list
dalfox file urls.txt --worker 5 -o dalfox-out.json
```
For complex SPAs, supplement with XSStrike:
```bash
python3 ~/tools/XSStrike/xsstrike.py -u "https://shop.example/search?q=test" --crawl
```

#### Command injection
```bash
python3 -m commix --url="https://shop.example/api/render?template=x" --batch
```
Focus on: search-by-image endpoints, CSV export tools, PDF-render APIs.

### Layer 2 — Merch-specific checks

For each, document repro steps + impact + fix. **Do not exploit beyond proof.**

#### Price tampering
- Intercept `POST /cart/add` — modify `price` field in payload, check if backend re-validates
- Test negative quantities: `quantity: -1` → free items?
- Currency flip: `currency: "JPY"` while paying in EUR

#### Coupon abuse
- Stack codes: apply two `SUMMER20` in one cart
- Race condition: 50 parallel `POST /coupon/apply` with same single-use code
- Brute force: enumerate `/api/coupon/check?code=XXXX` with rate-limit testing

#### IDOR
- `GET /api/orders/<your_id>` → swap to `<your_id+1>`
- `GET /account/addresses/<id>` → enumerate
- Webhook URLs containing predictable IDs

#### Checkout race conditions
- Limited-stock item: 100 parallel `POST /checkout/complete`
- Gift card double-spend: parallel `POST /apply-gift-card`

#### File-upload abuse (print-on-demand)
- Custom-engraving / artwork upload — try:
  - Polyglot files (image + PHP/JS payload)
  - SVG with embedded `<script>` (stored XSS)
  - Filename traversal: `../../etc/passwd`
  - Oversized files (DoS check — only with explicit auth)

#### Webhook signature bypass
- Capture a Shopify webhook HMAC
- Modify body, recompute → does the BFF reject?
- Replay old webhook → idempotency check

### Layer 3 — Auth & session

- Password reset: token entropy, reuse, host-header injection
- Session cookies: `Secure`, `HttpOnly`, `SameSite` flags
- JWT (if used): `alg: none`, weak secret, kid path traversal
- OAuth flows: redirect_uri validation, PKCE missing

## Output

`vuln-findings-<engagement>-<date>.md`:

```
# Finding N — <Title>
**Severity**: Critical/High/Medium/Low
**CVSS**: 3.1 vector
**Affected**: URL/endpoint/parameter
**Description**: ...
**Reproduction**:
1. ...
2. ...
**Impact**: ...
**Recommendation**: ...
**Evidence**: (sanitized request/response snippets)
```

## Tooling

| Tool | Purpose | Install |
|---|---|---|
| sqlmap | SQLi | `pip3 install sqlmap` |
| dalfox | XSS scanner | `go install github.com/hahwul/dalfox/v2@latest` |
| XSStrike | XSS DOM-aware | `git clone https://github.com/s0md3v/XSStrike ~/tools/XSStrike` |
| commix | Command injection | `pip3 install commix` |
| ffuf | Param fuzzing | `go install github.com/ffuf/ffuf/v2@latest` |

For race conditions: Burp Suite Repeater "send group in parallel" or `turbo-intruder`.
