# NEXT_ORCHESTRATOR.md — Strategic Handoff

This file is the handoff for the **next Orchestrator**, not the Worker.

Worker immediate tasks live in `NEXT_AGENT.md`.

## Roles

- **COOPERATOR** — human strategic coordinator of intent, risk, and direction
- **ORCHESTRATOR** — task shaping, coherence, evaluation, handoff control
- **WORKER** — repo inspection, edits, tests, honest reporting

## Recommended Read Order

1. `NEXT_ORCHESTRATOR.md`
2. `NEXT_AGENT.md`
3. `NEXT_WORKER.md`
4. `BOOT.md`
5. `BRAIN.md` only when deeper context is needed

## Current Repo State

- `.psmdl` file CLI exists
- in-repo file benchmark exists
- external-corpus benchmark harness exists
- `PSMDLR2` compact raw fallback implemented
- legacy `PSMDLRAW1` decode still supported
- latest verified tests: **285 passed**

Future product direction (not implemented): Linux CLI working name `analytic`.

## Current Compression Evidence

External corpus (10 small files outside repo):

- raw total: **15720 B**
- psmdl total before `PSMDLR2`: **15800 B** (+80 B aggregate)
- psmdl total after `PSMDLR2`: **15773 B** (+53 B aggregate)
- raw-fallback overhead improved from about **+12 B** to about **+9 B** per small file
- compressed files: **1** (`zoneinfo-utc.bin`, 114 → 86 B)
- raw fallback files: **9**
- roundtrip failures: **0**

Honest interpretation:

- aggregate is still negative versus raw
- one tiny real file compressed
- text/SVG/PNG mostly raw fallback
- no general compressor claim is justified

Synthetic mechanism check remains valid: `square_generated_64` can compress under favorable structure.

## Scientific Guardrails

- exact roundtrip mandatory
- raw fallback is normal
- actual bytes beat estimated bits
- synthetic wins validate mechanism only
- no universal compression claims

## Strategic Next Direction

Do not jump to entropy coding yet.

Do not start broad new theory.

Next compression focus:

1. investigate whether the `zoneinfo-utc.bin` win generalizes to a small structured binary class (tzif / similar tiny binaries)
2. if it does not generalize, consider default policy / UX for future `analytic` CLI, such as `--require-compression` or no-write-on-loss behavior

## Orchestrator Operating Rules

- trust report, verify repo via SHA and diff when possible
- keep handoff files purpose-separated and free of pasted chat answers
- Worker reports must include `git rev-parse HEAD`
