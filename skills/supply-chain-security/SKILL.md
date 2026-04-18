---
name: supply-chain-security
description: "Software supply-chain security: SBOM generation (Syft, CycloneDX, SPDX), signed artifacts (Sigstore/cosign), SLSA levels, SPIFFE/SPIRE workload identity, in-toto attestations, dependency confusion mitigation, trusted publishing. Triggers on SBOM, Sigstore, cosign, SLSA, SPIFFE, SPIRE, in-toto, supply chain, software bill of materials."
category: security
tags: [sbom, sigstore, cosign, slsa, spiffe, supply-chain, security]
---

# Software Supply-Chain Security

## Core problem
Attackers compromise not your code but your dependencies, build system, or distribution channel (Log4Shell, SolarWinds, xz-utils, npm event-stream, pypi malicious packages). Supply-chain security adds verifiable attestations at every stage.

## SBOM (Software Bill of Materials)

Machine-readable inventory of components, versions, licenses, hashes.

### Formats
- **CycloneDX** (OWASP) — JSON/XML; richer for security
- **SPDX** (Linux Foundation) — JSON/YAML/tag-value; richer for licensing

### Generate
```bash
# Syft — covers containers, binaries, source dirs, archives
syft dir:. -o cyclonedx-json > sbom.cdx.json
syft packages alpine:3.19 -o spdx-json > alpine.spdx.json

# CycloneDX Python
cyclonedx-py -p poetry.lock -o sbom.json

# npm
npm sbom --sbom-format cyclonedx
```

### Attach to artifacts
```bash
cosign attach sbom --sbom sbom.cdx.json myregistry/image:v1
```

## Sigstore / cosign

Free code-signing without managing keys — uses short-lived certs from OIDC identity (GitHub Actions, Google, Microsoft).

```bash
# Install
brew install cosign

# Keyless sign (CI/CD friendly)
cosign sign --yes myregistry/image:v1

# Verify
cosign verify --certificate-identity-regexp '.*@example.com$' \
  --certificate-oidc-issuer https://accounts.google.com \
  myregistry/image:v1

# Sign blobs (binaries, SBOMs)
cosign sign-blob --yes binary.tar.gz > binary.sig
cosign verify-blob --signature binary.sig --certificate cert.pem binary.tar.gz
```

Transparency log: Rekor (rekor.sigstore.dev) — all signatures publicly auditable.

## SLSA (Supply-chain Levels for Software Artifacts)

Maturity framework (1-4):

| Level | Requirements |
|-------|--------------|
| 1 | Build process documented |
| 2 | Hosted build service, signed provenance |
| 3 | Hardened build platform, non-falsifiable provenance |
| 4 | Two-person reviewed, hermetic, reproducible |

GitHub Actions → SLSA 3 via `slsa-github-generator`:
```yaml
- uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v2.0.0
```

## In-toto attestations

Signed statements about how software was built:
- **Build provenance**: what commit, what runner, what inputs
- **Test results**: which tests ran, pass/fail
- **Vulnerability scan**: CVEs at build time
- **Policy**: what gates approved the release

Stored as Sigstore-signed JSON. Verified by consumers before deploy.

## SPIFFE / SPIRE

Workload identity standard. Each service gets a short-lived SVID (SPIFFE Verifiable Identity Document) → X.509 cert or JWT. Replaces long-lived API keys / shared secrets.

```
spiffe://example.com/ns/prod/sa/billing-service
```

SPIRE = reference implementation. Integrates with Envoy, Istio, Kubernetes, AWS.

## Dependency confusion mitigation

Internal package names accidentally published to public registries get pulled by default. Defenses:
- Scoped packages (`@company/pkg`) on npm
- Private registry mirror (Verdaccio, JFrog, Artifactory, Nexus) with upstream allowlist
- Package signing (PEP 740, npm provenance) and verification at install
- Dependabot / Renovate for known-good version pins
- `.pypirc` / `.npmrc` pinning registry

## Trusted Publishing (OIDC-based)

PyPI, npm, GitHub Releases: skip long-lived tokens by using OIDC tokens from CI:

```yaml
# .github/workflows/publish.yml
permissions:
  id-token: write       # OIDC
- uses: pypa/gh-action-pypi-publish@release/v1
  # No TOKEN secret needed — uses OIDC exchange
```

## Vulnerability scanning

- **Trivy**: containers, IaC, SBOM, secrets
- **Grype**: SBOM → CVE
- **OSV-Scanner**: Google's OSV DB, Go / npm / PyPI / Maven / ...
- **Snyk, Dependabot, Renovate**: continuous updates
- **Semgrep**: code-level SAST

```bash
trivy image myregistry/image:v1
grype sbom:sbom.cdx.json
osv-scanner --lockfile=poetry.lock
```

## Minimum viable supply-chain hygiene

Checklist:
- [ ] SBOM generated + attached per release
- [ ] Images + binaries signed with cosign (keyless OIDC)
- [ ] SLSA 2+ build provenance
- [ ] Vulnerability scan in CI (Trivy / OSV-Scanner) — block on critical CVEs
- [ ] Renovate/Dependabot for dependency updates
- [ ] Branch protection + signed commits (Sigstore gitsign)
- [ ] No long-lived tokens in CI (use OIDC Trusted Publishing / federated identity)
- [ ] Private registry mirror with upstream allowlist
- [ ] SPIFFE / mTLS for service-to-service (no shared secrets)

## References
- slsa.dev
- sigstore.dev
- in-toto.io
- spiffe.io
- anchore.com/syft (Syft)
- aquasecurity.com/trivy
