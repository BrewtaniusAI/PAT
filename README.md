Here's the upgraded PAT README — copy and paste the full content:

```markdown
<p align="center">
  <strong>P · A · T</strong><br>
  <em>Pan-African Language Infrastructure for AI</em>
</p>

<p align="center">
  <a href="https://github.com/BrewtaniusAI/PAT/actions/workflows/ci.yml"><img src="https://github.com/BrewtaniusAI/PAT/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://doi.org/10.5281/zenodo.17046595"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17046595-blue" alt="DOI"></a>
  <a href="#license"><img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="License"></a>
  <a href="#ethical-framing"><img src="https://img.shields.io/badge/patent--free-public%20infrastructure-brightgreen" alt="Patent-Free"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/tests-13%20passing-brightgreen" alt="Tests">
  <img src="https://img.shields.io/badge/version-1.0.0-informational" alt="Version">
</p>

---

**PAT** is a patent-free, reproducible language infrastructure framework that enables African languages to exist natively inside modern AI systems. Released as **executable prior art**, PAT provides governed pipelines for language data ingestion, profile-aware tokenization, dialect detection, policy enforcement, and cryptographic proof generation — preventing patent lockout on foundational language technology.

> Part of the [CollectiveOS](https://github.com/BrewtaniusAI) ecosystem — governed by the **QC → GATA → GATA PRIME** pipeline.

---

## Table of Contents

- [Why PAT Exists](#why-pat-exists)
- [Architecture](#architecture)
- [Quickstart](#quickstart)
- [AI Chat](#ai-chat)
- [CLI Reference](#cli-reference)
- [Language Profiles](#language-profiles)
- [Pipeline Deep Dive](#pipeline-deep-dive)
- [Audit & Integrity](#audit--integrity)
- [Repository Structure](#repository-structure)
- [Testing](#testing)
- [Documentation](#documentation)
- [Dashboard](#dashboard)
- [Ethical Framing](#ethical-framing)
- [CollectiveOS Integration](#collectiveos-integration)
- [Contributing](#contributing)
- [Citation & Archival](#citation--archival)
- [License](#license)

---

## Why PAT Exists

African languages should not be an afterthought in AI. The infrastructure that powers language processing — tokenization, normalization, dialect detection, policy gates — is foundational. If that infrastructure is locked behind patents, the communities it affects lose control of their own linguistic tools.

PAT begins with a simple principle: **language infrastructure should be open, reproducible, ethically framed, and usable by the communities it serves.**

Every component is released as executable public knowledge — a technical disclosure with cryptographic proof bundles — so that no entity can claim exclusive ownership over these language processing methods.

---

## Architecture

```
┌─────────┐    ┌──────────┐    ┌────────┐    ┌──────────┐    ┌─────────┐    ┌─────────────┐
│  INPUT  │───▶│ VALIDATE │───▶│  HASH  │───▶│  POLICY  │───▶│ EXECUTE │───▶│ RECEIPT/    │
│         │    │          │    │        │    │          │    │         │    │ PROOF       │
└─────────┘    └──────────┘    └────────┘    └──────────┘    └─────────┘    └─────────────┘
     │              │               │              │              │               │
     ▼              ▼               ▼              ▼              ▼               ▼
  Raw text     Length &        SHA-256         Forbidden      Profile-aware    Cryptographic
  + profile    type checks    integrity       pattern scan   tokenization,    receipt +
  code                        chain                          dialect detect,  proof bundle
                                                             phoneme map      for archival
```

No pipeline stage bypasses validation or policy checks. Every execution produces a cryptographic receipt for full auditability.

### Pipeline Stages

| Stage | Module | Purpose |
|-------|--------|---------|
| **Ingest** | `pat_cli` | Accept raw text input with optional language profile code |
| **Validate** | `pat_validation` | Enforce input constraints (type, length bounds, emptiness) |
| **Hash** | `pat_audit` | Generate SHA-256 integrity chains for all artifacts |
| **Policy** | `pat_policy` | Scan for forbidden patterns (impersonation, political manipulation) |
| **Execute** | `pat_pipeline` | Run profile-aware tokenization, dialect detection, and phoneme mapping |
| **Receipt** | `pat_audit` | Export cryptographic receipts and proof bundles for archival |

---

## Quickstart

### Prerequisites

- Python 3.10 or higher
- pip

### Install

```bash
git clone https://github.com/BrewtaniusAI/PAT.git
cd PAT
python -m pip install -e .
```

### Verify Installation

```bash
pat version
# Output: 1.0.0
```

### Run the Pipeline

```bash
# Process Yorùbá text with language profile
pat run "Ẹ káàárọ̀ Africa" --profile yo

