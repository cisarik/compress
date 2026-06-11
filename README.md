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
- a small Tkinter research cockpit for grayscale image simulations
- pytest coverage for round-trip and random-data sanity checks

## GP-lite Indexed Anchor Law Search

The new GP-lite branch evolves decoder-known anchor laws `A(i)`.

- The encoder stores an index `i` plus a residual `x - A(i)`.
- The law is only useful if total transmitted bits beat raw fallback.
- This is different from a predictor-only model because the decoder reconstructs anchors from the transmitted index and the law tree.
- The current cost model still uses fixed-width index and residual accounting.
- Entropy coding, PySR, and heavier symbolic regression remain intentionally deferred.

## Optimizer Architecture

The repository now exposes a small optimizer registry with four visible choices:

- `GP-lite`: the existing tree-based indexed anchor-law search
- `SOMA`: a small continuous-parameter migration optimizer over affine and quadratic anchor laws
- `GP`: an honest placeholder for future richer topology search
- `ADAM`: an honest placeholder for future differentiable parameter tuning

All optimizers are judged by the same idea: the result only matters if `total_bits < raw_bits` after counting model, parameter, index, residual, flag, header, and escape costs.

## GUI Research Cockpit

The first GUI is a stdlib Tkinter cockpit focused on generated grayscale image simulations.

- It lets you choose an optimizer and a tiny image dataset.
- It reports raw size in bits and estimated transmitted size in bits.
- It is a research UI, not a final file compressor.
- Estimated bit accounting is still fixed-width; entropy coding is deferred.

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
- benchmark corpora integration
- binary file format packaging
