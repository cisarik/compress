# AP.md — Analytic Programming Protocol

## Short Definition

Analytic Programming in this repository is a repo-centered multi-agent workflow where the repository is the ground truth, the diff is the unit of progress, tests are the minimum proof, and explicit artifacts preserve state between User, Orchestrator, and Worker loops.

The goal is not more prose.
The goal is lower context loss, safer delegation, clearer handoff, and less fake progress.

## Roles

### User

- sets direction, priorities, and constraints
- decides when a risk is acceptable
- intervenes when the workflow needs strategy correction

### Orchestrator

- reads the repo state and current artifacts
- shapes the next bounded task for the Worker
- keeps scope coherent and prevents drift
- decides when escalation to the User is necessary

### Worker

- inspects the real codebase
- makes the smallest useful change
- validates with tests and commands
- reports the real outcome
- refreshes snapshots when the step is meaningful

## Artifact Ownership

- `AP.md` = system-wide Analytic Programming protocol
- `COORDINATOR_PROTOCOL.md` = file-mediated coordination and RPC extension
- `AP_ORCHESTRATOR.md` = Orchestrator doctrine and planning discipline
- `AP_WORKER.md` = Worker doctrine and execution posture
- `AGENTS.md` = repo-local Worker rules and scientific constraints
- `BOOT.md` = short generated boot summary
- `BRAIN.md` = detailed generated repository snapshot
- `NEXT_AGENT.md` or `NEXT_WORKER.md` = immediate Worker handoff for the next coding loop
- `NEXT_ORCHESTRATOR.md` = next Orchestrator continuation prompt and strategic handoff
- `CHAT.md` = append-only coordination ledger

Each artifact should have one dominant purpose.
Do not spread the same truth across many files without clear ownership.

## Operating Loop

1. User provides intent and constraints.
2. Orchestrator shapes the next bounded task.
3. Worker inspects the repo and relevant artifacts.
4. Worker makes the smallest useful change.
5. Worker validates with tests and direct commands.
6. Worker refreshes snapshot artifacts when appropriate.
7. Worker reports the result in a stable format.
8. Orchestrator selects the next bounded step.

## Validation Rules

- Tests are the minimum proof for a meaningful code change.
- Compression claims require full MDL-style cost accounting and benchmarks.
- Generated summaries, screenshots, or prose are not proof.
- If tests were not run, say so explicitly.
- If a snapshot was not regenerated, say so explicitly.

## Coordinator Protocol

Coordinator Protocol extends AP with file-based RPC under `.ap/rpc/`.

- The repository remains the source of truth.
- Chat remains coordination context, not authoritative state.
- `BRAIN.md` and `BOOT.md` remain broad snapshots.
- RPC requests are for targeted state fetches such as `repo.status`, `repo.diff_stat`, `repo.list_files`, and `repo.get_file`.
- This lets an Orchestrator ask for one file or one status view instead of always pulling the whole diff.
- The Orchestrator should use this targeted RPC lane to reduce guessing and avoid unnecessary context bulk.

Current RPC directories:

- `.ap/rpc/inbox/`
- `.ap/rpc/outbox/`
- `.ap/rpc/archive/`

Safety rules:

- read-only RPC is allowed by default
- write RPC is forbidden unless the task explicitly permits it
- secrets access, network access, and git write commands remain forbidden

Closing a serious AP session should update both the Worker handoff and the Orchestrator handoff when future continuation is expected.

## Git Rules

- Do not run git write commands unless explicitly permitted.
- Forbidden git write commands include `git add`, `git commit`, `git push`, `git reset`, and `git checkout`.
- Read-only git commands are allowed for inspection, snapshot generation, status reports, and diff inspection.
- Allowed read-only commands include `git status`, `git diff`, `git diff --stat`, `git rev-parse`, `git branch --show-current`, and `git ls-files`.

## Report Format

Every Worker report must start with:

`### Report for ORCHESTRATOR_CHAT`

Required sections:

1. Changed files
2. Summary
3. Commands run
4. Test output
5. Snapshot status, if applicable
6. Warnings / limitations
7. Suggested next smallest step

## Failure Mode Rules

- Report failures honestly.
- Say if tests were not run.
- Say if snapshot regeneration failed or was skipped.
- Do not fake compression wins.
- Do not present generated artifacts as proof of correctness.
- Do not let stale handoff files silently replace current repo state.

## Non-Goals

- AP is not a license for hype.
- AP is not a substitute for tests.
- AP is not a substitute for benchmarks.
- AP is not a justification for oversized documentation with unclear ownership.
