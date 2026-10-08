export const SDK_VERSION = "0.1.0";
export const EISF_VERSION = "1.0.0-draft";

export type Confidence = "low" | "medium" | "high" | number;

export interface StageItem {
  statement: string;
  confidence?: Confidence;
  [key: string]: unknown;
}

export interface EISfDecision extends StageItem {
  status?: "decided" | "deferred";
}

export interface EISfCase {
  event: StageItem;
  impacts: StageItem[];
  scenarios: StageItem[];
  adaptations: StageItem[];
  decision: EISfDecision;
  provenance?: Record<string, unknown>;
  [key: string]: unknown;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

function validConfidence(value: unknown): boolean {
  if (typeof value === "number") return value >= 0 && value <= 1;
  return value === "low" || value === "medium" || value === "high";
}

function validateItem(value: unknown, path: string, errors: string[]): void {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    errors.push(`${path} must be an object`);
    return;
  }
  const item = value as Record<string, unknown>;
  if (typeof item.statement !== "string" || item.statement.trim().length === 0) {
    errors.push(`${path}.statement must be a non-empty string`);
  }
  if ("confidence" in item && !validConfidence(item.confidence)) {
    errors.push(`${path}.confidence must be low/medium/high or a number from 0 to 1`);
  }
}

export function validateCase(value: unknown): ValidationResult {
  const errors: string[] = [];
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    return { valid: false, errors: ["case must be a JSON object"] };
  }

  const data = value as Record<string, unknown>;
  for (const stage of ["event", "impacts", "scenarios", "adaptations", "decision"]) {
    if (!(stage in data)) errors.push(`missing required stage: ${stage}`);
  }

  if ("event" in data) validateItem(data.event, "event", errors);

  for (const stage of ["impacts", "scenarios", "adaptations"] as const) {
    if (!(stage in data)) continue;
    const items = data[stage];
    if (!Array.isArray(items) || items.length === 0) {
      errors.push(`${stage} must be a non-empty array`);
      continue;
    }
    items.forEach((item, index) => validateItem(item, `${stage}[${index}]`, errors));
  }

  if ("decision" in data) {
    validateItem(data.decision, "decision", errors);
    if (typeof data.decision === "object" && data.decision !== null && !Array.isArray(data.decision)) {
      const status = (data.decision as Record<string, unknown>).status;
      if (status !== undefined && status !== "decided" && status !== "deferred") {
        errors.push("decision.status must be 'decided' or 'deferred'");
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

export function buildPrompt(eventStatement: string, developer = false): string {
  const extra = developer
    ? "\nFor software-development work, consider architecture, APIs, data, security, compatibility, testing, deployment, rollback, operations, cost, and acceptance criteria."
    : "";

  return `Use the EISf Public Canon: Event → Impact → Scenario → Adaptation → Decision.

Analyze the following Event:
${eventStatement}
${extra}

Return ONLY one JSON object with event, impacts, scenarios, adaptations, and decision. Do not collapse scenarios into decisions.`;
}

export interface Provider {
  generate(instructions: string, inputText?: string): Promise<string>;
}

export class ResponsesProvider implements Provider {
  constructor(
    public model: string,
    public endpoint: string,
    public apiKey?: string
  ) {}

  async generate(instructions: string, inputText = ""): Promise<string> {
    const headers: Record<string, string> = { "content-type": "application/json" };
    if (this.apiKey) headers.authorization = `Bearer ${this.apiKey}`;

    const response = await fetch(this.endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify({ model: this.model, instructions, input: inputText })
    });
    if (!response.ok) throw new Error(`provider HTTP ${response.status}: ${await response.text()}`);

    const data = await response.json() as Record<string, unknown>;
    if (typeof data.output_text === "string") return data.output_text;

    const chunks: string[] = [];
    const output = Array.isArray(data.output) ? data.output : [];
    for (const item of output) {
      if (typeof item !== "object" || item === null) continue;
      const content = Array.isArray((item as Record<string, unknown>).content)
        ? (item as Record<string, unknown>).content as unknown[]
        : [];
      for (const part of content) {
        if (typeof part === "object" && part !== null) {
          const text = (part as Record<string, unknown>).text;
          if (typeof text === "string") chunks.push(text);
        }
      }
    }
    if (!chunks.length) throw new Error("provider response did not contain text output");
    return chunks.join("\n");
  }
}

export class OpenAIResponsesProvider extends ResponsesProvider {
  constructor(model: string, apiKey?: string) {
    super(model, "https://api.openai.com/v1/responses", apiKey ?? process.env.OPENAI_API_KEY);
  }
}

export class OllamaProvider implements Provider {
  constructor(public model: string, public baseUrl = "http://localhost:11434") {}

  async generate(instructions: string, inputText = ""): Promise<string> {
    const response = await fetch(`${this.baseUrl.replace(/\/$/, "")}/api/chat`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        model: this.model,
        stream: false,
        messages: [
          { role: "system", content: instructions },
          { role: "user", content: inputText }
        ]
      })
    });
    if (!response.ok) throw new Error(`Ollama HTTP ${response.status}: ${await response.text()}`);
    const data = await response.json() as { message?: { content?: string } };
    if (typeof data.message?.content !== "string") throw new Error("Ollama response missing message.content");
    return data.message.content;
  }
}
