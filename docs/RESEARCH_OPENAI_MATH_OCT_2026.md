# External mathematics research intake — October 2026 (experimental)

**Origin:** [OpenAI Math](https://github.com/openai/math) — public research released October 6, 2026.  
**Boundary:** Public SDK interoperability/research tooling only. **No** proprietary JANUS EISf metrics, internal logic, model router, B-level implementation, or client information in this branch.

## Source status (reviewed October 15, 2026)

OpenAI's repository currently catalogs **719 manuscripts across 372 result families**; **300 top-line results have associated formalizations (~42%)**. The October 7 upstream history records **3 withdrawn manuscripts** and **14 repaired manuscripts**. These are OpenAI's claims and bookkeeping, not proof verification by Beesmash or independent expert endorsement.

The repository is licensed under Apache-2.0. Preserve its LICENSE and manuscript-specific citations. Do **not** copy the nearly 0.8 GiB research corpus into this public SDK or source-control client data.

## Acquisition

From this repository root on a networked development machine:

```bash
bash tools/openai_math_fetch.sh
python3 tools/openai_math_catalog.py .research/openai-math .research/openai-math-catalog.json
```

The first command acquires **all current files** in the upstream repository, including PDFs and Lean files; the second writes a metadata-only candidate family catalog with a pinned upstream SHA. The first command is intentionally resource intensive. Generated files stay outside version control (use the `.research/` directory).

## JANUS evidence gates

1. Event: source publication / revision / withdrawal.
2. Impact: candidate effect on computational complexity, probability, controls, logic and proof tooling.
3. Scenario: validation succeeds, fails or remains unresolved.
4. Adaptation: reproduce algorithms in an isolated harness, compare against existing baselines, quarantine retracted results.
5. Decision: only independently reviewed and tested work can enter controlled experimental integration; no auto-promotion to production.

**Every record must be treated as a research claim.** Even presence of a Lean formalization is **not** proof that this branch has compiled or validated it. Do not execute arbitrary source files from the upstream repository.

Private JANUS integration (KRONOS, internal routing, private equations, model B-level decisions) belongs in its separate private repository and is intentionally not implemented here.

Sources: https://github.com/openai/math | https://github.com/openai/math/blob/main/history.md | https://github.com/openai/math/blob/main/lean/formalization.yaml
