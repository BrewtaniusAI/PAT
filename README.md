# PAT — Pan-African Language Infrastructure

[![CI](https://github.com/BrewtaniusAI/PAT/actions/workflows/ci.yml/badge.svg)](https://github.com/BrewtaniusAI/PAT/actions/workflows/ci.yml)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17046595-blue)](https://doi.org/10.5281/zenodo.17046595)
[![License](https://img.shields.io/badge/license-Patent--Free-brightgreen)](#ethical-framing)

**A patent-free, reproducible language infrastructure framework designed to help African languages exist natively inside modern AI systems.**

> Part of the [CollectiveOS](https://github.com/BrewtaniusAI) ecosystem — governed by the QC → GATA → GATA PRIME pipeline.

---

## Overview

PAT is released as executable public knowledge. It is part of a broader patent-free science and open collaboration framework, functioning as:

- **Public infrastructure** for African language AI integration
- **Executable prior art** preventing patent lockout
- **Reproducible technical disclosure** with cryptographic proof bundles
- **Community stewardship foundation** with language steward roles

## Why PAT Exists

African languages should not be an afterthought in AI. PAT begins with a simple principle: language infrastructure should be open, reproducible, ethically framed, and usable by the communities it affects.

---

## Architecture

```
Input → Validation → Policy → Execution → Output → Receipt / Proof
```

No pipeline stage bypasses validation or policy checks. Every execution produces a cryptographic receipt for auditability.

### Core Pipeline

| Stage | Purpose |
|-------|---------|
| **Ingest** | Accept and normalize language input |
| **Validate** | Schema and profile-aware validation |
| **Hash** | SHA-256 integrity chain generation |
| **Policy** | Ethical and governance policy enforcement |
| **Receipt** | Cryptographic proof bundle export |

---

## Quickstart

```bash
# Install
python -m pip install -e .

# Verify
pat version

# Run with a language profile
pat run "Ẹ káàárọ̀ Africa" --profile yo
```

### Build Datasets

```bash
pat build-dataset input.json output.json
pat build-dataset-batch input_dir output_dir
```

### Generate Integrity Artifacts

```bash
pat receipt output.json
pat proof output.json
pat validate-output output.json
pat release-check --repo-root .
```

### Run Tests

```bash
pytest -q
```

---

## What This Release Includes

- Governed execution pipeline with 5-stage audit flow
- Validation and policy enforcement engine
- Language profiles for **Yorùbá**, **Kiswahili**, and **isiZulu**
- Profile-aware tokenization path
- Dataset builder and batch dataset builder
- Receipts and proof bundle export
- Schema validation and release integrity checks
- Contribution files and language steward guidance
- AI-integrated Liquid Glass dashboard (`dashboard/index.html`)

---

## Dashboard

PAT includes an AI-integrated **Liquid Glass** dashboard providing a visual interface for:

- Pipeline monitoring (5-stage INGEST → VALIDATE → HASH → POLICY → RECEIPT flow)
- Audit trail inspection
- Policy engine status
- Batch builder management
- AI Auditor chat with provenance chain analysis
- Command palette (`Ctrl+K`) with fuzzy search

Open `dashboard/index.html` in any browser to launch.

---

## Repository Structure

```
PAT/
├── src/                          # Runtime, validation, policy, audit, builder, CLI
│   └── pat/
│       ├── cli.py                # CLI entrypoint
│       ├── runtime.py            # Core execution engine
│       ├── validation.py         # Schema validation
│       └── policy.py             # Policy enforcement
├── configs/language_profiles/    # Seed language profiles (yo, sw, zu)
├── datasets/                     # Sample corpora and annotation materials
├── schemas/                      # Output and dataset JSON schemas
├── dashboard/                    # Liquid Glass AI dashboard
│   └── index.html
├── docs/                         # Governance, reproducibility, release docs
├── .github/workflows/            # CI/CD pipeline
├── feature_flags.yml             # Feature lifecycle management
├── provenance.json               # Data origin tracking
├── release_manifest.json         # Release integrity manifest
└── CITATION.cff                  # Citation metadata
```

---

## Ethical Framing

PAT must **not** be used for:

- Impersonation
- Political manipulation
- Deceptive synthetic communication
- Exploitative extraction of culturally sensitive material

See `docs/ETHICAL_USE.md` for the full ethical framework.

---

## CollectiveOS Integration

PAT operates within the CollectiveOS governance framework:

- **QC Gate** — Self-audit before significant actions
- **GATA** — Sandboxed testing and edge-case validation
- **GATA PRIME** — Formal verification and audit trail maintenance
- **Proof Vault** — WORM (Write Once Read Many) receipt logging
- **ELFE Kernel** — Fixed-time convergence stability guarantees

---

## Citation & Archival

- `CITATION.cff` — Machine-readable citation metadata
- `release_manifest.json` — SHA-256 integrity tracking
- `provenance.json` — Data origin and transformation history
- Zenodo DOI: [10.5281/zenodo.17046595](https://doi.org/10.5281/zenodo.17046595)

---

## Status

**PAT v0.9.0** — Public-alpha release candidate.
Intentionally small, reproducible, and extensible.

13 tests passing. CI green.

---

## License

Patent-free. See repository license files for details.
