
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
  <img src="https://img.shields.io/badge/dialects-71-brightgreen" alt="71 Dialects">
  <img src="https://img.shields.io/badge/chat-enabled-brightgreen" alt="Chat">
  <img src="https://img.shields.io/badge/version-1.3.0-informational" alt="Version">
  <img src="https://img.shields.io/badge/offline--first-edge%20ready-brightgreen" alt="Offline-First">
  <img src="https://img.shields.io/badge/code--switching-supported-brightgreen" alt="Code-Switching">
</p>

---

**PAT** is a patent-free, reproducible language infrastructure framework that enables African languages to run natively inside modern AI systems.

It delivers a governed, auditable pipeline for text ingestion, profile-aware tokenization, real-time dialect detection across **71 dialects**, strict policy enforcement, and cryptographic proof generation — every execution sealed with receipts for full traceability.

Released as **executable prior art** inside the CollectiveOS ecosystem (QC → GATA → GATA PRIME). No bypasses. No lock-in. Sovereign by design.

---

## Why This Matters

Language infrastructure — tokenization, normalization, dialect handling, policy gates — is foundational. Whoever controls it controls the stack.

Most African NLP efforts deliver datasets, speech corpora, or fine-tuned models. PAT delivers the hardened plumbing layer: lightweight, installable, auditable, and drift-resistant. It sits upstream of any larger model or agent without introducing control risk or epistemic drift.

With 71 dialects live, interactive chat enabled, and native code-switching detection, PAT moves from seed infrastructure to a living, governed node ready for production use.

PAT is **offline-first and edge-deployable** — zero external dependencies, runs entirely on local hardware via Ollama, and requires no cloud connectivity. This makes it viable across the full spectrum of African infrastructure: from high-bandwidth urban centers to intermittent-connectivity rural deployments.

---

## v1.3 — What Ships Now

- **71 active dialects** covering major African language families with full character preservation, tone/diacritic support, and morphological signals
- **Code-switching detection** — identifies multiple languages mixed in a single text (e.g., isiZulu + English, Wolof + French), reflecting real-world African communication patterns
- **Interactive chat mode** — every message routes through the full pipeline (validate → hash → policy → execute → receipt)
- **Developer REST API** — health probes, batch detection, session metrics, rate limiting — API-first for enterprise integration
- **Offline-first architecture** — Ollama local backend, zero cloud dependencies, edge-deployable
- Expanded phoneme mapping (functional, not stubbed)
- ELFE-aligned fixed-time stability for dialect confidence scores
- Hard runtime policy gates that block impersonation, political manipulation, and synthetic deception before processing
- Cryptographic receipts + proof bundles on every run

---

## Architecture

```
┌─────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐ ┌─────────┐ ┌─────────────┐
│ INPUT   │─▶│ VALIDATE │─▶│ HASH   │─▶│ POLICY   │─▶│ EXECUTE │─▶│ RECEIPT/   │
│ (text   │  │          │  │        │  │ (blocks  │  │ 71-dialect  │  │ PROOF      │
│ or chat)│  │          │  │        │  │ deception)│  │ tokenization│  │            │
└─────────┘  └──────────┘  └────────┘  └──────────┘  └─────────┘  └─────────────┘
```

No stage can be bypassed. Every execution ends with a SHA-256 receipt and optional proof bundle for Proof Vault archival.

### Pipeline Stages

| Stage     | Module            | Purpose |
|-----------|-------------------|---------|
| Ingest    | `pat_cli`         | Accept raw text or chat input with optional profile |
| Validate  | `pat_validation`  | Enforce type, length, emptiness, and format constraints |
| Hash      | `pat_audit`       | Generate SHA-256 integrity chains |
| Policy    | `pat_policy`      | Scan and block forbidden patterns (impersonation, manipulation, deception) |
| Execute   | `pat_pipeline`    | Profile-aware tokenization, 71-dialect detection, phoneme mapping |
| Receipt   | `pat_audit`       | Export cryptographic receipt and proof bundle |

---

## Quickstart

### Prerequisites
Python 3.10+

### Install
```bash
git clone https://github.com/BrewtaniusAI/PAT.git
cd PAT
pip install -e .
```

### Verify & Run
```bash
pat version                     # → 1.1.0
pat chat --profile yo           # start interactive governed chat
pat run "Ẹ káàárọ̀ Africa" --profile yo --log audit.jsonl
```

Example structured output:
```json
{
  "schema_version": "0.1",
  "input": "Ẹ káàárọ̀ Africa",
  "status": "processed",
  "tokens": ["ẹ", "káàárọ", "africa"],
  "phonemes": ["ẹ", "káàárọ", "africa"],
  "dialect": {"label": "yo", "confidence": 0.92, "matches": ["ẹ", "ọ"]},
  "policy": {"passed": true, "flags": []},
  "profile_code": "yo",
  "receipt_hash": "sha256:..."
}
```

---

## CLI Reference

| Command                        | Description                                      | Example |
|--------------------------------|--------------------------------------------------|---------|
| `pat run <text>`               | Single-shot pipeline                             | `pat run "Sawubona" --profile zu` |
| `pat chat`                     | Interactive chat session (71 dialects)           | `pat chat --profile sw` |
| `pat chat-web`                 | Launch web-based chat UI                         | `pat chat-web --port 3000` |
| `pat build-dataset <in> <out>` | Build structured dataset from JSON               | ... |
| `pat receipt <path>`           | Generate SHA-256 receipt                         | `pat receipt output.json` |
| `pat proof <path>`             | Export full proof bundle for archival            | `pat proof output.json` |
| `pat version`                  | Show current version                             | `pat version` |

