# COORDINATOR_PROTOCOL.md — Coordinator Protocol for Analytic Programming

## Short Definition

Coordinator Protocol is a file-mediated, repo-centered coordination protocol for `COOPERATOR`, `ORCHESTRATOR`, and `WORKER`.

It extends Analytic Programming with small structured messages that live next to the repository state instead of replacing it.

## Roles

### `COOPERATOR`

The user or strategic owner of intent.
This role sets direction, accepts or rejects risk, and decides when deeper intervention is needed.

### `ORCHESTRATOR`

The planning and evaluation role.
This role reads repository artifacts, asks for bounded work, requests focused state, and decides what the Worker should do next.

### `WORKER`

The execution role.
This role reads the real codebase, changes files when permitted, runs tests or inspections, and answers structured requests with real repository-backed results.

### `REPOSITORY`

The durable state carrier.
The repository stores code, documentation, AP artifacts, and RPC messages. It is the only source that can be audited after the conversation is gone.

## Core Idea

- The repository is the source of truth.
- Chat is not the source of truth.
- Snapshot files summarize repo state, but they do not replace the repo.
- RPC request and response files let an Orchestrator ask for a specific status, diff view, file, or later a bounded test action without copying entire conversations.

This keeps coordination narrow:

- `BRAIN.md` and `BOOT.md` stay broad snapshots.
- RPC stays targeted and method-shaped.
- `CHAT.md` stays a ledger, not a database.

## File-Based RPC Directories

The protocol uses scratch directories created on demand under `.ap/rpc/`:

- `.ap/rpc/inbox/`
- `.ap/rpc/outbox/`
- `.ap/rpc/archive/`

Typical flow:

1. `ORCHESTRATOR` writes a request JSON into `.ap/rpc/inbox/`.
2. `WORKER` reads the next request and handles it.
3. `WORKER` writes a response JSON into `.ap/rpc/outbox/`.
4. The original request is archived into `.ap/rpc/archive/` when practical.

No server, daemon, or network transport is required.

## Request JSON Schema In Prose

Each request JSON contains:

- `id`
  - unique request identifier
- `type: "rpc_request"`
  - explicit document kind
- `from`
  - usually `ORCHESTRATOR`
- `to`
  - usually `WORKER`
- `method`
  - requested operation name
- `params`
  - method-specific JSON object
- `created_at`
  - ISO-like creation timestamp

## Response JSON Schema In Prose

Each response JSON contains:

- `id`
  - the same request identifier
- `type: "rpc_response"`
  - explicit document kind
- `status: "ok" | "error"`
  - outcome classification
- `method`
  - echoed method name
- `result`
  - method result object when `status` is `ok`
- `error`
  - readable error text when `status` is `error`
- `created_at`
  - response creation timestamp

## Initial Read-Only Methods

The first proof-of-concept methods are intentionally small and read-only:

- `repo.status`
  - branch, HEAD, short git status
- `repo.diff_stat`
  - current diff summary
- `repo.list_files`
  - repository file list without volatile or forbidden internals
- `repo.get_file`
  - bounded text fetch for a single repository-relative file plus `sha256`, size, and truncation flag

These methods are enough to prove targeted repo introspection without introducing write capability.

## Safety Model

- Read-only RPC is the default allowed class.
- Write RPC is forbidden unless an explicit task permits it.
- Secrets access is forbidden.
- Network access is forbidden for this protocol by default.
- Git write operations are forbidden.
- Path traversal, absolute paths, and forbidden repository internals such as `.git/` and `.venv/` must be rejected.

The Worker must return `status: "error"` with a readable message when a request is invalid or unsafe.

## Relationship To Existing AP Artifacts

- `AP.md`
  - defines the overall Analytic Programming protocol
- `AP_WORKER.md`
  - defines the Worker execution doctrine
- `BRAIN.md`
  - broad generated repository snapshot
- `BOOT.md`
  - short generated boot summary
- `CHAT.md`
  - append-only coordination ledger
- `NEXT_AGENT.md`
  - immediate handoff file for the next coding loop

Coordinator Protocol does not replace these artifacts.
It adds a narrower request/response lane so an Orchestrator can ask for exactly one file or one status view instead of demanding the full diff or the full snapshot every time.

## Future Methods

Candidate follow-up methods:

- `tests.run`
- `snapshot.refresh`
- `repo.search`
- `code.get_symbol`
- `task.set`
- `handoff.build`

Planned controlled write-RPC for AP and handoff artifacts may later include:

- `update_ap_worker`
- `update_ap_orchestrator`
- `update_next_agent`
- `update_next_orchestrator`

These write methods are conceptual only in the current repository.
They are not implemented in the current read-only RPC surface.

These should remain bounded, inspectable, and explicit about safety before any write-capable expansion is allowed.
