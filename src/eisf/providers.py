from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class Provider(Protocol):
    def generate(self, instructions: str, input_text: str = "") -> str:
        ...


def _post_json(url: str, payload: dict, headers: dict[str, str] | None = None) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"provider HTTP {exc.code}: {detail}") from exc


def _extract_responses_text(data: dict) -> str:
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    chunks: list[str] = []
    for item in data.get("output", []):
        if not isinstance(item, dict):
            continue
        for part in item.get("content", []):
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunks.append(part["text"])
    if chunks:
        return "\n".join(chunks)
    raise RuntimeError("provider response did not contain text output")


@dataclass
class MockProvider:
    def generate(self, instructions: str, input_text: str = "") -> str:
        return json.dumps({
            "event": {"statement": input_text or "Example event"},
            "impacts": [{"statement": "The event may change system behavior."}],
            "scenarios": [{"statement": "A controlled implementation path is available."}],
            "adaptations": [{"statement": "Test, review, and preserve rollback options."}],
            "decision": {
                "statement": "Proceed only after acceptance criteria are satisfied.",
                "status": "decided"
            }
        })


@dataclass
class OpenAIResponsesProvider:
    model: str
    api_key: str | None = None
    base_url: str = "https://api.openai.com/v1/responses"

    def generate(self, instructions: str, input_text: str = "") -> str:
        key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is required")
        data = _post_json(
            self.base_url,
            {"model": self.model, "instructions": instructions, "input": input_text},
            {"Authorization": f"Bearer {key}"}
        )
        return _extract_responses_text(data)


@dataclass
class GenericResponsesProvider:
    model: str
    base_url: str
    api_key: str | None = None

    def generate(self, instructions: str, input_text: str = "") -> str:
        headers: dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        data = _post_json(
            self.base_url,
            {"model": self.model, "instructions": instructions, "input": input_text},
            headers
        )
        return _extract_responses_text(data)


@dataclass
class OllamaProvider:
    model: str
    base_url: str = "http://localhost:11434"

    def generate(self, instructions: str, input_text: str = "") -> str:
        data = _post_json(
            f"{self.base_url.rstrip('/')}/api/chat",
            {
                "model": self.model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": input_text}
                ]
            }
        )
        try:
            return data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError("Ollama response did not contain message.content") from exc


def provider_from_name(name: str, model: str | None, base_url: str | None = None) -> Provider:
    if name == "mock":
        return MockProvider()
    if name == "openai":
        if not model:
            raise ValueError("--model is required for openai")
        return OpenAIResponsesProvider(model=model)
    if name == "responses":
        if not model or not base_url:
            raise ValueError("--model and --base-url are required for responses")
        return GenericResponsesProvider(model=model, base_url=base_url, api_key=os.getenv("EISF_API_KEY"))
    if name == "ollama":
        if not model:
            raise ValueError("--model is required for ollama")
        return OllamaProvider(model=model, base_url=base_url or "http://localhost:11434")
    raise ValueError(f"unknown provider: {name}")
