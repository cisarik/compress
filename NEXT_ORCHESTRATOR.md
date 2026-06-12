# NEXT_ORCHESTRATOR.md — Strategic Handoff

This file is the handoff for the **next Orchestrator**, not the Worker.

## Recommended Read Order

1. `NEXT_ORCHESTRATOR.md`
2. `NEXT_AGENT.md` / `NEXT_WORKER.md`
3. `BOOT.md`
4. `BRAIN.md` only when deeper context is needed

## Current Phase

Compression practicalization. AP/meta is sufficient for this phase unless a blocking inconsistency appears.

Future product direction (not implemented): Linux CLI tool working name `analytic`.

## Verified Repo State

- `.psmdl` file CLI exists
- in-repo file benchmark exists
- external-corpus benchmark harness exists
- latest Worker target tests: `283 passed` before PSMDLRAW overhead work
- public commit verification loop: trust report, verify repo via SHA and diff

## Compression Evidence

External corpus (10 small files outside repo):

- 9/10 raw fallback with ~+12 B `PSMDLRAW1` overhead per file
- 1/10 compressed: `zoneinfo-utc.bin` 114 → 86 B (tiny structured file only)
- aggregate: 15720 → 15800 B (+80 B)
- exact roundtrip everywhere

Synthetic mechanism check still valid: `square_generated_64` can compress.

## Scientific Guardrails

- exact roundtrip mandatory
- raw fallback is normal
- actual bytes beat estimated bits
- no universal compression claims
- synthetic wins validate mechanism only

## Current Worker Direction

**PSMDLRAW overhead reduction** — reduce systematic raw-fallback container penalty before new anchor families or entropy coding.

## Recommended Strategy After Overhead Work

1. re-run the same 10-file external corpus and compare aggregate delta
2. only then consider narrow algorithm experiments or entropy coding

## Orchestrator Rules

- verify Worker reports against repo SHA and diff when possible
- keep `NEXT_AGENT.md` Worker-focused and `NEXT_ORCHESTRATOR.md` strategic
- do not let chat-style answers replace handoff files
