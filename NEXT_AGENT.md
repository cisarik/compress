# NEXT_AGENT

You are continuing work in the `PrimeSymbolicMDL` repository.

This file is the single active handoff prompt for the next Codex agent.
Do not create `NEXT_PROMPT`, `NEXT_PROMPT2`, `NEXT_PROMPT3`, or similar files.
When this handoff is no longer current, overwrite or delete this file and replace it with the latest one.

## Mission

`PrimeSymbolicMDL` is an experimental lossless compression research harness built around honest MDL-style accounting.

Core scientific posture:

- no hype
- no universal-compression claims
- exact reversibility for every path that claims to decode
- conservative, explicit transmitted-cost accounting
- fallback to raw is normal when a model loses

## Hard Rules

1. Do NOT run git commands.
2. Do NOT delete the original research markdown files:
   - `deep-research-report-1.md`
   - `deep-research-report-2.md`
3. Do NOT add network downloads.
4. Do NOT add heavy dependencies.
5. Use stdlib only plus real `pytest`.
6. Do NOT create local shims for third-party tools.
7. Keep behavior deterministic under a seed.
8. Comments and docstrings should be in Slovak.
9. Public docs may be in English.
10. Keep tests headless.
11. If Tkinter is missing, report that the system package `tk` is needed.
12. Do not fake compression wins. If a model loses to raw, report it honestly.

## Current Repository State

The repository already contains:

- deterministic fixed-width block packing in `src/primesymbolicmdl/blocks.py`
- prime-anchor accounting and codec baseline
- GP-lite indexed anchor-law search:
  - `anchor_laws.py`
  - `index_branch.py`
  - `law_search.py`
  - `law_demo.py`
- older family-based evolutionary search in `evolution.py`
- modular optimizer architecture in `src/primesymbolicmdl/optimizers/`
  - `GP-lite` adapter is real and wired
  - `SOMA` adapter is real and wired
  - `GP` is an honest placeholder
  - `ADAM` is an honest placeholder
- grayscale dataset generators in `image_datasets.py`
- headless simulation/reporting in `simulation.py`
- CLI demo in `sim_demo.py`
- Tkinter GUI research cockpit in `gui.py`

Important architectural split:

- GP-lite and SOMA currently operate mostly on a 1D byte-stream view
- GUI and simulation already operate on grayscale image datasets
- there is not yet an image-aware 2D predictor branch

## Current Test / Runtime Status

- real `pytest` is used
- Tkinter is available in the current environment
- current full test suite status at handoff:

```text
86 passed in 1.92s
```

Latest demo command:

```bash
python -m primesymbolicmdl.sim_demo
```

Latest demo output:

```text
optimizer: GP-lite
status: ok
dataset: gradient (16x16)
raw_bits: 2048
total_bits: 2340
saving_bits: -292
ratio_vs_raw: 1.143
best_model: 0
history:
  gen=0 total_bits=2340 saving_bits=-292 best=0
  gen=1 total_bits=2340 saving_bits=-292 best=0
  gen=2 total_bits=2340 saving_bits=-292 best=0
  gen=3 total_bits=2340 saving_bits=-292 best=0
  gen=4 total_bits=2340 saving_bits=-292 best=0

optimizer: SOMA
status: ok
dataset: gradient (16x16)
raw_bits: 2048
total_bits: 2355
saving_bits: -307
ratio_vs_raw: 1.150
best_model: affine(a=0.000, b=0.080)
history:
  gen=0 total_bits=2371 saving_bits=-323 best=affine(a=0.481, b=-14.529)
  gen=1 total_bits=2366 saving_bits=-318 best=quadratic(a=0.000, b=-7.015, c=0.000)
  gen=2 total_bits=2361 saving_bits=-313 best=affine(a=0.000, b=-5.927)
  gen=3 total_bits=2361 saving_bits=-313 best=affine(a=0.000, b=-5.927)
  gen=4 total_bits=2360 saving_bits=-312 best=affine(a=0.000, b=-3.257)
note: Float parameters are estimated research parameters, not a final codec format.
```

Interpretation:

- the optimizer architecture is working
- GP-lite and SOMA are wired end-to-end
- current image simulations do not yet beat raw storage
- the next meaningful step is to add a true 2D image-aware predictor baseline

## Current Important Files

- `AGENTS.md`
- `README.md`
- `docs/research_plan.md`
- `src/primesymbolicmdl/anchor_laws.py`
- `src/primesymbolicmdl/index_branch.py`
- `src/primesymbolicmdl/law_search.py`
- `src/primesymbolicmdl/optimizers/base.py`
- `src/primesymbolicmdl/optimizers/registry.py`
- `src/primesymbolicmdl/optimizers/gplite_adapter.py`
- `src/primesymbolicmdl/optimizers/soma.py`
- `src/primesymbolicmdl/optimizers/placeholders.py`
- `src/primesymbolicmdl/image_datasets.py`
- `src/primesymbolicmdl/simulation.py`
- `src/primesymbolicmdl/sim_demo.py`
- `src/primesymbolicmdl/gui.py`
- `tests/`

## Next Requested Task

Add a new optimizer named:

```text
Image-predictor
```

This optimizer should exploit 2D grayscale image structure using decoder-known predictors and exact residual coding.

Conceptual model:

```text
x = predictor(context) + residual
```

where the predictor may use only decoder-known information:

- `col`
- `row`
- `width`
- `height`
- previously decoded `left`
- previously decoded `up`
- previously decoded `up_left`

This is a predictor branch, not the indexed-anchor branch.

## Exact Requested Work

### A. Inspect current repository

Read:

