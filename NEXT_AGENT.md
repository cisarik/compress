# NEXT_AGENT.md — Worker Handoff

## Current Task Status

Handoff files cleaned. **PSMDLRAW overhead reduction implemented** (`PSMDLR2` compact raw fallback).

- tests: `285 passed`
- external corpus after fix: **15720 → 15773 B** (+53 B aggregate, +9 B per raw fallback file)
- legacy `PSMDLRAW1` decode still supported

## Project Mission

PrimeSymbolicMDL is an experimental lossless compression research harness with honest actual-byte accounting.

## Latest Evidence

External corpus benchmark (10 files outside repo):

| outcome | count |
|---------|-------|
| raw fallback (+12 B under PSMDLRAW1) | 9 |
| compressed (`zoneinfo-utc.bin`) | 1 |
| roundtrip failures | 0 |

Aggregate before overhead fix: **15720 → 15800 B** (+80 B).

Aggregate after `PSMDLR2`: **15720 → 15773 B** (+53 B).

## Hard Rules

- no git write unless explicitly permitted
- exact roundtrip mandatory
- actual bytes over estimated bits
- no universal compression claims
- report starts with `### Report for ORCHESTRATOR_CHAT`
- include `git rev-parse HEAD` in reports

## Commands That Work

```fish
cd /home/agile/compress
.venv/bin/pytest -q
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_corpus_benchmark --input-dir /path/to/corpus
```

Use `.venv/bin/pytest`, not `.venv/bin/python -m pytest` (Cursor appimage issue).

## Suggested Next Step

Overhead reduction helped but aggregate external corpus is still larger than raw (+53 B).

Choose one bounded direction:

1. further container overhead reduction for non-compressing files, or
2. a narrowly scoped anchor/residual experiment only if a specific file class shows promise

Do not start entropy coding or broad algorithm work without stronger actual-byte evidence.
