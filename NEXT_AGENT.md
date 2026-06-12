# NEXT_AGENT.md — Worker Handoff

## Current Status

Latest verified tests: **285 passed**

Implemented and verified in repo:

- `.psmdl` file CLI
- deterministic in-repo file benchmark
- external-corpus benchmark harness
- `PSMDLR2` compact raw fallback
- legacy `PSMDLRAW1` decode still supported

## Current Actual-Byte Evidence

External corpus (10 small files outside repo):

| metric | value |
|--------|-------|
| raw total | 15720 B |
| psmdl total before `PSMDLR2` | 15800 B (+80 B) |
| psmdl total after `PSMDLR2` | 15773 B (+53 B) |
| compressed files | 1 (`zoneinfo-utc.bin`, 114 → 86 B) |
| raw fallback files | 9 |
| roundtrip failures | 0 |

Interpretation:

- aggregate is **still worse than raw**
- random/text/SVG/PNG examples mostly raw fallback
- `PSMDLR2` reduced per-file raw-fallback overhead from about **+12 B** to about **+9 B**
- only `zoneinfo-utc.bin` compressed in the small external corpus
- this is not evidence of a general-purpose compressor

## Hard Rules

- exact roundtrip mandatory
- actual bytes over estimated bits
- no universal compression claims
- no git write commands unless explicitly permitted
- report starts with `### Report for ORCHESTRATOR_CHAT`
- include `git rev-parse HEAD` in reports

## Commands That Work

```fish
cd /home/agile/compress
.venv/bin/pytest -q
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_corpus_benchmark --input-dir /path/to/corpus
```

Use `.venv/bin/pytest`, not `.venv/bin/python -m pytest` (Cursor appimage issue).

## Suggested Next Smallest Step

Return to compression work.

Investigate one narrow actual-byte compression opportunity from the external corpus, starting with the tiny zoneinfo/tzif win and nearby structured small binary files, **without changing algorithms yet** unless the evidence supports a tiny bounded experiment.

Goal:

- understand why `zoneinfo-utc.bin` won
- determine whether that is a repeatable data-class signal or only a one-off tiny-file artifact

Do not reopen the external-corpus harness task; it is complete.

Do not start entropy coding or broad new theory without stronger actual-byte evidence.
