import test from "node:test";
import assert from "node:assert/strict";

import { buildPrompt, validateCase } from "../src/index.js";

function validCase() {
  return {
    event: { statement: "A change occurred." },
    impacts: [{ statement: "A system is affected." }],
    scenarios: [{ statement: "A plausible branch exists." }],
    adaptations: [{ statement: "A mitigation is available." }],
    decision: { statement: "Proceed with review.", status: "decided" }
  };
}

test("valid core case passes", () => {
  assert.equal(validateCase(validCase()).valid, true);
});

test("missing decision fails", () => {
  const value = validCase() as Record<string, unknown>;
  delete value.decision;
  assert.equal(validateCase(value).valid, false);
});

test("invalid confidence fails", () => {
  const value = validCase();
  value.event = { statement: "A change occurred.", confidence: 2 } as typeof value.event;
  assert.equal(validateCase(value).valid, false);
});

test("developer prompt includes engineering concerns", () => {
  const prompt = buildPrompt("Feature request", true);
  assert.match(prompt, /security/);
  assert.match(prompt, /rollback/);
});
