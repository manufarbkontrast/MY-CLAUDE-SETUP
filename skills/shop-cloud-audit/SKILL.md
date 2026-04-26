---
name: shop-cloud-audit
description: Cloud misconfiguration audit for self-hosted webshops on AWS/GCP/Azure plus container/K8s scanning. Uses Prowler, ScoutSuite, Trivy. Authorized engagements only — requires read-only IAM credentials.
---

# Shop Cloud Audit

Phase 4 of merch-pentest. Only applies to **self-hosted** shops — skip for fully Shopify-managed.

## ⚠️ Authorization

Requires:
- Read-only IAM credentials provisioned by the customer (AWS: `SecurityAudit` + `ViewOnlyAccess` policy; GCP: `roles/iam.securityReviewer`; Azure: `Reader` + `Security Reader`)
- Written approval to enumerate buckets/keys
- Customer awareness — Prowler/ScoutSuite generate noise in CloudTrail; coordinate

Never use offensive tools (`pacu`, `cloudgoat`) without explicit pentest scope.

## Common merch cloud surface

| Asset | Common risk |
|---|---|
| S3 buckets (product images, invoices, exports) | Public-readable, missing encryption, no versioning |
| RDS / Aurora (orders, customers) | Public endpoint, no encryption-at-rest, weak SG rules |
| ElastiCache / Redis (session, cart) | Open to 0.0.0.0/0, no AUTH |
| CloudFront / CDN | Origin headers missing, signed-URL bypass |
| Lambda (webhooks, BFF) | Over-privileged role, env-var secrets |
| Secrets Manager / Parameter Store | Plaintext secrets, no rotation |
| IAM | `*:*` policies, unused access keys, root key usage |
| EKS / ECS | Privileged containers, no network policy |

## Pipeline

### 1. AWS — Prowler
```bash
prowler aws --profile <readonly-profile> \
  --output-formats html json \
  --output-directory ./prowler-out \
  --severity critical high medium
```
Custom merch-relevant checks (`-c`):
- `s3_bucket_public_access`
- `s3_bucket_default_encryption`
- `rds_instance_public_access`
- `iam_root_hardware_mfa_enabled`
- `secretsmanager_automatic_rotation_enabled`

### 2. AWS/GCP/Azure — ScoutSuite
```bash
scout aws --profile <readonly-profile> --report-dir ./scout-aws/
scout gcp --user-account --report-dir ./scout-gcp/
scout azure --cli --report-dir ./scout-azure/
```
HTML report with finding counts per service.

### 3. Container / K8s — Trivy

Image scan:
```bash
trivy image --severity HIGH,CRITICAL \
  --format json --output trivy-image.json \
  <ecr-registry>/<merch-app>:<tag>
```

Filesystem (CI integration):
```bash
trivy fs --security-checks vuln,config,secret ./repo-checkout
```

K8s cluster:
```bash
trivy k8s --report summary cluster
```

Look for:
- Outdated base images (Node 14, Python 3.7 etc.)
- Hardcoded secrets in image layers (`AWS_SECRET_ACCESS_KEY=...`)
- Vulnerable dependencies (`log4j`, `prototype-pollution` libs)
- Insecure K8s configs (privileged: true, hostNetwork, no resource limits)

### 4. IaC — Trivy / Checkov on Terraform
If customer provides Terraform:
```bash
trivy config --severity HIGH,CRITICAL ./terraform/
```

### 5. Merch-specific deep-dives

- **S3 bucket per-environment naming**: `<brand>-prod-orders`, `<brand>-prod-invoices` — check ACL, bucket policy, MFA delete
- **Sentry / Datadog / Logtail**: are stack traces with PII forwarded? GDPR risk
- **Stripe webhooks**: Lambda endpoint signature verification (HMAC), secret in env vs Secrets Manager
- **Backup buckets**: daily DB dumps — public? encrypted? KMS-CMK or AWS-managed?

## Output

`cloud-audit-<engagement>-<date>.md`:

```
# Cloud Audit — <date>
## Inventory (account IDs, regions, services)
## Critical findings (S3 public, IAM root, etc.)
## High findings
## Medium / Low
## Compliance gap (if PCI-DSS / GDPR scope)
## Remediation roadmap
## Appendix: Prowler/ScoutSuite/Trivy raw outputs
```

## Tooling

| Tool | Purpose | Install |
|---|---|---|
| prowler | AWS/GCP/Azure security audit | `pip3 install prowler` |
| ScoutSuite | Multi-cloud audit | `pip3 install scoutsuite` |
| Trivy | Container/IaC/K8s | `apt install trivy` or `curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \| sh` |
