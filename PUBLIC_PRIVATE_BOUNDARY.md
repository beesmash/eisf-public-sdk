# Public / Private Boundary

This repository is a deliberately narrow **public core**, not a publication of the full Beesmash/JANUS system.

## Intentionally public

- Event → Impact → Scenario → Adaptation → Decision
- high-level semantic definitions
- portable JSON representation
- public validation rules
- public provider adapters
- public developer examples
- conformance fixtures and driver protocol
- public governance and contribution rules

## Reserved private implementation space

The public SDK does **not** disclose or license by implication proprietary JANUS prompts, internal scoring formulas, KRONOS orchestration logic, private routing/fallback policies, private B-level criteria, private client methods, private model-evaluation datasets, private RAG corpora, credentials, security internals, unpublished provenance infrastructure, private agent registries, private skill libraries, or proprietary JANUS FORGE extensions.

## Compatibility is not equivalence

A system may be **EISf Core Compatible** by implementing and passing the public conformance suite. That does not make the system JANUS, KRONOS, JANUS FORGE, or a Beesmash implementation.

## Publication gate

Before moving any internal capability into this repository, ask whether publication could disclose a trade secret, affect patent strategy, expose a client method, reveal a security control, or disclose third-party material. If in doubt, keep it private pending review.
