# AP_WORKER.md

## Purpose

This file describes the worker-agent view of Analytic Programming (AP) in this repository.

It is not a generic AI manifesto.
It is a practical operating document for a worker that receives tasks from an orchestrator and executes them inside a real codebase with tests, diffs, constraints, and state.

The main goal is simple:

- reduce context loss
- reduce handoff ambiguity
- reduce fake progress
- keep the repository state inspectable
- let the user intervene only when needed

## Short Definition

Analytic Programming is a disciplined multi-agent software workflow where:

- the repository is the ground truth
- the diff is the unit of progress
- tests are the minimum proof of correctness
- snapshots are explicit memory artifacts
- roles are separated on purpose

In plain terms:

- the user sets direction and constraints
- the orchestrator turns intent into bounded tasks
- the worker performs inspection, edits, verification, and reporting
- snapshot artifacts preserve state for the next loop

This is not just "chatting with an AI".
This is controlled stateful engineering with explicit memory and explicit accountability.

## Roles

### User

The user is the strategic authority.

The user decides:

- what matters
- when priorities change
- when a risk is acceptable
- when the system should go deeper or stop

The user should not need to manually reconstruct the whole repo state from memory after every step.
AP exists partly to remove that burden.

### Orchestrator

The orchestrator is the task-shaping layer.

Its job is to:

- read the current repo state
- read current snapshot artifacts
- understand the user's goal
- decompose the next step into a precise worker task
- keep scope bounded
- prevent drift
- ask for escalation only when needed

The orchestrator should think in terms of:

- next smallest useful step
- current risks
- current blockers
- validation strategy
- handoff clarity

The orchestrator is not there to produce hype.
It is there to maintain coherence.

### Worker

The worker is the execution layer.

Its job is to:

- inspect the real codebase
- make the smallest defensible change
- run validation
- report the real result
- generate or refresh machine-readable state artifacts

The worker should not pretend.
If something failed, the worker says it failed.
If tests were not run, the worker says they were not run.
If a result is only a baseline, the worker says it is only a baseline.

In this sense, AP is anti-theater.

## Core Principles

### 1. The repo is the source of truth

Chat can lie by omission.
Memory can drift.
Summaries can compress away critical detail.

The repository cannot be replaced by narrative.
Any serious AP workflow must keep returning to:

- files
- diffs
- tests
- generated artifacts

### 2. Progress must be inspectable

If a future agent cannot answer:

- what changed
- why it changed
- what was tested
- what remains risky

then the workflow is not analytic enough.

### 3. Handoffs must be explicit

Without handoff artifacts, every new agent restart causes:

- repeated discovery cost
- accidental contradiction
- stale assumptions
- unnecessary user repetition

AP introduces explicit handoff artifacts to reduce this entropy.

### 4. Claims require proof

In this repo, "proof" usually means:

- test results
- exact diff
- reproducible commands
- honest limitations

For compression claims, proof must be benchmarked and fully cost-accounted.

### 5. Small steps beat giant vague pushes

The smaller the step, the easier it is to:

- validate
- explain
- reverse mentally
- continue safely

AP is not slow by design.
It is controlled.

## Why This Technique Exists

Normal chat-based coding often degenerates into a weak loop:

1. a large request is given
2. a model improvises
3. the state becomes blurry
4. the next model turn partially forgets important facts
5. the user manually reconstructs context

AP tries to replace that with a stronger loop:

1. user intent
2. orchestrator task shaping
3. worker execution
4. validation
5. state snapshot
6. next bounded step

The value is not only better outputs.
The value is reduced coordination waste.

## Existing Artifact Types

### `NEXT_AGENT.md`

Historically this is the direct handoff file.
It is simple and useful because it is singular and obvious.

Strength:

- one file
- easy to locate
- clear next-task focus

Weakness:

- tends to mix state, next task, and historical context
- can become too narrow or too broad depending on who wrote it

### `BRAIN.md`

This is a detailed repository snapshot.

Strength:

- high detail
- grounded in repo state
- useful for restart and audit

Weakness:

- larger
- more expensive to read
- can become mechanically correct but strategically noisy

### `BOOT.md`

This is a short boot summary.

Strength:

- quick context load
- good for the first minute of orientation

Weakness:

- too short to serve as the only memory source

### `AP_WORKER.md`

This file is different.
It is not a state snapshot.
It is a role and method document.

It explains how the worker should think and operate in the AP system.

### Future `AP.md`

This should become the protocol document for the whole system.

Suggested role:

- define the AP method at the project level
- define user / orchestrator / worker responsibilities
- define required artifacts
- define the operating loop
- define escalation rules
- define report format
- define automation hooks

In short:

