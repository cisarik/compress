You are the WORKER in the public PrimeSymbolicMDL repository.

Working directory:

`/home/agile/compress`

Task type:

`compression practicalization / real external corpus evaluation`

## Context

The AP/meta layer is sufficiently clarified for this phase.

Do not continue with more AP/meta changes unless you discover a serious blocking inconsistency.

Return to the main compression project.

Current Worker-reported repo state:

* `.psmdl` file CLI exists
* deterministic in-repo benchmark exists
* external-corpus benchmark harness exists:

  * `src/primesymbolicmdl/huge_anchor_corpus_benchmark.py`
  * `tests/test_huge_anchor_corpus_benchmark.py`
* full test suite reportedly passes:

  * `283 passed`
* current honest evidence:

  * random-like data tends to raw fallback
  * small repo text/source files tend to raw fallback
  * synthetic `square_generated_64` can compress as a mechanism check
* no universal compression claim is allowed

The next bounded step is to use the external-corpus harness on a small real local corpus outside the repository and derive the next compression direction from actual results.

## Goal

Run the external-corpus benchmark on a small real local corpus outside the repo and produce an honest evidence report.

This is primarily a benchmarking / evaluation step, not an algorithm-invention step.

At the end, recommend the next smallest compression step based on the actual results.

## Hard Rules

* Do not run git write commands.
* Do not commit.
* Do not push.
* Do not create branches.
* Do not install dependencies.
* Do not use network.
* Do not change AP docs unless a serious blocking inconsistency is discovered.
* Do not change compression algorithms unless a tiny bug fix is absolutely necessary to make the benchmark run correctly.
* Do not claim universal compression.
* Do not present synthetic wins as general proof.
* Actual bytes matter more than estimated bits.
* Exact roundtrip is mandatory.
* Be privacy-conscious: do not crawl broad personal directories indiscriminately.

## Required Inspection

Inspect at least:

* `README.md`
* `NEXT_AGENT.md`
* `NEXT_ORCHESTRATOR.md`
* `src/primesymbolicmdl/huge_anchor_corpus_benchmark.py`
* related tests

Run read-only inspection:

```fish
cd /home/agile/compress
git status --short
git diff --stat
git rev-parse HEAD
```

Do not run git write commands.

## Corpus Selection Rules

Benchmark a **small real local corpus outside the repository**.

Preferred approach:

* choose a small, safe, non-sensitive corpus from local machine files outside `/home/agile/compress`
* keep it small and bounded
* use a mix of file types if possible

Target size:

* around 5 to 12 files
* small files preferred, roughly up to a few hundred KB each
* keep runtime reasonable

Good candidates if available:

* small text/config files
* small binaries
* small images
* small structured data files

Privacy / safety constraints:

* do not recursively crawl the user home broadly
* do not touch obviously sensitive personal data
* do not use browser profiles, SSH keys, wallet data, private documents, or large media folders
* if needed, explicitly create a small temporary corpus directory and copy in a few safe external files from outside the repo

If there is no suitable safe external corpus available, say so explicitly and explain what you used instead.

## Required Benchmark Work

Use the external-corpus harness to benchmark the selected corpus.

For each file, report at least:

* path or filename
* file type if obvious
* raw bytes
* `.psmdl` bytes
* delta bytes
* decision (`compressed` or `raw_fallback`)
* file format (`huge_anchor` or `raw_fallback`)
* roundtrip result

Also report an aggregate summary:

* file count
* total raw bytes
* total `.psmdl` bytes
* total delta bytes
* compressed count
* raw fallback count
* roundtrip failure count
* error count

## Required Analysis

After the benchmark, provide a short evidence-based analysis:

1. Did any real external files actually compress?
2. If not, is the dominant problem clearly:

   * raw-fallback container overhead,
   * poor match between current anchor families and real data,
   * or something else?
3. Based on actual results, what is the next **smallest** compression step?

Choose exactly one recommended next direction, preferably one of:

* overhead reduction
* better corpus/reporting before algorithm changes
* a narrowly scoped compression improvement in one specific area

Do not recommend a large mixed-scope task.

## Optional Small Code Changes

Avoid code changes if possible.

Only make a code change if:

* the benchmark harness has a real usability bug,
* reporting is missing an essential field,
* or a tiny correctness fix is needed.

If you do change code, keep it minimal and add tests.

## Validation

Run:

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
.venv/bin/pytest -q
```

Then run the benchmark harness on the chosen external corpus using the working invocation, for example:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_corpus_benchmark --input-dir /path/to/corpus --recursive
```

Adjust flags as needed.

Snapshot is optional in this step.

If you skip snapshot, explain why.

## Acceptance Criteria

This task is complete only if:

* a small real local external corpus outside the repo was benchmarked, or the reason this was not possible is clearly explained
* actual byte results are reported per file
* aggregate summary is reported
* exact roundtrip results are reported
* the analysis is honest and evidence-based
* one bounded next compression direction is recommended
* tests pass or failures are honestly reported
* no git write commands are run
* no hype is introduced

## Required Report Format

Your response must start exactly with:

`### Report for ORCHESTRATOR_CHAT`

Then include:

1. Summary
2. Files inspected
3. Corpus selection
4. Files changed
5. Commands run
6. Test output
7. Per-file benchmark results
8. Aggregate benchmark summary
9. Evidence-based analysis
10. Warnings and limitations
11. Suggested next smallest step

Be explicit about anything not done.
