---
name: subdomain-takeover-audit
description: Audit DNS records for orphan CNAMEs that could be claimed (subdomain takeover). Critical for merch shops with marketing campaign subdomains pointing to dead Heroku/S3/Shopify/Webflow. Authorized engagements only.
---

# Subdomain Takeover Audit

Detects DNS records pointing to providers that no longer host the underlying resource — claimable by an attacker → impersonation, cookie theft, brand damage.

## ⚠️ Authorization

Only run against zones you own or are explicitly authorized to test. Even passive DNS lookups against unowned zones may breach engagement scope.

## Why merch shops are at risk

Common pattern: marketing team spins up `summer-sale.brand.com` → `brand-summer.myshopify.com` for a campaign, takes the Shopify shop down 6 months later, forgets to remove the DNS CNAME. An attacker claims `brand-summer` on Shopify and now serves arbitrary content under the brand domain.

High-risk providers for merch:
- Shopify (`*.myshopify.com`)
- Heroku (`*.herokuapp.com`)
- AWS S3 (`*.s3.amazonaws.com`, region variants)
- AWS CloudFront (`*.cloudfront.net`)
- GitHub Pages (`*.github.io`)
- Webflow, Vercel, Netlify, Squarespace
- Mailchimp landing pages

## Pipeline

### 1. Collect all subdomains (from merch-recon Phase 1)
```bash
cat subs-resolved.txt | sort -u > all-subs.txt
```

### 2. Extract CNAME chains
```bash
dnsx -l all-subs.txt -cname -resp-only -silent -o cnames.txt
paste -d, all-subs.txt cnames.txt > sub-cname-pairs.csv
```

### 3. Match against vulnerable provider patterns
```bash
grep -iE "(myshopify\.com|herokuapp\.com|s3.*\.amazonaws\.com|cloudfront\.net|github\.io|webflow\.io|vercel-dns|netlify\.app|squarespace\.com|mailchimp)" sub-cname-pairs.csv > suspect.csv
```

### 4. Verify takeover-ability (passive)
For each suspect, check:
- HTTP response: 404 with provider's "no such app/site" page = takeover candidate
- DNS resolution: NXDOMAIN on the CNAME target = takeover candidate
- TLS cert: cert mismatch / no cert = often takeover candidate

```bash
httpx -l suspect-targets.txt -status-code -title -tls-probe -silent
```

Look for these markers:
- Shopify: "Sorry, this shop is currently unavailable"
- Heroku: "There's nothing here, yet"
- GitHub Pages: "There isn't a GitHub Pages site here"
- S3: "NoSuchBucket"
- AWS CloudFront: "Bad request. ERROR: The request could not be satisfied."

### 5. Do NOT claim

This is an **audit**, not an exploit. Document the candidate; do not register/claim the resource even to "prove" the issue, unless the engagement letter explicitly authorizes proof-of-claim AND you can immediately hand the resource back.

## Output

`subdomain-takeover-<domain>-<date>.csv`:

```
subdomain,cname_target,provider,status_code,title_snippet,severity,recommended_fix
shop-summer.brand.com,brand-summer.myshopify.com,Shopify,404,"Sorry...unavailable",Critical,Remove CNAME or re-claim shop
files.brand.com,brand-files.s3.amazonaws.com,AWS S3,404,"NoSuchBucket",Critical,Remove CNAME or re-create bucket
```

## Tooling

| Tool | Purpose | Install |
|---|---|---|
| dnsx | DNS / CNAME extraction | `go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest` |
| httpx | HTTP fingerprint | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` |
| nuclei (optional) | `nuclei -tags takeover -l all-subs.txt` template-based detection | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
