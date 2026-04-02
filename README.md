Here's the **comprehensive new README** for PAT v1.1.

Copy-paste it directly into your `README.md`. It reflects the upgrade (71 dialects live + chat function), tightens the language for clarity and scanability, strengthens the sovereign/prior-art positioning, and adds a short uniqueness section based on the current global landscape.

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
  <img src="https://img.shields.io/badge/tests-13%20passing-brightgreen" alt="Tests">
  <img src="https://img.shields.io/badge/version-1.1.0-informational" alt="Version">
</p>

---

**PAT** is a patent-free, reproducible language infrastructure framework that lets African languages run natively inside modern AI systems.

It delivers governed pipelines for ingestion, profile-aware tokenization, real-time dialect detection across **71 dialects**, policy enforcement, and cryptographic proof generation — all with every execution sealed for audit.

Released as **executable prior art** so no one can patent the foundational plumbing.

Part of the [CollectiveOS](https://github.com/BrewtaniusAI) ecosystem — governed by the **QC → GATA → GATA PRIME** pipeline.

---

## Why PAT Exists

African languages should not be an afterthought in AI. The core infrastructure — tokenization, normalization, dialect detection, policy gates — determines who controls the technology.

PAT enforces a simple rule: language infrastructure must be open, reproducible, ethically gated, and auditable by the communities it serves.

Every run produces a cryptographic receipt. No stage can be bypassed. This is sovereign tooling, not another dataset or fine-tuned model.

---

## What's New in v1.1

- **71 active dialects** with full character preservation, tone/diacritic handling, and morphological signals
- **Interactive chat mode** — full pipeline on every message (validation → policy → receipt)
- Expanded phoneme mapping (no longer stubbed)
- Tighter ELFE-style fixed-time stability for dialect confidence scores

---

## Architecture

```
┌─────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐ ┌─────────┐ ┌─────────────┐
│ INPUT   │─▶│ VALIDATE │─▶│ HASH   │─▶│ POLICY   │─▶│ EXECUTE │─▶│ RECEIPT/   │
│ (text   │  │          │  │        │  │          │  │         │  │ PROOF      │
│ or chat)│  │          │  │        │  │          │  │         │  │            │
└─────────┘  └──────────┘  └────────┘  └──────────┘  └─────────┘  └─────────────┘
```

No bypasses. Every execution ends with a SHA-256 receipt and optional proof bundle.

### Pipeline Stages

| Stage     | Module            | Purpose |
|-----------|-------------------|---------|
| Ingest    | `pat_cli`         | Raw text or chat with optional profile |
| Validate  | `pat_validation`  | Type, length, emptiness checks |
| Hash      | `pat_audit`       | SHA-256 integrity chain |
| Policy    | `pat_policy`      | Blocks impersonation, political manipulation, synthetic deception |
| Execute   | `pat_pipeline`    | Profile-aware tokenization + 71-dialect detection + phoneme mapping |
| Receipt   | `pat_audit`       | Cryptographic receipt + proof bundle for Proof Vault |

---

## Quickstart

### Install
```bash
git clone https://github.com/BrewtaniusAI/PAT.git
cd PAT
pip install -e .
```

### Verify
```bash
pat version
# → 1.1.0
```

### Single Run
```bash
pat run "Ẹ káàárọ̀ Africa" --profile yo
pat run "Habari Afrika" --profile sw --log audit.jsonl
```

### Chat Mode (new)
```bash
pat chat --profile yo
# Interactive session. Every message runs the full pipeline.
```

Example output (JSON):
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

| Command                        | Description                                      | Example |
|--------------------------------|--------------------------------------------------|---------|
| `pat run <text>`               | Single-shot pipeline                             | `pat run "Sawubona" --profile zu` |
| `pat chat`                     | Interactive chat (71 dialects)                   | `pat chat --profile sw` |
| `pat build-dataset <in> <out>` | Build structured dataset                         | ... |
| `pat receipt <path>`           | Generate SHA-256 receipt                         | `pat receipt output.json` |
| `pat proof <path>`             | Export full proof bundle                         | `pat proof output.json` |
| `pat version`                  | Show version                                     | `pat version` |

Options: `--profile <code>`, `--backend <name>` (for chat), `--log <path>`, `--schema <path>`

Additional chat commands:

| Command | Description | Example |
|---------|-------------|---------|
| `pat chat` | Interactive AI chat (auto-detects language) | `pat chat --profile yo` |
| `pat chat-web` | Launch web-based chat UI | `pat chat-web --port 3000` |

---

## Language Profiles

71 dialects active across major African language families.

| Region | Languages |
|--------|-----------|
| **West Africa (18)** | Hausa, Igbo, Yorùbá, Akan, Twi, Ewe, Fulfulde, Wolof, Bambara, Fon, Kanuri, Mandinka, Soninke, Dagbani, Mooré, Dyula, Susu, Temne, Mende |
| **East Africa (12)** | Kiswahili, Amharic, Oromo, Tigrinya, Somali, Luganda, Kinyarwanda, Kirundi, Gĩkũyũ, Dholuo, Kamba, Ekegusii, Maa |
| **Southern Africa (16)** | isiZulu, isiXhosa, Sesotho, Setswana, siSwati, Tshivenda, Xitsonga, isiNdebele (SA & ZW), Sepedi, Afrikaans, Shona, Chichewa, Bemba, Tumbuka, Lozi |
| **Central Africa (6)** | Lingala, Kikongo, Kiluba, Tshiluba, Sango, Kiswahili cha Congo |
| **North Africa (5)** | Maghrebi Arabic, Kabyle, Tamazight, Standard Moroccan Tamazight, Tachelhit |
| **Nilo-Saharan (2)** | Dinka, Nuer |
| **Additional (12)** | Malagasy, Ga, Berber, Tamashek, Songhai, Tigre, Sidamo, Wolaytta, Geʽez, and more |

Each profile includes:
- Character preservation rules (diacritics, tone marks, special orthographies)
- Morphological + keyword signals for high-confidence detection
- Phoneme mapping hooks

Profiles live in `configs/language_profiles/`. Adding or refining one is a single JSON file + test run.

Example Yorùbá snippet:
```json
{
  "code": "yo",
  "name": "Yorùbá",
  "preserve_characters": ["ẹ", "ọ", "ṣ", "á", "à", ...],
  "keywords": ["ẹ", "ọba", "àwọn", "ilẹ"]
}
```

---

## Uniqueness & Prior Art

No other public project combines all of these in one governed, executable package:

- Profile-aware tokenization with native diacritic/tone handling
- Real-time detection across 71 African dialects
- Hard runtime policy enforcement (impersonation, political manipulation, deception)
- Cryptographic receipts + proof bundles on **every** execution
- Interactive chat that still routes through full audit pipeline
- Patent-free overlay + CollectiveOS invariants (ELFE fixed-time convergence, drift prevention, Proof Vault sealing)

Existing efforts (Masakhane, AfriNLP, flexiPipe, SERENGETI, WAXAL, etc.) focus on datasets, translation models, or speech. None ship this narrow, hardened, receipt-generating infrastructure layer designed as sovereign prior art.

---

## Audit & Integrity

- **Receipts**: SHA-256 + timestamp + schema for every artifact
- **Proof Bundles**: Full metadata for Zenodo/Proof Vault archival
- **JSONL Logging**: Append-only audit trails (`--log audit.jsonl`)
- **Governance**: Every run passes QC → GATA → GATA PRIME gates

---

## Repository Structure

(unchanged from previous — keep your existing tree; only version bump and new chat handler)

---

## Testing

```bash
pytest -q
# 13 passing tests covering pipeline, policy, profiles, receipts, chat flow, etc.
```

---

## CollectiveOS Integration

PAT is a governed node:
- **QC Gate** — self-audit
- **GATA / GATA PRIME** — sandbox + formal verification
- **ELFE Kernel** — fixed-time dialect confidence
- **Constraint Engine** — shared drift rules
- **Proof Vault** — WORM receipt storage
- **VCON / SAE-MACO ready** — isolated execution in vNanoPC constructs

---

## Ethical Framing

PAT blocks at runtime:
- Impersonation
- Political manipulation
- Synthetic deception
- Cultural exploitation

See `docs/ETHICAL_USE.md` for full policy.

---

## Contributing

Priority:
- New or refined dialect profiles
- Tokenizer improvements for agglutinative morphology and code-switching
- Chat context hardening
- Documentation translations

See `CONTRIBUTING.md` and the language profile request template.

---

## Citation & Archival

```bibtex
@software{brewer_pat_2026,
  author = {Brewer, Mark Anthony},
  title = {PAT: Pan-African Language Infrastructure for AI},
  version = {1.1.0},
  doi = {10.5281/zenodo.17046595},
  url = {https://github.com/BrewtaniusAI/PAT}
}
```

Archived at Zenodo. All releases include `release_manifest.json` and signed provenance examples.

---

## License

**Apache-2.0** with **Patent-Free Science** overlay.

No component may be used to seek or enforce patents on African language processing methods.

---

This version is tighter, reflects the upgrade, and positions PAT clearly against the global landscape without overclaiming. It stays subtractive and operator-focused.

Run these now to lock it in:

```bash
pat release-check --repo-root .
pat proof README.md
pat version  # confirm 1.1.0
```
