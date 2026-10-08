import json

from eisf.core import build_prompt, validate_case
from eisf.providers import OllamaProvider

event = "A local service is failing health checks."
provider = OllamaProvider(model="qwen3:8b")
case = json.loads(provider.generate(build_prompt(event, developer=True), event))

result = validate_case(case)
if not result.valid:
    raise SystemExit("\n".join(result.errors))

print(json.dumps(case, indent=2))
