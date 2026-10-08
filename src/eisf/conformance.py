from __future__ import annotations

from copy import deepcopy

from .core import validate_case

SUITE_VERSION = "0.1"

_BASE = {
    "event": {"statement": "A change occurred."},
    "impacts": [{"statement": "A system is affected."}],
    "scenarios": [{"statement": "A branch is plausible."}],
    "adaptations": [{"statement": "A mitigation exists."}],
    "decision": {"statement": "Proceed with review.", "status": "decided"},
}


def fixtures() -> list[tuple[str, dict, bool]]:
    valid_minimal = deepcopy(_BASE)

    valid_rich = deepcopy(_BASE)
    valid_rich["event"]["confidence"] = "high"
    valid_rich["impacts"][0]["confidence"] = 0.9
    valid_rich["provenance"] = {"sdk": "0.1.0"}

    valid_deferred = deepcopy(_BASE)
    valid_deferred["decision"] = {
        "statement": "Defer until test results are available.",
        "status": "deferred",
    }

    missing_decision = deepcopy(_BASE)
    del missing_decision["decision"]

    empty_impacts = deepcopy(_BASE)
    empty_impacts["impacts"] = []

    empty_event = deepcopy(_BASE)
    empty_event["event"]["statement"] = ""

    malformed_scenario = deepcopy(_BASE)
    malformed_scenario["scenarios"] = ["not-an-object"]

    invalid_confidence = deepcopy(_BASE)
    invalid_confidence["event"]["confidence"] = 1.2

    return [
        ("01-valid-minimal", valid_minimal, True),
        ("02-valid-rich", valid_rich, True),
        ("03-valid-deferred", valid_deferred, True),
        ("04-missing-decision", missing_decision, False),
        ("05-empty-impacts", empty_impacts, False),
        ("06-empty-event", empty_event, False),
        ("07-malformed-scenario", malformed_scenario, False),
        ("08-invalid-confidence", invalid_confidence, False),
    ]


def run_internal_suite() -> tuple[int, int, list[tuple[str, bool]]]:
    results: list[tuple[str, bool]] = []
    for fixture_id, case, expected in fixtures():
        actual = validate_case(case).valid
        results.append((fixture_id, actual == expected))
    passed = sum(1 for _, ok in results if ok)
    return passed, len(results), results
