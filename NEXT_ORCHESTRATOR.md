Toto `NEXT_ORCHESTRATOR.md` je **dobré**, ale po poslednom Worker reporte je už **čiastočne zastarané**.

Najdôležitejšie rozpory oproti aktuálnemu stavu:

### Čo je už neaktuálne

1. **`expected tests after last verification: 267 passed`**

   * po novom reporte má byť **`276 passed`**

2. **`no real file CLI exists yet`**

   * to už **neplatí**
   * Worker už implementoval:

     * `src/primesymbolicmdl/huge_anchor_file.py`
     * `src/primesymbolicmdl/huge_anchor_file_cli.py`
     * `tests/test_huge_anchor_file_cli.py`

3. **Recommended Next Orchestrator Strategy**

   * krok „practicalize ... with a real file CLI“ je už splnený
   * ďalší krok má byť skôr:

     * **audit + benchmark CLI na malých reálnych súboroch**
     * potom až overhead reduction / entropy coding

4. **Suggested First Message For Next Orchestrator**

   * už nemá smerovať na implementáciu CLI
   * má smerovať na **vyhodnotenie CLI a benchmark**

---

Nižšie ti dávam **upravenú verziu**, ktorú by som teraz považovala za správny nový obsah `NEXT_ORCHESTRATOR.md`.

---

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

* no universal compression claims
* repository is the source of truth
* exact roundtrip is mandatory
* measured actual bytes matter more than estimated bit heuristics once a binary path exists

## Analytic Programming / Coordinator Protocol State

* `COOPERATOR` = Michal
* `ORCHESTRATOR` = strategic planner and evaluator
* `WORKER` = coding and validation agent
* repository = source of truth
* RPC = targeted repository-backed queries instead of guessing

Important artifacts:

* `AP.md`
* `AP_WORKER.md`
* `AP_ORCHESTRATOR.md`
* `AGENTS.md`
* `COORDINATOR_PROTOCOL.md`
* `BOOT.md`
* `BRAIN.md`
* `CHAT.md`
* `.ap/current_status.md`
* `.ap/last_report.md`
* `NEXT_AGENT.md`
* `NEXT_ORCHESTRATOR.md`

Current read-only RPC proof-of-concept methods:

* `repo.status`
* `repo.diff_stat`
* `repo.list_files`
* `repo.get_file`

## What Was Solved In This Session

Chronological high-level summary:

* Analytic Programming snapshot protocol was established around `BRAIN.md`, `BOOT.md`, `CHAT.md`, and `.ap/*`.
* AP chat and cycle scripts were added so the repo can refresh state and append machine-readable session history.
* Coordinator Protocol read-only RPC proof-of-concept was added for targeted repository inspection.
* The repository already contained image-aware optimizer lines and these remain part of the broader research harness.
* The scaled prime-index branch was added around exact 64-bit prime support and index-plus-diff accounting.
* The huge-anchor portfolio generalized that line into multiple anchor families.
* A real binary container for huge-anchor payloads was added.
* Actual-size reranking was added so top estimated candidates are serialized and judged by real `compressed_bytes`.
* A real file-based `.psmdl` workflow was added for huge-anchor binary compression and decompression.
* The file CLI now supports both:

  * `PSMDLHA1` — huge-anchor compressed payload
  * `PSMDLRAW1` — safe raw fallback payload
* CLI temp-file coverage was added with 9 tests.

## Compression Research State

* `huge_blocks.py`

  * reversible packing of larger integer blocks
* `prime_bigint.py`

  * prime utilities, with exact current support effectively bounded to the 64-bit line
* `scaled_prime_index.py`

  * scaled prime index construction logic
* `scaled_prime_search.py`

  * search over scaled prime-index candidates
* `huge_anchor_models.py`

  * model families and deterministic anchor reconstruction
* `huge_anchor_branch.py`

  * exact research payload branch and MDL-style accounting
* `huge_anchor_search.py`

  * estimated candidate search over the huge-anchor portfolio
* `huge_anchor_datasets.py`

  * deterministic synthetic and sanity datasets
* `bitstream.py`

  * deterministic bitstream primitives, varints, zigzag helpers
* `residual_binary.py`

  * exact residual binary serialization
* `huge_anchor_binary.py`

  * actual binary container plus actual-size reranking
* `huge_anchor_binary_demo.py`

  * actual byte demo over deterministic datasets
* `huge_anchor_file.py`

  * `.psmdl` file format handling
