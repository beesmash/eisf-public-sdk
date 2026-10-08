import json
import os

from eisf.core import build_prompt, validate_case
from eisf.providers import OpenAIResponsesProvider

event = "A production dependency introduced a breaking API change."
model = os.environ["OPENAI_MODEL"]

provider = OpenAIResponsesProvider(model=model)
case = json.loads(provider.generate(build_prompt(event, developer=True), event))

result = validate_case(case)
if not result.valid:
    raise SystemExit("\n".join(result.errors))

print(json.dumps(case, indent=2))
