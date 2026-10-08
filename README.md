# EISf Public SDK

**Event → Impact → Scenario → Adaptation → Decision**

A public, provider-neutral framework for structured reasoning, decision support, AI-assisted analysis, and software workflows.

Originated by **Erick Lester Brown / Beesmash Inc.**

> This repository contains the public EISf canon and public developer SDK only. It does **not** disclose proprietary JANUS prompts, KRONOS orchestration logic, private scoring methods, internal routing policies, client methods, private datasets, or other Beesmash trade-secret implementation details.

## Hello, world

EISf separates reasoning into five canonical stages:

1. **Event** — What happened, is happening, or is proposed?
2. **Impact** — What changes because of it, for whom, and on what timescale?
3. **Scenario** — What plausible futures or branches follow?
4. **Adaptation** — What actions reduce risk, capture opportunity, or improve resilience?
5. **Decision** — What should be chosen now, by whom, and with what review trigger?

## Public goals

- Give developers a stable, model-agnostic reasoning contract.
- Support OpenAI, local models, and other cloud models without vendor lock-in.
- Make AI outputs more inspectable by separating observations, consequences, futures, actions, and decisions.
- Encourage provenance, assumptions, confidence statements, and review triggers.
- Provide conformance tooling for implementations that claim **EISf Core Compatible**.

## Public / private boundary

The public SDK defines interoperability and developer tooling. The proprietary Beesmash stack—JANUS EISf, KRONOS, JANUS FORGE, private agents, private skills, private scoring and routing—remains separate.

## Status

**Public SDK:** v0.1.0  
**Public Canon:** v1.0.0-draft

## License

Apache License 2.0.

## Attribution

**EISf Public Canon — Event → Impact → Scenario → Adaptation → Decision**  
Erick Lester Brown / Beesmash Inc.