# Process without a specific profile
pat run "Hello World"

# Process with JSONL audit logging
pat run "Habari Afrika" --profile sw --log audit.jsonl
```

### Example Output

```json
{
  "schema_version": "0.1",
  "input": "Ẹ káàárọ Africa",
  "status": "processed",
  "tokens": ["ẹ", "káàárọ", "africa"],
  "phonemes": ["ẹ", "káàárọ", "africa"],
  "dialect": {
    "label": "yo",
    "confidence": 0.6,
    "matches": ["ẹ", "ọ"]
  },
  "policy": {
    "passed": true,
    "flags": []
  },
  "profile_code": "yo"
}
```

---

## AI Chat

PAT includes an AI chat module that works with all 71 African languages. It auto-detects the user's language and responds accordingly.

```bash
# Interactive terminal chat (auto-detects language)
pat chat

# Chat in a specific language
pat chat --profile yo

# Use a specific LLM backend
pat chat --backend ollama      # local/offline default
pat chat --backend openai      # requires OPENAI_API_KEY
pat chat --backend anthropic   # requires ANTHROPIC_API_KEY

# Launch web chat UI
pat chat-web
pat chat-web --port 3000
```

**Features:**
- Pluggable LLM backends: Ollama (local/offline default), OpenAI, Anthropic, Echo (testing)
- Auto language detection across all 71 profiles
- Language-aware system prompts for culturally appropriate responses
- Web chat UI with dark mode, language selector, and typing indicators
- CLI REPL with `/lang`, `/langs`, `/reset`, `/status` commands
- Zero external dependencies — all backends use stdlib `urllib` only

---

## CLI Reference

PAT provides a single `pat` CLI with the following subcommands:

| Command | Description | Example |
|---------|-------------|---------|
| `pat run <text>` | Run the full pipeline on input text | `pat run "Sawubona" --profile zu` |
| `pat chat` | Interactive AI chat (auto-detects language) | `pat chat --profile yo` |
| `pat chat-web` | Launch web-based chat UI | `pat chat-web --port 3000` |
| `pat build-dataset <in> <out>` | Build a structured dataset from JSON input | `pat build-dataset input.json output.json` |
| `pat build-dataset-batch <in_dir> <out_dir>` | Batch process all `.json` files in a directory | `pat build-dataset-batch corpus/ processed/` |
| `pat receipt <path>` | Generate a SHA-256 receipt for an artifact | `pat receipt output.json` |
| `pat proof <path>` | Export a full proof bundle for archival | `pat proof output.json` |
| `pat validate-output <path>` | Validate pipeline output against JSON schema | `pat validate-output output.json` |
| `pat release-check` | Check release readiness (required files, manifest) | `pat release-check --repo-root .` |
| `pat release-summary` | Generate a release summary report | `pat release-summary --repo-root .` |
| `pat version` | Print the current version | `pat version` |

### Options

- `--profile <code>` — Language profile code (`yo`, `sw`, `zu`, etc.) for profile-aware tokenization or chat
- `--backend <name>` — LLM backend for chat (`ollama`, `openai`, `anthropic`, `echo`)
- `--log <path>` — Append pipeline output to a JSONL audit log
- `--schema <path>` — Custom JSON schema path for output validation (default: `schemas/pipeline_output.schema.json`)
- `--repo-root <path>` — Repository root for release checks (default: `.`)

---

## Language Profiles

PAT ships with **71 language profiles** spanning all major African language families:

| Region | Languages |
|--------|-----------|
| **West Africa (18)** | Hausa, Igbo, Yorùbá, Akan, Twi, Ewe, Fulfulde, Wolof, Bambara, Fon, Kanuri, Mandinka, Soninke, Dagbani, Mooré, Dyula, Susu, Temne, Mende |
| **East Africa (12)** | Kiswahili, Amharic, Oromo, Tigrinya, Somali, Luganda, Kinyarwanda, Kirundi, Gĩkũyũ, Dholuo, Kamba, Ekegusii, Maa |
| **Southern Africa (16)** | isiZulu, isiXhosa, Sesotho, Setswana, siSwati, Tshivenda, Xitsonga, isiNdebele (SA & ZW), Sepedi, Afrikaans, Shona, Chichewa, Bemba, Tumbuka, Lozi |
| **Central Africa (6)** | Lingala, Kikongo, Kiluba, Tshiluba, Sango, Kiswahili cha Congo |
| **North Africa (5)** | Maghrebi Arabic, Kabyle, Tamazight, Standard Moroccan Tamazight, Tachelhit |
| **Nilo-Saharan (2)** | Dinka, Nuer |
| **Additional (12)** | Malagasy, Ga, Berber, Tamashek, Songhai, Tigre, Sidamo, Wolaytta, Geʽez, and more |

Each profile defines character preservation rules, keyword sets for dialect detection, and metadata for the tokenization pipeline.

Profiles are stored as JSON in `configs/language_profiles/` and loaded by ISO language code. Adding a new language is as simple as creating a new `.json` profile — see [Contributing](#contributing).

### Profile Structure

```json
{
  "code": "yo",
  "name": "Yorùbá",
  "preserve_characters": ["ẹ", "ọ", "ṣ", "á", "à", ...],
  "keywords": ["ẹ", "ọ", "ṣ", "ọba", "àwọn", "ilẹ"]
}
```

---

## Pipeline Deep Dive

### Tokenization

PAT uses Unicode NFC normalization before tokenization. The tokenizer handles diacritical marks, tone markers, and special characters natively — crucial for African languages where diacritics carry semantic meaning.

```python
from pat_core.tokenizer import tokenize

