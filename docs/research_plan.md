# Research Plan

PrimeSymbolicMDL should advance in small, benchmarkable steps.

## Roadmap

1. Baseline reversible transforms
2. Honest MDL bit accounting
3. Prime-anchor ablations
4. GP-lite indexed anchor law search
5. Modular optimizer architecture
6. GUI research cockpit
7. Entropy coder
8. Symbolic regression / PySR later
9. Benchmark suite

## Guardrails

- Prime anchors are experimental and must compete against other anchor families.
- Exact lossless reconstruction is mandatory for every codec path.
- Random bytes remain a required sanity baseline.
- "A transform is only useful if total transmitted cost is lower than fallback."

## Near-Term Questions

- When should anchors be transmitted directly versus as indices?
- Which residual coding choices materially improve total cost?
- Which structured sources, if any, benefit from prime anchors after honest accounting?

## GP-lite Indexed Anchor Law Search

This phase evolves small decoder-known anchor laws `A(i)` rather than only choosing from fixed hand-written anchor families.

- The encoder stores index `i` plus residual.
- The candidate law only matters when full transmitted cost beats raw fallback.
- This branch is different from predictor-only anchors because decoding reconstructs anchors from the law and the stored index.
- The current accounting is still fixed-width and does not pretend to be entropy coding.
- PySR and more advanced symbolic regression remain deferred until the smaller deterministic baseline is well characterized.

## Optimizer Architecture

The optimizer layer now separates the research harness into pluggable strategies.

- GP-lite searches tiny expression trees.
- SOMA tunes continuous parameters of small affine and quadratic anchor-law families.
- Future GP will target richer tree and topology search.
- Future ADAM will target differentiable parameter tuning.

All of them are measured against the same honest bit accounting. A candidate matters only when full transmitted cost beats raw fallback.

## GUI Research Cockpit

The first GUI is intentionally narrow and uses generated grayscale images as a headless-friendly simulation target.

- Image simulation is not final file compression.
- The GUI is a cockpit for optimizer comparison, not a claim of general compression performance.
- Estimated bit accounting is still fixed-width and entropy coding remains deferred.
