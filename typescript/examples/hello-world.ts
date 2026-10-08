import { validateCase } from "../src/index.js";

const caseObject = {
  event: { statement: "Hello, world: a developer is evaluating EISf." },
  impacts: [{ statement: "The developer can inspect a structured reasoning case." }],
  scenarios: [{ statement: "The SDK can be integrated into a larger application." }],
  adaptations: [{ statement: "Run validation and conformance before claiming compatibility." }],
  decision: { statement: "Proceed with a small integration test.", status: "decided" as const }
};

const result = validateCase(caseObject);

if (!result.valid) {
  console.error(result.errors);
  process.exit(1);
}

console.log("EISf hello world");
console.log(JSON.stringify(caseObject, null, 2));
