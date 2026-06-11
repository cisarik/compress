# NEXT_AGENT.md — PrimeSymbolicMDL Handoff

## Current Session Status

This session is closing.

- Latest verified tests: `267 passed`
- Analytic Programming and Coordinator Protocol infrastructure exists and is active
- Huge-anchor binary actual-size reranking exists
- `NEXT_AGENT.md` is now the active handoff file for the next Worker

## Project Mission

PrimeSymbolicMDL is an experimental lossless compression research harness.

The goal is exact lossless compression experiments under honest MDL accounting and, where implemented, honest actual byte accounting.

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

Current read-only RPC methods:

- `repo.status`
- `repo.diff_stat`
- `repo.list_files`
- `repo.get_file`

Strategic Orchestrator handoff lives in `NEXT_ORCHESTRATOR.md`.
This file remains the Worker-focused handoff.

## Compression Architecture Implemented

- fixed-width block packing
- huge-number block packing
- prime utilities with exact 64-bit prime support
- scaled prime-index branch
- huge anchor portfolio:
  - `linear_shift`
  - `affine_shift`
  - `multiple`
  - `square`
  - `scaled_prime`
- shared residual codec layer
- bitstream primitives
- residual binary serialization
- huge-anchor binary container
- actual-size reranking over top estimated huge-anchor candidates
- image branches:
  - `Image-predictor`
  - `Image-GP-lite`
  - `Image-SOMA`

## Current Hard Evidence

- `python -m pytest -q`
  - expected current result: `267 passed`
- `python -m primesymbolicmdl.huge_anchor_binary_demo`
  - works and reports actual bytes plus estimated-vs-actual divergence
- best synthetic actual compression currently demonstrated:
  - dataset: `square_generated`
  - width: `64-bit`
  - `raw_bytes: 256`
  - `compressed_bytes: 49`
  - `actual_saving_bytes: 207`
  - `roundtrip_ok: True`
- random-data sanity:
  - random data remains `raw_fallback`
- estimated-vs-actual warning:
  - `repeating_pattern` can look like an estimated win but still becomes actual fallback because of binary container overhead

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

Add a real file CLI for huge-anchor binary compression and decompression.

Why this is the right next step:

- the repo already has an in-memory huge-anchor binary demo
- the next practical step is a real file interface
- target commands:
  - `compress --input in.bin --output out.psmdl --width-bits 32`
  - `decompress --input out.psmdl --output restored.bin`
- the CLI must either store raw fallback safely or refuse compression when the binary blob is not smaller than raw
- the CLI must verify exact restore
- the CLI must have temp-file tests

## Alternative Next Steps

- add `repo.search` RPC
- add entropy coding or ANS later
- add more anchor families
- evaluate on small real corpora
- reduce container overhead

## Commands For Next Worker

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
python -m pytest -q
python -m primesymbolicmdl.huge_anchor_binary_demo
python -m primesymbolicmdl.huge_anchor_demo
fish scripts/ap_snapshot.fish --run-tests
```

## Required Report Format

- report starts with `### Report for ORCHESTRATOR_CHAT`
- include changed files
- include commands run
- include full test output
- include warnings
- include the suggested next step
