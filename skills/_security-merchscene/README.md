# _security-merchscene

Kuratiertes Security-Skill-Set für das **merchscene**-Projekt
(Shopify-Commerce + Supabase-Backend/Auth + Adobe-Firefly-KI-Bildgenerierung + Klaviyo).

Fokus: **High-Traffic-Frontend absichern, bis der Kunde zum Bezahlen an Shopify übergeben wird.**
Bis zum Checkout-Handoff trägt merchscene die Last und die Angriffsfläche — danach
übernimmt Shopify (PCI-Scope, Kartendaten). Diese Auswahl deckt genau diese Strecke ab.

## Herkunft & Lizenz

Ausgewählt aus [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)
(Community-Projekt, **nicht** von Anthropic). Lizenz: **Apache-2.0** — Kopieren mit
Attribution erlaubt. Original-`LICENSE` liegt in jedem Skill-Ordner.

44 von 754 Skills übernommen. Die übrigen ~710 (Malware-Reversing, Memory-Forensik,
OT/ICS, Threat Hunting, Red-Team-Exploits etc.) sind für eine Commerce-Web-App ohne
Nutzen und wurden bewusst weggelassen, damit der `prompt-optimizer` schlank bleibt.

## Auswahl nach Angriffsfläche

### A — Traffic / Verfügbarkeit / DDoS / Bot-Ansturm (Priorität)
Die kritische Strecke bei Lastspitzen (Drops, Kampagnen, Scalper-Bots).
- `implementing-ddos-mitigation-with-cloudflare`
- `implementing-cloud-waf-rules`
- `securing-api-gateway-with-aws-waf`
- `implementing-api-rate-limiting-and-throttling`
- `implementing-api-abuse-detection-with-rate-limiting`
- `implementing-network-traffic-baselining`
- `implementing-cloud-workload-protection`
- `detecting-sql-injection-via-waf-logs`

### A2 — Eigene Abwehr unter Last testen (offensive Selbsttests)
Nur gegen **dein eigenes** Staging einsetzen — Lastfestigkeit der Defenses verifizieren.
- `performing-api-rate-limiting-bypass`
- `performing-bandwidth-throttling-attack-simulation`
- `performing-web-application-firewall-bypass`
- `performing-web-cache-poisoning-attack`
- `performing-web-cache-deception-attack`

### B — API-Sicherheit (Supabase Edge Functions, Routen, Shopify-Webhooks/GraphQL)
- `implementing-api-key-security-controls`
- `implementing-api-schema-validation-security`
- `implementing-api-gateway-security-controls`
- `testing-api-authentication-weaknesses`
- `testing-api-security-with-owasp-top-10`
- `performing-graphql-security-assessment`
- `performing-graphql-introspection-attack` (Selbsttest)
- `exploiting-mass-assignment-in-rest-apis` (Selbsttest)

### C — Auth / IAM (Supabase Auth, JWT, OAuth, RLS)
- `testing-jwt-token-security`
- `testing-oauth2-implementation-flaws`
- `testing-for-broken-access-control`
- `exploiting-idor-vulnerabilities` (Selbsttest)
- `exploiting-jwt-algorithm-confusion-attack` (Selbsttest)
- `performing-jwt-none-algorithm-attack` (Selbsttest)

### D — Web-Frontend (XSS, CORS, Headers, CSP, Clickjacking)
- `performing-security-headers-audit`
- `testing-cors-misconfiguration`
- `testing-for-xss-vulnerabilities-with-burpsuite`
- `performing-content-security-policy-bypass` (Selbsttest)
- `performing-clickjacking-attack-test`
- `testing-for-open-redirect-vulnerabilities`
- `testing-for-host-header-injection`
- `exploiting-prototype-pollution-in-javascript` (Selbsttest)

### E — Datenexposition / Secrets
- `testing-for-sensitive-data-exposure`
- `implementing-secrets-scanning-in-ci-cd`
- `implementing-secrets-management-with-vault`
- `analyzing-cloud-storage-access-patterns` (Supabase Storage Buckets)

### F — KI-Bildgenerierung / LLM (Firefly + Prompt-Features)
- `implementing-llm-guardrails-for-security`
- `detecting-ai-model-prompt-injection-attacks`

### G — Checkout-Handoff / Compliance
- `implementing-pci-dss-compliance-controls` (Scope-Grenze zu Shopify sauber ziehen)

### H — Incident-Bereitschaft (für Lastevents / Drops)
- `building-incident-response-playbook`
- `building-incident-response-dashboard`

## Benutzung

Jeder Skill ist ein Ordner mit `SKILL.md` (Frontmatter + Workflow), oft `references/`
und `scripts/`. Claude Code lädt sie automatisch über die `description` im Frontmatter,
sobald ein Prompt thematisch passt.

**Aktivieren (auf neuem Rechner / nach Sync):**
```bash
cp -r skills/_security-merchscene ~/.claude/skills/
```

**Gezielt nutzen — Beispiele, die die richtigen Skills triggern:**
- „Härte die Supabase Edge Functions gegen Rate-Limit-Abuse und Bot-Traffic ab"
  → A + B greifen
- „Audit der Security-Header und CSP für das merchscene-Frontend"
  → `performing-security-headers-audit`, `performing-content-security-policy-bypass`
- „Lasttest: hält mein Cloudflare-Rate-Limit einem Drop-Ansturm stand?"
  → A2 (gegen Staging!)
- „Prüf, ob beim Checkout-Übergang an Shopify keine PII bei uns hängen bleibt"
  → `testing-for-sensitive-data-exposure`, `implementing-pci-dss-compliance-controls`

**Mit deinem prompt-optimizer:** nach dem Sync neu bauen, damit die Skills im Matching
auftauchen:
```bash
cd ~/my-claude-setup && po --build
```

## Wichtig: offensive Skills

Alle `performing-*` / `exploiting-*` Skills sind für **autorisiertes Testen der eigenen
Infrastruktur** (Staging/eigene Domains). Niemals gegen fremde Systeme.
