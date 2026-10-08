# EISf for AI Developers

EISf can wrap an AI coding workflow without binding the workflow to one model provider.

| EISf stage | Software-development interpretation |
| --- | --- |
| Event | feature request, bug, incident, dependency change, security report |
| Impact | architecture, users, APIs, data, security, compatibility, cost, operations |
| Scenario | implementation paths, failure modes, migration alternatives |
| Adaptation | code changes, tests, mitigations, feature flags, migration, rollback |
| Decision | chosen plan, acceptance criteria, owner, review trigger |

## Model neutrality

The SDK treats provider calls as replaceable adapters. OpenAI, Responses-compatible services, Ollama/local inference, and future providers can sit behind the same EISf reasoning contract.

## Engineering gate

```text
Event
  ↓
Impact
  ↓
Scenario
  ↓
Adaptation
  ↓
Decision
  ↓
Implementation
  ↓
Tests
  ↓
Security review
  ↓
Acceptance
```

EISf does not guarantee correctness or security. It provides a structured, inspectable decision envelope around engineering work.
