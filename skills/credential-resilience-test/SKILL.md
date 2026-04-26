---
name: credential-resilience-test
description: Assess password-policy strength, leaked-credential exposure, and hash-cracking resistance for a merch shop's user base (admin, staff, customers). Uses Hashcat, John the Ripper, Cupp, HaveIBeenPwned. Authorized engagements only — requires hash dump provided by customer.
---

# Credential Resilience Test

Phase 5 of merch-pentest. Tests how well the user base would survive a hash leak.

## ⚠️ Authorization

This phase requires **the customer to provide a hash dump** of their own database (or anonymized sample). Never extract hashes via SQLi, even if Phase 3 found a SQLi — that's exploitation, not testing.

Customer should provide:
- Hash sample (admin tier + staff tier + customer tier — anonymized usernames if desired)
- Hashing algorithm + parameters (bcrypt cost, argon2 m/t/p)
- Password policy in force (length, complexity, rotation)

## Per-tier risk model

| Tier | Acceptable crack-rate | Why |
|---|---|---|
| Admin | < 1% within 24h on RTX-4090-class | Total store compromise |
| Staff | < 5% within 7 days | Order / refund manipulation |
| Customer | < 25% within 30 days | Account takeover, payment fraud |

## Pipeline

### 1. Hash identification
```bash
haiti '<sample-hash>'
```
Confirm algorithm matches what the customer claims. Mismatch = misconfig finding by itself.

### 2. Build wordlists

**Generic**: `rockyou.txt`, `SecLists/Passwords/Common-Credentials/`
**Targeted (Cupp)** — based on brand, founders, products:
```bash
python3 ~/tools/cupp/cupp.py -i
# fill in: brand name, founder names, important dates, slogans
# generates BRANDcandidates.txt
```

### 3. Hash crack with Hashcat
```bash
# bcrypt — slow, narrow wordlist
hashcat -m 3200 hashes.txt rockyou.txt --status --status-timer 30

# argon2 — slowest, very narrow wordlist
hashcat -m 32100 hashes.txt brand-targeted.txt

# scrypt
hashcat -m 8900 hashes.txt rockyou.txt

# pbkdf2-sha256
hashcat -m 10900 hashes.txt rockyou.txt
```

Time-box per tier:
- Admin: 24h budget
- Staff: 7d budget
- Customer: 30d budget (or stop at 25% cracked)

### 4. John the Ripper (alternative / specific formats)
```bash
john --format=bcrypt --wordlist=rockyou.txt hashes.txt
john --show --format=bcrypt hashes.txt
```

### 5. Leaked-password check
For each cracked password, check public breaches:
```bash
# HIBP API — k-anonymity prefix lookup, doesn't expose plaintext
PW="<cracked>"
HASH=$(echo -n "$PW" | sha1sum | awk '{print toupper($1)}')
PREFIX=${HASH:0:5}
SUFFIX=${HASH:5}
curl -s "https://api.pwnedpasswords.com/range/$PREFIX" | grep -i "$SUFFIX"
```
Returned count = number of times this PW appeared in known breaches.

### 6. Policy stress-tests

Even uncracked, evaluate the policy:
- Min length ≥ 12 (NIST SP 800-63B current)
- No composition rules (per NIST — counterproductive)
- Breach-list rejection on signup (top 10k common PWs)
- Argon2id or bcrypt cost ≥ 12
- Rotation enforced only on compromise — not periodic
- MFA mandatory for admin/staff

## Output

`credential-report-<engagement>-<date>.md`:

```
# Credential Resilience — <date>
## Sample size & tiers
## Algorithm assessment (✓ / ✗)
## Crack rates per tier
   - Admin: X / N cracked in T hours
   - Staff: X / N cracked in T days
   - Customer: X / N cracked in T days
## Top 10 cracked passwords (sanitized — patterns only, not plaintext)
## HIBP breach exposure (% appearing in public breaches)
## Policy gaps vs NIST 800-63B
## Recommendations
   - Algorithm migration if needed
   - Cost-factor bump
   - Breach-list signup gate
   - MFA enforcement
```

**Never include plaintext cracked passwords in the report.** Show patterns (`brandname2024`, `Companyname!`) but not actual customer secrets.

## Tooling

| Tool | Purpose | Install |
|---|---|---|
| hashcat | GPU hash cracker | `apt install hashcat` |
| john | CPU hash cracker | `apt install john` |
| haiti | Hash type identifier | `gem install haiti-hash` |
| cupp | Targeted wordlist gen | `git clone https://github.com/Mebus/cupp ~/tools/cupp` |
| SecLists | Wordlist collection | `git clone https://github.com/danielmiessler/SecLists ~/tools/SecLists` |

GPU recommended (Hashcat without GPU is 100-1000x slower).