* `huge_anchor_file_cli.py`

  * file CLI for `compress` / `decompress`

## Current Hard Evidence

* expected tests after last verification: `276 passed`
* best synthetic actual compression currently demonstrated:

  * dataset: `square_generated`
  * width: `64-bit`
  * `raw_bytes: 256`
  * `compressed_bytes: 49`
  * `actual_saving_bytes: 207`
  * `roundtrip_ok: True`
* random data:

  * random bytes remain `raw_fallback`
* estimated vs actual:

  * `repeating_pattern` can look like an estimated win but still becomes actual fallback because of container overhead
* file CLI:

  * exact roundtrip is verified before writing output
  * default behavior allows safe raw fallback
  * `--require-compression` refuses output creation when compression does not beat raw size

## Scientific Guardrails

* synthetic wins are not general compression proof
* exact roundtrip is mandatory
* random-data sanity is required
* raw fallback is normal
* actual bytes are stronger evidence than estimated bits
* prime anchors are one family, not privileged truth
* huge-number ideas must compete honestly under full accounting
* no hype

## Current Risks

* container overhead is still large
* no entropy coder exists yet
* search is still synthetic-heavy
* exact prime support is limited to the 64-bit line
* raw fallback still has small container overhead
* CLI has been implemented, but practical real-file benchmarking is still missing
* the worktree may contain many uncommitted changes
* `BRAIN.md` can become large
* RPC methods are still minimal

## Recommended Next Orchestrator Strategy

Do not start with another big theory cycle.

Recommended order:

1. audit and benchmark the new file CLI on small real files and deterministic sanity inputs
2. confirm honest actual-size behavior, raw fallback behavior, and exact roundtrip
3. only then spend effort on overhead reduction, entropy coding, or new anchor families

The next practical validation target should include:

* `compress --input in.bin --output out.psmdl --width-bits 32`
* `decompress --input out.psmdl --output restored.bin`

Benchmark expectations:

* random bytes should normally end as raw fallback
* repetitive/synthetic data may show actual wins
* small real text/source files should be measured honestly by actual output size
* the benchmark must explicitly distinguish:

  * raw input bytes
  * `.psmdl` output bytes
  * whether huge-anchor compression or raw fallback was used
  * whether `--require-compression` succeeds or fails

## Next Worker Prompt Direction

Draft outline for the next Worker task:

* task type: compression practicalization / validation
* goal: audit and benchmark the new `.psmdl` CLI on small real files and deterministic sanity inputs
* forbidden: git write commands, new algorithms, heavy dependencies
* tests: full pytest plus temp-file/CLI validation
* acceptance:

  * exact restored bytes
  * honest raw fallback handling
  * actual-size benchmark table
  * clear note of `--require-compression` behavior

Optional bounded addition:

* a small repeatable benchmark/demo script for the file CLI, only if it keeps scope small and honest

## What The Next Orchestrator Must Not Do

* must not claim universal compression
* must not ignore actual bytes in favor of estimated bits
* must not skip tests
* must not give the Worker a large mixed-scope task
* must not prioritize entropy coding before CLI benchmarking unless strategy explicitly changes
* must not forget random-data sanity

## Useful Commands

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
.venv/bin/pytest -q
python -m primesymbolicmdl.huge_anchor_binary_demo
python -m primesymbolicmdl.huge_anchor_demo
python -m primesymbolicmdl.huge_anchor_file_cli compress --input in.bin --output out.psmdl --width-bits 32
python -m primesymbolicmdl.huge_anchor_file_cli decompress --input out.psmdl --output restored.bin
fish scripts/ap_snapshot.fish --run-tests
fish scripts/ap_rpc_call.fish --method repo.status
fish scripts/ap_rpc_call.fish --method repo.get_file --path NEXT_AGENT.md --max-bytes 20000
fish scripts/ap_rpc_call.fish --method repo.get_file --path NEXT_ORCHESTRATOR.md --max-bytes 30000
```

## Suggested First Message For Next Orchestrator

Read `NEXT_ORCHESTRATOR.md` first, then `NEXT_AGENT.md`, verify the tests still pass, and prepare a bounded Worker prompt for auditing and benchmarking the huge-anchor `.psmdl` file CLI with exact roundtrip, raw-fallback validation, and actual-size reporting.

---

Ak chceš, v ďalšej odpovedi ti môžem pripraviť aj **nový aktualizovaný `NEXT_AGENT.md`**, aby bol zosúladený s týmto novým stavom po implementácii CLI.
