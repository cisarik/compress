# NEXT_ORCHESTRATOR.md — Strategic Handoff

This file is the handoff for the **next Orchestrator**, not the Worker.

The Worker should read `NEXT_AGENT.md` instead.

## Recommended Read Order

1. `NEXT_ORCHESTRATOR.md`
2. `NEXT_AGENT.md`
3. `BOOT.md`
4. `.ap/current_status.md`
5. `.ap/last_report.md`
6. `BRAIN.md` only when deeper context is needed

## Big Picture

PrimeSymbolicMDL is an experimental lossless compression research harness.

The project tests anchor-and-residual transforms under honest MDL accounting and, where implemented, honest actual byte accounting.

Prime anchors are one candidate anchor family, not a privileged truth.

The repository is benchmark-driven, deterministic, and exactly reversible.

## Analytic Programming / Coordinator Protocol

AP is active in this repository.

Core roles:

- `COOPERATOR` (user)
- `ORCHESTRATOR`
- `WORKER`

Important protocol files:

- `AP.md`
- `AP_ORCHESTRATOR.md`
- `AP_WORKER.md`
- `AGENTS.md`
- `COORDINATOR_PROTOCOL.md`

Important handoff and snapshot files:

- `NEXT_ORCHESTRATOR.md` = strategic Orchestrator handoff
- `NEXT_AGENT.md` = immediate Worker handoff
- `BOOT.md` = short generated boot summary
- `BRAIN.md` = detailed generated repository snapshot
- `CHAT.md` = append-only coordination ledger

Current read-only RPC methods:

- `repo.status`
- `repo.diff_stat`
- `repo.list_files`
- `repo.get_file`

The repository remains the source of truth.

Chat and snapshots are supporting artifacts, not proof of compression performance.

## What Has Been Solved So Far

- deterministic baseline and bit accounting
- prime-anchor and indexed anchor-law branches
- huge-anchor portfolio across multiple families
- shared residual codec layer
- huge-anchor binary container with actual-size reranking
- `.psmdl` file CLI for huge-anchor compression and decompression
- deterministic in-repo file benchmark for actual `.psmdl` byte sizes
- AP / Coordinator Protocol infrastructure
- GUI research cockpit for small grayscale simulations
- pytest coverage for roundtrip and random-data sanity

## Current Compression Evidence

Latest verified tests:

- `277 passed`

File path exists:

- `src/primesymbolicmdl/huge_anchor_file.py`
- `src/primesymbolicmdl/huge_anchor_file_cli.py`
- `src/primesymbolicmdl/huge_anchor_file_benchmark.py`

Benchmark summary from the in-repo deterministic file benchmark:

| input | raw bytes | `.psmdl` bytes | outcome |
|-------|-----------|----------------|---------|
| random_bytes_128 | 128 | 140 | raw fallback |
| repeating_pattern | 128 | 140 | raw fallback |
| README.md | 11548 | 11560 | raw fallback |
| AGENTS.md | 9904 | 9916 | raw fallback |
| huge_anchor_file.py | 5182 | 5194 | raw fallback |
| square_generated_64 | 256 | 49 | synthetic huge-anchor win |

Interpretation:

- exact roundtrip verified for all benchmark cases
- random bytes remained raw fallback
- small real repo files remained raw fallback
- `square_generated_64` is a synthetic mechanism check, not general compression proof
- `--require-compression` refuses raw-fallback cases and succeeds for the synthetic compressed case

## Scientific Guardrails

- exact roundtrip is mandatory
- raw fallback is normal and often expected
- actual bytes are stronger evidence than estimated bits
- random-byte sanity is required
- synthetic wins validate mechanism only
- do not claim universal compression without established corpora and full cost accounting
- generated snapshots are not proof of compression quality

## Current Risks

- no entropy coder exists yet
- the small in-repo benchmark does not compress real text/source files
- raw fallback has container overhead and can make `.psmdl` larger than raw input
- benchmark runtime is around 90–115 seconds for the current in-repo set
- public documentation must stay non-hype
- estimated wins can still diverge from actual serialized bytes because of container overhead
- exact prime support remains limited to the 64-bit line in the scaled-prime branch

## Recommended Next Strategy

Do not start with another large theory cycle.

Recommended order:

1. keep public documentation aligned with actual CLI behavior
2. build a small honest external-corpus benchmark harness for actual `.psmdl` file sizes
3. only then consider container overhead reduction or entropy coding

The next Worker task should stay bounded:

- external corpus benchmark only
- no new algorithms unless required for reporting
- report actual bytes, decisions, and roundtrip status honestly

## What The Next Orchestrator Must Not Do

- must not claim universal compression
- must not treat synthetic wins as broad proof
- must not skip tests
- must not give the Worker a large mixed-scope task
- must not prioritize entropy coding before honest external benchmarking unless strategy explicitly changes
- must not let stale handoff files replace current repository state

## Closing Note

When a serious AP session ends, update both:

- `NEXT_ORCHESTRATOR.md` for strategic continuation
- `NEXT_AGENT.md` for the next Worker task

Keep one dominant purpose per artifact.
