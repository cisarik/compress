You are the WORKER in the PrimeSymbolicMDL repository.

Working directory:

`/home/agile/compress`

Task type:

`compression practicalization / validation`

## Context

The previous Worker implemented a real file CLI for huge-anchor binary compression/decompression.

Reported changed files:

* `src/primesymbolicmdl/huge_anchor_file.py`
* `src/primesymbolicmdl/huge_anchor_file_cli.py`
* `tests/test_huge_anchor_file_cli.py`

Reported commands:

* `.venv/bin/pytest -q tests/test_huge_anchor_file_cli.py`
* `.venv/bin/pytest -q`

Reported results:

* `9 passed` for new CLI tests
* `276 passed` for the full suite

Important warning from the previous report:

* In this environment, use `.venv/bin/pytest`.
* Do not rely on `.venv/bin/python -m pytest`, because it may resolve incorrectly through the Cursor appimage environment.

## Goal

Do a small, bounded post-implementation audit and practical benchmark of the new `.psmdl` file CLI.

The goal is not to invent a new algorithm.

The goal is to verify that the new CLI is understandable, safe, roundtrips exactly, and produces honest actual-size behavior on small real files and deterministic sanity inputs.

## Hard Rules

* Do not run any git write commands.
* Do not commit.
* Do not push.
* Do not create branches.
* Do not install new dependencies.
* Do not use the network.
* Do not introduce new compression algorithms.
* Do not make universal compression claims.
* Exact byte-for-byte roundtrip is mandatory.
* Actual file size matters more than estimated bits.
* Random bytes should normally remain raw fallback.
* Keep changes minimal.

## Allowed Actions

You may:

* read relevant source files
* run tests
* run the new CLI on temporary files
* add a small benchmark/demo script if useful
* add tests for that script only if the script is committed as part of the repo
* update documentation only if needed to make the CLI usage clear

Prefer temporary files under a safe temporary directory created by Python or shell.

Do not leave generated benchmark files committed into the repo.

## Required Inspection

First inspect:

* `src/primesymbolicmdl/huge_anchor_file.py`
* `src/primesymbolicmdl/huge_anchor_file_cli.py`
* `tests/test_huge_anchor_file_cli.py`

Check for:

* clear format handling
* safe raw fallback behavior
* exact roundtrip verification
* good error handling for invalid input
* clear CLI output
* no misleading compression claims

## Required Benchmark

Run the CLI on a small deterministic benchmark set.

Use at least these inputs:

1. small random bytes
2. repeated bytes or repeated pattern
3. a small real text file from the repository, for example `README.md` or `AGENTS.md`
4. a small Python source file from `src/primesymbolicmdl/`
5. a synthetic square-generated style dataset if it can be constructed cleanly using existing repo code

For each case report:

* input name
* raw input bytes
* `.psmdl` output bytes
* whether huge-anchor compression or raw fallback was used
* exact roundtrip result
* whether `--require-compression` succeeds or fails
* any surprising behavior

## Optional Small Repo Change

If it is useful and keeps scope small, add a script such as:

`src/primesymbolicmdl/huge_anchor_file_benchmark.py`

or similar.

The script should:

* generate deterministic temporary inputs
* run the existing file compression/decompression path directly or through the CLI
* print an honest table of actual sizes
* clearly mark raw fallback versus actual huge-anchor compression
* not claim general compression success

Only add this script if it makes the benchmark repeatable and simple.

If adding a script, add minimal tests for it.

## Validation Commands

Run:

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
.venv/bin/pytest -q
```

If you add a benchmark script, also run it, for example:

```fish
.venv/bin/python -m primesymbolicmdl.huge_anchor_file_benchmark
```

If `.venv/bin/python -m ...` has the Cursor appimage problem, use the safest working invocation and report exactly what worked.

## Acceptance Criteria

This task is complete only if:

* the new CLI behavior has been audited
* exact roundtrip is verified on temporary real files
* random bytes do not produce misleading compression claims
* actual `.psmdl` byte sizes are reported
* raw fallback behavior is clearly shown
* the full pytest suite passes
* any new script or docs are minimal and honest

## Required Report Format

Your response must start exactly with:

`### Report for ORCHESTRATOR_CHAT`

Then include:

1. Summary
2. Files inspected
3. Files changed
4. Commands run
5. Full test results
6. Benchmark table with actual byte sizes
7. Roundtrip verification results
8. Raw fallback / `--require-compression` behavior
9. Warnings and limitations
10. Suggested next smallest step

Be explicit about anything not done.
