# PrimeSymbolicMDL

PrimeSymbolicMDL is an experimental research harness for lossless compression built around MDL-guided anchor-and-residual coding.

The current `v0` milestone is intentionally conservative:

- it is deterministic and exactly reversible
- it treats prime anchors as one candidate transform family
- it falls back to raw storage when the prime-anchor branch is not cheaper
- it does not yet include entropy coding
- it does not yet include symbolic regression

This repository is for honest measurement, not compression hype. A transform is only interesting if its full transmitted cost is lower than the fallback after counting metadata, model choices, and residuals.

## Current Components

- fixed-width block packing for 8, 16, 24, and 32 bit blocks
- prime anchor helpers
- simple experimental bit-cost accounting
- a reversible research payload for raw and prime-anchor branches
- a small deterministic evolutionary search over indexed anchor families
- a GP-lite indexed anchor law search over tiny expression trees
- a modular optimizer registry with GP-lite, SOMA, and honest placeholders
- a shared residual codec layer with fixed-width, zero-RLE, and byte-RLE research baselines
- an experimental huge-anchor binary bitstream container with exact byte-length measurement
- a `.psmdl` file CLI for huge-anchor compression and decompression
- a deterministic in-repo file benchmark for actual `.psmdl` byte sizes
- a small Tkinter research cockpit for grayscale image simulations
- pytest coverage for round-trip and random-data sanity checks

## GP-lite Indexed Anchor Law Search

The new GP-lite branch evolves decoder-known anchor laws `A(i)`.

- The encoder stores an index `i` plus a residual `x - A(i)`.
- The law is only useful if total transmitted bits beat raw fallback.
- This is different from a predictor-only model because the decoder reconstructs anchors from the transmitted index and the law tree.
- The current cost model uses fixed-width index accounting and a small residual codec selector baseline.
- Entropy coding, PySR, and heavier symbolic regression remain intentionally deferred.

## Scaled Prime-index Branch

The repository now also includes a scaled prime-index experiment over larger Python integer blocks.

- Bytes can be packed into big-endian Python integer blocks up to 128 bits for reversible block experiments.
- The current exact prime-anchor branch is intentionally limited to `width_bits <= 64`.
- The model tries `x = prev_prime(index << shift) + diff`.
- In this construction, `index` is smaller than the original block value and the decoder reconstructs the prime anchor from `index` and `shift`.
- The model only matters when the full transmitted cost of flags, indices, residual payload, escapes, headers, and model parameters beats raw storage.
- Arbitrary-size exact prime search is deferred. This branch does not fake primality above 64-bit integers.
- Random data is expected to often lose against raw storage, and that is an honest result.
- This branch currently ships as a CLI and testable module, not yet as a GUI-integrated optimizer.

## Huge Anchor Portfolio

The huge anchor portfolio generalizes the scaled prime-index branch into a broader family benchmark.

- Each family tests the same idea: `x = anchor(index, params) + diff`.
- `scaled_prime` is only one family inside that larger search space.
- Other current families include `linear_shift`, `affine_shift`, `multiple`, and `square`.
- If a simpler family beats `scaled_prime`, that is important evidence against prime-anchor special pleading.
- Synthetic wins are useful because they validate the exact-lossless mechanism and full accounting, not because they prove universal compression.
- Random-byte sanity remains mandatory.
- The real result only matters when total transmitted bits beat raw storage after counting model, parameter, header, flag, index, residual, and escape costs.

## Huge-anchor Binary Proof-of-concept

The repository now also includes a first real binary container for huge-anchor payloads.

- Earlier huge-anchor experiments used exact research payloads plus estimated bit accounting.
- The new container produces real `compressed_bytes` and therefore real `actual_bits = len(blob) * 8`.
- A synthetic win now means more than a promising estimate: the branch can emit a smaller exact-decodable blob for structure-compatible generated data.
- Random-byte sanity remains mandatory. If the binary container loses to raw bytes, that is the correct result.
- This is still not a universal file compressor. It is a narrow proof that one exact binary huge-anchor path can sometimes beat raw bytes on favorable synthetic data.

