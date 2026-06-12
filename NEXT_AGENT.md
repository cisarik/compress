# NEXT_AGENT.md — PrimeSymbolicMDL Worker Handoff

## Current Session Status

Documentation and AP handoff cleanup after the completed `.psmdl` CLI audit/benchmark step.

- Latest verified tests: `277 passed`
- `.psmdl` file CLI exists and is documented in `README.md`
- In-repo file benchmark exists: `src/primesymbolicmdl/huge_anchor_file_benchmark.py`
- `NEXT_ORCHESTRATOR.md` has been rewritten as a clean strategic handoff

## Project Mission

PrimeSymbolicMDL is an experimental lossless compression research harness.

The goal is exact lossless compression experiments under honest MDL accounting and honest actual byte accounting where implemented.

Do not make universal compression claims.

## Analytic Programming / Coordinator Protocol

Core roles:

- `COOPERATOR`
- `ORCHESTRATOR`
- `WORKER`

Important files:

- `AP.md`
- `AP_WORKER.md`
- `AP_ORCHESTRATOR.md`
- `AGENTS.md`
- `COORDINATOR_PROTOCOL.md`
- `BOOT.md`
- `BRAIN.md`
- `CHAT.md`
- `.ap/current_status.md`
- `.ap/last_report.md`

Strategic Orchestrator handoff lives in `NEXT_ORCHESTRATOR.md`.

This file remains the Worker-focused handoff.

## Current Known Benchmark Summary

In-repo deterministic benchmark (`huge_anchor_file_benchmark`):

| input | raw bytes | `.psmdl` bytes | outcome |
|-------|-----------|----------------|---------|
| random_bytes_128 | 128 | 140 | raw fallback |
| repeating_pattern | 128 | 140 | raw fallback |
| README.md | 11548 | 11560 | raw fallback |
| AGENTS.md | 9904 | 9916 | raw fallback |
| huge_anchor_file.py | 5182 | 5194 | raw fallback |
| square_generated_64 | 256 | 49 | synthetic huge-anchor win |

All cases roundtrip exactly.

`--require-compression` refuses raw-fallback cases and succeeds for `square_generated_64`.

## Hard Rules For Next Worker

- no git write commands unless explicitly permitted
- run tests after meaningful changes
- no network downloads
- no heavy dependencies
- no fake compression claims
- exact roundtrip is mandatory
- random-bytes sanity is required
- actual bytes are stronger evidence than estimated bits
- report starts with `### Report for ORCHESTRATOR_CHAT`

## Suggested Next Smallest Step

Create or extend a small **external-corpus benchmark harness** for actual `.psmdl` file sizes.

Why this is the right next step:

- the in-repo benchmark already validated CLI behavior on repo files and synthetic inputs
- the next honest step is a small corpus **outside** the repository tree
- use temporary files only; do not commit generated benchmark blobs
- report actual bytes, `decision`, `file_format`, and roundtrip status
- include random-byte sanity and at least a few small real external files supplied locally by the harness or documented temp inputs

Suggested shape:

- extend `huge_anchor_file_benchmark.py` or add a sibling such as `huge_anchor_external_benchmark.py`
- keep scope small: a handful of files, deterministic where possible
- add minimal tests only if a committed script is added

Do not introduce new compression algorithms in this step.

## Commands That Worked

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
.venv/bin/pytest -q
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_benchmark
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_cli compress --input in.bin --output out.psmdl --width-bits 32
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_cli decompress --input out.psmdl --output restored.bin
fish scripts/ap_snapshot.fish --run-tests
```

## Python Invocation Warning

In this environment:

- use `.venv/bin/pytest` for tests
- do not rely on `.venv/bin/python -m pytest`; it may resolve incorrectly through the Cursor appimage
- for module execution, prefer `PYTHONPATH=src /usr/bin/python3.14 -m ...`

## Required Report Format

- report starts with `### Report for ORCHESTRATOR_CHAT`
- include changed files
- include commands run
- include full test output
- include warnings
- include the suggested next step