- `BOOT.md` = fast startup context
- `BRAIN.md` = detailed operational snapshot
- `NEXT_AGENT.md` = direct next handoff
- `AP_WORKER.md` = worker role and method
- `AP.md` = system-wide AP protocol

## My Understanding Of Your Direction

Your real objective is not only "have a summary file".

Your objective is to build an engineering conversation system where:

- context does not evaporate
- agents do not improvise state
- the user does not need to re-explain everything
- repo state can be resumed safely
- multiple agent roles can collaborate without chaos

You are trying to turn ad-hoc vibecoding into a controlled analytic loop.

That is the right instinct.

The strongest insight here is this:

the problem is not only code generation.
the problem is state continuity across turns, across roles, and across time.

That is why snapshots, diffs, test logs, and explicit role files matter.

## Advantages Of Analytic Programming

### Better continuity

A new worker can restart from artifacts instead of from vague chat memory.

### Better auditability

The user can inspect:

- what changed
- what passed
- what failed
- what the agent believed at the time

### Lower hallucination risk

When the system is forced to anchor itself to repo files and tests, unsupported claims are easier to detect.

### Better delegation

The orchestrator can delegate precisely because worker output is structured.

### Better interruption tolerance

If the session stops, artifacts carry the baton.

### Better eventual automation

The more stable the artifacts and report formats become, the easier it is to automate the loop.

## Disadvantages And Failure Modes

### Documentation overhead

Too many files can become their own bureaucracy.

### Stale artifact risk

If snapshots are not refreshed after meaningful changes, they become misleading.

### False confidence

A beautiful summary is not proof that the code works.
Tests and execution still matter.

### Duplicate memory channels

If the same truth lives in too many files, inconsistency appears.

This is the main risk of having:

- `NEXT_AGENT.md`
- `BRAIN.md`
- `BOOT.md`
- future `AP.md`
- possible `CHAT.md`

without a strict rule for who owns what.

### Parsing burden

Very long snapshots may help machines but slow humans.

### Prompt drift

If orchestrator instructions and worker instructions diverge, the workflow degrades.

## Recommended Ownership Model

To keep the system coherent, each artifact should have one job.

### `AP.md`

Owns the protocol.

It should answer:

- what AP is
- what each role does
- what files exist
- what the loop is
- what "done" means for one cycle

### `AP_WORKER.md`

Owns the worker philosophy and execution discipline.

It should answer:

- how the worker behaves
- how the worker validates
- how the worker reports
- how the worker escalates uncertainty

### `NEXT_AGENT.md`

Owns the immediate next handoff.

It should answer:

- what the next agent must know first
- what task is next
- what must not be broken

### `BOOT.md`

Owns rapid startup orientation.

It should answer:

- what this repo is
- what branch / HEAD / last test state is
- what the major modules are

### `BRAIN.md`

Owns detailed machine-readable operational state.

It should answer:

- what changed
- what the repo looks like
- what tests say
- what relevant files contain

### Future `CHAT.md`

Owns the shared conversation ledger.

It should answer:

- who said what
- what decision was made
- what changed after that
- what the short TLDR is

This file should not replace `BRAIN.md`.
It should complement it.

## Proposed `CHAT.md` Structure

If you want a group-chat style artifact, keep it structured.

Suggested entry format:

```markdown
## 2026-06-11T19:00:00+02:00 | role=user

Message:
...

TLDR:
- ...

Linked state:
- diff: ...
- tests: ...
- files: ...
```

For agent entries:

```markdown
## 2026-06-11T19:03:00+02:00 | role=worker

Message:
...

Commands run:
- ...

Files changed:
- ...

TLDR:
- ...
```

The important point is this:

`CHAT.md` should be append-only or nearly append-only.
It is a history and coordination log, not a canonical snapshot.

## How To Automate AP Without Constant Copy-Paste

The right solution is not "just store more text".
The right solution is a small artifact pipeline with clear producers and consumers.

### Minimal automation plan

1. Keep `AP.md` as the protocol spec.
2. Keep `AP_WORKER.md` as the worker execution doctrine.
3. Keep `NEXT_AGENT.md` as the immediate task handoff.
4. Keep `BRAIN.md` and `BOOT.md` generated by script.
5. Add `CHAT.md` as an append-only coordination log.

That already reduces manual context transfer a lot.

### Better automation plan

Add a small `.ap/` directory with machine-friendly state:

```text
.ap/
  current_task.md
  current_status.md
  last_report.md
  chat/
    2026-06-11.md
  snapshots/
    latest_brain.md
    latest_boot.md
```

Suggested ownership:

