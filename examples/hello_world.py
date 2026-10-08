"""Smallest useful EISf Public SDK example."""

import json

from eisf.core import validate_case
from eisf.providers import MockProvider


event = "Hello, world: a developer is evaluating EISf."

raw = MockProvider().generate("Use the EISf Public Canon.", event)
case = json.loads(raw)

result = validate_case(case)
if not result.valid:
    raise SystemExit("\n".join(result.errors))

print("EISf hello world")
print(json.dumps(case, indent=2))
