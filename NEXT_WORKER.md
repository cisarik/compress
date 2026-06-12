You are the WORKER in the public PrimeSymbolicMDL repository.

Working directory:

`/home/agile/compress`

Task type:

`AP/meta session artifacts + product direction`

## Context

The COOPERATOR clarified the strategic direction:

* AP/meta work is not decorative.
* Analytic Programming / Coordinator Protocol is being developed because it may later become a real tool or SaaS.
* The future product/tool working name is `analytic`.
* Long-term practical compression goal: a Linux CLI command that takes an input file and produces a compressed output file.
* Example future direction:

```fish
analytic compress input.file --output input.file.analytic
analytic decompress input.file.analytic --output restored.file
```

or eventually a simpler workflow such as:

```fish
analytic input.file
```

This task is still a bounded AP/meta/documentation task.

Do not implement the `analytic` CLI yet.

Do not change compression algorithms.

The previous compression step reportedly added:

* `src/primesymbolicmdl/huge_anchor_corpus_benchmark.py`
* `tests/test_huge_anchor_corpus_benchmark.py`
* README external-corpus benchmark note
* tests: `283 passed`

The previous AP protocol evolution step added:

* COOPERATOR role
* living protocol artifacts
* Worker/Orchestrator doctrine evolution
* planned controlled write-RPC as conceptual only

## Goal

Finish the current AP/meta cleanup by adding session-working handoff artifacts and recording the future `analytic` product direction clearly, without overbuilding.

After this task, the next Worker step should return to compression work.

## Hard Rules

* Do not run git write commands.
* Do not commit.
* Do not push.
* Do not create branches.
* Do not install dependencies.
* Do not use network.
* Do not modify compression algorithms.
* Do not modify compression tests unless absolutely necessary.
* Do not implement the `analytic` CLI in this task.
* Do not claim the project is already a production compressor.
* Do not claim universal compression.
* Keep documentation concise and purpose-separated.
* If write-RPC is mentioned, describe it as planned/conceptual unless implemented.

## Required Inspection

Inspect at least:

* `AP.md`
* `AP_WORKER.md`
* `AP_ORCHESTRATOR.md`
* `COORDINATOR_PROTOCOL.md`
* `NEXT_AGENT.md`
* `NEXT_ORCHESTRATOR.md`
* `README.md`
* current repo state
* if present:

  * `src/primesymbolicmdl/huge_anchor_corpus_benchmark.py`
  * `tests/test_huge_anchor_corpus_benchmark.py`

Run read-only inspection:

```fish
cd /home/agile/compress
git status --short
git diff --stat
git rev-parse HEAD
```

Do not run git write commands.

## Required Changes

### 1. Add `AP_WORKER_NEXT_SESSION.md`

Create a concise working/staging artifact.

It should explain:

* this is a temporary session-working artifact
* it is not the final Worker handoff
* final Worker handoff remains `NEXT_AGENT.md`
* use it to collect candidate next Worker tasks, unresolved questions, warnings, command notes, and observations during an active AP session
* consolidate into `NEXT_AGENT.md` only at session close or when explicitly requested
* stale staged notes must not override current repo state, current reports, tests, or `NEXT_AGENT.md`

Keep it short.

### 2. Add `AP_ORCHESTRATOR_NEXT_SESSION.md`

Create a concise working/staging artifact.

It should explain:

* this is a temporary session-working artifact
* it is not the final Orchestrator handoff
* final Orchestrator handoff remains `NEXT_ORCHESTRATOR.md`
* use it to collect strategic notes, report evaluations, risk notes, possible branches, and doctrine observations during an active AP session
* consolidate into `NEXT_ORCHESTRATOR.md` only at session close or when explicitly requested
* stale staged notes must not override current repo state, current reports, tests, or `NEXT_ORCHESTRATOR.md`

Keep it short.

### 3. Update `AP.md`

Add a concise section explaining the difference between:

* session-working artifacts:

  * `AP_WORKER_NEXT_SESSION.md`
  * `AP_ORCHESTRATOR_NEXT_SESSION.md`

and final handoff artifacts:

* `NEXT_AGENT.md`
* `NEXT_ORCHESTRATOR.md`

Make clear:

* session-working artifacts are optional staging areas
* final handoff files remain authoritative at session close
* serious AP session close should consolidate staged notes into final handoffs
* stale staged notes must not override current repo evidence

Also add a short note that AP itself may later become part of a tool/SaaS named `analytic`, but that this is currently product direction, not implemented functionality.

### 4. Update `AP_WORKER.md`

Add a short section or note explaining Worker usage of `AP_WORKER_NEXT_SESSION.md`.

Rules:

* Worker may update it only when explicitly asked
* Worker must not silently treat it as final handoff
* Worker reports must mention if it was changed
* final Worker handoff remains `NEXT_AGENT.md`

### 5. Update `AP_ORCHESTRATOR.md`

Add a short section or note explaining Orchestrator usage of `AP_ORCHESTRATOR_NEXT_SESSION.md`.

Rules:

* Orchestrator may ask Worker to update it through bounded AP/meta tasks
* Orchestrator uses it as staging, not final truth
* final strategic handoff remains `NEXT_ORCHESTRATOR.md`
* when closing a serious session, Orchestrator should decide whether staged notes are consolidated or discarded

### 6. Update `COORDINATOR_PROTOCOL.md` only if appropriate

If it already lists artifacts or future RPC methods, add a minimal note about session-working artifacts.

Do not bloat it.

### 7. Add or update a small roadmap/direction note

Add a concise future direction note.

Preferred option:

* create `PRODUCT_DIRECTION.md`

Alternative if you judge it better:

* add a short section to `README.md`

The note should say:

* future tool working name: `analytic`
* possible future CLI:

  * `analytic compress input.file --output input.file.analytic`
  * `analytic decompress input.file.analytic --output restored.file`
* this is not implemented yet
* current repo is still an experimental lossless compression research harness
* current `.psmdl` and corpus benchmark are stepping stones toward a real file workflow
* no general-purpose compression claim is made

Keep this concise. Do not turn it into marketing.

### 8. Update `README.md` only minimally

If `PRODUCT_DIRECTION.md` is created, add one short link/note to README.

If you instead add the product note directly into README, keep it small.

## Validation

Run:

```fish
cd /home/agile/compress
source .venv/bin/activate.fish
.venv/bin/pytest -q
```

Snapshot is optional.

If you run snapshot, report it.

If you skip snapshot, explain why.

## Acceptance Criteria

This task is complete only if:

* `AP_WORKER_NEXT_SESSION.md` exists
* `AP_ORCHESTRATOR_NEXT_SESSION.md` exists
* `AP.md` explains session-working artifacts vs final handoff artifacts
* `AP_WORKER.md` explains Worker usage of the Worker session artifact
* `AP_ORCHESTRATOR.md` explains Orchestrator usage of the Orchestrator session artifact
* future `analytic` product/CLI direction is documented as direction, not implemented feature
* README links or briefly mentions the product direction if a separate file is created
* tests pass or failures are honestly reported
* no git write commands are run
* no compression algorithms are changed

## Required Report Format

Your response must start exactly with:

`### Report for ORCHESTRATOR_CHAT`

Then include:

1. Summary
2. Files inspected
3. Files changed
4. Commands run
5. Test output
6. Snapshot status
7. Explanation of new session-working artifacts
8. Explanation of future `analytic` product direction
9. How final handoff files remain authoritative
10. Warnings and limitations
11. Suggested next smallest step

The suggested next smallest step should return to compression work unless there is a serious AP artifact problem.
