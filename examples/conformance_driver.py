#!/usr/bin/env python3
"""Minimal language-neutral conformance-driver example using the Python SDK."""

import json
import sys

from eisf.core import validate_case


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if request.get("operation") != "validate":
            raise ValueError("unsupported operation")
        case = request["case"]
    except Exception as exc:
        json.dump({"valid": False, "errors": [f"driver request error: {exc}"]}, sys.stdout)
        return 2

    result = validate_case(case)
    response = {
        "valid": result.valid,
        "errors": list(result.errors),
    }
    if result.valid:
        response["case"] = case
    json.dump(response, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
