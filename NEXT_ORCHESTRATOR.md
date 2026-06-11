# NEXT_ORCHESTRATOR.md — PrimeSymbolicMDL Orchestrator Handoff

## How To Use This File

This file is the handoff for the next Orchestrator, not the next Worker.

Recommended read order for the next Orchestrator:

1. read this file first
2. read `NEXT_AGENT.md`
3. verify quick state in `BOOT.md`
4. pull deeper context from `BRAIN.md`, `CHAT.md`, `.ap/current_status.md`, and `.ap/last_report.md` as needed

Use this file to recover strategy and continuity without rereading the whole session transcript.

## Current Big Picture

PrimeSymbolicMDL is an experimental lossless compression research harness.

The practical goal is to progress from estimated and in-memory demonstrations toward a real exact compressed file workflow.

Important constraints:

- no universal compression claims
- repository is the source of truth
- exact roundtrip is mandatory
- measured actual bytes matter more than estimated bit heuristics once a binary path exists

## Analytic Programming / Coordinator Protocol State

- `COOPERATOR` = Michal
- `ORCHESTRATOR` = strategic planner and evaluator
- `WORKER` = coding and validation agent
- repository = source of truth
- RPC = targeted repository-backed queries instead of guessing

Important artifacts:

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
- `NEXT_AGENT.md`
- `NEXT_ORCHESTRATOR.md`

Current read-only RPC proof-of-concept methods:

- `repo.status`
- `repo.diff_stat`
- `repo.list_files`
- `repo.get_file`

## What Was Solved In This Session

Chronological high-level summary:

- Analytic Programming snapshot protocol was established around `BRAIN.md`, `BOOT.md`, `CHAT.md`, and `.ap/*`.
- AP chat and cycle scripts were added so the repo can refresh state and append machine-readable session history.
- Coordinator Protocol read-only RPC proof-of-concept was added for targeted repository inspection.
- The repository already contained image-aware optimizer lines and these remain part of the broader research harness.
- The scaled prime-index branch was added around exact 64-bit prime support and index-plus-diff accounting.
- The huge-anchor portfolio generalized that line into multiple anchor families.
- A real binary container for huge-anchor payloads was added.
- Actual-size reranking was added so top estimated candidates are serialized and judged by real `compressed_bytes`.

## Compression Research State

- `huge_blocks.py`
  - reversible packing of larger integer blocks
- `prime_bigint.py`
  - prime utilities, with exact current support effectively bounded to the 64-bit line
- `scaled_prime_index.py`
  - scaled prime index construction logic
- `scaled_prime_search.py`
  - search over scaled prime-index candidates
- `huge_anchor_models.py`
  - model families and deterministic anchor reconstruction
- `huge_anchor_branch.py`
  - exact research payload branch and MDL-style accounting
- `huge_anchor_search.py`
  - estimated candidate search over the huge-anchor portfolio
- `huge_anchor_datasets.py`
  - deterministic synthetic and sanity datasets
- `bitstream.py`
  - deterministic bitstream primitives, varints, zigzag helpers
- `residual_binary.py`
  - exact residual binary serialization
- `huge_anchor_binary.py`
  - actual binary container plus actual-size reranking
- `huge_anchor_binary_demo.py`
  - actual byte demo over deterministic datasets

## Current Hard Evidence

- expected tests after last verification: `267 passed`
- best synthetic actual compression currently demonstrated:
  - dataset: `square_generated`
  - width: `64-bit`
  - `raw_bytes: 256`
  - `compressed_bytes: 49`
  - `actual_saving_bytes: 207`
  - `roundtrip_ok: True`
- random data:
  - random bytes remain `raw_fallback`
- estimated vs actual:
  - `repeating_pattern` can look like an estimated win but still becomes actual fallback because of container overhead

## Scientific Guardrails

- synthetic wins are not general compression proof
- exact roundtrip is mandatory
- random-data sanity is required
- raw fallback is normal
- actual bytes are stronger evidence than estimated bits
- prime anchors are one family, not privileged truth
- huge-number ideas must compete honestly under full accounting
- no hype

## Current Risks

- container overhead is still large
- no entropy coder exists yet
- search is still synthetic-heavy
- exact prime support is limited to the 64-bit line
- no real file CLI exists yet
- the worktree may contain many uncommitted changes
- `BRAIN.md` can become large
- RPC methods are still minimal

## Recommended Next Orchestrator Strategy

Do not start with another big theory cycle.

Recommended order:

1. practicalize the current huge-anchor binary path with a real file CLI
2. benchmark that CLI on small real files
3. only then spend effort on overhead reduction, entropy coding, or new anchor families

The next CLI target should be:

- `compress --input in.bin --output out.psmdl --width-bits 32`
- `decompress --input out.psmdl --output restored.bin`

CLI requirements:

- use existing `compress_best_huge_anchor_binary`
- write the blob only when it makes sense or clearly mark raw fallback behavior
- verify exact restore
- include temp-file tests

## Next Worker Prompt Direction

Draft outline for the next Worker task:

- task type: compression practicalization
- goal: file CLI for huge-anchor binary compression and decompression
- forbidden: git write commands, new algorithms, heavy dependencies
- tests: pytest plus CLI roundtrip temp-file tests
- acceptance: real `.psmdl` file support, exact restored bytes, honest raw fallback handling

## What The Next Orchestrator Must Not Do

- must not claim universal compression
- must not ignore actual bytes in favor of estimated bits
- must not skip tests
- must not give the Worker a large mixed-scope task
- must not prioritize entropy coding before file CLI unless strategy explicitly changes
- must not forget random-data sanity

## Useful Commands

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
python -m pytest -q
python -m primesymbolicmdl.huge_anchor_binary_demo
python -m primesymbolicmdl.huge_anchor_demo
fish scripts/ap_snapshot.fish --run-tests
fish scripts/ap_rpc_call.fish --method repo.status
fish scripts/ap_rpc_call.fish --method repo.get_file --path NEXT_AGENT.md --max-bytes 20000
fish scripts/ap_rpc_call.fish --method repo.get_file --path NEXT_ORCHESTRATOR.md --max-bytes 30000
```

## Suggested First Message For Next Orchestrator

Read `NEXT_ORCHESTRATOR.md` first, then `NEXT_AGENT.md`, verify the tests still pass, and prepare a bounded Worker prompt for the huge-anchor binary file CLI with exact roundtrip and temp-file coverage.