tokenize("Ẹ káàárọ̀ Africa")
# → ['ẹ', 'káàárọ', 'africa']
```

### Dialect Detection

When a language profile is provided, PAT scans input text against the profile's keyword set and returns a confidence-scored dialect classification:

```python
from pat_core.dialect import detect_dialect
from pat_core.language_profiles import load_profile

profile = load_profile("yo")
result = detect_dialect("Ẹ káàárọ̀ ọba ilẹ", profile)
# → DialectResult(label='yo', confidence=0.8, matches=['ẹ', 'ọ', 'ọba', 'ọba'])
```

### Policy Enforcement

All input passes through the policy engine before execution. PAT blocks text containing forbidden patterns and raises a `PermissionError` on violation:

```python
from pat_policy.policy import enforce_policy

enforce_policy("Hello world")       # → PolicyResult(passed=True, flags=[])
enforce_policy("impersonate admin") # → raises PermissionError
```

### Schema Validation

Pipeline output is validated against a JSON schema (`schemas/pipeline_output.schema.json`) ensuring all required fields (`schema_version`, `input`, `status`, `tokens`, `phonemes`, `dialect`, `policy`, `profile_code`) are present.

---

## Audit & Integrity

PAT treats auditability as a first-class concern. Every pipeline run can produce:

### Receipts

A receipt records the SHA-256 hash, timestamp, schema version, and source for any artifact:

```bash
pat receipt output.json
# Creates output.json.receipt.json
```

```json
{
  "file": "output.json",
  "sha256": "a3f2b8c...",
  "timestamp": "2026-04-02T12:00:00+00:00",
  "schema_version": "0.1",
  "source": "PAT pipeline"
}
```

### Proof Bundles

A proof bundle wraps the receipt with artifact metadata for Proof Vault or DOI-linked archival:

```bash
pat proof output.json
# Creates output.json.proof.json
```

### JSONL Audit Logging

Pipeline runs can stream output to append-only JSONL logs for continuous auditing:

```bash
pat run "Habari" --profile sw --log audit.jsonl
```

---

## Repository Structure

```
PAT/
├── src/
│   ├── pat_cli.py                        # CLI entrypoint — subcommand router
│   ├── pat_core/                         # Core language processing
│   │   ├── tokenizer.py                  #   Unicode NFC tokenization
│   │   ├── language_profiles.py          #   Profile loader (JSON → dict)
│   │   ├── dialect.py                    #   Keyword-based dialect detection
│   │   └── phoneme.py                    #   Phoneme mapping (stub for expansion)
│   ├── pat_pipeline/
│   │   └── pipeline.py                   # Full pipeline orchestration
│   ├── pat_policy/
│   │   └── policy.py                     # Forbidden-pattern policy engine
│   ├── pat_validation/
│   │   ├── validator.py                  # Input constraint validation
│   │   └── schema_check.py              # JSON schema output validation
│   ├── pat_audit/
│   │   ├── receipts.py                   # SHA-256 receipt generation
│   │   ├── proof_export.py               # Proof bundle export
│   │   └── jsonl_export.py               # Append-only JSONL logging
│   ├── pat_builder/
│   │   ├── builder.py                    # Single-file dataset builder
│   │   └── batch.py                      # Batch directory processing
│   ├── pat_release.py                    # Release readiness checker
│   ├── pat_release_pack.py               # Release summary generator
│   └── pat_version.py                    # Version reader (from VERSION file)
├── configs/
│   └── language_profiles/                # Language profile definitions
│       ├── yo.json                       #   Yorùbá
│       ├── sw.json                       #   Kiswahili
│       └── zu.json                       #   isiZulu
├── datasets/
│   └── sample_corpora/                   # Seed data for testing and demos
│       ├── sample.json
│       └── pat_seed_parallel_sample.json
├── schemas/
│   └── pipeline_output.schema.json       # JSON schema for pipeline output
├── docs/                                 # Full documentation suite
│   ├── INDEX.md                          #   Documentation index
│   ├── OVERVIEW.md                       #   Project overview
│   ├── ARCHITECTURE.md                   #   Pipeline architecture
│   ├── GOVERNANCE.md                     #   Governance framework
│   ├── ETHICAL_USE.md                    #   Ethical use policy
│   ├── REPRODUCIBILITY.md               #   Reproducibility guide
│   ├── CHANGELOG.md                     #   Version history
│   ├── COMMUNITY_LANGUAGE_CONTRIBUTION.md # Language steward guide
│   ├── ARCHIVAL_HASH_NOTES.md           #   Hash and archival notes
│   ├── SIGNED_PROVENANCE.md             #   Signed provenance docs
│   ├── PUBLICATION_CHECKLIST.md         #   Pre-publication checklist
│   ├── GITHUB_RELEASE_TEXT.md           #   GitHub release body
│   ├── GITHUB_RELEASE_DRAFT.md          #   Release draft template
│   ├── ZENODO_RELEASE_NOTES.md          #   Zenodo release notes
│   ├── ZENODO_PUBLICATION_TEXT.md       #   Zenodo publication text
│   ├── PUBLIC_RELEASE_MANIFEST.md       #   Release manifest docs
│   ├── REPOSITORY_METADATA.md           #   Repo metadata suggestions
│   ├── LANDING_PAGE.md                  #   Landing page draft
│   └── FIRST_PUBLIC_RELEASE_CHECKLIST.md # Final release checklist
├── tests/                                # Test suite (13 tests)
│   ├── test_pipeline.py
│   ├── test_policy.py
│   ├── test_profiles.py
│   ├── test_receipts.py
│   ├── test_proof_export.py
│   ├── test_provenance.py
│   ├── test_batch_builder.py
│   ├── test_schema_validation.py
│   ├── test_release_check.py
│   ├── test_release_summary.py
│   └── test_version.py
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                        # CI pipeline (Python 3.11, pytest)
│   │   └── release.yml                   # Automated release workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── language_profile_request.md
│   └── pull_request_template.md
├── pyproject.toml                        # Project metadata and build config
├── VERSION                               # Canonical version (1.0.0)
├── CITATION.cff                          # Machine-readable citation
├── CONTRIBUTING.md                       # Contribution guidelines
├── CODE_OF_CONDUCT.md                    # Community code of conduct
├── LICENSE.md                            # Apache-2.0 + Patent-Free overlay
├── release_manifest.json                 # Release integrity manifest
├── provenance.json                       # Data origin tracking (unsigned stub)
├── feature_flags.yml                     # Feature lifecycle management
└── mkdocs.yml                            # Documentation site config
```

---

## Testing

```bash
# Run the full test suite
pytest -q

