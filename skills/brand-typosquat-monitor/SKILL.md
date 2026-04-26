---
name: brand-typosquat-monitor
description: Detect look-alike domains (typo-squatting, IDN homograph, bit-squatting) targeting a merch brand. Uses dnstwist, EvilURL. Defensive monitoring — passive only.
---

# Brand Typosquat Monitor

Phase 6 of merch-pentest. **Defensive** — purely passive enumeration of domains attackers might use to phish your customers.

## ⚠️ Authorization

This skill only **enumerates** registered look-alike domains via public DNS / WHOIS — no active probing of the look-alike sites themselves. If a candidate is found and you want to verify it's malicious, **do not interact** with the site beyond fetching the homepage. Submit suspected phishing URLs to:
- Google Safe Browsing
- PhishTank
- Brand-protection vendor (if customer has one)

## Threat model for merch

Look-alike domains are used for:
1. Phishing customers (fake login → credential theft → ATO → fraud)
2. Phishing staff (admin login)
3. Order interception (fake order-confirmation emails)
4. Fake product listings drive ad-spend before customer realizes
5. Trademark dilution

## Pipeline

### 1. dnstwist — broad permutation engine
```bash
dnstwist --registered --tld dnstwist-tlds.txt --format json brand.com > typo-candidates.json
```

Permutation classes generated:
- Bitsquatting (bit-flip): `bra*d.com`
- Homoglyph: `bránd.com`, `brаnd.com` (Cyrillic 'а')
- Hyphenation: `b-rand.com`
- Insertion / omission / repetition / replacement
- Transposition: `brnad.com`
- TLD swap: `brand.shop`, `brand.store`, `brand.co`, `brand.online`

`--registered` flag filters to **only domains that actually exist**.

### 2. IDN homograph — EvilURL
```bash
python3 ~/tools/EvilURL/evilurl.py
# enter brand.com → outputs Unicode-confusable variants with their punycode
```
Output: `xn--brnd-jua.com` style domains — already-registered ones are concerning.

### 3. Enrichment

For each candidate from steps 1-2:
- WHOIS: registration date (recent = higher risk), registrar, registrant country
- DNS: A / MX / NS records — MX present = phishing-ready
- TLS cert: valid LE cert + brand string in subject = setup for phishing
- HTTP HEAD: is there a live site?
- Wayback: any historical content?

```bash
for d in $(jq -r '.[].domain' typo-candidates.json); do
  echo "=== $d ==="
  whois "$d" 2>/dev/null | grep -iE "creation|registrar|country" | head -3
  dig +short "$d" A
  dig +short "$d" MX
done > typo-enriched.txt
```

### 4. Risk scoring

| Signal | Score |
|---|---|
| Registered < 90 days ago | +3 |
| Has MX records | +2 |
| Valid TLS cert | +2 |
| Live HTTP site | +3 |
| Live HTTP site with brand assets | +5 |
| WHOIS-privacy / shell registrant | +1 |
| Registrar known for abuse | +1 |

Score ≥ 5 = priority for takedown / monitoring.

### 5. Customer's own DNS hygiene (defensive)
While at it, check:
- DMARC record present and `p=reject` (not `p=none`)
- SPF record (`v=spf1 ... -all`)
- DKIM keys current, ≥ 2048-bit
- BIMI record (logo enforcement)
- DNSSEC enabled

```bash
dig +short TXT _dmarc.brand.com
dig +short TXT brand.com | grep spf
dig +short TXT default._domainkey.brand.com
```

## Output

`typosquat-<brand>-<date>.csv`:

```
domain,permutation_type,registered,registrar,country,a_record,mx_present,tls_cert,live_site,risk_score,recommended_action
brаnd.com,homoglyph,2025-03-14,Namecheap,PA,1.2.3.4,yes,LE,yes,9,UDRP filing
br-and.com,hyphenation,2024-11-02,GoDaddy,US,parked,no,none,parked,1,monitor
xn--brnd-jua.com,IDN,2025-04-01,REGRU,RU,5.6.7.8,yes,LE,yes,11,immediate takedown request
```

Plus DMARC/SPF/DKIM gap report.

## Recommended actions per risk band

- **Score 0-2**: Add to watch-list, re-scan monthly
- **Score 3-5**: Re-scan weekly, prepare UDRP material
- **Score 6+**: Immediate UDRP / brand-protection-vendor takedown, Safe Browsing report, customer-facing warning if site is live

## Tooling

| Tool | Purpose | Install |
|---|---|---|
| dnstwist | Permutation generator + enrichment | `apt install dnstwist` or `pip3 install dnstwist` |
| EvilURL | IDN homograph generator | `git clone https://github.com/UndeadSec/EvilURL ~/tools/EvilURL` |
| dig / whois | Standard | `apt install dnsutils whois` |
