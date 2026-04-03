# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.1.x   | ✅ |
| 1.0.x   | ✅ |
| < 1.0   | ❌ |

## Reporting a Vulnerability

PAT is public infrastructure. Responsible disclosure is critical to keeping the ecosystem safe.

**Do NOT open a public GitHub issue for security vulnerabilities.**

To report a vulnerability, please email:

**security@brewtaniusai.com**

Include the following in your report:

- A clear description of the vulnerability
- Steps to reproduce the issue
- The affected version(s)
- Any potential impact or proof-of-concept (if safe to share)

## Response Timeline

| Action | Target |
| ------ | ------ |
| Initial acknowledgement | Within 48 hours |
| Triage and severity assessment | Within 5 business days |
| Patch or mitigation | Within 30 days for critical issues |
| Public disclosure | Coordinated with reporter |

## Scope

This policy covers the PAT repository, including:

- `src/` — all Python modules (CLI, pipeline, policy, audit, validation, chat)
- `configs/` — language profiles
- `schemas/` — JSON output schemas
- `.github/workflows/` — CI and release automation

Out of scope:

- Third-party dependencies (report those to their respective maintainers)
- Issues in forked copies of this repository

## Coordinated Disclosure

We follow a coordinated disclosure model. After a fix is released, we will publish an advisory crediting the reporter (unless they prefer anonymity). We ask reporters to allow us at least 30 days before public disclosure.

## Thank You

Security researchers who responsibly disclose vulnerabilities will be credited in the release notes and our Hall of Thanks (coming soon). PAT is sovereign public infrastructure — keeping it safe is a community responsibility.