## Actual-size Reranking

Estimated MDL accounting remains the fast search heuristic, but it is no longer the final judge for the binary huge-anchor path.

- The search still finds promising candidates by estimated `total_bits`.
- The binary stage now serializes the top `N` estimated candidates and reranks them by real `compressed_bytes`.
- This makes container overhead visible instead of assumed away.
- An estimated win can still become `raw_fallback` after real byte serialization.
- Actual compressed bytes are the stronger evidence because they include headers, alignment, and real residual payload size.

## PSMDL File CLI

The repository includes a small file CLI for the huge-anchor binary path.

This is **not** a general-purpose compressor. It is a research file interface for exact-lossless experiments with honest actual-byte reporting.

Compress:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_cli compress --input in.bin --output out.psmdl --width-bits 32
```

Decompress:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_cli decompress --input out.psmdl --output restored.bin
```

Optional strict mode:

```fish
... --require-compression
```

If the huge-anchor blob is not smaller than the raw input, `--require-compression` refuses to write output.

### File formats

- `PSMDLHA1` = actual huge-anchor compressed payload
- `PSMDLRAW1` = raw fallback wrapper used when huge-anchor compression does not beat raw bytes

Default behavior stores a safe raw fallback when compression does not win. That keeps exact roundtrip, but the `.psmdl` file can be **larger** than the original input because of container overhead.

### In-repo benchmark summary

