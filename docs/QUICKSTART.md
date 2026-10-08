# EISf Public SDK Quickstart

This guide gets a developer from clone to a valid EISf case with no cloud model required.

## Python

```bash
git clone https://github.com/beesmash/eisf-public-sdk.git
cd eisf-public-sdk

python -m venv .venv
source .venv/bin/activate
pip install -e .

python examples/hello_world.py
eisf validate examples/basic_case.json
eisf conformance
```

Expected compatibility line:

```text
EISf Core Compatible — Self-Tested against EISf Conformance Suite v0.1
```

## TypeScript

```bash
cd typescript
npm install
npm run hello
npm test
```

## OpenAI Responses

Set an API key and choose a currently available model name:

```bash
export OPENAI_API_KEY="..."
eisf analyze "A production service changed behavior" --provider openai --model YOUR_MODEL
```

The SDK deliberately does not hard-code one OpenAI model. Model selection remains an implementation choice.

## Generic Responses-compatible endpoint

```bash
export EISF_API_KEY="..."
eisf analyze "A requirement changed" \
  --provider responses \
  --model YOUR_MODEL \
  --base-url https://provider.example/v1/responses
```

## Ollama / local inference

```bash
ollama serve
eisf analyze "A local service is failing health checks" \
  --provider ollama \
  --model qwen3:8b
```

## Developer mode

```bash
eisf dev "Add passwordless authentication" --provider mock
```

Developer mode asks the provider to consider architecture, APIs, data, security, compatibility, testing, deployment, rollback, operations, cost, and acceptance criteria when relevant.

## Next

- Read [AI_FOR_DEVELOPERS.md](AI_FOR_DEVELOPERS.md).
- Review [../SPECIFICATION.md](../SPECIFICATION.md).
- Run [../conformance/README.md](../conformance/README.md) if you are implementing EISf in another tool or language.