# Expected output:
# 13 passed in 0.05s
```

The test suite covers:

| Test File | Coverage |
|-----------|----------|
| `test_pipeline.py` | End-to-end pipeline execution |
| `test_policy.py` | Policy enforcement and violation detection |
| `test_profiles.py` | Language profile loading and listing |
| `test_receipts.py` | SHA-256 receipt generation |
| `test_proof_export.py` | Proof bundle export |
| `test_provenance.py` | Provenance file validation |
| `test_batch_builder.py` | Batch dataset processing |
| `test_schema_validation.py` | Output schema validation |
| `test_release_check.py` | Release readiness verification |
| `test_release_summary.py` | Release summary generation |
| `test_version.py` | Version reporting |

---

## Documentation

Full documentation lives in `docs/` and is indexed in [`docs/INDEX.md`](docs/INDEX.md):

| Category | Documents |
|----------|-----------|
| **Core** | Overview, Architecture, Governance, Ethical Use |
| **Data & Schema** | Reproducibility, Archival Hash Notes |
| **Release** | Changelog, GitHub Release Text, Zenodo Publication Text, Publication Checklist |
| **Community** | Language Contribution Guide |

A `mkdocs.yml` is included for building a documentation site.

---

## Dashboard

PAT has an AI-integrated **Liquid Glass** dashboard providing a visual interface for:

- Pipeline monitoring (5-stage INGEST → VALIDATE → HASH → POLICY → RECEIPT flow)
- Audit trail inspection with receipt viewer
- Policy engine status and violation history
- Batch builder management
- AI Auditor chat with provenance chain analysis
- Command palette (`Ctrl+K`) with fuzzy search
- EU AI Act transparency labels

> **Note:** The dashboard is available on the [`devin/1775154432-ai-dashboard`](https://github.com/BrewtaniusAI/PAT/tree/devin/1775154432-ai-dashboard) branch. Once merged, open `dashboard/index.html` in any browser.

---

## Ethical Framing

PAT is released as public infrastructure with explicit ethical constraints. It must **not** be used for:

- **Impersonation** — Generating text that falsely represents another person
- **Political manipulation** — Creating deceptive political messaging
- **Synthetic deception** — Producing fake communications presented as authentic
- **Cultural exploitation** — Extractive use of culturally sensitive linguistic material

The policy engine enforces these constraints at runtime by scanning all input against forbidden patterns before execution. See [`docs/ETHICAL_USE.md`](docs/ETHICAL_USE.md) for the full ethical framework.

---

## CollectiveOS Integration

PAT operates within the broader CollectiveOS governance ecosystem:

| Integration | Role |
|------------|------|
| **QC Gate** | Self-audit before significant actions |
| **GATA** | Sandboxed testing and edge-case validation |
| **GATA PRIME** | Formal verification and audit trail maintenance |
| **Proof Vault** | WORM (Write Once Read Many) receipt logging |
| **ELFE Kernel** | Fixed-time convergence stability guarantees |
| **Constraint Engine** | Shared drift measurement and enforcement patterns |
| **SFO App** | Governed API gateway integration |

---

## Contributing

PAT welcomes contributions that improve reproducibility, clarity, language support, or safety. Priority areas:

- **New language profiles** — Add your language via a JSON profile
- **Tokenizer improvements** — Better handling of tone markers, diacritics, agglutinative morphology
- **Documentation** — Translations, tutorials, dataset annotation guides
- **Validation and tests** — Expand coverage for edge cases

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines and the pull request checklist.

### Adding a Language Profile

1. Create `configs/language_profiles/<iso-code>.json`:

```json
{
  "code": "<iso-code>",
  "name": "<Language Name>",
  "preserve_characters": ["<char1>", "<char2>"],
  "keywords": ["<keyword1>", "<keyword2>"]
}
```

2. Run the test suite to verify: `pytest -q`
3. Submit a PR using the [language profile request](https://github.com/BrewtaniusAI/PAT/issues/new?template=language_profile_request.md) template.

---

## Citation & Archival

### Cite PAT

```bibtex
@software{brewer_pat_2025,
  author  = {Brewer, Mark Anthony},
  title   = {PAT: Pan-African Language Infrastructure for AI},
  version = {1.0.0},
  doi     = {10.5281/zenodo.17046595},
  url     = {https://github.com/BrewtaniusAI/PAT}
}
```

### Integrity Artifacts

| Artifact | Purpose |
|----------|---------|
| `CITATION.cff` | Machine-readable citation metadata |
| `release_manifest.json` | SHA-256 integrity tracking for all release artifacts |
| `provenance.json` | Data origin and transformation history |
| `provenance.signed.example.json` | Template for signed provenance flows |

### Zenodo Archive

Archived at [doi.org/10.5281/zenodo.17046595](https://doi.org/10.5281/zenodo.17046595)

---

## License

**Apache-2.0** with a **Patent-Free Science** overlay.

PAT is released as executable public knowledge and prior art. No component of this framework may be used to seek or enforce patents on African language processing methods.
```
