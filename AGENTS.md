# AGENTS Protocol

## Project Mission

PrimeSymbolicMDL is an experimental research harness for lossless compression based on anchor-and-residual coding under a Minimum Description Length (MDL) objective. Prime anchors are one candidate anchor family, not a privileged truth.

## Scientific Framing

- Keep the project non-hype and benchmark-driven.
- Treat every transform as experimental until it wins after full cost accounting.
- Do not claim broad usefulness from isolated examples.

## Safety Rule

Do not make "universal compression" claims without benchmark proof on established corpora and transparent accounting.

## Losslessness Rule

Every codec path must round-trip exactly. Reversibility is mandatory.

## MDL Rule

Always count the full transmitted cost:

- model cost
- headers and metadata
- anchors or indices
- residuals
- fallback/raw cost

## Benchmark Rule

Random bytes must always be included as a sanity check. A transform that loses to raw storage on random data is behaving normally, not failing.

## Agent Workflow

- Make small diffs.
- Run tests after every meaningful change.
- Do not run git write commands unless explicitly permitted.
- Forbidden git write commands include `git add`, `git commit`, `git push`, `git reset`, and `git checkout`.
- Allowed read-only git commands for snapshot generation, status reports, and diff inspection include `git status`, `git diff`, `git diff --stat`, `git rev-parse`, `git branch --show-current`, and `git ls-files`.
- Do not create local shims for third-party tools such as pytest. If a required tool is missing, report the dependency and the exact install command.
- Report changed files and test results clearly.
- Use `NEXT_AGENT.md` as the single authoritative handoff file for the next Codex agent.
- `NEXT_ORCHESTRATOR.md` is the strategic handoff for the next Orchestrator and should not be casually overwritten by the Worker.
- Do not create `NEXT_PROMPT.md`, `NEXT_PROMPT2.md`, `NEXT_PROMPT3.md`, or similar chains of prompt files.
- When preparing a handoff, overwrite `NEXT_AGENT.md` with the current state and the current next task.
- During an explicit closing or handoff task, update both `NEXT_AGENT.md` and `NEXT_ORCHESTRATOR.md` when the session is expected to continue.
- After the handoff is consumed, the file may be deleted or replaced, but there should still be only one active handoff file at a time.

## Analytic Programming

- In this repository, "Analytic programming" means structured communication aimed at an orchestrator-style workflow.
- `AP_ORCHESTRATOR.md` is the orchestrator-side doctrine that complements `AP_WORKER.md`.
- When useful, provide a complete, explicit operational report instead of a casual summary.
- Prefer a stable report heading such as `### Report for ORCHESTRATOR_CHAT` when the work benefits from machine-readable handoff or orchestration.
- Explain the real state, the safety checks, the commands run, the outputs that matter, and the remaining risks.
- Do not fake success, hidden work, or compression wins.
- If a future Codex agent continues the project, assume this communication style is preferred unless the user asks otherwise.

## Analytic Coding Repo Snapshot Protocol

- After a meaningful change, the worker should run `fish scripts/ap_snapshot.fish --run-tests`.
- `BRAIN.md` is the detailed repository snapshot for an Orchestrator or follow-on worker.
- `BOOT.md` is the shorter boot summary for fast context loading.
- These snapshot files do not replace tests.
- These snapshot files must not be used as evidence of compression performance.
- Read-only git commands are allowed for snapshot generation, status reports, and diff inspection.
- Git write commands remain forbidden unless explicitly permitted.

## Coordinator Protocol

- Coordinator Protocol is the file-based RPC extension on top of Analytic Programming.
- The repository remains the source of truth; chat and snapshots remain supporting artifacts.
- RPC scratch directories live under `.ap/rpc/` and are created on demand.
- Read-only RPC methods such as `repo.status`, `repo.diff_stat`, `repo.list_files`, and `repo.get_file` are allowed by default.
- Write RPC is forbidden unless the explicit task permits it.
- Secrets access, network access, and git write commands remain forbidden.
- Targeted RPC fetches are preferred when the Orchestrator needs one file or one bounded state view instead of a full diff dump.

## Architecture Phases

1. deterministic baseline and bit accounting
2. prime-anchor exploratory transform
3. GP-lite indexed anchor law search
4. modular optimizer architecture
5. GUI research cockpit
6. entropy coding backend
7. symbolic-regression-discovered anchors
8. benchmark suite

## GP-lite Indexed Anchor Law Search