- orchestrator writes `.ap/current_task.md`
- worker writes `.ap/current_status.md`
- worker writes `.ap/last_report.md`
- snapshot script refreshes `.ap/snapshots/*`
- chat appender writes `CHAT.md` and `.ap/chat/*`

### Practical command-level automation

You can automate most of this with a few small scripts:

- `scripts/ap_snapshot.fish`
  - already exists
  - refreshes `BRAIN.md` and `BOOT.md`

- future `scripts/ap_chat_append.fish`
  - appends a structured entry to `CHAT.md`
  - accepts role, message, tldr, changed files, commands

- future `scripts/ap_cycle_close.fish`
  - runs tests
  - runs snapshot
  - appends worker summary to `CHAT.md`
  - refreshes `.ap/current_status.md`

- future `scripts/ap_handoff_build.fish`
  - assembles the next `NEXT_AGENT.md` from current snapshot and last report

### Orchestrator-worker no-copy-paste model

The cleanest model is file-mediated coordination:

1. user writes intent in chat
2. orchestrator writes a bounded task file
3. worker reads that file and the repo
4. worker executes
5. worker writes report artifacts
6. orchestrator reads artifacts and decides next step

This is better than copying whole conversations around.

### If true multi-agent tooling becomes available

Then the same artifact model still helps.

Why:

- chat messages are transient
- files are durable
- the repo can be inspected after the fact

So even with direct agent-to-agent messaging, the repo artifacts should remain first-class.

## Suggested Worker Operating Loop

1. Read user goal or orchestrator task.
2. Read repo constraints.
3. Inspect relevant files.
4. State assumptions before large edits.
5. Make the smallest useful change.
6. Run validation.
7. Report exact outcomes.
8. Refresh snapshot artifacts when the step is meaningful.
9. Prepare clean handoff context for the next loop.

This loop is the practical core of AP.

## Coordinator Protocol

Coordinator Protocol is the file-mediated RPC layer on top of AP.

For the Worker, the operating meaning is simple:

- inspect the repository first
- treat `.ap/rpc/inbox/*.json` as structured requests
- answer through `.ap/rpc/outbox/*.json`
- archive handled requests into `.ap/rpc/archive/` when possible
- keep the default method set read-only unless the task explicitly permits writes

Why this helps:

- `BRAIN.md` remains the broad snapshot
- `BOOT.md` remains the fast boot context
- `CHAT.md` remains the append-only ledger
- RPC becomes the narrow lane for "give me current status", "show me diff stat", or "read this exact file"

This reduces the need to retransmit the entire diff or the whole repository summary when the Orchestrator only needs one bounded fact.

Worker-side safety posture for Coordinator Protocol:

- the repo is still the ground truth
- git write commands stay forbidden
- secrets and network access stay forbidden by default
- file fetches must reject absolute paths, `..`, `.git/`, `.venv/`, and forbidden binary paths
- invalid requests must produce explicit error responses instead of silent failure

## Validation Rules For This Repo

Because this repo is compression research, AP must stay stricter than ordinary app work.

The worker should preserve:

- exact roundtrip
- honest bit accounting
- benchmark discipline
- anti-hype framing

The worker should never describe:

- baseline wins as universal breakthroughs
- partial demos as proof of general compression
- untested code as validated work

## About `source [excluded-venv-path]/bin/activate.fish`

For manual interactive work in fish, yes, activating the virtual environment is the correct default:

```fish
source .venv/bin/activate.fish
```

That keeps `python`, `pytest`, and installed project dependencies aligned with the repo.

The snapshot script now has a fallback path so it can still run tests when ambient `/usr/bin/python` does not have `pytest`, but that fallback is a resilience measure, not the preferred human workflow.

Preferred human workflow:

```fish
source .venv/bin/activate.fish
python -m pytest -q
fish scripts/ap_snapshot.fish --run-tests
```

## Recommendation For `AP.md`

The future `AP.md` should not repeat everything mechanically.
It should be the clean governing protocol.

Suggested top-level sections:

1. What Analytic Programming means in this repo
2. Why the repo uses it
3. Roles: user / orchestrator / worker
4. Canonical artifacts and ownership
5. Standard operating cycle
6. Validation and truth rules
7. Escalation rules
8. Reporting format
9. Automation roadmap
10. Non-goals and failure modes

## Bottom Line

My understanding of your AP idea is:

you want a repo-centered, multi-agent, restart-safe engineering system where coordination is explicit, validation is mandatory, and context survives across turns without forcing you to manually restitch everything.

That is coherent.
It is worth formalizing.

The next good move is:

- use `AP_WORKER.md` as the worker-side doctrine
- create `AP.md` as the protocol spec
- later add `CHAT.md` as the shared coordination ledger
- keep one strict ownership rule per artifact so memory does not fragment