- `AGENTS.md`
- `README.md`
- `docs/research_plan.md`
- `src/primesymbolicmdl/*.py`
- `src/primesymbolicmdl/optimizers/*.py`
- `tests/*.py`

Understand the existing image dataset, simulation, optimizer registry, and GUI before editing.

### B. Add image predictor model module

Create:

- `src/primesymbolicmdl/image_predictors.py`
- `tests/test_image_predictors.py`

Implement a tiny deterministic set of grayscale predictors.

Define a small model representation, for example:

- `ImagePredictorModel`
  - `name: str`
  - `params: dict[str, int]`

Implement:

- `predict_pixel(model, col, row, width, height, left, up, up_left) -> int`
- `default_image_predictor_models() -> list[ImagePredictorModel]`
- `render_image_predictor(model) -> str`
- `image_predictor_model_bits(model) -> int`
- `image_predictor_parameter_bits(model) -> int`

All predictions must be clamped to `0..255`.

Required predictors:

1. `zero`
2. `left`
3. `up`
4. `avg_left_up`
5. `gradient`
6. `x_ramp`
7. `y_ramp`
8. `diagonal_ramp`
9. `checker(block=...)`
   - candidate block sizes: `1, 2, 4, 8, 16`

### C. Add image predictor codec / cost module

Create:

- `src/primesymbolicmdl/image_predictor_branch.py`
- `tests/test_image_predictor_branch.py`

Implement:

- `estimate_image_predictor_cost(image, model) -> dict`
- `encode_image_predictor_payload(image, model) -> dict`
- `decode_image_predictor_payload(payload) -> bytes`
- `roundtrip_image_predictor(image, model) -> bytes`

Required cost fields:

- `raw_bits`
- `model_bits`
- `parameter_bits`
- `header_bits`
- `residual_bits`
- `total_bits`
- `saving_bits`
- `ratio_vs_raw`
- `min_residual`
- `max_residual`
- `residual_width`
- `pixel_count`
- model string

Cost model:

- `raw_bits = width * height * 8`
- `header_bits` can be a conservative fixed cost such as `64`
- `residual_width = 0` if every residual is exactly zero
- otherwise use a fixed signed width for the observed min/max residual range
- exact decode must use only model + width/height + residuals + previously decoded pixels

### D. Add Image-predictor optimizer

Create:

- `src/primesymbolicmdl/optimizers/image_predictor.py`
- `tests/test_image_predictor_optimizer.py`

Important optimizer-abstraction change:

Prefer extending `OptimizerRequest` with:

- `metadata: dict[str, object]`

Use metadata to pass:

- `image_width`
- `image_height`
- `dataset_name`

Implement optimizer:

- `name = "Image-predictor"`
- `available = True`
- evaluate all default image predictor models
- choose the model with lowest `total_bits`
- return honest `OptimizerResult`

Required `details` should include at least:

- `residual_width`
- `min_residual`
- `max_residual`
- `would_use_fallback: total_bits >= raw_bits`

Do not silently force fallback in the optimizer result. Report the candidate honestly.

### E. Integrate registry, simulation, CLI, GUI

Update:

- `src/primesymbolicmdl/optimizers/registry.py`
- `src/primesymbolicmdl/simulation.py`
- `src/primesymbolicmdl/sim_demo.py`
- `src/primesymbolicmdl/gui.py`

Requirements:

- preserve existing names:
  - `GP-lite`
  - `SOMA`
  - `GP`
  - `ADAM`
- add:
  - `Image-predictor`

Simulation:

- pass image metadata through `OptimizerRequest`
- `format_simulation_report()` should include:
  - fallback recommendation if `total_bits >= raw_bits`
  - win marker if `total_bits < raw_bits`

sim_demo:

- run at least:
  - `Image-predictor` on `gradient`
  - `Image-predictor` on `diagonal_ramp`
  - `Image-predictor` on `checker`
  - `GP-lite` on `gradient`
  - `SOMA` on `gradient`
- keep it quick

GUI:

- dropdown must include `Image-predictor`
- output must show:
  - raw bits
  - estimated total bits
  - saving bits
  - ratio
  - best model
  - fallback recommendation

### F. Documentation updates

Update:

- `README.md`
- `docs/research_plan.md`
- `AGENTS.md`

Add a section:

`Image-aware predictor branch`

Explain:

- predictor/residual branch, not index branch
- decoder-known 2D context
- necessary baseline before stronger GP/SOMA claims
- fixed-width residual accounting only
- entropy coding deferred
- a result matters only if `total_bits < raw_bits`

### G. Tests

Add/update tests proving:

1. image predictors are clamped and deterministic
2. `x_ramp`, `y_ramp`, and `checker` behave correctly
3. branch costing exposes all required fields
4. gradient and checker roundtrip exactly
5. registry includes `Image-predictor`
6. optimizer runs and exposes readable best model/history
7. simulation works with `Image-predictor`
8. at least one structured generated image beats raw
9. noise is not required to beat raw
10. GUI imports headlessly and includes `Image-predictor`
11. existing tests still pass

### H. Run commands

Run:

```bash
python -m pytest -q
python -m primesymbolicmdl.sim_demo
```

Do not run the GUI automatically during tests.

## Acceptance Criteria

- all tests pass
- no git commands were run
- no heavy dependencies were added
- existing optimizers still work
- new `Image-predictor` optimizer exists and is registered
- `Image-predictor` can beat raw on at least one structured generated image
- roundtrip is exact
- GUI dropdown includes `Image-predictor`
- documentation clearly states limitations

## Working Style Reminder

- use `apply_patch` for file edits
- keep diffs small and readable
- prefer shared abstractions instead of duplicated accounting logic
- preserve deterministic behavior
- report exact test output
- keep the answer honest if the new branch loses on some datasets
