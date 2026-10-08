from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SDK_VERSION = "0.1.0"
EISF_VERSION = "1.0.0-draft"
STAGES = ("event", "impacts", "scenarios", "adaptations", "decision")
CONFIDENCE_LABELS = {"low", "medium", "high"}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]


def _valid_confidence(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return 0 <= value <= 1
    return isinstance(value, str) and value in CONFIDENCE_LABELS


def _validate_item(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return
    statement = value.get("statement")
    if not isinstance(statement, str) or not statement.strip():
        errors.append(f"{path}.statement must be a non-empty string")
    if "confidence" in value and not _valid_confidence(value["confidence"]):
        errors.append(f"{path}.confidence must be low/medium/high or a number from 0 to 1")


def validate_case(case: Any) -> ValidationResult:
    errors: list[str] = []
    if not isinstance(case, dict):
        return ValidationResult(False, ("case must be a JSON object",))

    for key in STAGES:
        if key not in case:
            errors.append(f"missing required stage: {key}")

    if "event" in case:
        _validate_item(case["event"], "event", errors)

    for stage in ("impacts", "scenarios", "adaptations"):
        if stage not in case:
            continue
        value = case[stage]
        if not isinstance(value, list) or not value:
            errors.append(f"{stage} must be a non-empty array")
            continue
        for index, item in enumerate(value):
            _validate_item(item, f"{stage}[{index}]", errors)

    if "decision" in case:
        _validate_item(case["decision"], "decision", errors)
        if isinstance(case["decision"], dict):
            status = case["decision"].get("status")
            if status is not None and status not in {"decided", "deferred"}:
                errors.append("decision.status must be 'decided' or 'deferred'")

    return ValidationResult(not errors, tuple(errors))


def build_prompt(event_statement: str, developer: bool = False) -> str:
    extra = ""
    if developer:
        extra = (
            "\nFor software-development work, explicitly consider architecture, APIs, "
            "data, security, compatibility, testing, deployment, rollback, operations, "
            "cost, and acceptance criteria when relevant."
        )
    return f"""Use the EISf Public Canon: Event → Impact → Scenario → Adaptation → Decision.

Analyze the following Event:
{event_statement}
{extra}

Return ONLY one JSON object with this shape:
{{
  "event": {{"statement": "..."}},
  "impacts": [{{"statement": "..."}}],
  "scenarios": [{{"statement": "..."}}],
  "adaptations": [{{"statement": "..."}}],
  "decision": {{"statement": "...", "status": "decided"}}
}}

Do not collapse scenarios into decisions. State uncertainty explicitly where relevant."""
