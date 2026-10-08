# @beesmash/eisf-public-sdk

TypeScript reference implementation of the EISf Public Canon.

```ts
import { validateCase } from "@beesmash/eisf-public-sdk";

const result = validateCase(caseObject);
if (!result.valid) console.error(result.errors);
```

Provider helpers include generic Responses-compatible endpoints, OpenAI Responses, and Ollama/local inference.