- Evolve small decoder-known anchor laws `A(i)` for the index-plus-residual branch.
- Always count law model bits, parameter bits, index bits, residual bits, flags, headers, and escapes.
- A law is only interesting when full transmitted cost beats raw fallback.
- Keep this branch separate from predictor-only experiments.
- Do not introduce PySR or heavier symbolic regression dependencies at this stage.

## Scaled Prime-index Branch

- The scaled prime-index experiment packs bytes into larger Python integer blocks and tests `x = prev_prime(index << shift) + diff`.
- The decoder must reconstruct the prime anchor deterministically from the transmitted index and model parameters.
- Exact primality in this branch is currently limited to `width_bits <= 64`.
- Do not pretend that arbitrary-size primality is implemented when it is not.
- Always count model bits, parameter bits, headers, flags, index bits, residual codec bits, and raw escapes.
- Random-data losses are expected and must be reported honestly.

## Huge Anchor Portfolio

- The huge anchor portfolio generalizes the same index-plus-diff idea across multiple anchor families.
- Every family must still satisfy exact-lossless decode from transmitted model parameters, indices, residuals, flags, and raw escapes.
- `scaled_prime` is only one family and must compete against simpler families such as `linear_shift`, `affine_shift`, `multiple`, and `square`.
- Synthetic favorable datasets are valid mechanism checks, not proof of broad usefulness.
- Random bytes remain a mandatory sanity baseline.
- A portfolio win only matters when the full transmitted cost beats raw storage after honest accounting.

## Huge-anchor Binary Proof-of-concept

- Distinguish estimated accounting from actual byte output.
- `estimated_total_bits` are useful for search, but `actual_bits = len(compressed_bytes) * 8` are the stronger evidence.
- A synthetic actual-byte win only proves that one exact binary path can emit a smaller blob for compatible generated structure.
- Random bytes must remain in the report and must not be dressed up as a fake compression win.
- If the binary container loses to raw bytes, report the loss honestly.

## Actual-size Reranking

- Use estimated MDL cost as a search heuristic, not as the final binary truth.
- For the huge-anchor binary path, rerank top estimated candidates by real `compressed_bytes` when the task calls for actual-size selection.
- If estimated and actual winners diverge, report the divergence explicitly.
- Actual byte size is the stronger proof because it includes real container overhead.

## Optimizer Architecture

- Keep optimizer names and registry wiring explicit and testable.
- Do not pretend placeholder optimizers are implemented.
- Reuse shared accounting and roundtrip machinery across optimizer families whenever possible.
- Compare optimizers on the same raw-bit baseline and the same MDL-style accounting.

## Image-aware Search Optimizers

- `Image-predictor` is the manual fairness baseline for small grayscale image experiments.
- `Image-GP-lite` searches tiny decoder-known expression trees over 2D pixel context.
- `Image-SOMA` tunes a fixed-point linear 2D predictor over the same decoder-known context.
- All image-aware branches must reuse the shared residual codec layer.
- A synthetic dataset win matters only when `total_bits < raw_bits` after full accounting.
- Synthetic image wins are debugging and research signals, not proof of universal compression.

## Image-GP-lite Primitive Ablations

- `local` means only decoder-known neighborhood context.
- `ramp` means local context plus procedural coordinate ramps.
- `structure` means ramp context plus explicit block/parity primitives.
- Checker-like wins under `structure` are valid only as primitive baselines and must be reported as such.
- Any image GP benchmark that omits the primitive set label is incomplete and not safely comparable.

## Residual Codec Layer

- Predictors and anchor laws both create residual streams.
- Residual streams should be costed through shared deterministic codec candidates when possible.
- Fixed-width signed residuals are a baseline, not a permanent truth.
- Zero-run-length coding is a valid small baseline for sparse residual streams.
- Byte-RLE is a valid baseline for raw-like repeated byte streams.
- Do not call this entropy coding or pretend it is ANS/arithmetic coding.
- Exact roundtrip remains mandatory for any residual codec path.

## GUI Research Cockpit

- The GUI is for small deterministic research simulations, not benchmark theater.
- Prefer generated grayscale datasets first because they are cheap, reproducible, and headless-test friendly.
- If Tkinter is missing, report that the system package `tk` is needed instead of vendoring UI code.

## Handoff File

- `NEXT_AGENT.md` must contain the most important current context for the next Codex agent continuing this repository.
- The file should summarize architecture, hard rules, current test status, known limitations, and the exact next requested task.
- Keep it current. Replace stale handoff content instead of accumulating multiple prompt files.
