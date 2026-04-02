## Zenodo Record

PAT concept paper and release context:
DOI: 10.5281/zenodo.17046595
Zenodo record: https://doi.org/10.5281/zenodo.17046595
# PAT — Pan-African Language Infrastructure

PAT is a patent-free, reproducible language infrastructure project designed to help African languages exist natively inside modern AI systems.

This repository is released as executable public knowledge. It is part of a broader patent-free science and open collaboration framework and is intended to function as:
- public infrastructure
- executable prior art
- reproducible technical disclosure
- a foundation for community stewardship

## Why PAT exists

African languages should not be an afterthought in AI.

PAT begins with a simple principle: language infrastructure should be open, reproducible, ethically framed, and usable by the communities it affects.

## What this release includes

- governed execution pipeline
- validation and policy enforcement
- 71 language profiles spanning West, East, Southern, Central, and North Africa
- seed profiles include Yorùbá, Kiswahili, isiZulu, Hausa, Igbo, Amharic, Oromo, Wolof, Bambara, Lingala, Shona, isiXhosa, Sesotho, Setswana, and many more
- profile-aware tokenization path
- dataset builder and batch dataset builder
- receipts and proof bundle export
- schema validation and release integrity checks
- contribution files and language steward guidance
- publication pack for GitHub and Zenodo release
- AI chat with all 71 languages (CLI + web UI)
- pluggable LLM backends: Ollama (local/offline), OpenAI, Anthropic
- auto language detection across all profiles

## Core execution model

```text
Input → Validation → Policy → Execution → Output → Receipt / Proof
```

No pipeline stage is intended to bypass validation or policy checks.

## Quickstart

```bash
python -m pip install -e .
pat version
pat run "Ẹ káàárọ̀ Africa" --profile yo
```

### Build datasets

```bash
pat build-dataset input.json output.json
pat build-dataset-batch input_dir output_dir
```

### AI Chat

```bash
# Interactive terminal chat (auto-detects language)
pat chat

# Chat in a specific language
pat chat --profile yo

# Use a specific LLM backend
pat chat --backend ollama
pat chat --backend openai   # requires OPENAI_API_KEY
pat chat --backend anthropic # requires ANTHROPIC_API_KEY

# Launch web chat UI
pat chat-web
pat chat-web --port 3000
```

### Generate integrity artifacts

```bash
pat receipt output.json
pat proof output.json
pat validate-output output.json
pat release-check --repo-root .
```

## Repository map

- `src/` — runtime, validation, policy, audit, builder, chat, and CLI code
- `src/pat_chat/` — AI chat engine, backends, web UI, language detection
- `configs/language_profiles/` — 71 language profiles across the continent
- `datasets/` — sample corpora and annotation materials
- `schemas/` — output and dataset schemas
- `docs/` — governance, reproducibility, release, and publication materials
- `.github/` — CI, templates, and release workflow

## Public release files

See:
- `docs/GITHUB_RELEASE_TEXT.md`
- `docs/ZENODO_PUBLICATION_TEXT.md`
- `docs/PUBLICATION_CHECKLIST.md`
- `docs/REPOSITORY_METADATA.md`

## Ethical framing

PAT should not be used for:
- impersonation
- political manipulation
- deceptive synthetic communication
- exploitative extraction of culturally sensitive material

See `docs/ETHICAL_USE.md`.

## Citation and archival path

- `CITATION.cff`
- `release_manifest.json`
- `provenance.json`
- receipt and proof bundle outputs

## Status

PAT v0.9.0 is a public-alpha release candidate.

It is intentionally small, reproducible, and extensible.
