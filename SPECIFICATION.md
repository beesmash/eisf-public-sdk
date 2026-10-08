# EISf Public Canon Specification v1.0.0-draft

## Scope

EISf separates five kinds of reasoning that are often collapsed into a single answer:

**Event → Impact → Scenario → Adaptation → Decision**

A conforming implementation MUST preserve the semantic distinction among all five stages even if its internal processing is iterative or parallel.

## Event

The Event stage states the triggering condition, observation, proposal, requirement, incident, signal, or change being examined. An Event MUST contain a non-empty `statement`.

## Impact

Impact identifies consequences attributable to, or materially associated with, the Event. A case MUST contain at least one Impact.

## Scenario

Scenario represents plausible future branches, states, interpretations, or implementation paths. A case MUST contain at least one Scenario. A Scenario is not a prediction unless explicitly labeled as one.

## Adaptation

Adaptation describes actions that could reduce harm, improve resilience, exploit opportunity, gather information, or preserve optionality. A case MUST contain at least one Adaptation.

## Decision

Decision records the selected course of action or an explicit decision to defer. A Decision MUST contain a non-empty `statement`. It MAY carry `status: "decided"` or `status: "deferred"`.

An implementation MUST NOT silently convert a Scenario into a Decision.

## Provenance

Implementations SHOULD retain sufficient provenance to reconstruct how a case was produced.

## Confidence

Confidence MAY be categorical (`low`, `medium`, `high`) or numerical in the inclusive range 0 through 1.

## Core compatibility

An implementation is **EISf Core Compatible** when it represents all five stages, preserves their semantic distinctions, rejects malformed core cases, produces an explicit Decision or deferred-decision state, exposes a portable case, and passes the mandatory public conformance suite for the claimed version.

## Non-goals

The public canon does not define proprietary scoring, a preferred LLM, mandatory hidden prompts, a required orchestration engine, a mandatory agent architecture, or Beesmash proprietary implementation methods.