Deterministic benchmark command:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_benchmark
```

Current honest results from the in-repo set:

- random bytes: raw fallback
- repeating pattern: raw fallback
- small repo text/source files (`README.md`, `AGENTS.md`, Python source): raw fallback
- `square_generated_64`: synthetic actual win, `256 B -> 49 B`

Synthetic wins validate the exact mechanism only. They are not evidence of universal compression.

## Residual Codec Layer

Predictors and anchor laws both create a residual stream:

```text
x = predicted_or_anchor + residual
```

This repository now includes a small shared residual codec layer so different branches can compare against the same residual backend.

- `fixed_signed` is the deterministic fixed-width signed baseline.
- `zero_rle` is a deterministic zero-run-length baseline for residual streams with many zeros.
- `byte_rle` is a raw-like baseline for repeated pixel bytes.
- `raw_bytes` remains the honest fallback baseline for byte streams.

This is still not ANS or arithmetic coding. Entropy coding remains deferred. Exact roundtrip remains mandatory for any branch that claims decode support.

## Optimizer Architecture

The repository now exposes a small optimizer registry with seven visible choices:

- `GP-lite`: the existing tree-based indexed anchor-law search
- `SOMA`: a small continuous-parameter migration optimizer over affine and quadratic anchor laws
- `GP`: an honest placeholder for future richer topology search
- `ADAM`: an honest placeholder for future differentiable parameter tuning
- `Image-predictor`: a deterministic 2D grayscale predictor baseline with exact residual roundtrip
- `Image-GP-lite`: a deterministic expression-tree search over 2D pixel context
- `Image-SOMA`: a deterministic fixed-point linear search over 2D pixel context

All optimizers are judged by the same idea: the result only matters if `total_bits < raw_bits` after counting model, parameter, index, residual, flag, header, and escape costs.

## Image-aware Search Optimizers

The repository now separates a fair manual baseline from two image-aware search branches:

- `Image-predictor` is the manual baseline over small decoder-known 2D predictors.
- `Image-GP-lite` searches tiny expression trees over decoder-known pixel context.
- `Image-SOMA` tunes a fixed-point linear predictor over decoder-known pixel context.
- All three reuse the same shared residual codec layer.
- A result only matters if `total_bits < raw_bits`.
- Synthetic gradients, checkerboards, and ramps are useful for deterministic debugging, not as proof of universal compression.

## Image-GP-lite Primitive Ablations

`Image-GP-lite` can now be run with explicit primitive sets:

- `local` uses only decoder-known neighborhood context such as `left`, `up`, and `up_left`.
- `ramp` adds procedural coordinate ramps such as `x_ramp`, `y_ramp`, and `diag_ramp`.
- `structure` adds block/parity primitives intended for checker-like and piecewise structure baselines.

Important interpretation rules:

- `checker_parity` wins are valid only as explicit primitive baselines, not as evidence that the search discovered a universal image law.
- Ablation reports must include the primitive set name or they are not comparable.
- Synthetic wins still need the same `total_bits < raw_bits` accounting rule as every other branch.

## GUI Research Cockpit

The first GUI is a stdlib Tkinter cockpit focused on generated grayscale image simulations.

- It lets you choose an optimizer and a tiny image dataset.
- It reports raw size in bits and estimated transmitted size in bits.
- It can also report which residual codec or raw-byte baseline won under the current accounting.
- It is a research UI, not a final file compressor.
- Estimated bit accounting now includes a small residual codec selector, but entropy coding is still deferred.

## Analytic Coding Snapshots

Use the fish snapshot helper to generate an agent-readable repository state:

```fish
fish scripts/ap_snapshot.fish
fish scripts/ap_snapshot.fish --run-tests
```

This generates:

- `BRAIN.md`
- `BOOT.md`

These files are intended for orchestration and repository-state handoff, not as proof of compression quality.

## Analytic Programming / Analytic Coding

Recommended interactive fish workflow:

```fish
source .venv/bin/activate.fish
```

Core AP commands:

```fish
fish scripts/ap_snapshot.fish --run-tests
fish scripts/ap_chat_append.fish --role worker --message "..." --tldr "..."
fish scripts/ap_cycle_close.fish --message "..." --tldr "..."
```

AP artifact roles:

- `AP.md`, `AP_WORKER.md`, and `AP_ORCHESTRATOR.md` are living, repo-visible protocol and doctrine artifacts that may evolve through explicit AP/meta tasks.
- `AP.md` is the system-wide protocol.
- `COORDINATOR_PROTOCOL.md` extends AP with file-based RPC.
- `AP_ORCHESTRATOR.md` explains the orchestrator-side discipline.
- `AP_WORKER.md` is the Worker doctrine.
- `NEXT_ORCHESTRATOR.md` is the strategic handoff for the next Orchestrator.
- `BRAIN.md` and `BOOT.md` are generated repository snapshots.

## Coordinator Protocol

Coordinator Protocol is a file-based, repo-centered RPC proof of concept for `COOPERATOR`, `ORCHESTRATOR`, and `WORKER`.

- The repository remains the source of truth.
- `BRAIN.md` and `BOOT.md` remain broad snapshots.
- `CHAT.md` remains the append-only coordination ledger.
- RPC is the narrow lane for targeted status and file requests.
- This means the Orchestrator does not always need the whole diff when it only needs one file or one status view.
- The Orchestrator should request exact repo information via RPC instead of guessing from partial context.
- The default RPC surface is read-only and preserves the same safety model: no secrets access, no network dependency, and no git write commands.
- A continuation session should ideally start with `NEXT_ORCHESTRATOR.md` and `NEXT_AGENT.md`.

RPC commands:

```fish
fish scripts/ap_rpc_call.fish --method repo.status
fish scripts/ap_rpc_call.fish --method repo.get_file --path AP.md
fish scripts/ap_rpc_request.fish --method repo.get_file --path src/primesymbolicmdl/simulation.py
fish scripts/ap_rpc_handle_next.fish
```

Scaled-prime demo command:

```bash
python -m primesymbolicmdl.scaled_prime_demo
```

Huge-anchor portfolio demo command:

```bash
python -m primesymbolicmdl.huge_anchor_demo
```

Huge-anchor binary demo command:

```bash
python -m primesymbolicmdl.huge_anchor_binary_demo
```

## Run Tests

```bash
python -m pytest -q
```

## Run Demos

```bash
python -m primesymbolicmdl.sim_demo
python -m primesymbolicmdl.gui
```

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -U pip
python -m pip install -e ".[dev]"
python -m pytest -q
```

## Status

This version does not yet implement:

- entropy coding
- heavy symbolic regression search
- external benchmark corpora integration
- entropy-backed general-purpose file compression
