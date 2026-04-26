---
name: merch-recon
description: Reconnaissance pipeline for e-commerce / merch shop pentests. Subdomain enumeration, tech-stack fingerprint, endpoint discovery, Nuclei vulnerability templates. Use as Phase 1 of merch-pentest. Authorized engagements only.
---

# Merch Recon

Phase 1 of a merch pentest. Builds the attack surface map.

## ⚠️ Authorization

Only run against domains the user **owns** or has **written authorization** to test (engagement letter, bug bounty program in-scope domain). Refuse if scope is unclear.

## Inputs

- Target apex domain (e.g. `examplemerch.com`)
- Hosting model: Shopify-managed / Self-hosted / Headless
- Rate limit ceiling from engagement

## Pipeline

### 1. Subdomain enumeration (passive)
```bash
subfinder -d <domain> -all -silent -o subs-raw.txt
```
Passive sources only — no DNS brute-force unless engagement allows.

### 2. Resolve and probe
```bash
dnsx -l subs-raw.txt -resp -silent -o subs-resolved.txt
httpx -l subs-resolved.txt -title -tech-detect -status-code -silent -o subs-live.json -json
```

### 3. Tech-stack fingerprint
Inspect `subs-live.json` for:
- Shop platform: Shopify (`x-shopify-` headers, `cdn.shopify.com`), WooCommerce (`/wp-content/plugins/woocommerce/`), Magento (`Mage.Cookies`), Medusa, Saleor, BigCommerce
- CDN/WAF: Cloudflare, Fastly, Akamai
- Frontend: Next.js, Remix, Hydrogen, Liquid (Shopify themes)
- Auth/payment: Stripe, PayPal, Klarna, Shop Pay

### 4. Endpoint discovery
```bash
gospider -S subs-live.txt -d 2 -c 10 --no-redirect -o gospider-out/
```
Look for: `/admin`, `/api/v1`, `/graphql`, `/checkout`, `/cart.json`, `/wp-admin`, `/wp-json`, `/.git`, `/sitemap.xml`, `/robots.txt`, `/.well-known/`

### 5. Nuclei templates (light)
Start with informational + medium severity, never DoS templates:
```bash
nuclei -l subs-live.txt -severity info,low,medium -tags cve,exposure,misconfig -rate-limit 50 -o nuclei-out.txt
```
Add `-severity high,critical` only after engagement-permitted depth.

### 6. Shop-specific probes
- `<domain>/products.json` — Shopify catalog leak
- `<domain>/.json` endpoints — public Shopify API
- `<domain>/admin.json`, `<domain>/admin/api/` — should be 401/403, not 200
- `<domain>/cart.js` — Shopify Ajax API
- GraphQL introspection: `POST /graphql {"query": "{__schema{types{name}}}"}` — should be disabled in prod

## Output

`recon-<domain>-<date>.md`:

```
# Recon — <domain> — <date>
## Scope
## Subdomains (resolved / live)
## Tech stack
## Interesting endpoints
## Quick wins (Nuclei findings, exposed configs)
## Suggested deeper-tests for Phase 3
```

## Rate-limit etiquette

- subfinder: passive — no rate concern
- dnsx: `-rl 100` default fine
- httpx: `-rl 50` for production targets
- nuclei: `-rate-limit 50 -bulk-size 25` for production
- gospider: `-c 5` for production (default 10 too aggressive)

## Tooling

| Tool | Purpose | Install |
|---|---|---|
| subfinder | Subdomain enum | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| dnsx | DNS resolution | `go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest` |
| httpx | HTTP probing | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` |
| nuclei | Template scanner | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
| gospider | Web crawler | `go install github.com/jaeles-project/gospider@latest` |
