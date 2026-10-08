# EISf Public SDK

[![CI](https://github.com/beesmash/eisf-public-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/beesmash/eisf-public-sdk/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/beesmash/eisf-public-sdk)](https://github.com/beesmash/eisf-public-sdk/releases/latest)

**Event → Impact → Scenario → Adaptation → Decision**

A public, provider-neutral framework and developer SDK for structured reasoning, decision support, AI-assisted analysis, and software workflows.

Originated by **Erick Lester Brown / Beesmash Inc.**

> This repository intentionally contains only the public EISf canon and public SDK. It does **not** disclose proprietary JANUS prompts, KRONOS orchestration logic, private scoring methods, private routing policies, client methods, private datasets, internal B-level logic, or other Beesmash trade-secret implementation details.

## Canon

1. **Event** — What happened, is happening, or is proposed?
2. **Impact** — What changes because of it, for whom, and on what timescale?
3. **Scenario** — What plausible futures or branches follow?
4. **Adaptation** — What actions reduce risk, capture opportunity, or improve resilience?
5. **Decision** — What should be chosen now, by whom, with what assumptions and review trigger?

EISf is the reasoning contract, not the model.

## Start here

For a first run, see [docs/QUICKSTART.md](docs/QUICKSTART.md).

Python:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/hello_world.py
```

TypeScript:

```bash
cd typescript
npm install
npm run hello
```

## SDK v0.1.0

The public SDK provides:

- Python reference package and `eisf` CLI
- TypeScript package
- canonical JSON Schema
- OpenAI Responses adapter
- generic Responses-compatible adapter
- Ollama/local adapter
- deterministic mock provider for offline testing
- conformance suite for **EISf Core Compatible**
- GitHub CI and release workflows

## CLI

```bash
eisf validate examples/basic_case.json
eisf analyze "A dependency introduced a breaking API change" --provider mock
eisf dev "Add passwordless authentication" --provider mock
eisf conformance
```

OpenAI:

```bash
export OPENAI_API_KEY="..."
eisf analyze "Production API latency doubled" --provider openai --model YOUR_MODEL
```

Ollama/local:

```bash
eisf analyze "A local service is failing health checks" --provider ollama --model qwen3:8b
```

## Conformance

A third-party implementation may claim:

> **EISf Core Compatible — Self-Tested against EISf Conformance Suite v0.1**

only when it passes all mandatory fixtures in this repository using the documented driver protocol.

This is a self-test compatibility claim, **not independent certification**.

## Public / private boundary

See [PUBLIC_PRIVATE_BOUNDARY.md](PUBLIC_PRIVATE_BOUNDARY.md). Compatibility with the public EISf canon does not imply equivalence with JANUS, KRONOS, JANUS FORGE, or another proprietary Beesmash implementation.

## Release verification

The v0.1.0 tag, CI state, artifact names, and SHA-256 digests are recorded in [docs/RELEASE_VERIFICATION_v0.1.0.md](docs/RELEASE_VERIFICATION_v0.1.0.md).

## Status

- **EISf Public SDK:** v0.1.0
- **EISf Public Canon:** v1.0.0-draft
- **License:** Apache-2.0

## Attribution

**EISf Public Canon — Event → Impact → Scenario → Adaptation → Decision**  
Erick Lester Brown / Beesmash Inc.

## Citation

GitHub can read the repository's [`CITATION.cff`](CITATION.cff). For human-readable attribution:

> EISf Public Canon — Event → Impact → Scenario → Adaptation → Decision. Erick Lester Brown / Beesmash Inc.

## Release history

See [CHANGELOG.md](CHANGELOG.md).