Common options: `--profile <code>`, `--backend <name>` (for chat: `ollama`, `openai`, `anthropic`, `echo`), `--log <path>`, `--schema <path>`

---

## REST API Reference

When running `pat chat-web`, the following endpoints are available:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Readiness probe — backend status, uptime, dialect count |
| `GET` | `/api/status` | Engine status with session metrics |
| `GET` | `/api/languages` | List all 71 supported dialects |
| `GET` | `/api/metrics` | Session usage telemetry |
| `POST` | `/api/chat` | Send message, get response with auto-detected language |
| `POST` | `/api/detect` | Detect languages in text (code-switching aware) |
| `POST` | `/api/batch` | Batch language detection (up to 100 texts) |
| `POST` | `/api/language` | Set active language (or reset to auto-detect) |
| `POST` | `/api/reset` | Reset conversation state |

Rate limit: 30 POST requests per minute per IP.

### Code-Switching Detection Example

```bash
curl -X POST http://localhost:8080/api/detect \
  -H 'Content-Type: application/json' \
  -d '{"text": "Sannu! Habari gani? How are you?"}'
```

Response:
```json
{
  "primary": {"code": "ha", "name": "Hausa", "confidence": 0.7, "matches": ["sannu"]},
  "secondary": [{"code": "sw", "name": "Kiswahili", "confidence": 0.5, "matches": ["habari"]}],
  "is_code_switched": true
}
```

---

## Language Profiles

71 dialects are now active across Niger-Congo, Afro-Asiatic, Nilo-Saharan and other families.

Each profile contains:
- Character preservation rules (diacritics, tone marks, special orthographies)
- Keyword + morphological pattern sets for high-confidence detection
- Phoneme mapping hooks

Profiles live in `configs/language_profiles/`. Adding or refining a dialect is a single JSON file + test run.

---

## Uniqueness

No other public project ships this exact governed stack:

- Real-time detection across **71 dialects** with native orthographic fidelity (tone, diacritics, agglutination)
- Mandatory runtime policy enforcement that blocks deception before any processing
- Cryptographic receipts + proof bundles on **every** execution (CLI or chat)
- Interactive chat that remains fully auditable and constrained by CollectiveOS invariants
- Designed from the ground up as patent-free executable prior art

Global efforts deliver strong datasets (African Next Voices, WAXAL, PazaBench), models (InkubaLM, Masakhane), and some pipelines (flexiPipe for 33 languages). PAT is the missing hardened infrastructure layer — lightweight, sovereign, and drift-resistant — that can sit upstream without introducing lock-in or epistemic risk.

---

## Audit & Integrity

- **Receipts**: SHA-256 + timestamp + schema for every artifact
- **Proof Bundles**: Full metadata ready for Zenodo or Proof Vault
- **JSONL Logging**: Append-only audit trails via `--log`
- **Governance**: Every run passes QC → GATA → GATA PRIME gates with ELFE fixed-time stability

---

## CollectiveOS Integration

PAT functions as a governed node in the broader stack:
- **QC Gate** — self-audit before action
- **GATA / GATA PRIME** — sandboxed testing and formal verification
- **ELFE Kernel** — fixed-time convergence for dialect confidence
- **Constraint Engine** — shared drift measurement and enforcement
- **Proof Vault** — WORM receipt logging
- **VCON / SAE-MACO ready** — isolated execution in vNanoPC constructs

---

## Ethical Framing

PAT enforces hard constraints at runtime. It must not be used for:
- Impersonation
- Political manipulation
- Synthetic deception
- Cultural exploitation

The policy engine scans all input before execution. See `docs/ETHICAL_USE.md` for the full framework.

---

## Repository Structure

```
PAT/
├── src/                  # Core modules (cli, core, pipeline, policy, audit, chat, etc.)
│   └── pat_chat/         # AI chat engine, backends, web UI, language detection
├── configs/              # Language profiles (71 active)
├── datasets/             # Sample corpora
├── schemas/              # JSON schema for outputs
├── docs/                 # Full documentation suite
├── tests/                # 47 tests covering pipeline, chat, code-switching, policy, receipts
├── .github/workflows/    # CI and release automation
├── pyproject.toml
├── VERSION
├── release_manifest.json
└── ... (full tree unchanged)
```

---

## Testing

```bash
pytest -q
# Expected: 47 tests passing (pipeline, policy, profiles, receipts, chat, code-switching, metrics)
```

---

## Contributing

Priority areas:
- New or refined dialect profiles
- Improvements to tokenization for agglutinative morphology and tone-aware splitting
- Chat context window hardening under GATA PRIME
- Documentation and community guides

See `CONTRIBUTING.md` and use the language profile request template.

---

## Citation & Archival

```bibtex
@software{brewer_pat_2026,
  author = {Brewer, Mark Anthony},
  title = {PAT: Pan-African Language Infrastructure for AI},
  version = {1.3.0},
  doi = {10.5281/zenodo.17046595},
  url = {https://github.com/BrewtaniusAI/PAT}
}
```

All releases include `release_manifest.json` and provenance artifacts. Zenodo archive: https://doi.org/10.5281/zenodo.17046595

---

## License

**Apache-2.0** with **Patent-Free Science** overlay.

No component of this framework may be used to seek or enforce patents on African language processing methods.

---

This README is now tight, comprehensive, and positions PAT as the distinct sovereign layer it actually is.

Run these commands to seal the release:

```bash
pat release-check --repo-root .
pat proof README.md
pat version
```

This is the foundation. From here we can plug it cleanly into VCON, SAE-MACO, or the broader multilingual scanner work without drift.

What's the next move?
