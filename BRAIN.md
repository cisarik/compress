# BRAIN.md — Analytic Coding Repository Snapshot

## 2. Timestamp

- Generated: `2026-06-12T10:41:28+02:00`

## 3. Repo Root

- Repo root: `/home/agile/compress`

## 4. Branch

- Branch: `main`

## 5. HEAD Commit

- HEAD: `463787c1d4bbd2677b9b8913b170b7b4c078e44e`

## 6. Python Info

- command -v python: `/usr/bin/python`
- python --version: `Python 3.14.5`
- which python: `/usr/bin/python`
- sys.executable: `/usr/bin/python`
- sys.prefix: `/usr`
- .venv exists: `yes`
- active python inside .venv: `no`

> WARNING: .venv exists but active python is not the project virtual environment.

## 7. Git Status

```text
 M AP.md
 M AP_ORCHESTRATOR.md
 M AP_WORKER.md
 M COORDINATOR_PROTOCOL.md
 M README.md
```

## 8. Diff Stat

```text
 AP.md                   | 64 ++++++++++++++++++++++++++++++++++++++++++++-----
 AP_ORCHESTRATOR.md      | 42 ++++++++++++++++++++++++++++++++
 AP_WORKER.md            | 31 ++++++++++++++++++++----
 COORDINATOR_PROTOCOL.md | 10 ++++++++
 README.md               |  1 +
 5 files changed, 137 insertions(+), 11 deletions(-)
```

## 9. Full Diff

```diff
diff --git a/AP.md b/AP.md
index 10eed0c..1b28b7d 100644
--- a/AP.md
+++ b/AP.md
@@ -2,25 +2,33 @@
 
 ## Short Definition
 
-Analytic Programming in this repository is a repo-centered multi-agent workflow where the repository is the ground truth, the diff is the unit of progress, tests are the minimum proof, and explicit artifacts preserve state between User, Orchestrator, and Worker loops.
+Analytic Programming in this repository is a repo-centered multi-agent workflow where the repository is the ground truth, the diff is the unit of progress, tests are the minimum proof, and explicit artifacts preserve state between COOPERATOR, Orchestrator, and Worker loops.
 
 The goal is not more prose.
 The goal is lower context loss, safer delegation, clearer handoff, and less fake progress.
 
 ## Roles
 
-### User
+### COOPERATOR
 
-- sets direction, priorities, and constraints
+The COOPERATOR is the human strategic coordinator.
+
+- owns intent, direction, risk tolerance, and final judgment
+- sets priorities and constraints
 - decides when a risk is acceptable
 - intervenes when the workflow needs strategy correction
+- may reshape the protocol itself through explicit AP/meta tasks
+- is not expected to manually remember all repository state; AP artifacts exist to reduce that burden
+
+In older notes, this role may appear as "User". In this repository, `COOPERATOR` is the preferred name.
 
 ### Orchestrator
 
 - reads the repo state and current artifacts
 - shapes the next bounded task for the Worker
 - keeps scope coherent and prevents drift
-- decides when escalation to the User is necessary
+- decides when escalation to the COOPERATOR is necessary
+- may propose doctrine or handoff updates after evaluating Worker reports
 
 ### Worker
 
@@ -29,6 +37,27 @@ The goal is lower context loss, safer delegation, clearer handoff, and less fake
 - validates with tests and commands
 - reports the real outcome
 - refreshes snapshots when the step is meaningful
+- may recommend doctrine updates in reports, but changes doctrine only in explicit bounded AP/meta tasks
+
+## Living Protocol Artifacts
+
+AP documentation is not a frozen essay set.
+
+These files are living, repo-visible protocol and doctrine artifacts:
+
+- `AP.md` = system-wide Analytic Programming protocol
+- `AP_WORKER.md` = Worker-side operating doctrine
+- `AP_ORCHESTRATOR.md` = Orchestrator-side planning and evaluation doctrine
+
+They may evolve as the project learns, but only through explicit, bounded AP/meta tasks.
+
+Rules:
+
+- changes must be repo-visible, inspectable, and report-backed
+- doctrine must not be rewritten silently during unrelated coding tasks
+- the Orchestrator may propose updates after evaluating Worker reports
+- the Worker may implement doctrine updates only when explicitly asked in a bounded AP/meta task
+- repository files remain the source of truth; chat memory is not
 
 ## Artifact Ownership
 
@@ -46,9 +75,22 @@ The goal is lower context loss, safer delegation, clearer handoff, and less fake
 Each artifact should have one dominant purpose.
 Do not spread the same truth across many files without clear ownership.
 
+## Handoff Artifact Separation
+
+- `NEXT_AGENT.md` = immediate next Worker task
+- `NEXT_ORCHESTRATOR.md` = strategic continuation for the next Orchestrator
+
+These files must not be conflated.
+
+`NEXT_AGENT.md` should stay narrow, actionable, and Worker-focused.
+
+`NEXT_ORCHESTRATOR.md` should stay strategic, contextual, and Orchestrator-focused.
+
+Closing a serious AP session should update both when future continuation is expected.
+
 ## Operating Loop
 
-1. User provides intent and constraints.
+1. COOPERATOR provides intent and constraints.
 2. Orchestrator shapes the next bounded task.
 3. Worker inspects the repo and relevant artifacts.
 4. Worker makes the smallest useful change.
@@ -88,7 +130,17 @@ Safety rules:
 - write RPC is forbidden unless the task explicitly permits it
 - secrets access, network access, and git write commands remain forbidden
 
-Closing a serious AP session should update both the Worker handoff and the Orchestrator handoff when future continuation is expected.
+Planned controlled write-RPC for AP and handoff artifacts is conceptual only unless implemented in the repository.
+
+Candidate future methods include:
+
+- `update_ap_worker`
+- `update_ap_orchestrator`
+- `update_next_agent`
+- `update_next_orchestrator`
+
+Such methods are not implemented in the current proof-of-concept RPC surface.
+They would need explicit COOPERATOR authority, bounded scope, and full repo auditability before adoption.
 
 ## Git Rules
 
diff --git a/AP_ORCHESTRATOR.md b/AP_ORCHESTRATOR.md
index 400182f..d19d32c 100644
--- a/AP_ORCHESTRATOR.md
+++ b/AP_ORCHESTRATOR.md
@@ -118,6 +118,48 @@ Core rule:
 
 - If a file can answer the question, request the file instead of guessing.
 
+### Planned Controlled Write-RPC
+
+The current repository implements read-only RPC methods only.
+
+Write-RPC remains forbidden unless an explicit task permits it.
+
+Future controlled write-RPC may allow structured, auditable updates to AP and handoff artifacts.
+
+Conceptual candidate methods:
+
+- `update_ap_worker`
+- `update_ap_orchestrator`
+- `update_next_agent`
+- `update_next_orchestrator`
+
+These methods are not implemented in the current proof-of-concept RPC surface.
+
+If adopted later, they must:
+
+- preserve COOPERATOR authority over strategic direction
+- remain repo-visible and diff-inspectable
+- use bounded, explicit task permission
+- avoid silent doctrine drift or hidden memory substitutes
+
+## Orchestrator Doctrine Evolution
+
+`AP_ORCHESTRATOR.md` is a living Orchestrator-side doctrine artifact.
+
+The Orchestrator may update its project-specific understanding after evaluating Worker reports.
+
+Rules:
+
+- convert learning into bounded Worker prompts, not hidden chat memory
+- doctrine changes should be explicit and repo-visible
+- do not silently rely on hidden memory when the repository can store the doctrine
+- after significant Worker reports, decide whether `AP.md`, `AP_WORKER.md`, `AP_ORCHESTRATOR.md`, `NEXT_AGENT.md`, or `NEXT_ORCHESTRATOR.md` need updating
+- propose or schedule doctrine updates through explicit AP/meta tasks when the Worker is not already tasked with them
+
+The Orchestrator remains planning-focused.
+
+Doctrine evolution is how the system learns without losing auditability.
+
 ## Prompt Construction Rules
 
 - every prompt must include the working directory
diff --git a/AP_WORKER.md b/AP_WORKER.md
index 8c1d7c6..89b9b0e 100644
--- a/AP_WORKER.md
+++ b/AP_WORKER.md
@@ -37,20 +37,23 @@ This is controlled stateful engineering with explicit memory and explicit accoun
 
 ## Roles
 
-### User
+### COOPERATOR
 
-The user is the strategic authority.
+The COOPERATOR is the human strategic coordinator.
 
-The user decides:
+The COOPERATOR decides:
 
 - what matters
 - when priorities change
 - when a risk is acceptable
 - when the system should go deeper or stop
+- when protocol or doctrine should change
 
-The user should not need to manually reconstruct the whole repo state from memory after every step.
+The COOPERATOR should not need to manually reconstruct the whole repo state from memory after every step.
 AP exists partly to remove that burden.
 
+In older notes, this role may appear as "User". In this repository, `COOPERATOR` is the preferred name.
+
 ### Orchestrator
 
 The orchestrator is the task-shaping layer.
@@ -59,7 +62,7 @@ Its job is to:
 
 - read the current repo state
 - read current snapshot artifacts
-- understand the user's goal
+- understand the COOPERATOR's goal
 - decompose the next step into a precise worker task
 - keep scope bounded
 - prevent drift
@@ -561,6 +564,24 @@ So even with direct agent-to-agent messaging, the repo artifacts should remain f
 
 This loop is the practical core of AP.
 
+## Worker Doctrine Evolution
+
+`AP_WORKER.md` is a living Worker-side doctrine artifact, not a frozen manifesto.
+
+The Worker may refine this project-specific operating doctrine when explicitly tasked in a bounded AP/meta session.
+
+Rules:
+
+- doctrine changes must be small, justified, and report-backed
+- the Worker must not rewrite its own rules silently as part of unrelated coding tasks
+- if the Worker discovers repeated ambiguity, safety risk, or handoff confusion, it may recommend an `AP_WORKER.md` update in its report
+- the actual doctrine update should happen in a bounded AP/meta task unless the prompt explicitly permits it during the current task
+- repository files remain the source of truth; chat memory is not
+
+The Worker remains execution-focused.
+
+Doctrine evolution is a controlled exception, not a license to drift into meta work during compression or implementation tasks.
+
 ## Coordinator Protocol
 
 Coordinator Protocol is the file-mediated RPC layer on top of AP.
diff --git a/COORDINATOR_PROTOCOL.md b/COORDINATOR_PROTOCOL.md
index dc1b9c0..66fc5c3 100644
--- a/COORDINATOR_PROTOCOL.md
+++ b/COORDINATOR_PROTOCOL.md
@@ -151,4 +151,14 @@ Candidate follow-up methods:
 - `task.set`
 - `handoff.build`
 
+Planned controlled write-RPC for AP and handoff artifacts may later include:
+
+- `update_ap_worker`
+- `update_ap_orchestrator`
+- `update_next_agent`
+- `update_next_orchestrator`
+
+These write methods are conceptual only in the current repository.
+They are not implemented in the current read-only RPC surface.
+
 These should remain bounded, inspectable, and explicit about safety before any write-capable expansion is allowed.
diff --git a/README.md b/README.md
index 90fa54e..3671092 100644
--- a/README.md
+++ b/README.md
@@ -233,6 +233,7 @@ fish scripts/ap_cycle_close.fish --message "..." --tldr "..."
 
 AP artifact roles:
 
+- `AP.md`, `AP_WORKER.md`, and `AP_ORCHESTRATOR.md` are living, repo-visible protocol and doctrine artifacts that may evolve through explicit AP/meta tasks.
 - `AP.md` is the system-wide protocol.
 - `COORDINATOR_PROTOCOL.md` extends AP with file-based RPC.
 - `AP_ORCHESTRATOR.md` explains the orchestrator-side discipline.
```

## 10. Test Output

- Test status: `passed`
- Test runner: `project virtual environment python -m pytest -q`

```text
........................................................................ [ 25%]
........................................................................ [ 51%]
........................................................................ [ 77%]
.............................................................            [100%]
277 passed in 119.91s (0:01:59)
```

## 11. Relevant File Tree

- `AGENTS.md` (9904 bytes)
- `AP.md` (6847 bytes)
- `AP_WORKER.md` (16573 bytes)
- `CHAT.md` (27677 bytes)
- `COORDINATOR_PROTOCOL.md` (5000 bytes)
- `docs/research_plan.md` (7097 bytes)
- `.gitignore` (663 bytes)
- `pyproject.toml` (481 bytes)
- `README.md` (13431 bytes)
- `scripts/ap_chat_append.fish` (3258 bytes)
- `scripts/ap_cycle_close.fish` (7131 bytes)
- `scripts/ap_rpc_call.fish` (2224 bytes)
- `scripts/ap_rpc_handle_next.fish` (2764 bytes)
- `scripts/ap_rpc_request.fish` (2156 bytes)
- `scripts/ap_snapshot.fish` (11453 bytes)
- `src/primesymbolicmdl/anchor_laws.py` (6188 bytes)
- `src/primesymbolicmdl/ap_rpc.py` (12732 bytes)
- `src/primesymbolicmdl/bitcost.py` (4143 bytes)
- `src/primesymbolicmdl/bitstream.py` (5249 bytes)
- `src/primesymbolicmdl/blocks.py` (1612 bytes)
- `src/primesymbolicmdl/codec.py` (2739 bytes)
- `src/PrimeSymbolicMDL.egg-info/dependency_links.txt` (1 bytes)
- `src/PrimeSymbolicMDL.egg-info/PKG-INFO` (11805 bytes)
- `src/PrimeSymbolicMDL.egg-info/requires.txt` (14 bytes)
- `src/PrimeSymbolicMDL.egg-info/SOURCES.txt` (3353 bytes)
- `src/PrimeSymbolicMDL.egg-info/top_level.txt` (17 bytes)
- `src/primesymbolicmdl/evolution.py` (11032 bytes)
- `src/primesymbolicmdl/experiments.py` (4680 bytes)
- `src/primesymbolicmdl/gui.py` (29699 bytes)
- `src/primesymbolicmdl/huge_anchor_binary_demo.py` (3330 bytes)
- `src/primesymbolicmdl/huge_anchor_binary.py` (20537 bytes)
- `src/primesymbolicmdl/huge_anchor_branch.py` (12350 bytes)
- `src/primesymbolicmdl/huge_anchor_datasets.py` (2697 bytes)
- `src/primesymbolicmdl/huge_anchor_demo.py` (4000 bytes)
- `src/primesymbolicmdl/huge_anchor_file_benchmark.py` (4369 bytes)
- `src/primesymbolicmdl/huge_anchor_file_cli.py` (3145 bytes)
- `src/primesymbolicmdl/huge_anchor_file.py` (5182 bytes)
- `src/primesymbolicmdl/huge_anchor_models.py` (6808 bytes)
- `src/primesymbolicmdl/huge_anchor_search.py` (6378 bytes)
- `src/primesymbolicmdl/huge_blocks.py` (1722 bytes)
- `src/primesymbolicmdl/image_ablation.py` (3138 bytes)
- `src/primesymbolicmdl/image_context_laws.py` (14012 bytes)
- `src/primesymbolicmdl/image_datasets.py` (3122 bytes)
- `src/primesymbolicmdl/image_law_branch.py` (7422 bytes)
- `src/primesymbolicmdl/image_predictor_branch.py` (7406 bytes)
- `src/primesymbolicmdl/image_predictors.py` (4121 bytes)
- `src/primesymbolicmdl/index_branch.py` (6703 bytes)
- `src/primesymbolicmdl/__init__.py` (188 bytes)
- `src/primesymbolicmdl/law_demo.py` (1365 bytes)
- `src/primesymbolicmdl/law_search.py` (11824 bytes)
- `src/primesymbolicmdl/optimizers/base.py` (1133 bytes)
- `src/primesymbolicmdl/optimizers/gplite_adapter.py` (1811 bytes)
- `src/primesymbolicmdl/optimizers/image_gplite.py` (18472 bytes)
- `src/primesymbolicmdl/optimizers/image_predictor.py` (3577 bytes)
- `src/primesymbolicmdl/optimizers/image_soma.py` (19187 bytes)
- `src/primesymbolicmdl/optimizers/__init__.py` (343 bytes)
- `src/primesymbolicmdl/optimizers/placeholders.py` (1855 bytes)
- `src/primesymbolicmdl/optimizers/registry.py` (1354 bytes)
- `src/primesymbolicmdl/optimizers/soma.py` (9779 bytes)
- `src/primesymbolicmdl/prime_anchors.py` (3973 bytes)
- `src/primesymbolicmdl/prime_bigint.py` (2225 bytes)
- `src/primesymbolicmdl/residual_binary.py` (6185 bytes)
- `src/primesymbolicmdl/residual_codecs.py` (11387 bytes)
- `src/primesymbolicmdl/scaled_prime_demo.py` (2717 bytes)
- `src/primesymbolicmdl/scaled_prime_index.py` (12579 bytes)
- `src/primesymbolicmdl/scaled_prime_search.py` (4203 bytes)
- `src/primesymbolicmdl/sim_demo.py` (1843 bytes)
- `src/primesymbolicmdl/simulation.py` (13361 bytes)
- `tests/conftest.py` (299 bytes)
- `tests/test_anchor_laws.py` (1553 bytes)
- `tests/test_ap_rpc.py` (2981 bytes)
- `tests/test_bitcost.py` (1020 bytes)
- `tests/test_bitstream.py` (1606 bytes)
- `tests/test_blocks.py` (1047 bytes)
- `tests/test_codec_roundtrip.py` (1295 bytes)
- `tests/test_evolution.py` (1930 bytes)
- `tests/test_experiments.py` (1648 bytes)
- `tests/test_gui_import.py` (714 bytes)
- `tests/test_huge_anchor_binary_demo.py` (990 bytes)
- `tests/test_huge_anchor_binary.py` (4823 bytes)
- `tests/test_huge_anchor_branch.py` (3273 bytes)
- `tests/test_huge_anchor_datasets.py` (828 bytes)
- `tests/test_huge_anchor_demo.py` (811 bytes)
- `tests/test_huge_anchor_file_benchmark.py` (995 bytes)
- `tests/test_huge_anchor_file_cli.py` (5679 bytes)
- `tests/test_huge_anchor_models.py` (1661 bytes)
- `tests/test_huge_anchor_search.py` (2415 bytes)
- `tests/test_huge_blocks.py` (1456 bytes)
- `tests/test_image_ablation.py` (1103 bytes)
- `tests/test_image_context_laws.py` (4263 bytes)
- `tests/test_image_datasets.py` (913 bytes)
- `tests/test_image_gplite_optimizer.py` (4295 bytes)
- `tests/test_image_law_branch.py` (1761 bytes)
- `tests/test_image_predictor_branch.py` (2847 bytes)
- `tests/test_image_predictor_optimizer.py` (1411 bytes)
- `tests/test_image_predictors.py` (2082 bytes)
- `tests/test_image_soma_optimizer.py` (2395 bytes)
- `tests/test_index_branch.py` (2259 bytes)
- `tests/test_law_demo.py` (496 bytes)
- `tests/test_law_search.py` (2049 bytes)
- `tests/test_optimizers.py` (3012 bytes)
- `tests/test_prime_anchors.py` (1542 bytes)
- `tests/test_prime_bigint.py` (1485 bytes)
- `tests/test_random_sanity.py` (403 bytes)
- `tests/test_repository_rules.py` (175 bytes)
- `tests/test_residual_binary.py` (1508 bytes)
- `tests/test_residual_codecs.py` (2212 bytes)
- `tests/test_scaled_prime_demo.py` (718 bytes)
- `tests/test_scaled_prime_index.py` (2920 bytes)
- `tests/test_scaled_prime_search.py` (1528 bytes)
- `tests/test_sim_demo.py` (676 bytes)
- `tests/test_simulation.py` (5996 bytes)

## 12. Selected File Contents

## File: `AGENTS.md`

```markdown
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
```

## File: `AP.md`

```markdown
# AP.md — Analytic Programming Protocol

## Short Definition

Analytic Programming in this repository is a repo-centered multi-agent workflow where the repository is the ground truth, the diff is the unit of progress, tests are the minimum proof, and explicit artifacts preserve state between COOPERATOR, Orchestrator, and Worker loops.

The goal is not more prose.
The goal is lower context loss, safer delegation, clearer handoff, and less fake progress.

## Roles

### COOPERATOR

The COOPERATOR is the human strategic coordinator.

- owns intent, direction, risk tolerance, and final judgment
- sets priorities and constraints
- decides when a risk is acceptable
- intervenes when the workflow needs strategy correction
- may reshape the protocol itself through explicit AP/meta tasks
- is not expected to manually remember all repository state; AP artifacts exist to reduce that burden

In older notes, this role may appear as "User". In this repository, `COOPERATOR` is the preferred name.

### Orchestrator

- reads the repo state and current artifacts
- shapes the next bounded task for the Worker
- keeps scope coherent and prevents drift
- decides when escalation to the COOPERATOR is necessary
- may propose doctrine or handoff updates after evaluating Worker reports

### Worker

- inspects the real codebase
- makes the smallest useful change
- validates with tests and commands
- reports the real outcome
- refreshes snapshots when the step is meaningful
- may recommend doctrine updates in reports, but changes doctrine only in explicit bounded AP/meta tasks

## Living Protocol Artifacts

AP documentation is not a frozen essay set.

These files are living, repo-visible protocol and doctrine artifacts:

- `AP.md` = system-wide Analytic Programming protocol
- `AP_WORKER.md` = Worker-side operating doctrine
- `AP_ORCHESTRATOR.md` = Orchestrator-side planning and evaluation doctrine

They may evolve as the project learns, but only through explicit, bounded AP/meta tasks.

Rules:

- changes must be repo-visible, inspectable, and report-backed
- doctrine must not be rewritten silently during unrelated coding tasks
- the Orchestrator may propose updates after evaluating Worker reports
- the Worker may implement doctrine updates only when explicitly asked in a bounded AP/meta task
- repository files remain the source of truth; chat memory is not

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

## Handoff Artifact Separation

- `NEXT_AGENT.md` = immediate next Worker task
- `NEXT_ORCHESTRATOR.md` = strategic continuation for the next Orchestrator

These files must not be conflated.

`NEXT_AGENT.md` should stay narrow, actionable, and Worker-focused.

`NEXT_ORCHESTRATOR.md` should stay strategic, contextual, and Orchestrator-focused.

Closing a serious AP session should update both when future continuation is expected.

## Operating Loop

1. COOPERATOR provides intent and constraints.
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

Planned controlled write-RPC for AP and handoff artifacts is conceptual only unless implemented in the repository.

Candidate future methods include:

- `update_ap_worker`
- `update_ap_orchestrator`
- `update_next_agent`
- `update_next_orchestrator`

Such methods are not implemented in the current proof-of-concept RPC surface.
They would need explicit COOPERATOR authority, bounded scope, and full repo auditability before adoption.

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
```

## File: `AP_WORKER.md`

```markdown
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

### COOPERATOR

The COOPERATOR is the human strategic coordinator.

The COOPERATOR decides:

- what matters
- when priorities change
- when a risk is acceptable
- when the system should go deeper or stop
- when protocol or doctrine should change

The COOPERATOR should not need to manually reconstruct the whole repo state from memory after every step.
AP exists partly to remove that burden.

In older notes, this role may appear as "User". In this repository, `COOPERATOR` is the preferred name.

### Orchestrator

The orchestrator is the task-shaping layer.

Its job is to:

- read the current repo state
- read current snapshot artifacts
- understand the COOPERATOR's goal
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

## Worker Doctrine Evolution

`AP_WORKER.md` is a living Worker-side doctrine artifact, not a frozen manifesto.

The Worker may refine this project-specific operating doctrine when explicitly tasked in a bounded AP/meta session.

Rules:

- doctrine changes must be small, justified, and report-backed
- the Worker must not rewrite its own rules silently as part of unrelated coding tasks
- if the Worker discovers repeated ambiguity, safety risk, or handoff confusion, it may recommend an `AP_WORKER.md` update in its report
- the actual doctrine update should happen in a bounded AP/meta task unless the prompt explicitly permits it during the current task
- repository files remain the source of truth; chat memory is not

The Worker remains execution-focused.

Doctrine evolution is a controlled exception, not a license to drift into meta work during compression or implementation tasks.

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
```

## File: `CHAT.md`

```markdown
# CHAT.md — Analytic Programming Coordination Ledger

Append-only coordination log for User, Orchestrator, and Worker.

## 2026-06-11T19:07:23+02:00 | role=worker

Message:
Validated AP chat append script.

TLDR:
- CHAT.md append path works.

Commands run:
- fish scripts/ap_chat_append.fish --role worker --message "..." --tldr "..."

Files changed:
- scripts/ap_chat_append.fish

## 2026-06-11T19:07:36+02:00 | role=worker

Message:
Validated Analytic Programming workflow hardening artifacts.  Cycle close result: tests passed and snapshot refreshed.

TLDR:
- AP.md, chat append, cycle close, and snapshot env diagnostics are in place. Test status: passed Snapshot status: generated

Commands run:
- python -m pytest -q fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_residual_codecs.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T19:08:46+02:00 | role=worker

Message:
Polished AP cycle close chat formatting. Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Cycle-close chat payload now stays single-line and deterministic. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_residual_codecs.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T19:14:35+02:00 | role=worker

Message:
Manual AP cycle verification Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Manual verification after AP hardening. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- docs/research_plan.md
- .gitignore
- README.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_residual_codecs.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T20:08:59+02:00 | role=worker

Message:
Added image-aware GP-lite and SOMA optimizers Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added Image-GP-lite and Image-SOMA over 2D pixel context with residual codec accounting. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_gui_import.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_residual_codecs.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T20:21:28+02:00 | role=worker

Message:
Added Image-GP-lite primitive ablations Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added image structure primitives and ablation benchmark for Image-GP-lite. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_gui_import.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_residual_codecs.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T22:06:22+02:00 | role=worker

Message:
Added Coordinator Protocol RPC proof of concept Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added file-based RPC for repo.status, repo.diff_stat, repo.list_files, and repo.get_file. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_gui_import.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_residual_codecs.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T22:29:07+02:00 | role=worker

Message:
Added scaled prime-index branch Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added huge-number block packing and scaled prime-index plus diff experiment with exact 64-bit prime anchors. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/huge_blocks.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/prime_bigint.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/scaled_prime_demo.py
- src/primesymbolicmdl/scaled_prime_index.py
- src/primesymbolicmdl/scaled_prime_search.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_gui_import.py
- tests/test_huge_blocks.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_prime_bigint.py
- tests/test_residual_codecs.py
- tests/test_scaled_prime_demo.py
- tests/test_scaled_prime_index.py
- tests/test_scaled_prime_search.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T22:45:49+02:00 | role=worker

Message:
Added huge anchor portfolio benchmark Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added general index-plus-diff anchor families and synthetic datasets to compare against scaled prime anchors. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/huge_anchor_branch.py
- src/primesymbolicmdl/huge_anchor_datasets.py
- src/primesymbolicmdl/huge_anchor_demo.py
- src/primesymbolicmdl/huge_anchor_models.py
- src/primesymbolicmdl/huge_anchor_search.py
- src/primesymbolicmdl/huge_blocks.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/prime_bigint.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/scaled_prime_demo.py
- src/primesymbolicmdl/scaled_prime_index.py
- src/primesymbolicmdl/scaled_prime_search.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_gui_import.py
- tests/test_huge_anchor_branch.py
- tests/test_huge_anchor_datasets.py
- tests/test_huge_anchor_demo.py
- tests/test_huge_anchor_models.py
- tests/test_huge_anchor_search.py
- tests/test_huge_blocks.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_prime_bigint.py
- tests/test_residual_codecs.py
- tests/test_scaled_prime_demo.py
- tests/test_scaled_prime_index.py
- tests/test_scaled_prime_search.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T23:02:25+02:00 | role=worker

Message:
Added huge-anchor binary compression proof Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added actual bitstream container for huge-anchor payloads and demonstrated exact compressed bytes on synthetic datasets. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/bitstream.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/huge_anchor_binary.py
- src/primesymbolicmdl/huge_anchor_binary_demo.py
- src/primesymbolicmdl/huge_anchor_branch.py
- src/primesymbolicmdl/huge_anchor_datasets.py
- src/primesymbolicmdl/huge_anchor_demo.py
- src/primesymbolicmdl/huge_anchor_models.py
- src/primesymbolicmdl/huge_anchor_search.py
- src/primesymbolicmdl/huge_blocks.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/prime_bigint.py
- src/primesymbolicmdl/residual_binary.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/scaled_prime_demo.py
- src/primesymbolicmdl/scaled_prime_index.py
- src/primesymbolicmdl/scaled_prime_search.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_bitstream.py
- tests/test_gui_import.py
- tests/test_huge_anchor_binary.py
- tests/test_huge_anchor_binary_demo.py
- tests/test_huge_anchor_branch.py
- tests/test_huge_anchor_datasets.py
- tests/test_huge_anchor_demo.py
- tests/test_huge_anchor_models.py
- tests/test_huge_anchor_search.py
- tests/test_huge_blocks.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_prime_bigint.py
- tests/test_residual_binary.py
- tests/test_residual_codecs.py
- tests/test_scaled_prime_demo.py
- tests/test_scaled_prime_index.py
- tests/test_scaled_prime_search.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T23:16:49+02:00 | role=worker

Message:
Added actual-size reranking for huge-anchor binary compression Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Top estimated huge-anchor candidates are now serialized and reranked by real compressed byte size. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/bitstream.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/huge_anchor_binary.py
- src/primesymbolicmdl/huge_anchor_binary_demo.py
- src/primesymbolicmdl/huge_anchor_branch.py
- src/primesymbolicmdl/huge_anchor_datasets.py
- src/primesymbolicmdl/huge_anchor_demo.py
- src/primesymbolicmdl/huge_anchor_models.py
- src/primesymbolicmdl/huge_anchor_search.py
- src/primesymbolicmdl/huge_blocks.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/prime_bigint.py
- src/primesymbolicmdl/residual_binary.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/scaled_prime_demo.py
- src/primesymbolicmdl/scaled_prime_index.py
- src/primesymbolicmdl/scaled_prime_search.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_bitstream.py
- tests/test_gui_import.py
- tests/test_huge_anchor_binary.py
- tests/test_huge_anchor_binary_demo.py
- tests/test_huge_anchor_branch.py
- tests/test_huge_anchor_datasets.py
- tests/test_huge_anchor_demo.py
- tests/test_huge_anchor_models.py
- tests/test_huge_anchor_search.py
- tests/test_huge_blocks.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_prime_bigint.py
- tests/test_residual_binary.py
- tests/test_residual_codecs.py
- tests/test_scaled_prime_demo.py
- tests/test_scaled_prime_index.py
- tests/test_scaled_prime_search.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T23:37:57+02:00 | role=worker

Message:
Closed session with orchestrator doctrine and final handoff Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added AP_ORCHESTRATOR.md and refreshed NEXT_AGENT.md for the next Worker. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_ORCHESTRATOR.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/bitstream.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/huge_anchor_binary.py
- src/primesymbolicmdl/huge_anchor_binary_demo.py
- src/primesymbolicmdl/huge_anchor_branch.py
- src/primesymbolicmdl/huge_anchor_datasets.py
- src/primesymbolicmdl/huge_anchor_demo.py
- src/primesymbolicmdl/huge_anchor_models.py
- src/primesymbolicmdl/huge_anchor_search.py
- src/primesymbolicmdl/huge_blocks.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/prime_bigint.py
- src/primesymbolicmdl/residual_binary.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/scaled_prime_demo.py
- src/primesymbolicmdl/scaled_prime_index.py
- src/primesymbolicmdl/scaled_prime_search.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_bitstream.py
- tests/test_gui_import.py
- tests/test_huge_anchor_binary.py
- tests/test_huge_anchor_binary_demo.py
- tests/test_huge_anchor_branch.py
- tests/test_huge_anchor_datasets.py
- tests/test_huge_anchor_demo.py
- tests/test_huge_anchor_models.py
- tests/test_huge_anchor_search.py
- tests/test_huge_blocks.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_prime_bigint.py
- tests/test_residual_binary.py
- tests/test_residual_codecs.py
- tests/test_scaled_prime_demo.py
- tests/test_scaled_prime_index.py
- tests/test_scaled_prime_search.py
- tests/test_sim_demo.py
- tests/test_simulation.py

## 2026-06-11T23:47:02+02:00 | role=worker

Message:
Closed session with orchestrator handoff Status note: Cycle close result: tests passed and snapshot refreshed.

TLDR:
- Added NEXT_ORCHESTRATOR.md and documented orchestrator-side continuation strategy. | Test status: passed | Snapshot status: generated

Commands run:
- python -m pytest -q
- fish scripts/ap_snapshot.fish --run-tests

Files changed:
- .gitignore
- AGENTS.md
- AP.md
- AP_ORCHESTRATOR.md
- AP_WORKER.md
- CHAT.md
- COORDINATOR_PROTOCOL.md
- NEXT_ORCHESTRATOR.md
- README.md
- docs/research_plan.md
- scripts/ap_chat_append.fish
- scripts/ap_cycle_close.fish
- scripts/ap_rpc_call.fish
- scripts/ap_rpc_handle_next.fish
- scripts/ap_rpc_request.fish
- scripts/ap_snapshot.fish
- src/primesymbolicmdl/ap_rpc.py
- src/primesymbolicmdl/bitstream.py
- src/primesymbolicmdl/gui.py
- src/primesymbolicmdl/huge_anchor_binary.py
- src/primesymbolicmdl/huge_anchor_binary_demo.py
- src/primesymbolicmdl/huge_anchor_branch.py
- src/primesymbolicmdl/huge_anchor_datasets.py
- src/primesymbolicmdl/huge_anchor_demo.py
- src/primesymbolicmdl/huge_anchor_models.py
- src/primesymbolicmdl/huge_anchor_search.py
- src/primesymbolicmdl/huge_blocks.py
- src/primesymbolicmdl/image_ablation.py
- src/primesymbolicmdl/image_context_laws.py
- src/primesymbolicmdl/image_datasets.py
- src/primesymbolicmdl/image_law_branch.py
- src/primesymbolicmdl/image_predictor_branch.py
- src/primesymbolicmdl/image_predictors.py
- src/primesymbolicmdl/index_branch.py
- src/primesymbolicmdl/optimizers/base.py
- src/primesymbolicmdl/optimizers/gplite_adapter.py
- src/primesymbolicmdl/optimizers/image_gplite.py
- src/primesymbolicmdl/optimizers/image_predictor.py
- src/primesymbolicmdl/optimizers/image_soma.py
- src/primesymbolicmdl/optimizers/registry.py
- src/primesymbolicmdl/optimizers/soma.py
- src/primesymbolicmdl/prime_bigint.py
- src/primesymbolicmdl/residual_binary.py
- src/primesymbolicmdl/residual_codecs.py
- src/primesymbolicmdl/scaled_prime_demo.py
- src/primesymbolicmdl/scaled_prime_index.py
- src/primesymbolicmdl/scaled_prime_search.py
- src/primesymbolicmdl/sim_demo.py
- src/primesymbolicmdl/simulation.py
- tests/test_ap_rpc.py
- tests/test_bitstream.py
- tests/test_gui_import.py
- tests/test_huge_anchor_binary.py
- tests/test_huge_anchor_binary_demo.py
- tests/test_huge_anchor_branch.py
- tests/test_huge_anchor_datasets.py
- tests/test_huge_anchor_demo.py
- tests/test_huge_anchor_models.py
- tests/test_huge_anchor_search.py
- tests/test_huge_blocks.py
- tests/test_image_ablation.py
- tests/test_image_context_laws.py
- tests/test_image_gplite_optimizer.py
- tests/test_image_law_branch.py
- tests/test_image_predictor_branch.py
- tests/test_image_predictor_optimizer.py
- tests/test_image_predictors.py
- tests/test_image_soma_optimizer.py
- tests/test_index_branch.py
- tests/test_optimizers.py
- tests/test_prime_bigint.py
- tests/test_residual_binary.py
- tests/test_residual_codecs.py
- tests/test_scaled_prime_demo.py
- tests/test_scaled_prime_index.py
- tests/test_scaled_prime_search.py
- tests/test_sim_demo.py
- tests/test_simulation.py

```

## File: `COORDINATOR_PROTOCOL.md`

```markdown
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
```

## File: `docs/research_plan.md`

```markdown
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

## Residual Codec Layer

Predictors and anchor laws create residual streams.

- A residual stream should be evaluated through a shared codec layer, not hand-waved as a single hardcoded width forever.
- The current research layer now compares small deterministic candidates such as fixed-width signed residuals and zero-run-length coding.
- Raw-like byte streams can also be compared against a byte-RLE baseline.
- This is still not ANS or arithmetic coding.
- Exact roundtrip remains mandatory.

## GP-lite Indexed Anchor Law Search

This phase evolves small decoder-known anchor laws `A(i)` rather than only choosing from fixed hand-written anchor families.

- The encoder stores index `i` plus residual.
- The candidate law only matters when full transmitted cost beats raw fallback.
- This branch is different from predictor-only anchors because decoding reconstructs anchors from the law and the stored index.
- The current accounting uses a small residual codec selector baseline and still does not pretend to be entropy coding.
- PySR and more advanced symbolic regression remain deferred until the smaller deterministic baseline is well characterized.

## Scaled Prime-index Branch

The original prime-index-plus-diff hypothesis now has a more explicit scaled form:

```text
x = prev_prime(index << shift) + diff
```

- Input bytes are packed into reversible big-endian Python integer blocks.
- The branch searches a small local neighborhood around `index = x >> shift`.
- The decoder reconstructs the prime anchor from the stored index and model parameters instead of transmitting the prime directly.
- Full accounting still includes model bits, parameter bits, headers, per-block flags, index bits, residual payload bits, and raw escapes.
- The current exact prime utility is deliberately limited to `width_bits <= 64`.
- Exact arbitrary-size prime anchors are deferred until there is a credible need and a clear cost model for them.
- A result matters only when `total_bits < raw_bits`.
- This branch is currently evaluated through direct modules and CLI demo, not through the GUI cockpit.

## Huge Anchor Portfolio

The next generalization is a portfolio of anchor families over the same huge-block interface.

- Every family is tested under the same exact-lossless equation: `x = anchor(index, params) + diff`.
- `scaled_prime` becomes one candidate family, not a privileged answer.
- Simpler families such as `linear_shift`, `affine_shift`, `multiple`, and `square` can beat the prime family, and that is a meaningful result.
- Synthetic generated wins validate the mechanism and the accounting pipeline, not universal compression.
- Random-byte sanity remains required because a branch that loses on random data is behaving normally.
- The actual research goal remains the same: find cases where full transmitted cost beats raw storage honestly.

## Huge-anchor Binary Proof-of-concept

The next checkpoint after estimated accounting is an actual binary payload.

- Estimated `total_bits` remain useful for model search, ranking, and quick ablations.
- Actual `compressed_bytes` are stronger evidence because they include real container overhead and real byte alignment.
- A synthetic actual-byte win only proves that the mechanism can emit a smaller exact-lossless blob for data generated by a compatible anchor family.
- Random-byte sanity remains required. A binary loss on random data is expected behavior, not a bug.
- This proof-of-concept is intentionally narrow and stdlib-only. It is not yet a general file compression format.

## Actual-size Reranking

The next refinement is to stop trusting estimated search ranking as the final answer.

- Estimated accounting is still the right fast heuristic for broad candidate search.
- Actual-size reranking serializes the top estimated candidates and chooses by real `compressed_bytes`.
- This catches cases where estimated wins disappear once container overhead is counted honestly.
- Actual byte measurement is therefore the stronger compression signal for the binary path.

## Optimizer Architecture

The optimizer layer now separates the research harness into pluggable strategies.

- GP-lite searches tiny expression trees.
- SOMA tunes continuous parameters of small affine and quadratic anchor-law families.
- Image-GP-lite searches tiny expression trees over decoder-known 2D pixel context.
- Image-SOMA tunes a fixed-point linear predictor over decoder-known 2D pixel context.
- Future GP will target richer tree and topology search.
- Future ADAM will target differentiable parameter tuning.

All of them are measured against the same honest bit accounting. A candidate matters only when full transmitted cost beats raw fallback.

## Image-aware Search Optimizers

The current image research branch now has three distinct roles:

- `Image-predictor` is the fair manual baseline.
- `Image-GP-lite` explores small context laws over `left`, `up`, `up_left`, and simple ramps.
- `Image-SOMA` explores fixed-point linear combinations of the same decoder-known context.

All three branches share the same residual codec layer. A synthetic dataset win is only interesting when the full transmitted cost beats raw fallback, and it is still not evidence of universal compression.

## Image-GP-lite Primitive Ablations

The image GP branch now needs explicit primitive-set reporting:

- `local` means only decoder-known neighborhood context.
- `ramp` means local context plus procedural coordinate ramps.
- `structure` means ramp context plus explicit block/parity primitives.

These primitive sets are intentionally not equivalent. A checker-like win under `structure` is a valid primitive baseline, but it must not be confused with a win discovered from purely local context. Benchmarks without the primitive set label are incomplete.

## GUI Research Cockpit

The first GUI is intentionally narrow and uses generated grayscale images as a headless-friendly simulation target.

- Image simulation is not final file compression.
- The GUI is a cockpit for optimizer comparison, not a claim of general compression performance.
- Estimated bit accounting now includes a small residual codec selector baseline and entropy coding remains deferred.
```

## File: `.gitignore`

```gitignore
# Python bytecode and caches
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
env/
.env
.env.*
!.env.example

# Test and coverage artifacts
.pytest_cache/
.coverage
.coverage.*
htmlcov/

# Build and packaging artifacts
build/
dist/
site/
*.egg-info/
.eggs/
pip-wheel-metadata/

# Tool caches
.mypy_cache/
.ruff_cache/
.pyre/

# Temporary files and folders
tmp/
temp/
*.tmp
*.temp

# Local editor / OS files
.DS_Store
Thumbs.db
.idea/
.vscode/

# Local runtime notes or scratch outputs
*.log
.ap/

# Large generated model / array artifacts
*.pt
*.pth
*.ckpt
*.safetensors
*.onnx
*.gguf
*.npy
*.npz

# Session handoff archives
NEXT_AGENT_*.md
```

## File: `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "PrimeSymbolicMDL"
version = "0.1.0"
description = "Experimental MDL-guided anchor-and-residual compression harness."
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## File: `README.md`

```markdown
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
- a shared residual codec layer with fixed-width, zero-RLE, and byte-RLE research baselines
- an experimental huge-anchor binary bitstream container with exact byte-length measurement
- a `.psmdl` file CLI for huge-anchor compression and decompression
- a deterministic in-repo file benchmark for actual `.psmdl` byte sizes
- a small Tkinter research cockpit for grayscale image simulations
- pytest coverage for round-trip and random-data sanity checks

## GP-lite Indexed Anchor Law Search

The new GP-lite branch evolves decoder-known anchor laws `A(i)`.

- The encoder stores an index `i` plus a residual `x - A(i)`.
- The law is only useful if total transmitted bits beat raw fallback.
- This is different from a predictor-only model because the decoder reconstructs anchors from the transmitted index and the law tree.
- The current cost model uses fixed-width index accounting and a small residual codec selector baseline.
- Entropy coding, PySR, and heavier symbolic regression remain intentionally deferred.

## Scaled Prime-index Branch

The repository now also includes a scaled prime-index experiment over larger Python integer blocks.

- Bytes can be packed into big-endian Python integer blocks up to 128 bits for reversible block experiments.
- The current exact prime-anchor branch is intentionally limited to `width_bits <= 64`.
- The model tries `x = prev_prime(index << shift) + diff`.
- In this construction, `index` is smaller than the original block value and the decoder reconstructs the prime anchor from `index` and `shift`.
- The model only matters when the full transmitted cost of flags, indices, residual payload, escapes, headers, and model parameters beats raw storage.
- Arbitrary-size exact prime search is deferred. This branch does not fake primality above 64-bit integers.
- Random data is expected to often lose against raw storage, and that is an honest result.
- This branch currently ships as a CLI and testable module, not yet as a GUI-integrated optimizer.

## Huge Anchor Portfolio

The huge anchor portfolio generalizes the scaled prime-index branch into a broader family benchmark.

- Each family tests the same idea: `x = anchor(index, params) + diff`.
- `scaled_prime` is only one family inside that larger search space.
- Other current families include `linear_shift`, `affine_shift`, `multiple`, and `square`.
- If a simpler family beats `scaled_prime`, that is important evidence against prime-anchor special pleading.
- Synthetic wins are useful because they validate the exact-lossless mechanism and full accounting, not because they prove universal compression.
- Random-byte sanity remains mandatory.
- The real result only matters when total transmitted bits beat raw storage after counting model, parameter, header, flag, index, residual, and escape costs.

## Huge-anchor Binary Proof-of-concept

The repository now also includes a first real binary container for huge-anchor payloads.

- Earlier huge-anchor experiments used exact research payloads plus estimated bit accounting.
- The new container produces real `compressed_bytes` and therefore real `actual_bits = len(blob) * 8`.
- A synthetic win now means more than a promising estimate: the branch can emit a smaller exact-decodable blob for structure-compatible generated data.
- Random-byte sanity remains mandatory. If the binary container loses to raw bytes, that is the correct result.
- This is still not a universal file compressor. It is a narrow proof that one exact binary huge-anchor path can sometimes beat raw bytes on favorable synthetic data.

## Actual-size Reranking

Estimated MDL accounting remains the fast search heuristic, but it is no longer the final judge for the binary huge-anchor path.

- The search still finds promising candidates by estimated `total_bits`.
- The binary stage now serializes the top `N` estimated candidates and reranks them by real `compressed_bytes`.
- This makes container overhead visible instead of assumed away.
- An estimated win can still become `raw_fallback` after real byte serialization.
- Actual compressed bytes are the stronger evidence because they include headers, alignment, and real residual payload size.

## PSMDL File CLI

The repository includes a small file CLI for the huge-anchor binary path.

This is **not** a general-purpose compressor. It is a research file interface for exact-lossless experiments with honest actual-byte reporting.

Compress:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_cli compress --input in.bin --output out.psmdl --width-bits 32
```

Decompress:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_cli decompress --input out.psmdl --output restored.bin
```

Optional strict mode:

```fish
... --require-compression
```

If the huge-anchor blob is not smaller than the raw input, `--require-compression` refuses to write output.

### File formats

- `PSMDLHA1` = actual huge-anchor compressed payload
- `PSMDLRAW1` = raw fallback wrapper used when huge-anchor compression does not beat raw bytes

Default behavior stores a safe raw fallback when compression does not win. That keeps exact roundtrip, but the `.psmdl` file can be **larger** than the original input because of container overhead.

### In-repo benchmark summary

Deterministic benchmark command:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_benchmark
```

Current honest results from the in-repo set:

- random bytes: raw fallback
- repeating pattern: raw fallback
- small repo text/source files (`README.md`, `AGENTS.md`, Python source): raw fallback
- `square_generated_64`: synthetic actual win, `256 B -> 49 B`

Synthetic wins validate the exact mechanism only. They are not evidence of universal compression.

## Residual Codec Layer

Predictors and anchor laws both create a residual stream:

```text
x = predicted_or_anchor + residual
```

This repository now includes a small shared residual codec layer so different branches can compare against the same residual backend.

- `fixed_signed` is the deterministic fixed-width signed baseline.
- `zero_rle` is a deterministic zero-run-length baseline for residual streams with many zeros.
- `byte_rle` is a raw-like baseline for repeated pixel bytes.
- `raw_bytes` remains the honest fallback baseline for byte streams.

This is still not ANS or arithmetic coding. Entropy coding remains deferred. Exact roundtrip remains mandatory for any branch that claims decode support.

## Optimizer Architecture

The repository now exposes a small optimizer registry with seven visible choices:

- `GP-lite`: the existing tree-based indexed anchor-law search
- `SOMA`: a small continuous-parameter migration optimizer over affine and quadratic anchor laws
- `GP`: an honest placeholder for future richer topology search
- `ADAM`: an honest placeholder for future differentiable parameter tuning
- `Image-predictor`: a deterministic 2D grayscale predictor baseline with exact residual roundtrip
- `Image-GP-lite`: a deterministic expression-tree search over 2D pixel context
- `Image-SOMA`: a deterministic fixed-point linear search over 2D pixel context

All optimizers are judged by the same idea: the result only matters if `total_bits < raw_bits` after counting model, parameter, index, residual, flag, header, and escape costs.

## Image-aware Search Optimizers

The repository now separates a fair manual baseline from two image-aware search branches:

- `Image-predictor` is the manual baseline over small decoder-known 2D predictors.
- `Image-GP-lite` searches tiny expression trees over decoder-known pixel context.
- `Image-SOMA` tunes a fixed-point linear predictor over decoder-known pixel context.
- All three reuse the same shared residual codec layer.
- A result only matters if `total_bits < raw_bits`.
- Synthetic gradients, checkerboards, and ramps are useful for deterministic debugging, not as proof of universal compression.

## Image-GP-lite Primitive Ablations

`Image-GP-lite` can now be run with explicit primitive sets:

- `local` uses only decoder-known neighborhood context such as `left`, `up`, and `up_left`.
- `ramp` adds procedural coordinate ramps such as `x_ramp`, `y_ramp`, and `diag_ramp`.
- `structure` adds block/parity primitives intended for checker-like and piecewise structure baselines.

Important interpretation rules:

- `checker_parity` wins are valid only as explicit primitive baselines, not as evidence that the search discovered a universal image law.
- Ablation reports must include the primitive set name or they are not comparable.
- Synthetic wins still need the same `total_bits < raw_bits` accounting rule as every other branch.

## GUI Research Cockpit

The first GUI is a stdlib Tkinter cockpit focused on generated grayscale image simulations.

- It lets you choose an optimizer and a tiny image dataset.
- It reports raw size in bits and estimated transmitted size in bits.
- It can also report which residual codec or raw-byte baseline won under the current accounting.
- It is a research UI, not a final file compressor.
- Estimated bit accounting now includes a small residual codec selector, but entropy coding is still deferred.

## Analytic Coding Snapshots

Use the fish snapshot helper to generate an agent-readable repository state:

```fish
fish scripts/ap_snapshot.fish
fish scripts/ap_snapshot.fish --run-tests
```

This generates:

- `BRAIN.md`
- `BOOT.md`

These files are intended for orchestration and repository-state handoff, not as proof of compression quality.

## Analytic Programming / Analytic Coding

Recommended interactive fish workflow:

```fish
source .venv/bin/activate.fish
```

Core AP commands:

```fish
fish scripts/ap_snapshot.fish --run-tests
fish scripts/ap_chat_append.fish --role worker --message "..." --tldr "..."
fish scripts/ap_cycle_close.fish --message "..." --tldr "..."
```

AP artifact roles:

- `AP.md`, `AP_WORKER.md`, and `AP_ORCHESTRATOR.md` are living, repo-visible protocol and doctrine artifacts that may evolve through explicit AP/meta tasks.
- `AP.md` is the system-wide protocol.
- `COORDINATOR_PROTOCOL.md` extends AP with file-based RPC.
- `AP_ORCHESTRATOR.md` explains the orchestrator-side discipline.
- `AP_WORKER.md` is the Worker doctrine.
- `NEXT_ORCHESTRATOR.md` is the strategic handoff for the next Orchestrator.
- `BRAIN.md` and `BOOT.md` are generated repository snapshots.

## Coordinator Protocol

Coordinator Protocol is a file-based, repo-centered RPC proof of concept for `COOPERATOR`, `ORCHESTRATOR`, and `WORKER`.

- The repository remains the source of truth.
- `BRAIN.md` and `BOOT.md` remain broad snapshots.
- `CHAT.md` remains the append-only coordination ledger.
- RPC is the narrow lane for targeted status and file requests.
- This means the Orchestrator does not always need the whole diff when it only needs one file or one status view.
- The Orchestrator should request exact repo information via RPC instead of guessing from partial context.
- The default RPC surface is read-only and preserves the same safety model: no secrets access, no network dependency, and no git write commands.
- A continuation session should ideally start with `NEXT_ORCHESTRATOR.md` and `NEXT_AGENT.md`.

RPC commands:

```fish
fish scripts/ap_rpc_call.fish --method repo.status
fish scripts/ap_rpc_call.fish --method repo.get_file --path AP.md
fish scripts/ap_rpc_request.fish --method repo.get_file --path src/primesymbolicmdl/simulation.py
fish scripts/ap_rpc_handle_next.fish
```

Scaled-prime demo command:

```bash
python -m primesymbolicmdl.scaled_prime_demo
```

Huge-anchor portfolio demo command:

```bash
python -m primesymbolicmdl.huge_anchor_demo
```

Huge-anchor binary demo command:

```bash
python -m primesymbolicmdl.huge_anchor_binary_demo
```

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
- external benchmark corpora integration
- entropy-backed general-purpose file compression
```

## File: `scripts/ap_chat_append.fish`

```fish
#!/usr/bin/env fish

# Pridava strukturovany zaznam do CHAT.md bez prepisania historie.

function log_info -a message
    echo "🧠 $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_done -a message
    echo "✅ $message"
end

function ensure_chat_file -a chat_path
    # Ak ledger este neexistuje, vytvorime ho s kratkou hlavickou.
    if not test -f $chat_path
        begin
            echo "# CHAT.md — Analytic Programming Coordination Ledger"
            echo
            echo "Append-only coordination log for User, Orchestrator, and Worker."
            echo
        end > $chat_path
        log_info "Created $chat_path"
    end
end

function emit_bullet_lines -a raw_value
    # Text delime po novych riadkoch a prazdne polozky preskocime.
    for line in (string split \n -- $raw_value)
        set -l trimmed (string trim -- $line)
        if test -n "$trimmed"
            echo "- $trimmed"
        end
    end
end

function emit_command_lines -a raw_value
    # Prikazy akceptuju viacriadkovy vstup alebo bodkociarkou oddelene prikazy.
    if string match -q "*\n*" -- $raw_value
        emit_bullet_lines $raw_value
        return 0
    end

    for line in (string split ';' -- $raw_value)
        set -l trimmed (string trim -- $line)
        if test -n "$trimmed"
            echo "- $trimmed"
        end
    end
end

function emit_file_lines -a raw_value
    # Zoznam suborov vieme rozdelit po novych riadkoch alebo medzerach.
    if string match -q "*\n*" -- $raw_value
        emit_bullet_lines $raw_value
        return 0
    end

    for token in (string split ' ' -- $raw_value)
        set -l trimmed (string trim -- $token)
        if test -n "$trimmed"
            echo "- $trimmed"
        end
    end
end

argparse 'role=' 'message=' 'tldr=' 'commands=' 'files=' -- $argv
or begin
    echo "❌ Invalid arguments."
    exit 2
end

if not set -q _flag_role
    echo "❌ --role is required."
    exit 2
end
if not set -q _flag_message
    echo "❌ --message is required."
    exit 2
end

set -l ROLE $_flag_role
set -l MESSAGE $_flag_message
set -l TLDR ""
set -l COMMANDS_TEXT ""
set -l FILES_TEXT ""

if set -q _flag_tldr
    set TLDR $_flag_tldr
end
if set -q _flag_commands
    set COMMANDS_TEXT $_flag_commands
end
if set -q _flag_files
    set FILES_TEXT $_flag_files
end

switch $ROLE
    case user worker orchestrator
    case '*'
        echo "❌ --role must be one of: user, worker, orchestrator."
        exit 2
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l CHAT_PATH "CHAT.md"
set -l TIMESTAMP (date -Iseconds)

log_info "Appending $ROLE entry to $CHAT_PATH ..."
ensure_chat_file $CHAT_PATH

begin
    echo "## $TIMESTAMP | role=$ROLE"
    echo
    echo "Message:"
    echo "$MESSAGE"
    echo
    if test -n "$TLDR"
        echo "TLDR:"
        emit_bullet_lines $TLDR
        echo
    end
    if test -n "$COMMANDS_TEXT"
        echo "Commands run:"
        emit_command_lines $COMMANDS_TEXT
        echo
    end
    if test -n "$FILES_TEXT"
        echo "Files changed:"
        emit_file_lines $FILES_TEXT
        echo
    end
end >> $CHAT_PATH

log_done "CHAT.md updated."
```

## File: `scripts/ap_cycle_close.fish`

```fish
#!/usr/bin/env fish

# Uzatvara jeden Worker cyklus: testy, snapshot, chat zaznam a kratky stav.

function log_info -a message
    echo "🧠 $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_done -a message
    echo "✅ $message"
end

function find_project_python
    # Najprv skusime bezne virtualenv cesty v repozitari.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    # Fallback: najdeme hocijaky lokalny python pod repozitarom.
    set -l discovered (find . -maxdepth 4 -path '*/bin/python' 2>/dev/null | head -n 1)
    if test -n "$discovered"
        echo $discovered
        return 0
    end

    return 1
end

function collect_changed_files
    # Poskladame modifikovane aj untracked subory a odfiltrujeme generated handoff artefakty.
    begin
        git diff --name-only -- . ':!BRAIN.md' ':!BOOT.md' ':!NEXT_AGENT.md' ':!NEXT_AGENT_*.md'
        git ls-files --others --exclude-standard
    end | sed '/^BRAIN\.md$/d;/^BOOT\.md$/d;/^NEXT_AGENT\(_[0-9]\+\)\?\.md$/d;/^\.ap\//d' | sort -u
end

argparse 'message=' 'tldr=' -- $argv
or begin
    echo "❌ Invalid arguments."
    exit 2
end

if not set -q _flag_message
    echo "❌ --message is required."
    exit 2
end

set -l MESSAGE $_flag_message
set -l TLDR $_flag_tldr
if test -z "$TLDR"
    set TLDR "$MESSAGE"
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l TMP_DIR (mktemp -d)
set -l TIMESTAMP (date -Iseconds)
set -l TEST_OUTPUT_FILE "$TMP_DIR/test_output.txt"
set -l SNAPSHOT_OUTPUT_FILE "$TMP_DIR/snapshot_output.txt"
set -l CHAT_OUTPUT_FILE "$TMP_DIR/chat_output.txt"
set -l AP_DIR ".ap"
set -l CURRENT_STATUS_FILE "$AP_DIR/current_status.md"
set -l LAST_REPORT_FILE "$AP_DIR/last_report.md"

mkdir -p $AP_DIR

set -l TEST_STATUS "failed"
set -l TEST_RUNNER "python -m pytest -q"
set -l SNAPSHOT_STATUS "not run"
set -l CHAT_STATUS "not appended"
set -l FINAL_EXIT 0

log_info "Running worker cycle tests ..."
python -m pytest -q > $TEST_OUTPUT_FILE 2>&1
set -l TEST_EXIT $status
if test $TEST_EXIT -eq 0
    set TEST_STATUS "passed"
else
    set -l PROJECT_PYTHON (find_project_python)
    if test -n "$PROJECT_PYTHON"; and string match -rq 'No module named pytest' -- (string join \n -- (cat $TEST_OUTPUT_FILE))
        log_warn "System python has no pytest, retrying with project virtual environment python."
        $PROJECT_PYTHON -m pytest -q > $TEST_OUTPUT_FILE 2>&1
        set TEST_EXIT $status
        set TEST_RUNNER "project virtual environment python -m pytest -q"
    end

    if test $TEST_EXIT -eq 0
        set TEST_STATUS "passed"
    else
        set TEST_STATUS "failed"
        set FINAL_EXIT 1
    end
end

log_info "Refreshing repository snapshot ..."
fish scripts/ap_snapshot.fish --run-tests > $SNAPSHOT_OUTPUT_FILE 2>&1
set -l SNAPSHOT_EXIT $status
if test $SNAPSHOT_EXIT -eq 0
    set SNAPSHOT_STATUS "generated"
else
    set SNAPSHOT_STATUS "failed"
    log_warn "Snapshot regeneration failed."
    if test $FINAL_EXIT -eq 0
        set FINAL_EXIT 1
    end
end

set -l STATUS_NOTE "Cycle close result: tests passed and snapshot refreshed."
if test "$TEST_STATUS" = "failed"
    set STATUS_NOTE "Cycle close result: tests failed."
else if test "$SNAPSHOT_STATUS" != "generated"
    set STATUS_NOTE "Cycle close result: tests passed but snapshot regeneration failed."
end

set -l CHAT_MESSAGE "$MESSAGE Status note: $STATUS_NOTE"
set -l CHAT_TLDR "$TLDR | Test status: $TEST_STATUS | Snapshot status: $SNAPSHOT_STATUS"
set -l COMMANDS_TEXT "python -m pytest -q; fish scripts/ap_snapshot.fish --run-tests"
set -l FILES_TEXT (string join \n (collect_changed_files))

log_info "Appending Worker cycle entry to CHAT.md ..."
fish scripts/ap_chat_append.fish --role worker --message "$CHAT_MESSAGE" --tldr "$CHAT_TLDR" --commands "$COMMANDS_TEXT" --files "$FILES_TEXT" > $CHAT_OUTPUT_FILE 2>&1
set -l CHAT_EXIT $status
if test $CHAT_EXIT -eq 0
    set CHAT_STATUS "appended"
else
    set CHAT_STATUS "failed"
    log_warn "CHAT.md append failed."
    if test $FINAL_EXIT -eq 0
        set FINAL_EXIT 1
    end
end

set -l NEXT_STEP "Review BRAIN.md and choose the next bounded AP task."
if test "$TEST_STATUS" = "failed"
    set NEXT_STEP "Investigate the failing test output before making new code changes."
else if test "$SNAPSHOT_STATUS" != "generated"
    set NEXT_STEP "Fix snapshot regeneration before trusting the AP handoff chain."
end

log_info "Writing $CURRENT_STATUS_FILE ..."
begin
    echo "# Current AP Worker Status"
    echo
    echo "- Generated: `$TIMESTAMP`"
    echo "- Message: `$MESSAGE`"
    echo "- TLDR: `$TLDR`"
    echo "- Test status: `$TEST_STATUS`"
    echo "- Test runner: `$TEST_RUNNER`"
    echo "- Snapshot status: `$SNAPSHOT_STATUS`"
    echo "- CHAT status: `$CHAT_STATUS`"
    echo "- Detail artifacts: `BRAIN.md`, `BOOT.md`, `CHAT.md`, `.ap/last_report.md`"
end > $CURRENT_STATUS_FILE

log_info "Writing $LAST_REPORT_FILE ..."
begin
    echo "### Report for ORCHESTRATOR_CHAT"
    echo
    echo "1. Changed files"
    echo
    if test -n "$FILES_TEXT"
        for path in (string split \n -- $FILES_TEXT)
            set -l trimmed (string trim -- $path)
            if test -n "$trimmed"
                echo "- `$trimmed`"
            end
        end
    else
        echo "- No changed files detected outside generated exclusions."
    end
    echo
    echo "2. Summary"
    echo
    echo "$MESSAGE"
    echo
    echo "TLDR: $TLDR"
    echo
    echo "3. Commands run"
    echo
    echo "- `python -m pytest -q`"
    echo "- `fish scripts/ap_snapshot.fish --run-tests`"
    echo "- `fish scripts/ap_chat_append.fish ...`"
    echo
    echo "4. Test output"
    echo
    echo "- Status: `$TEST_STATUS`"
    echo "- Runner: `$TEST_RUNNER`"
    echo
    echo '```text'
    cat $TEST_OUTPUT_FILE
    echo '```'
    echo
    echo "5. Snapshot status, if applicable"
    echo
    echo "- Snapshot status: `$SNAPSHOT_STATUS`"
    echo "- CHAT status: `$CHAT_STATUS`"
    echo
    echo '```text'
    if test -s $SNAPSHOT_OUTPUT_FILE
        cat $SNAPSHOT_OUTPUT_FILE
    else
        echo "(no snapshot output)"
    end
    echo '```'
    echo
    echo "6. Warnings / limitations"
    echo
    if test "$TEST_STATUS" = "failed"
        echo "- Tests failed during cycle close."
    else
        echo "- Tests passed during cycle close."
    end
    if test "$SNAPSHOT_STATUS" != "generated"
        echo "- Snapshot regeneration failed."
    else
        echo "- Snapshot regeneration completed."
    end
    if test "$CHAT_STATUS" != "appended"
        echo "- CHAT append failed."
    else
        echo "- CHAT entry appended."
    end
    echo
    echo "7. Suggested next smallest step"
    echo
    echo "- $NEXT_STEP"
end > $LAST_REPORT_FILE

log_done "Worker cycle artifacts refreshed."
log_done "Test status: $TEST_STATUS"
log_done "Snapshot status: $SNAPSHOT_STATUS"
log_done "CHAT status: $CHAT_STATUS"

rm -rf $TMP_DIR
exit $FINAL_EXIT
```

## File: `scripts/ap_rpc_call.fish`

```fish
#!/usr/bin/env fish

# Lokalny smoke workflow: request -> handle -> kratke zhrnutie response.

function log_info -a message
    echo "🧠 $message"
end

function log_done -a message
    echo "✅ $message"
end

function log_error -a message
    echo "❌ $message" >&2
end

argparse 'method=' 'path=' 'max-bytes=' -- $argv
or begin
    log_error "Invalid arguments."
    exit 2
end

if not set -q _flag_method
    log_error "--method is required."
    exit 2
end

set -l METHOD $_flag_method
set -l FORWARD_ARGS --method $METHOD

if set -q _flag_path
    set FORWARD_ARGS $FORWARD_ARGS --path $_flag_path
end
if set -q _flag_max_bytes
    set FORWARD_ARGS $FORWARD_ARGS --max-bytes $_flag_max_bytes
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT
set -l TMP_DIR (mktemp -d)
set -l REQUEST_LOG "$TMP_DIR/request.log"
set -l HANDLE_LOG "$TMP_DIR/handle.log"

log_info "Spustam lokalny RPC call pre $METHOD ..."
fish scripts/ap_rpc_request.fish $FORWARD_ARGS > $REQUEST_LOG 2>&1
set -l REQUEST_EXIT $status
cat $REQUEST_LOG
if test $REQUEST_EXIT -ne 0
    rm -rf $TMP_DIR
    exit $REQUEST_EXIT
end

set -l REQUEST_PATH (cat $REQUEST_LOG | string match -r '^REQUEST_PATH=.*' | string replace 'REQUEST_PATH=' '')
if test -z "$REQUEST_PATH"
    log_error "Nepodarilo sa zistit REQUEST_PATH."
    rm -rf $TMP_DIR
    exit 1
end

fish scripts/ap_rpc_handle_next.fish --request $REQUEST_PATH > $HANDLE_LOG 2>&1
set -l HANDLE_EXIT $status
cat $HANDLE_LOG
if test $HANDLE_EXIT -ne 0
    rm -rf $TMP_DIR
    exit $HANDLE_EXIT
end

set -l RESPONSE_PATH (cat $HANDLE_LOG | string match -r '^RESPONSE_PATH=.*' | string replace 'RESPONSE_PATH=' '')
set -l RESPONSE_STATUS (cat $HANDLE_LOG | string match -r '^RESPONSE_STATUS=.*' | string replace 'RESPONSE_STATUS=' '')

if test -z "$RESPONSE_PATH"
    log_error "Nepodarilo sa zistit RESPONSE_PATH."
    rm -rf $TMP_DIR
    exit 1
end
if test -z "$RESPONSE_STATUS"
    log_error "Nepodarilo sa zistit RESPONSE_STATUS."
    rm -rf $TMP_DIR
    exit 1
end

log_done "RPC call dokonceny so stavom $RESPONSE_STATUS"
echo "RESPONSE_PATH=$RESPONSE_PATH"
echo "RESPONSE_STATUS=$RESPONSE_STATUS"
rm -rf $TMP_DIR
```

## File: `scripts/ap_rpc_handle_next.fish`

```fish
#!/usr/bin/env fish

# Spracuje jeden RPC request z inboxu a zapise response do outboxu.

function log_info -a message
    echo "🧠 $message"
end

function log_done -a message
    echo "✅ $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_error -a message
    echo "❌ $message" >&2
end

function find_project_python
    # Preferujeme projektovy virtualenv, aby handler bezal nad rovnakym Python prostredim.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    if command -sq python
        command -s python
        return 0
    end

    return 1
end

argparse 'request=' -- $argv
or begin
    log_error "Invalid arguments."
    exit 2
end

set -l EXPLICIT_REQUEST ""
if set -q _flag_request
    set EXPLICIT_REQUEST $_flag_request
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l PYTHON_CMD (find_project_python)
if test -z "$PYTHON_CMD"
    log_error "Python was not found."
    exit 1
end

set -lx PYTHONPATH "$REPO_ROOT/src"
set -l COMMAND $PYTHON_CMD -m primesymbolicmdl.ap_rpc handle --repo-root $REPO_ROOT
if test -n "$EXPLICIT_REQUEST"
    set COMMAND $COMMAND --request $EXPLICIT_REQUEST
    log_info "Spracuvam explicitny RPC request $EXPLICIT_REQUEST ..."
else
    log_info "Spracuvam najstarsi RPC request z inboxu ..."
end

set -l META_JSON ($COMMAND 2>&1)
set -l EXIT_CODE $status
if test $EXIT_CODE -ne 0
    log_error "RPC handler failed."
    printf "%s\n" "$META_JSON" >&2
    exit $EXIT_CODE
end

set -l REQUEST_ID (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_id"])')
set -l REQUEST_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_path"])')
set -l RESPONSE_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["response_path"])')
set -l RESPONSE_STATUS (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["response_status"])')
set -l ARCHIVE_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; value=json.load(sys.stdin)["archive_path"]; print("" if value is None else value)')

log_done "RPC response ulozena do $RESPONSE_PATH"
if test -n "$ARCHIVE_PATH"
    log_done "RPC request archivovany do $ARCHIVE_PATH"
else
    log_warn "RPC request sa nepodarilo archivovat."
end

echo "REQUEST_ID=$REQUEST_ID"
echo "REQUEST_PATH=$REQUEST_PATH"
echo "RESPONSE_PATH=$RESPONSE_PATH"
echo "RESPONSE_STATUS=$RESPONSE_STATUS"
if test -n "$ARCHIVE_PATH"
    echo "ARCHIVE_PATH=$ARCHIVE_PATH"
end
```

## File: `scripts/ap_rpc_request.fish`

```fish
#!/usr/bin/env fish

# Vytvori read-only RPC request pre Worker a ulozi ho do inboxu.

function log_info -a message
    echo "🧠 $message"
end

function log_done -a message
    echo "✅ $message"
end

function log_error -a message
    echo "❌ $message" >&2
end

function find_project_python
    # Preferujeme projektovy virtualenv, aby bol import modulu stabilny.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    if command -sq python
        command -s python
        return 0
    end

    return 1
end

argparse 'method=' 'path=' 'max-bytes=' -- $argv
or begin
    log_error "Invalid arguments."
    exit 2
end

if not set -q _flag_method
    log_error "--method is required."
    exit 2
end

set -l METHOD $_flag_method
set -l FILE_PATH ""
set -l MAX_BYTES ""

if set -q _flag_path
    set FILE_PATH $_flag_path
end
if set -q _flag_max_bytes
    set MAX_BYTES $_flag_max_bytes
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l PYTHON_CMD (find_project_python)
if test -z "$PYTHON_CMD"
    log_error "Python was not found."
    exit 1
end

set -lx PYTHONPATH "$REPO_ROOT/src"
set -l COMMAND $PYTHON_CMD -m primesymbolicmdl.ap_rpc request --repo-root $REPO_ROOT --method $METHOD
if test -n "$FILE_PATH"
    set COMMAND $COMMAND --path $FILE_PATH
end
if test -n "$MAX_BYTES"
    set COMMAND $COMMAND --max-bytes $MAX_BYTES
end

log_info "Vytvaram RPC request pre metodu $METHOD ..."
set -l META_JSON ($COMMAND 2>&1)
set -l EXIT_CODE $status
if test $EXIT_CODE -ne 0
    log_error "RPC request creation failed."
    printf "%s\n" "$META_JSON" >&2
    exit $EXIT_CODE
end

set -l REQUEST_ID (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_id"])')
set -l REQUEST_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_path"])')

log_done "RPC request ulozeny do $REQUEST_PATH"
echo "REQUEST_ID=$REQUEST_ID"
echo "REQUEST_PATH=$REQUEST_PATH"
```

## File: `scripts/ap_snapshot.fish`

```fish
#!/usr/bin/env fish

# Generuje analyticky snapshot repozitara pre Orchestrator chat.

set -l BRAIN_OUT "BRAIN.md"
set -l BOOT_OUT "BOOT.md"
set -l MAX_FILE_KB 80
set -l RUN_TESTS 0
set -l TOTAL_CONTENT_BUDGET_KB 1024
set -l DIFF_BUDGET_KB 256

function log_info -a message
    echo "🧠 $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_done -a message
    echo "✅ $message"
end

function sanitize_output
    # Cez cat explicitne preposleme stdin, aby sanitizacia fungovala aj vo fish funkcii.
    cat
end

function find_project_python
    # Najprv skus bezne virtualenv cesty v repozitari.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    # Fallback: najdi hocijaky spustitelny python pod repozitarom.
    set -l discovered (find . -maxdepth 4 -path '*/bin/python' 2>/dev/null | head -n 1)
    if test -n "$discovered"
        echo $discovered
        return 0
    end

    return 1
end

function extension_language -a path
    switch $path
        case "*.py"
            echo "python"
        case "*.fish"
            echo "fish"
        case "*.md"
            echo "markdown"
        case "*.toml"
            echo "toml"
        case ".gitignore"
            echo "gitignore"
        case "*.json"
            echo "json"
        case "*.yml" "*.yaml"
            echo "yaml"
        case "*.ini" "*.cfg"
            echo "ini"
        case "*.txt"
            echo "text"
        case '*'
            echo "text"
    end
end

function should_skip_file -a path
    if string match -rq '(^|/)(\.git|\.venv|__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache)(/|$)' -- $path
        return 0
    end
    if string match -rq '(^|/)(BRAIN|BOOT)\.md$' -- $path
        return 0
    end
    if string match -rq '(^|/)NEXT_AGENT(_[0-9]+)?\.md$' -- $path
        return 0
    end
    if string match -rq '\.(pyc|png|jpg|jpeg|gif|webp|mp4|mov|zip|sqlite|db)$' -- $path
        return 0
    end
    return 1
end

function collect_candidate_files
    set -l roots src tests docs scripts
    set -l items

    for root in $roots
        if test -d $root
            for item in (find $root -type f | sort)
                set items $items (string replace -r '^\.?/' '' -- $item)
            end
        end
    end

    for root_file in AGENTS.md AP.md AP_WORKER.md COORDINATOR_PROTOCOL.md README.md CHAT.md pyproject.toml .gitignore
        if test -f $root_file
            set items $items $root_file
        end
    end

    printf "%s\n" $items | sort -u
end

argparse 'run-tests' 'max-file-kb=' 'brain=' 'boot=' -- $argv
or begin
    echo "❌ Invalid arguments."
    exit 2
end

if set -q _flag_run_tests
    set RUN_TESTS 1
end
if set -q _flag_max_file_kb
    set MAX_FILE_KB $_flag_max_file_kb
end
if set -q _flag_brain
    set BRAIN_OUT $_flag_brain
end
if set -q _flag_boot
    set BOOT_OUT $_flag_boot
end

if not string match -rq '^[0-9]+$' -- $MAX_FILE_KB
    echo "❌ --max-file-kb must be a non-negative integer."
    exit 2
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l TMP_DIR (mktemp -d)
set -l TIMESTAMP (date -Iseconds)
set -l BRANCH (git branch --show-current 2>/dev/null)
if test -z "$BRANCH"
    set BRANCH "n/a"
end
set -l HEAD_HASH (git rev-parse HEAD 2>/dev/null)
if test -z "$HEAD_HASH"
    set HEAD_HASH "n/a"
end
set -l PYTHON_VERSION (python --version 2>&1)
set -l PYTHON_COMMAND_V (command -v python 2>/dev/null)
set -l PYTHON_PATH (which python 2>/dev/null)
if test -z "$PYTHON_PATH"
    set PYTHON_PATH "python not found"
end
if test -z "$PYTHON_COMMAND_V"
    set PYTHON_COMMAND_V "python not found"
end
set -l PYTHON_SYS_EXECUTABLE (python -c 'import sys; print(sys.executable)' 2>&1)
set -l PYTHON_SYS_PREFIX (python -c 'import sys; print(sys.prefix)' 2>&1)
set -l PROJECT_VENV_EXISTS "no"
if test -d ".venv"
    set PROJECT_VENV_EXISTS "yes"
end
set -l PYTHON_INSIDE_PROJECT_VENV "no"
if string match -rq '(^|/)\.venv/' -- $PYTHON_SYS_EXECUTABLE
    set PYTHON_INSIDE_PROJECT_VENV "yes"
end
set -l PYTHON_ENV_WARNING ""
if test "$PROJECT_VENV_EXISTS" = "yes"; and test "$PYTHON_INSIDE_PROJECT_VENV" != "yes"
    set PYTHON_ENV_WARNING "WARNING: .venv exists but active python is not the project virtual environment."
end

set -l GIT_STATUS_FILE "$TMP_DIR/git_status.txt"
set -l DIFF_STAT_FILE "$TMP_DIR/diff_stat.txt"
set -l FULL_DIFF_FILE "$TMP_DIR/full_diff.txt"
set -l TEST_OUTPUT_FILE "$TMP_DIR/test_output.txt"

git status --short | sed '/NEXT_AGENT\(_[0-9]\+\)\?\.md$/d' > $GIT_STATUS_FILE 2>&1
git diff --stat -- . ':!BRAIN.md' ':!BOOT.md' ':!NEXT_AGENT.md' ':!NEXT_AGENT_*.md' > $DIFF_STAT_FILE 2>&1
git diff -- . ':!BRAIN.md' ':!BOOT.md' ':!NEXT_AGENT.md' ':!NEXT_AGENT_*.md' > $FULL_DIFF_FILE 2>&1

set -l TEST_STATUS "not run"
set -l TEST_RUNNER "not run"
echo "Tests were not run. Use --run-tests to execute pytest." > $TEST_OUTPUT_FILE

if test $RUN_TESTS -eq 1
    log_info "Running tests for snapshot..."
    python -m pytest -q > $TEST_OUTPUT_FILE 2>&1
    set -l TEST_EXIT $status
    if test $TEST_EXIT -eq 0
        set TEST_STATUS "passed"
        set TEST_RUNNER "python -m pytest -q"
    else
        set -l PROJECT_PYTHON (find_project_python)
        if test -n "$PROJECT_PYTHON"; and string match -rq 'No module named pytest' -- (string join \n -- (cat $TEST_OUTPUT_FILE))
            log_warn "System python has no pytest, retrying with project virtual environment python."
            $PROJECT_PYTHON -m pytest -q > $TEST_OUTPUT_FILE 2>&1
            set TEST_EXIT $status
            if test $TEST_EXIT -eq 0
                set TEST_STATUS "passed"
                set TEST_RUNNER "project virtual environment python -m pytest -q"
            else
                set TEST_STATUS "failed"
                set TEST_RUNNER "project virtual environment python -m pytest -q"
            end
        else
            set TEST_STATUS "failed"
            set TEST_RUNNER "python -m pytest -q"
        end
    end
end

log_info "Writing $BRAIN_OUT ..."
begin
    echo "# BRAIN.md — Analytic Coding Repository Snapshot"
    echo
    echo "## 2. Timestamp"
    echo
    echo "- Generated: `$TIMESTAMP`"
    echo
    echo "## 3. Repo Root"
    echo
    echo "- Repo root: `$REPO_ROOT`"
    echo
    echo "## 4. Branch"
    echo
    echo "- Branch: `$BRANCH`"
    echo
    echo "## 5. HEAD Commit"
    echo
    echo "- HEAD: `$HEAD_HASH`"
    echo
    echo "## 6. Python Info"
    echo
    echo "- command -v python: `$PYTHON_COMMAND_V`"
    echo "- python --version: `$PYTHON_VERSION`"
    echo "- which python: `$PYTHON_PATH`"
    echo "- sys.executable: `$PYTHON_SYS_EXECUTABLE`"
    echo "- sys.prefix: `$PYTHON_SYS_PREFIX`"
    echo "- .venv exists: `$PROJECT_VENV_EXISTS`"
    echo "- active python inside .venv: `$PYTHON_INSIDE_PROJECT_VENV`"
    if test -n "$PYTHON_ENV_WARNING"
        echo
        echo "> $PYTHON_ENV_WARNING"
    end
    echo
    echo "## 7. Git Status"
    echo
    echo '```text'
    if test -s $GIT_STATUS_FILE
        cat $GIT_STATUS_FILE | sanitize_output
    else
        echo "(clean working tree)"
    end
    echo '```'
    echo
    echo "## 8. Diff Stat"
    echo
    echo '```text'
    if test -s $DIFF_STAT_FILE
        cat $DIFF_STAT_FILE | sanitize_output
    else
        echo "(no diff stat output)"
    end
    echo '```'
    echo
    echo "## 9. Full Diff"
    echo
    echo '```diff'
    set -l FULL_DIFF_LIMIT_BYTES (math "$DIFF_BUDGET_KB * 1024")
    set -l FULL_DIFF_SIZE (stat -c '%s' -- $FULL_DIFF_FILE 2>/dev/null)
    if test -n "$FULL_DIFF_SIZE"; and test $FULL_DIFF_SIZE -gt $FULL_DIFF_LIMIT_BYTES
        head -c $FULL_DIFF_LIMIT_BYTES $FULL_DIFF_FILE | sanitize_output
        echo
        echo "... TRUNCATED: diff exceeded $DIFF_BUDGET_KB KB budget ..."
    else if test -s $FULL_DIFF_FILE
        cat $FULL_DIFF_FILE | sanitize_output
    else
        echo "(no diff output)"
    end
    echo '```'
    echo
    echo "## 10. Test Output"
    echo
    echo "- Test status: `$TEST_STATUS`"
    echo "- Test runner: `$TEST_RUNNER`"
    echo
    echo '```text'
    if test -s $TEST_OUTPUT_FILE
        cat $TEST_OUTPUT_FILE | sanitize_output
    else
        echo "(no test output)"
    end
    echo '```'
    echo
    echo "## 11. Relevant File Tree"
    echo
    for path in (collect_candidate_files)
        if should_skip_file $path
            continue
        end
        set -l size_bytes (stat -c '%s' -- $path 2>/dev/null)
        if test -z "$size_bytes"
            set size_bytes "?"
        end
        echo "- `$path` ($size_bytes bytes)"
    end
    echo
    echo "## 12. Selected File Contents"
    echo
    set -l INCLUDED_BYTES 0
    set -l TOTAL_CONTENT_LIMIT_BYTES (math "$TOTAL_CONTENT_BUDGET_KB * 1024")
    set -l FILE_LIMIT_BYTES (math "$MAX_FILE_KB * 1024")
    for path in (collect_candidate_files)
        if should_skip_file $path
            continue
        end
        if not test -f $path
            continue
        end
        set -l size_bytes (stat -c '%s' -- $path 2>/dev/null)
        if test -z "$size_bytes"
            set size_bytes 0
        end
        echo "## File: `$path`"
        echo
        set -l language (extension_language $path)
        echo "```$language"
        if test $size_bytes -gt $FILE_LIMIT_BYTES
            echo "SKIPPED: file too large"
        else if test (math "$INCLUDED_BYTES + $size_bytes") -gt $TOTAL_CONTENT_LIMIT_BYTES
            echo "SKIPPED: snapshot content budget exceeded"
        else
            cat $path | sanitize_output
            set INCLUDED_BYTES (math "$INCLUDED_BYTES + $size_bytes")
        end
        echo '```'
        echo
    end
end > $BRAIN_OUT

log_info "Writing $BOOT_OUT ..."
begin
    echo "# BOOT.md — Analytic Coding Boot Summary"
    echo
    echo "PrimeSymbolicMDL je experimentalny lossless compression research harness orientovany na honest MDL accounting, anchor/residual vetvy a male deterministicke baseline experimenty."
    echo
    echo "## Current Git State"
    echo
    echo "- Branch: `$BRANCH`"
    echo "- HEAD: `$HEAD_HASH`"
    echo
    echo "## Last Test Status"
    echo
    if test $RUN_TESTS -eq 1
        echo "- Status: `$TEST_STATUS`"
        echo "- Runner: `$TEST_RUNNER`"
    else
        echo "- Tests were not run during this snapshot."
    end
    echo
    echo "## Main Modules"
    echo
    echo "- block packing"
    echo "- prime/index branch"
    echo "- GP-lite law search"
    echo "- SOMA"
    echo "- Image-predictor"
    echo "- residual codec layer"
    echo "- GUI"
    echo
    echo "## Worker Agent Rules"
    echo
    echo "- no git write commands"
    echo "- make small changes"
    echo "- run tests after meaningful changes"
    echo "- after meaningful changes run `fish scripts/ap_snapshot.fish --run-tests`"
    echo "- report begins with `### Report for ORCHESTRATOR_CHAT`"
    echo
    echo "## Detail Source"
    echo
    echo "- Detailed repository state: `BRAIN.md`"
end > $BOOT_OUT

set -l BRAIN_SIZE (stat -c '%s' -- $BRAIN_OUT 2>/dev/null)
set -l BOOT_SIZE (stat -c '%s' -- $BOOT_OUT 2>/dev/null)

log_done "Snapshot complete."
log_done "$BRAIN_OUT size: $BRAIN_SIZE bytes"
log_done "$BOOT_OUT size: $BOOT_SIZE bytes"
if test $RUN_TESTS -eq 1
    log_done "Test status: $TEST_STATUS"
end

rm -rf $TMP_DIR
```

## File: `src/primesymbolicmdl/anchor_laws.py`

```python
"""Male deterministicke stromove anchor zakony pre indexovu vetvu."""

from __future__ import annotations

from dataclasses import dataclass

from .bitcost import bits_unsigned_range

_TERMINAL_MODEL_BITS = 3
_OPERATOR_MODEL_BITS = 5


@dataclass(frozen=True)
class LawNode:
    """Nemenny uzol maleho vyrazoveho stromu."""

    kind: str
    value: int | None = None
    left: "LawNode | None" = None
    right: "LawNode | None" = None


def idx_law() -> LawNode:
    """Vrati terminal reprezentujuci index i."""

    return LawNode("idx")


def const_law(value: int) -> LawNode:
    """Vrati konstantny terminal."""

    return LawNode("const", value=int(value))


def add_law(left: LawNode, right: LawNode) -> LawNode:
    """Vrati uzol scitania."""

    return LawNode("add", left=left, right=right)


def sub_law(left: LawNode, right: LawNode) -> LawNode:
    """Vrati uzol odcitania."""

    return LawNode("sub", left=left, right=right)


def mul_small_law(child: LawNode, factor: int) -> LawNode:
    """Vrati uzol nasobenia malou kladnou konstantou."""

    if factor <= 0:
        raise ValueError("factor must be positive")
    return LawNode("mul_small", value=int(factor), left=child)


def floordiv_pow2_law(child: LawNode, shift: int) -> LawNode:
    """Vrati uzol podlahoveho delenia mocninou dvojky."""

    if shift < 0 or shift > 8:
        raise ValueError("shift must be in range 0..8")
    return LawNode("floordiv_pow2", value=int(shift), left=child)


def square_law(child: LawNode) -> LawNode:
    """Vrati uzol druhej mocniny."""

    return LawNode("square", left=child)


def clamp_nonnegative_law(child: LawNode) -> LawNode:
    """Vrati uzol useknutia na nezaporny rozsah."""

    return LawNode("clamp_nonnegative", left=child)


def anchor_value(law: LawNode, index: int) -> int:
    """Vyhodnoti anchor zakon A(i) pre zadany index."""

    if index < 0:
        raise ValueError("index must be non-negative")

    if law.kind == "idx":
        return index
    if law.kind == "const":
        if law.value is None:
            raise ValueError("const node requires a value")
        return int(law.value)
    if law.kind == "add":
        return anchor_value(_require_child(law.left), index) + anchor_value(_require_child(law.right), index)
    if law.kind == "sub":
        return anchor_value(_require_child(law.left), index) - anchor_value(_require_child(law.right), index)
    if law.kind == "mul_small":
        if law.value is None:
            raise ValueError("mul_small node requires a factor")
        return anchor_value(_require_child(law.left), index) * int(law.value)
    if law.kind == "floordiv_pow2":
        if law.value is None:
            raise ValueError("floordiv_pow2 node requires a shift")
        return anchor_value(_require_child(law.left), index) // (1 << int(law.value))
    if law.kind == "square":
        value = anchor_value(_require_child(law.left), index)
        return value * value
    if law.kind == "clamp_nonnegative":
        return max(0, anchor_value(_require_child(law.left), index))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def law_model_bits(law: LawNode) -> int:
    """Vrati konzervativny odhad modelovej ceny stromu bez parametrov."""

    if law.kind in {"idx", "const"}:
        return _TERMINAL_MODEL_BITS
    if law.kind in {"add", "sub"}:
        return _OPERATOR_MODEL_BITS + law_model_bits(_require_child(law.left)) + law_model_bits(_require_child(law.right))
    if law.kind in {"mul_small", "floordiv_pow2", "square", "clamp_nonnegative"}:
        return _OPERATOR_MODEL_BITS + law_model_bits(_require_child(law.left))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def law_parameter_bits(law: LawNode) -> int:
    """Vrati konzervativny odhad ceny ciselnych parametrov stromu."""

    if law.kind == "idx":
        return 0
    if law.kind == "const":
        return _signed_int_bits(_require_value(law.value))
    if law.kind in {"add", "sub"}:
        return law_parameter_bits(_require_child(law.left)) + law_parameter_bits(_require_child(law.right))
    if law.kind == "mul_small":
        return bits_unsigned_range(_require_value(law.value)) + law_parameter_bits(_require_child(law.left))
    if law.kind == "floordiv_pow2":
        return bits_unsigned_range(_require_value(law.value)) + law_parameter_bits(_require_child(law.left))
    if law.kind in {"square", "clamp_nonnegative"}:
        return law_parameter_bits(_require_child(law.left))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def render_law(law: LawNode) -> str:
    """Vrati stabilnu citatelnu reprezentaciu anchor zakona."""

    if law.kind == "idx":
        return "idx"
    if law.kind == "const":
        return str(_require_value(law.value))
    if law.kind == "add":
        return f"add({render_law(_require_child(law.left))}, {render_law(_require_child(law.right))})"
    if law.kind == "sub":
        return f"sub({render_law(_require_child(law.left))}, {render_law(_require_child(law.right))})"
    if law.kind == "mul_small":
        return f"mul_small({render_law(_require_child(law.left))}, {_require_value(law.value)})"
    if law.kind == "floordiv_pow2":
        return f"floordiv_pow2({render_law(_require_child(law.left))}, {_require_value(law.value)})"
    if law.kind == "square":
        return f"square({render_law(_require_child(law.left))})"
    if law.kind == "clamp_nonnegative":
        return f"clamp_nonnegative({render_law(_require_child(law.left))})"
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def _signed_int_bits(value: int) -> int:
    """Vrati konzervativny pocet bitov pre male cele cislo so znamienkom."""

    if value == 0:
        return 1
    return 1 + bits_unsigned_range(abs(value))


def _require_child(child: LawNode | None) -> LawNode:
    """Overi pritomnost potomka pre unary alebo binary uzol."""

    if child is None:
        raise ValueError("law node is missing a child")
    return child


def _require_value(value: int | None) -> int:
    """Overi pritomnost parametra v uzle."""

    if value is None:
        raise ValueError("law node is missing a value")
    return int(value)
```

## File: `src/primesymbolicmdl/ap_rpc.py`

```python
"""File-based Coordinator Protocol RPC helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

DEFAULT_MAX_BYTES = 40_000
FORBIDDEN_BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".mp4",
    ".mov",
    ".zip",
    ".db",
    ".sqlite",
    ".pyc",
}
FORBIDDEN_PATH_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}
LISTING_SKIP_PARTS = FORBIDDEN_PATH_PARTS | {".ap"}


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _new_request_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{secrets.token_hex(4)}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ensure_rpc_directories(repo_root: Path) -> dict[str, Path]:
    rpc_root = repo_root / ".ap" / "rpc"
    inbox = rpc_root / "inbox"
    outbox = rpc_root / "outbox"
    archive = rpc_root / "archive"
    for path in (inbox, outbox, archive):
        path.mkdir(parents=True, exist_ok=True)
    return {"rpc_root": rpc_root, "inbox": inbox, "outbox": outbox, "archive": archive}


def is_forbidden_file_path(path: str) -> bool:
    pure_path = PurePosixPath(path)
    lower_parts = {part.lower() for part in pure_path.parts}
    if lower_parts & FORBIDDEN_PATH_PARTS:
        return True
    return pure_path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES


def validate_repo_relative_path(path: str) -> None:
    if not path or path in {".", "./"}:
        raise ValueError("Path must point to a repository file.")
    pure_path = PurePosixPath(path)
    if pure_path.is_absolute():
        raise ValueError("Absolute paths are forbidden.")
    if any(part == ".." for part in pure_path.parts):
        raise ValueError("Parent path traversal is forbidden.")
    if is_forbidden_file_path(path):
        raise ValueError(f"Forbidden file path: {path}")


def build_request(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    from_role: str = "ORCHESTRATOR",
    to_role: str = "WORKER",
    request_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    if not method:
        raise ValueError("RPC method is required.")
    request_params = dict(params or {})
    if method == "repo.get_file":
        if "path" not in request_params:
            raise ValueError("repo.get_file requires a path parameter.")
        validate_repo_relative_path(str(request_params["path"]))
        if "max_bytes" in request_params:
            request_params["max_bytes"] = _normalize_max_bytes(request_params["max_bytes"])
    return {
        "id": request_id or _new_request_id(),
        "type": "rpc_request",
        "from": from_role,
        "to": to_role,
        "method": method,
        "params": request_params,
        "created_at": created_at or _now_iso(),
    }


def build_response(
    request_id: str,
    method: str,
    *,
    status: str,
    result: dict[str, Any] | None = None,
    error: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    return {
        "id": request_id,
        "type": "rpc_response",
        "status": status,
        "method": method,
        "result": result if status == "ok" else None,
        "error": error if status == "error" else None,
        "created_at": created_at or _now_iso(),
    }


def _normalize_max_bytes(raw_value: Any) -> int:
    try:
        max_bytes = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("max_bytes must be an integer.") from exc
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive.")
    return max_bytes


def _run_git_command(repo_root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git is not available in PATH.") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or f"git {' '.join(args)} failed."
        raise RuntimeError(message) from exc
    return completed.stdout.rstrip("\n")


def _is_hidden_from_listing(path: str) -> bool:
    parts = {part.lower() for part in PurePosixPath(path).parts}
    return bool(parts & LISTING_SKIP_PARTS)


def _fallback_list_files(repo_root: Path) -> list[str]:
    files: list[str] = []
    for candidate in repo_root.rglob("*"):
        if not candidate.is_file():
            continue
        relative = candidate.relative_to(repo_root).as_posix()
        if _is_hidden_from_listing(relative):
            continue
        files.append(relative)
    return sorted(set(files))


def _repo_status(repo_root: Path) -> dict[str, Any]:
    return {
        "branch": _run_git_command(repo_root, "branch", "--show-current"),
        "head": _run_git_command(repo_root, "rev-parse", "HEAD"),
        "status_short": _run_git_command(repo_root, "status", "--short"),
    }


def _repo_diff_stat(repo_root: Path) -> dict[str, Any]:
    return {"diff_stat": _run_git_command(repo_root, "diff", "--stat")}


def _repo_list_files(repo_root: Path) -> dict[str, Any]:
    try:
        tracked = _run_git_command(repo_root, "ls-files").splitlines()
        untracked = _run_git_command(repo_root, "ls-files", "--others", "--exclude-standard").splitlines()
        files = sorted(
            {
                path
                for path in tracked + untracked
                if path and not _is_hidden_from_listing(path)
            }
        )
    except RuntimeError:
        files = _fallback_list_files(repo_root)
    return {"files": files}


def _resolve_repo_path(repo_root: Path, relative_path: str) -> Path:
    validate_repo_relative_path(relative_path)
    candidate = (repo_root / PurePosixPath(relative_path)).resolve(strict=False)
    resolved_root = repo_root.resolve()
    if not candidate.is_relative_to(resolved_root):
        raise ValueError("Resolved path escapes the repository root.")
    return candidate


def _repo_get_file(repo_root: Path, params: dict[str, Any]) -> dict[str, Any]:
    path = str(params.get("path") or "")
    max_bytes = _normalize_max_bytes(params.get("max_bytes", DEFAULT_MAX_BYTES))
    candidate = _resolve_repo_path(repo_root, path)
    if not candidate.exists():
        raise FileNotFoundError(f"Repository file does not exist: {path}")
    if not candidate.is_file():
        raise ValueError(f"Repository path is not a file: {path}")
    data = candidate.read_bytes()
    excerpt = data[:max_bytes].decode("utf-8", errors="replace")
    return {
        "path": path,
        "content": excerpt,
        "size_bytes": len(data),
        "truncated": len(data) > max_bytes,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def handle_request(request: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    request_id = str(request.get("id") or "unknown_request")
    method = str(request.get("method") or "")
    try:
        if request.get("type") != "rpc_request":
            raise ValueError('Request type must be "rpc_request".')
        params = request.get("params") or {}
        if not isinstance(params, dict):
            raise ValueError("Request params must be a JSON object.")
        if method == "repo.status":
            result = _repo_status(repo_root)
        elif method == "repo.diff_stat":
            result = _repo_diff_stat(repo_root)
        elif method == "repo.list_files":
            result = _repo_list_files(repo_root)
        elif method == "repo.get_file":
            result = _repo_get_file(repo_root, params)
        else:
            raise ValueError(f"Unknown RPC method: {method}")
        return build_response(request_id, method, status="ok", result=result)
    except Exception as exc:
        return build_response(request_id, method, status="error", error=str(exc))


def _load_request_file(request_path: Path) -> dict[str, Any]:
    raw_payload = json.loads(request_path.read_text(encoding="utf-8"))
    if not isinstance(raw_payload, dict):
        raise ValueError("Request JSON root must be an object.")
    return raw_payload


def _pick_oldest_request(inbox_dir: Path) -> Path | None:
    candidates = list(inbox_dir.glob("*.json"))
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: (path.stat().st_mtime, path.name))[0]


def create_request_file(
    repo_root: Path,
    method: str,
    *,
    path: str | None = None,
    max_bytes: int | None = None,
) -> dict[str, Any]:
    directories = ensure_rpc_directories(repo_root)
    params: dict[str, Any] = {}
    if path is not None:
        params["path"] = path
    if max_bytes is not None:
        params["max_bytes"] = max_bytes
    request = build_request(method, params)
    request_path = directories["inbox"] / f"{request['id']}.json"
    _write_json(request_path, request)
    return {
        "request_id": request["id"],
        "request_path": str(request_path.resolve()),
    }


def handle_request_file(repo_root: Path, request_path: Path | None = None) -> dict[str, Any]:
    directories = ensure_rpc_directories(repo_root)
    selected_request = request_path or _pick_oldest_request(directories["inbox"])
    if selected_request is None:
        raise FileNotFoundError("No RPC request file found in .ap/rpc/inbox.")

    selected_request = selected_request.resolve(strict=False)
    request_id = selected_request.stem
    method = ""

    try:
        request = _load_request_file(selected_request)
        request.setdefault("id", request_id)
        method = str(request.get("method") or "")
        response = handle_request(request, repo_root)
    except Exception as exc:
        response = build_response(
            request_id,
            method,
            status="error",
            error=f"Invalid request file: {exc}",
        )

    response_path = directories["outbox"] / f"{request_id}.json"
    _write_json(response_path, response)

    archive_path: Path | None = None
    if selected_request.exists():
        archive_path = directories["archive"] / f"{request_id}.json"
        if selected_request != archive_path:
            shutil.move(str(selected_request), str(archive_path))
        else:
            archive_path = selected_request

    return {
        "request_id": request_id,
        "request_path": str(selected_request),
        "response_path": str(response_path.resolve()),
        "archive_path": str(archive_path.resolve()) if archive_path is not None else None,
        "response_status": str(response["status"]),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Coordinator Protocol RPC helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    request_parser = subparsers.add_parser("request", help="Create an RPC request file.")
    request_parser.add_argument("--repo-root", default=".", help="Repository root directory.")
    request_parser.add_argument("--method", required=True, help="RPC method name.")
    request_parser.add_argument("--path", help="Repository-relative file path.")
    request_parser.add_argument("--max-bytes", type=int, help="Optional truncation limit.")

    handle_parser = subparsers.add_parser("handle", help="Handle one RPC request file.")
    handle_parser.add_argument("--repo-root", default=".", help="Repository root directory.")
    handle_parser.add_argument("--request", help="Explicit request file path.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        if args.command == "request":
            payload = create_request_file(
                repo_root,
                args.method,
                path=args.path,
                max_bytes=args.max_bytes,
            )
        else:
            request_path = Path(args.request) if args.request else None
            payload = handle_request_file(repo_root, request_path)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## File: `src/primesymbolicmdl/bitcost.py`

```python
"""Konzervativne a citatelne bitove odhady pre v0 experiment."""

from __future__ import annotations

import math

from .blocks import SUPPORTED_WIDTHS
from .prime_anchors import prime_anchor_residual, prime_count

# Konzervativny fixny rozpocet pre identifikator transformacie a mod kotvy.
_FIXED_MODEL_BITS = 8
# Konzervativny fixny rozpocet pre experimentalny header chunku vo v0.
_FIXED_HEADER_BITS = 32


def bits_raw(data_size_bytes: int) -> int:
    """Vrati presny pocet bitov pre surove bajty."""

    if data_size_bytes < 0:
        raise ValueError("data_size_bytes must be non-negative")
    return data_size_bytes * 8


def bits_unsigned_range(max_value: int) -> int:
    """Vrati pocet bitov potrebnych pre rozsah od 0 po max_value."""

    if max_value < 0:
        raise ValueError("max_value must be non-negative")
    if max_value == 0:
        return 0
    return math.ceil(math.log2(max_value + 1))


def bits_signed_range(min_value: int, max_value: int) -> int:
    """Vrati pocet bitov potrebnych pre cely podpisany rozsah."""

    if min_value > max_value:
        raise ValueError("min_value must not exceed max_value")

    span = max_value - min_value + 1
    if span <= 1:
        return 0
    return math.ceil(math.log2(span))


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze sirka blokov patri medzi podporovane hodnoty."""

    if width_bits not in SUPPORTED_WIDTHS:
        raise ValueError(f"Unsupported block width: {width_bits}")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer celkovej ceny voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits


def estimate_prime_anchor_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    mode: str,
) -> dict:
    """Odhadne cenu prime-index plus reziduum reprezentacie pre v0 vyskum."""

    _validate_width_bits(width_bits)

    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    max_block_value = 1 << width_bits
    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")

    for block in blocks:
        if block < 0 or block >= max_block_value:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")

    raw_bits = bits_raw(original_size)
    block_count = len(blocks)
    flag_bits = block_count

    anchors: list[int] = []
    residuals: list[int] = []
    escape_count = 0

    for block in blocks:
        if mode == "lower" and block < 2:
            escape_count += 1
            continue

        anchor, residual = prime_anchor_residual(block, mode)
        residuals.append(residual)
        anchors.append(anchor)

    if anchors:
        # Maximalny index je zhodny s poziciou najvacsieho anchoru v utriedenom
        # zozname vsetkych prvocisel do danej hranice, ale nepouzivame jeho
        # plnu materializaciu iba na ucel odhadu sirky indexu.
        max_index = prime_count(max(anchors)) - 1
        index_width = bits_unsigned_range(max_index)
        index_bits = index_width * len(anchors)
    else:
        index_bits = 0

    if residuals:
        residual_width = bits_signed_range(min(residuals), max(residuals))
        residual_bits = residual_width * len(residuals)
    else:
        residual_bits = 0

    escape_bits = width_bits * escape_count
    total_bits = (
        _FIXED_MODEL_BITS
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )

    return {
        "raw_bits": raw_bits,
        "model_bits": _FIXED_MODEL_BITS,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "mode": mode,
        "width_bits": width_bits,
        "block_count": block_count,
    }
```

## File: `src/primesymbolicmdl/bitstream.py`

```python
"""Male deterministicke bitstream primitiva pre binarne payloady."""

from __future__ import annotations


class BitWriter:
    """Zapisuje bity po jednom v stabilnom poradi od najvyssieho bitu."""

    def __init__(self) -> None:
        self._buffer = bytearray()
        self._current_byte = 0
        self._bits_in_current = 0
        self._bit_length = 0

    @property
    def bit_length(self) -> int:
        """Vrati pocet uz zapisanych bitov pred paddingom."""

        return self._bit_length

    def write_bit(self, value: int) -> None:
        """Zapise jeden bit do streamu."""

        bit = _coerce_bit(value)
        self._current_byte = (self._current_byte << 1) | bit
        self._bits_in_current += 1
        self._bit_length += 1

        if self._bits_in_current == 8:
            self._buffer.append(self._current_byte)
            self._current_byte = 0
            self._bits_in_current = 0

    def write_bits(self, value: int, width: int) -> None:
        """Zapise `width` bitov z hodnoty v MSB-first poradi."""

        if not isinstance(width, int) or width < 0:
            raise ValueError("width must be a non-negative integer")
        if not isinstance(value, int) or value < 0:
            raise ValueError("value must be a non-negative integer")
        if width == 0:
            if value != 0:
                raise ValueError("value must be zero when width is zero")
            return
        if value >= (1 << width):
            raise ValueError("value does not fit into the requested width")

        for shift in range(width - 1, -1, -1):
            self.write_bit((value >> shift) & 1)

    def write_bool(self, value: bool) -> None:
        """Zapise bool ako jeden bit."""

        self.write_bit(1 if value else 0)

    def to_bytes(self) -> bytes:
        """Vrati aktualny stream doplneny nulami po koniec posledneho bajtu."""

        output = bytearray(self._buffer)
        if self._bits_in_current:
            output.append(self._current_byte << (8 - self._bits_in_current))
        return bytes(output)


class BitReader:
    """Cita bity v rovnakom MSB-first poradi ako `BitWriter` zapisuje."""

    def __init__(self, data: bytes) -> None:
        self._data = bytes(data)
        self._byte_index = 0
        self._bit_index = 0
        self._bits_consumed = 0

    @property
    def bits_consumed(self) -> int:
        """Vrati pocet precitanych bitov."""

        return self._bits_consumed

    def read_bit(self) -> int:
        """Precita jeden bit zo streamu."""

        if self._byte_index >= len(self._data):
            raise ValueError("No more bits remain in the stream")

        current_byte = self._data[self._byte_index]
        bit = (current_byte >> (7 - self._bit_index)) & 1

        self._bit_index += 1
        self._bits_consumed += 1
        if self._bit_index == 8:
            self._byte_index += 1
            self._bit_index = 0

        return bit

    def read_bits(self, width: int) -> int:
        """Precita `width` bitov a vrati ich ako nezapornu hodnotu."""

        if not isinstance(width, int) or width < 0:
            raise ValueError("width must be a non-negative integer")

        value = 0
        for _ in range(width):
            value = (value << 1) | self.read_bit()
        return value

    def read_bool(self) -> bool:
        """Precita jeden bit a vrati ho ako bool."""

        return bool(self.read_bit())


def encode_unsigned_varint(n: int) -> bytes:
    """Zakoduje nezaporne cele cislo do deterministickeho unsigned varintu."""

    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")

    value = n
    output = bytearray()
    while True:
        chunk = value & 0x7F
        value >>= 7
        if value:
            output.append(chunk | 0x80)
            continue
        output.append(chunk)
        return bytes(output)


def decode_unsigned_varint(data: bytes, offset: int = 0) -> tuple[int, int]:
    """Dekoduje unsigned varint zo zadaneho offsetu a vrati novy offset."""

    payload = bytes(data)
    if not isinstance(offset, int) or offset < 0 or offset > len(payload):
        raise ValueError("offset must point inside the input bytes")

    value = 0
    shift = 0
    position = offset

    while position < len(payload):
        byte_value = payload[position]
        position += 1
        value |= (byte_value & 0x7F) << shift
        if not (byte_value & 0x80):
            return value, position
        shift += 7

    raise ValueError("Truncated unsigned varint")


def zigzag_encode(n: int) -> int:
    """Prevedie podpisane cele cislo na nezaporny zigzag tvar."""

    value = int(n)
    return (value << 1) if value >= 0 else ((-value << 1) - 1)


def zigzag_decode(z: int) -> int:
    """Vrati povodne podpisane cele cislo zo zigzag reprezentacie."""

    value = int(z)
    if value < 0:
        raise ValueError("zigzag value must be non-negative")
    if value % 2 == 0:
        return value // 2
    return -((value + 1) // 2)


def _coerce_bit(value: int) -> int:
    """Prevedie vstup na korektny 0/1 bit."""

    if value in {0, False}:
        return 0
    if value in {1, True}:
        return 1
    raise ValueError("bit value must be 0 or 1")
```

## File: `src/primesymbolicmdl/blocks.py`

```python
"""Pomocne funkcie pre deterministicke balenie blokov."""

from __future__ import annotations

SUPPORTED_WIDTHS = {8, 16, 24, 32}


def _width_bytes(width_bits: int) -> int:
    """Vrati sirku bloku v bajtoch alebo vyhodi chybu."""

    if width_bits not in SUPPORTED_WIDTHS:
        raise ValueError(f"Unsupported block width: {width_bits}")
    return width_bits // 8


def bytes_to_uint_blocks(data: bytes, width_bits: int) -> list[int]:
    """Prevedie byty na big-endian bloky nezapornych cisel."""

    width_bytes = _width_bytes(width_bits)
    if not data:
        return []

    blocks: list[int] = []
    for start in range(0, len(data), width_bytes):
        chunk = data[start : start + width_bytes]
        if len(chunk) < width_bytes:
            chunk = chunk + (b"\x00" * (width_bytes - len(chunk)))
        blocks.append(int.from_bytes(chunk, "big"))
    return blocks


def uint_blocks_to_bytes(blocks: list[int], width_bits: int, original_size: int) -> bytes:
    """Zlozi bloky spat na byty a oreze nulove doplnenie na povodnu dlzku."""

    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    width_bytes = _width_bytes(width_bits)
    upper_bound = 1 << width_bits
    output = bytearray()

    for block in blocks:
        if block < 0 or block >= upper_bound:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")
        output.extend(block.to_bytes(width_bytes, "big"))

    if original_size > len(output):
        raise ValueError("original_size exceeds decoded byte length")

    return bytes(output[:original_size])
```

## File: `src/primesymbolicmdl/codec.py`

```python
"""Reverzibilny experimentalny codec s raw fallbackom."""

from __future__ import annotations

from .bitcost import estimate_prime_anchor_cost
from .blocks import bytes_to_uint_blocks, uint_blocks_to_bytes
from .prime_anchors import prime_anchor_residual


def compress_experimental(data: bytes, width_bits: int = 16, mode: str = "nearest") -> dict:
    """Skusi prime-anchor vetvu a inak ulozi data ako raw."""

    raw_bytes = bytes(data)
    blocks = bytes_to_uint_blocks(raw_bytes, width_bits)
    estimated_costs = estimate_prime_anchor_cost(blocks, width_bits, len(raw_bytes), mode)

    metadata = {
        "mode": mode,
        "estimated_costs": estimated_costs,
        "experimental": True,
    }

    if estimated_costs["total_bits"] >= estimated_costs["raw_bits"]:
        return {
            "codec": "raw",
            "width_bits": width_bits,
            "original_size": len(raw_bytes),
            "data": raw_bytes,
            "metadata": metadata,
        }

    anchors: list[int] = []
    residuals: list[int] = []
    for block in blocks:
        anchor, residual = prime_anchor_residual(block, mode)
        anchors.append(anchor)
        residuals.append(residual)

    return {
        "codec": "prime_anchor",
        "width_bits": width_bits,
        "original_size": len(raw_bytes),
        "anchors": anchors,
        "residuals": residuals,
        "metadata": metadata,
    }


def decompress_experimental(payload: dict) -> bytes:
    """Dekoduje raw alebo prime-anchor payload bez straty informacie."""

    codec = payload.get("codec")
    width_bits = payload.get("width_bits")
    original_size = payload.get("original_size")

    if not isinstance(width_bits, int):
        raise ValueError("width_bits must be an integer")
    if not isinstance(original_size, int) or original_size < 0:
        raise ValueError("original_size must be a non-negative integer")

    if codec == "raw":
        raw_bytes = bytes(payload.get("data", b""))
        if len(raw_bytes) != original_size:
            raise ValueError("Raw payload length does not match original_size")
        return raw_bytes

    if codec == "prime_anchor":
        anchors = payload.get("anchors")
        residuals = payload.get("residuals")

        if not isinstance(anchors, list) or not isinstance(residuals, list):
            raise ValueError("Prime-anchor payload must contain anchor and residual lists")
        if len(anchors) != len(residuals):
            raise ValueError("Anchor and residual counts must match")

        blocks = [anchor + residual for anchor, residual in zip(anchors, residuals)]
        return uint_blocks_to_bytes(blocks, width_bits, original_size)

    raise ValueError(f"Unsupported codec: {codec}")
```

## File: `src/PrimeSymbolicMDL.egg-info/dependency_links.txt`

```text

```

## File: `src/PrimeSymbolicMDL.egg-info/PKG-INFO`

```text
Metadata-Version: 2.4
Name: PrimeSymbolicMDL
Version: 0.1.0
Summary: Experimental MDL-guided anchor-and-residual compression harness.
Requires-Python: >=3.10
Description-Content-Type: text/markdown
Provides-Extra: dev
Requires-Dist: pytest; extra == "dev"

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
- a shared residual codec layer with fixed-width, zero-RLE, and byte-RLE research baselines
- an experimental huge-anchor binary bitstream container with exact byte-length measurement
- a small Tkinter research cockpit for grayscale image simulations
- pytest coverage for round-trip and random-data sanity checks

## GP-lite Indexed Anchor Law Search

The new GP-lite branch evolves decoder-known anchor laws `A(i)`.

- The encoder stores an index `i` plus a residual `x - A(i)`.
- The law is only useful if total transmitted bits beat raw fallback.
- This is different from a predictor-only model because the decoder reconstructs anchors from the transmitted index and the law tree.
- The current cost model uses fixed-width index accounting and a small residual codec selector baseline.
- Entropy coding, PySR, and heavier symbolic regression remain intentionally deferred.

## Scaled Prime-index Branch

The repository now also includes a scaled prime-index experiment over larger Python integer blocks.

- Bytes can be packed into big-endian Python integer blocks up to 128 bits for reversible block experiments.
- The current exact prime-anchor branch is intentionally limited to `width_bits <= 64`.
- The model tries `x = prev_prime(index << shift) + diff`.
- In this construction, `index` is smaller than the original block value and the decoder reconstructs the prime anchor from `index` and `shift`.
- The model only matters when the full transmitted cost of flags, indices, residual payload, escapes, headers, and model parameters beats raw storage.
- Arbitrary-size exact prime search is deferred. This branch does not fake primality above 64-bit integers.
- Random data is expected to often lose against raw storage, and that is an honest result.
- This branch currently ships as a CLI and testable module, not yet as a GUI-integrated optimizer.

## Huge Anchor Portfolio

The huge anchor portfolio generalizes the scaled prime-index branch into a broader family benchmark.

- Each family tests the same idea: `x = anchor(index, params) + diff`.
- `scaled_prime` is only one family inside that larger search space.
- Other current families include `linear_shift`, `affine_shift`, `multiple`, and `square`.
- If a simpler family beats `scaled_prime`, that is important evidence against prime-anchor special pleading.
- Synthetic wins are useful because they validate the exact-lossless mechanism and full accounting, not because they prove universal compression.
- Random-byte sanity remains mandatory.
- The real result only matters when total transmitted bits beat raw storage after counting model, parameter, header, flag, index, residual, and escape costs.

## Huge-anchor Binary Proof-of-concept

The repository now also includes a first real binary container for huge-anchor payloads.

- Earlier huge-anchor experiments used exact research payloads plus estimated bit accounting.
- The new container produces real `compressed_bytes` and therefore real `actual_bits = len(blob) * 8`.
- A synthetic win now means more than a promising estimate: the branch can emit a smaller exact-decodable blob for structure-compatible generated data.
- Random-byte sanity remains mandatory. If the binary container loses to raw bytes, that is the correct result.
- This is still not a universal file compressor. It is a narrow proof that one exact binary huge-anchor path can sometimes beat raw bytes on favorable synthetic data.

## Actual-size Reranking

Estimated MDL accounting remains the fast search heuristic, but it is no longer the final judge for the binary huge-anchor path.

- The search still finds promising candidates by estimated `total_bits`.
- The binary stage now serializes the top `N` estimated candidates and reranks them by real `compressed_bytes`.
- This makes container overhead visible instead of assumed away.
- An estimated win can still become `raw_fallback` after real byte serialization.
- Actual compressed bytes are the stronger evidence because they include headers, alignment, and real residual payload size.

## Residual Codec Layer

Predictors and anchor laws both create a residual stream:

```text
x = predicted_or_anchor + residual
```

This repository now includes a small shared residual codec layer so different branches can compare against the same residual backend.

- `fixed_signed` is the deterministic fixed-width signed baseline.
- `zero_rle` is a deterministic zero-run-length baseline for residual streams with many zeros.
- `byte_rle` is a raw-like baseline for repeated pixel bytes.
- `raw_bytes` remains the honest fallback baseline for byte streams.

This is still not ANS or arithmetic coding. Entropy coding remains deferred. Exact roundtrip remains mandatory for any branch that claims decode support.

## Optimizer Architecture

The repository now exposes a small optimizer registry with seven visible choices:

- `GP-lite`: the existing tree-based indexed anchor-law search
- `SOMA`: a small continuous-parameter migration optimizer over affine and quadratic anchor laws
- `GP`: an honest placeholder for future richer topology search
- `ADAM`: an honest placeholder for future differentiable parameter tuning
- `Image-predictor`: a deterministic 2D grayscale predictor baseline with exact residual roundtrip
- `Image-GP-lite`: a deterministic expression-tree search over 2D pixel context
- `Image-SOMA`: a deterministic fixed-point linear search over 2D pixel context

All optimizers are judged by the same idea: the result only matters if `total_bits < raw_bits` after counting model, parameter, index, residual, flag, header, and escape costs.

## Image-aware Search Optimizers

The repository now separates a fair manual baseline from two image-aware search branches:

- `Image-predictor` is the manual baseline over small decoder-known 2D predictors.
- `Image-GP-lite` searches tiny expression trees over decoder-known pixel context.
- `Image-SOMA` tunes a fixed-point linear predictor over decoder-known pixel context.
- All three reuse the same shared residual codec layer.
- A result only matters if `total_bits < raw_bits`.
- Synthetic gradients, checkerboards, and ramps are useful for deterministic debugging, not as proof of universal compression.

## Image-GP-lite Primitive Ablations

`Image-GP-lite` can now be run with explicit primitive sets:

- `local` uses only decoder-known neighborhood context such as `left`, `up`, and `up_left`.
- `ramp` adds procedural coordinate ramps such as `x_ramp`, `y_ramp`, and `diag_ramp`.
- `structure` adds block/parity primitives intended for checker-like and piecewise structure baselines.

Important interpretation rules:

- `checker_parity` wins are valid only as explicit primitive baselines, not as evidence that the search discovered a universal image law.
- Ablation reports must include the primitive set name or they are not comparable.
- Synthetic wins still need the same `total_bits < raw_bits` accounting rule as every other branch.

## GUI Research Cockpit

The first GUI is a stdlib Tkinter cockpit focused on generated grayscale image simulations.

- It lets you choose an optimizer and a tiny image dataset.
- It reports raw size in bits and estimated transmitted size in bits.
- It can also report which residual codec or raw-byte baseline won under the current accounting.
- It is a research UI, not a final file compressor.
- Estimated bit accounting now includes a small residual codec selector, but entropy coding is still deferred.

## Analytic Coding Snapshots

Use the fish snapshot helper to generate an agent-readable repository state:

```fish
fish scripts/ap_snapshot.fish
fish scripts/ap_snapshot.fish --run-tests
```

This generates:

- `BRAIN.md`
- `BOOT.md`

These files are intended for orchestration and repository-state handoff, not as proof of compression quality.

## Analytic Programming / Analytic Coding

Recommended interactive fish workflow:

```fish
source .venv/bin/activate.fish
```

Core AP commands:

```fish
fish scripts/ap_snapshot.fish --run-tests
fish scripts/ap_chat_append.fish --role worker --message "..." --tldr "..."
fish scripts/ap_cycle_close.fish --message "..." --tldr "..."
```

AP artifact roles:

- `AP.md` is the system-wide protocol.
- `COORDINATOR_PROTOCOL.md` extends AP with file-based RPC.
- `AP_ORCHESTRATOR.md` explains the orchestrator-side discipline.
- `AP_WORKER.md` is the Worker doctrine.
- `NEXT_ORCHESTRATOR.md` is the strategic handoff for the next Orchestrator.
- `BRAIN.md` and `BOOT.md` are generated repository snapshots.

## Coordinator Protocol

Coordinator Protocol is a file-based, repo-centered RPC proof of concept for `COOPERATOR`, `ORCHESTRATOR`, and `WORKER`.

- The repository remains the source of truth.
- `BRAIN.md` and `BOOT.md` remain broad snapshots.
- `CHAT.md` remains the append-only coordination ledger.
- RPC is the narrow lane for targeted status and file requests.
- This means the Orchestrator does not always need the whole diff when it only needs one file or one status view.
- The Orchestrator should request exact repo information via RPC instead of guessing from partial context.
- The default RPC surface is read-only and preserves the same safety model: no secrets access, no network dependency, and no git write commands.
- A continuation session should ideally start with `NEXT_ORCHESTRATOR.md` and `NEXT_AGENT.md`.

RPC commands:

```fish
fish scripts/ap_rpc_call.fish --method repo.status
fish scripts/ap_rpc_call.fish --method repo.get_file --path AP.md
fish scripts/ap_rpc_request.fish --method repo.get_file --path src/primesymbolicmdl/simulation.py
fish scripts/ap_rpc_handle_next.fish
```

Scaled-prime demo command:

```bash
python -m primesymbolicmdl.scaled_prime_demo
```

Huge-anchor portfolio demo command:

```bash
python -m primesymbolicmdl.huge_anchor_demo
```

Huge-anchor binary demo command:

```bash
python -m primesymbolicmdl.huge_anchor_binary_demo
```

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
- general file format packaging beyond the current huge-anchor proof-of-concept
```

## File: `src/PrimeSymbolicMDL.egg-info/requires.txt`

```text

[dev]
pytest
```

## File: `src/PrimeSymbolicMDL.egg-info/SOURCES.txt`

```text
README.md
pyproject.toml
src/PrimeSymbolicMDL.egg-info/PKG-INFO
src/PrimeSymbolicMDL.egg-info/SOURCES.txt
src/PrimeSymbolicMDL.egg-info/dependency_links.txt
src/PrimeSymbolicMDL.egg-info/requires.txt
src/PrimeSymbolicMDL.egg-info/top_level.txt
src/primesymbolicmdl/__init__.py
src/primesymbolicmdl/anchor_laws.py
src/primesymbolicmdl/ap_rpc.py
src/primesymbolicmdl/bitcost.py
src/primesymbolicmdl/bitstream.py
src/primesymbolicmdl/blocks.py
src/primesymbolicmdl/codec.py
src/primesymbolicmdl/evolution.py
src/primesymbolicmdl/experiments.py
src/primesymbolicmdl/gui.py
src/primesymbolicmdl/huge_anchor_binary.py
src/primesymbolicmdl/huge_anchor_binary_demo.py
src/primesymbolicmdl/huge_anchor_branch.py
src/primesymbolicmdl/huge_anchor_datasets.py
src/primesymbolicmdl/huge_anchor_demo.py
src/primesymbolicmdl/huge_anchor_file.py
src/primesymbolicmdl/huge_anchor_file_cli.py
src/primesymbolicmdl/huge_anchor_models.py
src/primesymbolicmdl/huge_anchor_search.py
src/primesymbolicmdl/huge_blocks.py
src/primesymbolicmdl/image_ablation.py
src/primesymbolicmdl/image_context_laws.py
src/primesymbolicmdl/image_datasets.py
src/primesymbolicmdl/image_law_branch.py
src/primesymbolicmdl/image_predictor_branch.py
src/primesymbolicmdl/image_predictors.py
src/primesymbolicmdl/index_branch.py
src/primesymbolicmdl/law_demo.py
src/primesymbolicmdl/law_search.py
src/primesymbolicmdl/prime_anchors.py
src/primesymbolicmdl/prime_bigint.py
src/primesymbolicmdl/residual_binary.py
src/primesymbolicmdl/residual_codecs.py
src/primesymbolicmdl/scaled_prime_demo.py
src/primesymbolicmdl/scaled_prime_index.py
src/primesymbolicmdl/scaled_prime_search.py
src/primesymbolicmdl/sim_demo.py
src/primesymbolicmdl/simulation.py
src/primesymbolicmdl/optimizers/__init__.py
src/primesymbolicmdl/optimizers/base.py
src/primesymbolicmdl/optimizers/gplite_adapter.py
src/primesymbolicmdl/optimizers/image_gplite.py
src/primesymbolicmdl/optimizers/image_predictor.py
src/primesymbolicmdl/optimizers/image_soma.py
src/primesymbolicmdl/optimizers/placeholders.py
src/primesymbolicmdl/optimizers/registry.py
src/primesymbolicmdl/optimizers/soma.py
tests/test_anchor_laws.py
tests/test_ap_rpc.py
tests/test_bitcost.py
tests/test_bitstream.py
tests/test_blocks.py
tests/test_codec_roundtrip.py
tests/test_evolution.py
tests/test_experiments.py
tests/test_gui_import.py
tests/test_huge_anchor_binary.py
tests/test_huge_anchor_binary_demo.py
tests/test_huge_anchor_branch.py
tests/test_huge_anchor_datasets.py
tests/test_huge_anchor_demo.py
tests/test_huge_anchor_file_cli.py
tests/test_huge_anchor_models.py
tests/test_huge_anchor_search.py
tests/test_huge_blocks.py
tests/test_image_ablation.py
tests/test_image_context_laws.py
tests/test_image_datasets.py
tests/test_image_gplite_optimizer.py
tests/test_image_law_branch.py
tests/test_image_predictor_branch.py
tests/test_image_predictor_optimizer.py
tests/test_image_predictors.py
tests/test_image_soma_optimizer.py
tests/test_index_branch.py
tests/test_law_demo.py
tests/test_law_search.py
tests/test_optimizers.py
tests/test_prime_anchors.py
tests/test_prime_bigint.py
tests/test_random_sanity.py
tests/test_repository_rules.py
tests/test_residual_binary.py
tests/test_residual_codecs.py
tests/test_scaled_prime_demo.py
tests/test_scaled_prime_index.py
tests/test_scaled_prime_search.py
tests/test_sim_demo.py
tests/test_simulation.py```

## File: `src/PrimeSymbolicMDL.egg-info/top_level.txt`

```text
primesymbolicmdl
```

## File: `src/primesymbolicmdl/evolution.py`

```python
"""Deterministicke evolucne hladanie indexovanych anchor modelov."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from random import Random

from .bitcost import bits_raw, bits_signed_range, bits_unsigned_range
from .blocks import bytes_to_uint_blocks
from .prime_anchors import nearest_lower_prime, prime_count

_FIXED_MODEL_BITS = 12
_FIXED_HEADER_BITS = 32
_SUPPORTED_FAMILIES = ("prime_lower", "multiple", "power", "square")


@dataclass(frozen=True, order=True)
class AnchorGenome:
    """Jednoducha genomova reprezentacia anchor rodiny a parametra."""

    family: str
    param: int = 0


def _canonicalize_genome(genome: AnchorGenome, max_value: int) -> AnchorGenome:
    """Normalizuje genom do maleho deterministickeho priestoru."""

    if genome.family not in _SUPPORTED_FAMILIES:
        raise ValueError(f"Unsupported genome family: {genome.family}")

    if genome.family == "prime_lower":
        return AnchorGenome("prime_lower", 0)
    if genome.family == "square":
        return AnchorGenome("square", 0)
    if genome.family == "multiple":
        upper = max(1, min(max_value, 4096))
        return AnchorGenome("multiple", min(max(1, genome.param), upper))
    upper = max(2, min(max_value, 16))
    return AnchorGenome("power", min(max(2, genome.param), upper))


def encode_block_with_genome(block: int, genome: AnchorGenome) -> dict:
    """Zakoduje jeden blok cez lower-anchor genom."""

    if block < 0:
        raise ValueError("block must be non-negative")

    if genome.family == "prime_lower":
        if block < 2:
            return {"escaped": True, "anchor": None, "index": None, "residual": None}
        anchor = nearest_lower_prime(block)
        if anchor is None:
            return {"escaped": True, "anchor": None, "index": None, "residual": None}
        return {
            "escaped": False,
            "anchor": anchor,
            "index": prime_count(anchor) - 1,
            "residual": block - anchor,
        }

    if genome.family == "multiple":
        step = max(1, genome.param)
        anchor = (block // step) * step
        return {
            "escaped": False,
            "anchor": anchor,
            "index": anchor // step,
            "residual": block - anchor,
        }

    if genome.family == "power":
        base = max(2, genome.param)
        if block < 1:
            return {"escaped": True, "anchor": None, "index": None, "residual": None}
        anchor = 1
        index = 0
        while anchor * base <= block:
            anchor *= base
            index += 1
        return {
            "escaped": False,
            "anchor": anchor,
            "index": index,
            "residual": block - anchor,
        }

    if genome.family == "square":
        root = isqrt(block)
        anchor = root * root
        return {
            "escaped": False,
            "anchor": anchor,
            "index": root,
            "residual": block - anchor,
        }

    raise ValueError(f"Unsupported genome family: {genome.family}")


def estimate_genome_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    genome: AnchorGenome,
) -> dict:
    """Spocita fitnes kandidata ako plnu odhadovanu cenu modelu."""

    if width_bits <= 0:
        raise ValueError("width_bits must be positive")
    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    raw_bits = bits_raw(original_size)
    block_count = len(blocks)
    flag_bits = block_count

    escaped_count = 0
    indices: list[int] = []
    residuals: list[int] = []

    for block in blocks:
        encoded = encode_block_with_genome(block, genome)
        if encoded["escaped"]:
            escaped_count += 1
            continue
        indices.append(int(encoded["index"]))
        residuals.append(int(encoded["residual"]))

    index_bits = 0
    if indices:
        index_width = bits_unsigned_range(max(indices))
        index_bits = index_width * len(indices)

    residual_bits = 0
    if residuals:
        residual_width = bits_signed_range(min(residuals), max(residuals))
        residual_bits = residual_width * len(residuals)

    param_bits = 0 if genome.param <= 0 else bits_unsigned_range(genome.param)
    model_bits = _FIXED_MODEL_BITS + 3 + param_bits
    escape_bits = escaped_count * width_bits
    total_bits = (
        model_bits
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )

    return {
        "family": genome.family,
        "param": genome.param,
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "escape_bits": escape_bits,
        "escape_count": escaped_count,
        "block_count": block_count,
        "total_bits": total_bits,
        "fitness": raw_bits - total_bits,
        "ratio_vs_raw": 0.0 if raw_bits == 0 and total_bits == 0 else (total_bits / raw_bits if raw_bits else float("inf")),
    }


def _random_genome(rng: Random, max_value: int) -> AnchorGenome:
    """Vygeneruje nahodny genom v malom priestore kandidatov."""

    family = rng.choice(_SUPPORTED_FAMILIES)
    if family == "multiple":
        return _canonicalize_genome(AnchorGenome(family, rng.randint(1, max(1, min(max_value, 4096)))), max_value)
    if family == "power":
        return _canonicalize_genome(AnchorGenome(family, rng.randint(2, max(2, min(max_value, 16)))), max_value)
    return _canonicalize_genome(AnchorGenome(family, 0), max_value)


def _genome_space_size(max_value: int) -> int:
    """Vrati horny odhad poctu rozlisitelnych genomov v malom priestore."""

    multiple_count = max(1, min(max_value, 4096))
    power_count = max(1, min(max_value, 16) - 1)
    return 2 + multiple_count + power_count


def _mutate_genome(genome: AnchorGenome, rng: Random, max_value: int) -> AnchorGenome:
    """Aplikuje malu deterministicku mutaciu parametra alebo rodiny."""

    if rng.random() < 0.25:
        return _random_genome(rng, max_value)

    if genome.family == "multiple":
        delta = rng.choice((-64, -16, -4, -1, 1, 4, 16, 64))
        return _canonicalize_genome(AnchorGenome("multiple", genome.param + delta), max_value)
    if genome.family == "power":
        delta = rng.choice((-2, -1, 1, 2))
        return _canonicalize_genome(AnchorGenome("power", genome.param + delta), max_value)
    if genome.family == "prime_lower":
        return _canonicalize_genome(AnchorGenome(rng.choice(("prime_lower", "square")), 0), max_value)
    return _canonicalize_genome(AnchorGenome(rng.choice(("square", "prime_lower")), 0), max_value)


def _crossover_genomes(left: AnchorGenome, right: AnchorGenome, rng: Random, max_value: int) -> AnchorGenome:
    """Zlozi dieta z dvoch rodicov bez narusenia deterministickosti."""

    family = rng.choice((left.family, right.family))
    if family == "multiple":
        params = [genome.param for genome in (left, right) if genome.family == "multiple"]
        if params:
            param = sum(params) // len(params)
        else:
            param = rng.randint(1, max(1, min(max_value, 4096)))
        return _canonicalize_genome(AnchorGenome("multiple", param), max_value)
    if family == "power":
        params = [genome.param for genome in (left, right) if genome.family == "power"]
        if params:
            param = max(2, sum(params) // len(params))
        else:
            param = rng.randint(2, max(2, min(max_value, 16)))
        return _canonicalize_genome(AnchorGenome("power", param), max_value)
    return _canonicalize_genome(AnchorGenome(family, 0), max_value)


def search_best_genome(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    *,
    generations: int = 12,
    population_size: int = 24,
    seed: int = 1234,
) -> dict:
    """Spusti male evolucne hladanie nad anchor rodinami a vrati najlepsi genom."""

    max_value = max(blocks) if blocks else 16
    effective_population_size = min(population_size, _genome_space_size(max_value))
    rng = Random(seed)

    population = {
        _canonicalize_genome(AnchorGenome("prime_lower", 0), max_value),
        _canonicalize_genome(AnchorGenome("square", 0), max_value),
        _canonicalize_genome(AnchorGenome("multiple", 1), max_value),
        _canonicalize_genome(AnchorGenome("multiple", 2), max_value),
        _canonicalize_genome(AnchorGenome("multiple", 4), max_value),
        _canonicalize_genome(AnchorGenome("power", 2), max_value),
    }

    while len(population) < effective_population_size:
        population.add(_random_genome(rng, max_value))

    history: list[dict] = []
    best_costs: dict | None = None
    best_genome: AnchorGenome | None = None

    for generation in range(generations):
        scored = []
        for genome in sorted(population):
            costs = estimate_genome_cost(blocks, width_bits, original_size, genome)
            scored.append((costs["total_bits"], -costs["fitness"], genome, costs))

        scored.sort(key=lambda item: (item[0], item[1], item[2]))
        current_best = scored[0]
        best_genome = current_best[2]
        best_costs = current_best[3]
        history.append(
            {
                "generation": generation,
                "family": best_genome.family,
                "param": best_genome.param,
                "fitness": best_costs["fitness"],
                "total_bits": best_costs["total_bits"],
            }
        )

        elite_count = max(2, effective_population_size // 4)
        elites = [entry[2] for entry in scored[:elite_count]]
        next_population = set(elites)

        while len(next_population) < effective_population_size:
            left = rng.choice(elites)
            right = rng.choice(elites)
            child = _crossover_genomes(left, right, rng, max_value)
            child = _mutate_genome(child, rng, max_value)
            next_population.add(child)

        population = next_population

    if best_genome is None or best_costs is None:
        raise RuntimeError("Evolution search did not produce a best genome")

    return {
        "best_genome": {"family": best_genome.family, "param": best_genome.param},
        "best_costs": best_costs,
        "history": history,
        "seed": seed,
        "generations": generations,
        "population_size": effective_population_size,
    }


def search_best_genome_for_bytes(
    data: bytes,
    width_bits: int = 16,
    *,
    generations: int = 12,
    population_size: int = 24,
    seed: int = 1234,
) -> dict:
    """Pomocna obalka pre evolucne hladanie priamo nad bytmi."""

    payload = bytes(data)
    blocks = bytes_to_uint_blocks(payload, width_bits)
    return search_best_genome(
        blocks,
        width_bits,
        len(payload),
        generations=generations,
        population_size=population_size,
        seed=seed,
    )
```

## File: `src/primesymbolicmdl/experiments.py`

```python
"""Deterministicke experimenty pre prime-anchor maticu."""

from __future__ import annotations

import math
import random

from .bitcost import estimate_prime_anchor_cost
from .blocks import bytes_to_uint_blocks


def dataset_empty() -> bytes:
    """Vrati prazdnu testovaciu vzorku."""

    return b""


def dataset_ascii_small() -> bytes:
    """Vrati malu ASCII vzorku s citatelnym obsahom."""

    return b"PrimeSymbolicMDL experimental harness"


def dataset_zeros(size: int = 1024) -> bytes:
    """Vrati nulovy dataset pevnej dlzky."""

    if size < 0:
        raise ValueError("size must be non-negative")
    return b"\x00" * size


def dataset_ramp_u16(count: int = 512) -> bytes:
    """Vrati rastucu rampu 16-bitovych hodnot v big-endian tvare."""

    if count < 0:
        raise ValueError("count must be non-negative")
    return b"".join((value % (1 << 16)).to_bytes(2, "big") for value in range(count))


def dataset_random(size: int = 1024, seed: int = 1234) -> bytes:
    """Vrati deterministicke pseudo-nahodne byty."""

    if size < 0:
        raise ValueError("size must be non-negative")
    rng = random.Random(seed)
    return bytes(rng.randrange(256) for _ in range(size))


def default_datasets() -> dict[str, bytes]:
    """Vrati malu deterministicku sadu datasetov pre rychle lokalne porovnanie."""

    return {
        "empty": dataset_empty(),
        "zeros_256": dataset_zeros(256),
        "ramp_u16_64": dataset_ramp_u16(64),
    }


def run_prime_anchor_matrix(
    datasets: dict[str, bytes],
    widths: tuple[int, ...],
    modes: tuple[str, ...],
) -> list[dict]:
    """Spusti deterministicku maticu sirka x mod nad zadanou sadou datasetov."""

    rows: list[dict] = []

    for dataset_name, data in datasets.items():
        for width_bits in widths:
            blocks = bytes_to_uint_blocks(data, width_bits)
            for mode in modes:
                costs = estimate_prime_anchor_cost(blocks, width_bits, len(data), mode)
                rows.append(
                    {
                        "dataset": dataset_name,
                        "size_bytes": len(data),
                        "width_bits": width_bits,
                        "mode": mode,
                        "raw_bits": costs["raw_bits"],
                        "total_bits": costs["total_bits"],
                        "ratio_vs_raw": costs["ratio_vs_raw"],
                        "escape_count": costs["escape_count"],
                        "block_count": costs["block_count"],
                    }
                )

    return rows


def _format_cell(column: str, value) -> str:
    """Zjednoti formatovanie buniek pre terminalovy markdown."""

    if column == "ratio_vs_raw" and isinstance(value, (int, float)):
        if math.isinf(value):
            return "inf"
        return f"{float(value):.3f}"
    return str(value)


def format_markdown_table(rows: list[dict]) -> str:
    """Vrati maticu ako jednoduchu markdown tabulku."""

    columns = [
        "dataset",
        "size_bytes",
        "width_bits",
        "mode",
        "raw_bits",
        "total_bits",
        "ratio_vs_raw",
        "escape_count",
        "block_count",
    ]
    headers = {
        "dataset": "dataset",
        "size_bytes": "size_bytes",
        "width_bits": "width_bits",
        "mode": "mode",
        "raw_bits": "raw_bits",
        "total_bits": "total_bits",
        "ratio_vs_raw": "ratio_vs_raw",
        "escape_count": "escape_count",
        "block_count": "block_count",
    }

    rendered_rows = []
    for row in rows:
        rendered_rows.append([_format_cell(column, row.get(column, "")) for column in columns])

    widths = []
    for index, column in enumerate(columns):
        cell_width = len(headers[column])
        for rendered_row in rendered_rows:
            cell_width = max(cell_width, len(rendered_row[index]))
        widths.append(cell_width)

    header_line = "| " + " | ".join(headers[column].ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    separator_line = "| " + " | ".join("-" * widths[index] for index, _ in enumerate(columns)) + " |"
    body_lines = [
        "| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(columns))) + " |"
        for row in rendered_rows
    ]

    return "\n".join([header_line, separator_line, *body_lines])


def main() -> None:
    """Vypise predvolenu markdown tabulku experimentov."""

    rows = run_prime_anchor_matrix(
        datasets=default_datasets(),
        widths=(8, 16, 24, 32),
        modes=("lower", "upper", "nearest"),
    )
    print(format_markdown_table(rows))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/gui.py`

```python
"""Jednoduchy Tkinter cockpit pre male vyskumne simulacie."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .image_datasets import GrayImage, get_image_dataset_names, make_gray_image, make_image_dataset
from .optimizers.image_gplite import available_image_gplite_primitive_sets
from .optimizers.registry import get_optimizer_names
from .simulation import format_simulation_report, run_gray_image_simulation


def tkinter_available() -> bool:
    """Vrati pravdu iba ak je Tkinter importovatelny."""

    try:
        import tkinter  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def parse_optional_int(text: str) -> int | None:
    """Prevedie prazdny string na None a inak vrati int."""

    stripped = text.strip()
    if not stripped:
        return None
    return int(stripped)


def parse_positive_int(text: str) -> int:
    """Vrati kladne cele cislo alebo vyhodi chybu."""

    value = int(text.strip())
    if value <= 0:
        raise ValueError("value must be positive")
    return value


def ensure_tkinter():
    """Importuje Tkinter az pri manualnom spusteni GUI."""

    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ModuleNotFoundError as exc:
        raise RuntimeError("Tkinter is unavailable; install the system package 'tk'.") from exc
    return tk, ttk, messagebox, filedialog


@dataclass
class _CanvasPanel:
    """Spoji canvas s titulkom nad nim."""

    title_var: object
    canvas: object


@dataclass
class _GuiState:
    """Pomocny kontajner pre parsed vstupy z formulára."""

    optimizer_name: str
    dataset_name: str
    image_width: int
    image_height: int
    seed: int
    population_size: int
    generations: int
    image_gplite_primitive_set: str
    max_index: int | None
    strict_lower: bool


class ResearchCockpit:
    """Jednoduche synchronne GUI pre prve porovnania optimizerov."""

    def __init__(self) -> None:
        tk, ttk, messagebox, filedialog = ensure_tkinter()
        self._tk = tk
        self._ttk = ttk
        self._messagebox = messagebox
        self._filedialog = filedialog
        self.root = tk.Tk()
        self.root.title("PrimeSymbolicMDL Research Cockpit")
        self.root.geometry("1480x980")

        optimizer_names = get_optimizer_names()
        dataset_names = get_image_dataset_names()
        self.optimizer_var = tk.StringVar(value=optimizer_names[0])
        self.dataset_var = tk.StringVar(value=dataset_names[0])
        self.preview_mode_var = tk.StringVar(value="Residuals")
        self.source_var = tk.StringVar(value="dataset")
        self.loaded_path_var = tk.StringVar(value="No file loaded")
        self.status_var = tk.StringVar(
            value="Choose a generated dataset or load a small PNG/GIF/PGM/PPM image."
        )
        self.width_var = tk.StringVar(value="32")
        self.height_var = tk.StringVar(value="32")
        self.seed_var = tk.StringVar(value="1234")
        self.population_var = tk.StringVar(value="24")
        self.generations_var = tk.StringVar(value="12")
        self.image_gplite_primitive_set_var = tk.StringVar(value="full")
        self.max_index_var = tk.StringVar(value="31")
        self.strict_lower_var = tk.BooleanVar(value=False)

        self.loaded_image: GrayImage | None = None
        self.active_image: GrayImage | None = None
        self._results_by_name: dict[str, dict] = {}

        self.original_panel: _CanvasPanel | None = None
        self.coded_panel: _CanvasPanel | None = None
        self.decoded_panel: _CanvasPanel | None = None
        self.history_canvas = None
        self.results_tree = None
        self.output = None

        self._build_layout()
        self._clear_results()
        self._refresh_preview(clear_results=False)

    def run(self) -> None:
        """Spusti Tkinter event loop."""

        self.root.mainloop()

    def _build_layout(self) -> None:
        """Postavi formular, preview panely, tabulku a report."""

        frame = self._ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)

        controls = self._ttk.LabelFrame(frame, text="Input and search", padding=12)
        controls.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        controls.columnconfigure(1, weight=1)

        self._ttk.Label(controls, text="Source").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        source_row = self._ttk.Frame(controls)
        source_row.grid(row=0, column=1, sticky="ew", pady=4)
        self._ttk.Radiobutton(
            source_row,
            text="Generated",
            variable=self.source_var,
            value="dataset",
            command=self._refresh_preview,
        ).grid(row=0, column=0, sticky="w")
        self._ttk.Radiobutton(
            source_row,
            text="Loaded file",
            variable=self.source_var,
            value="file",
            command=self._refresh_preview,
        ).grid(row=0, column=1, sticky="w", padx=(8, 0))

        row_index = 1
        dataset_box = self._ttk.Combobox(controls, textvariable=self.dataset_var, values=get_image_dataset_names(), state="readonly")
        preview_box = self._ttk.Combobox(controls, textvariable=self.preview_mode_var, values=("Residuals", "Anchors"), state="readonly")
        primitive_box = self._ttk.Combobox(
            controls,
            textvariable=self.image_gplite_primitive_set_var,
            values=available_image_gplite_primitive_sets(),
            state="readonly",
        )
        controls_spec = [
            ("Optimizer", self._ttk.Combobox(controls, textvariable=self.optimizer_var, values=get_optimizer_names(), state="readonly")),
            ("Dataset", dataset_box),
            ("View", preview_box),
            ("Width", self._ttk.Entry(controls, textvariable=self.width_var)),
            ("Height", self._ttk.Entry(controls, textvariable=self.height_var)),
            ("Seed", self._ttk.Entry(controls, textvariable=self.seed_var)),
            ("Population", self._ttk.Entry(controls, textvariable=self.population_var)),
            ("Generations", self._ttk.Entry(controls, textvariable=self.generations_var)),
            ("Image-GP set", primitive_box),
            ("Max index", self._ttk.Entry(controls, textvariable=self.max_index_var)),
        ]

        for label, widget in controls_spec:
            self._ttk.Label(controls, text=label).grid(row=row_index, column=0, sticky="w", padx=(0, 8), pady=4)
            widget.grid(row=row_index, column=1, sticky="ew", pady=4)
            row_index += 1

        strict_box = self._ttk.Checkbutton(controls, text="Strict lower anchor", variable=self.strict_lower_var)
        strict_box.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(8, 4))
        row_index += 1

        file_row = self._ttk.Frame(controls)
        file_row.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=(8, 4))
        file_row.columnconfigure(1, weight=1)
        self._ttk.Button(file_row, text="Load image", command=self._load_image).grid(row=0, column=0, sticky="w")
        self._ttk.Label(file_row, textvariable=self.loaded_path_var, wraplength=260).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(8, 0),
        )
        row_index += 1

        button_row = self._ttk.Frame(controls)
        button_row.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=(8, 4))
        button_row.columnconfigure(1, weight=1)
        self._ttk.Button(button_row, text="Run selected", command=self._run_selected_optimizer).grid(row=0, column=0, sticky="w")
        self._ttk.Button(button_row, text="Run all", command=self._run_all_optimizers).grid(row=0, column=1, sticky="w", padx=(8, 0))
        self._ttk.Button(button_row, text="Refresh input", command=self._refresh_preview).grid(row=0, column=2, sticky="e")
        row_index += 1

        self._ttk.Label(controls, textvariable=self.status_var, wraplength=320).grid(
            row=row_index,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(12, 0),
        )

        preview_frame = self._ttk.LabelFrame(frame, text="Image views", padding=12)
        preview_frame.grid(row=0, column=1, sticky="nsew")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(2, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        self.original_panel = self._build_panel(preview_frame, 0, "Input image")
        self.coded_panel = self._build_panel(preview_frame, 1, "Residuals / anchors")
        self.decoded_panel = self._build_panel(preview_frame, 2, "Decoded image")

        history_title = self._ttk.Label(preview_frame, text="Search history (total_bits vs raw_bits)")
        history_title.grid(row=2, column=0, columnspan=3, sticky="w", pady=(12, 4))
        self.history_canvas = self._tk.Canvas(preview_frame, width=960, height=210, bg="white", highlightthickness=1)
        self.history_canvas.grid(row=3, column=0, columnspan=3, sticky="ew")

        lower_frame = self._ttk.Frame(frame)
        lower_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        lower_frame.columnconfigure(0, weight=1)
        lower_frame.columnconfigure(1, weight=1)
        lower_frame.rowconfigure(0, weight=1)

        result_frame = self._ttk.LabelFrame(lower_frame, text="Optimizer comparison", padding=12)
        result_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        columns = ("optimizer", "status", "raw_bytes", "total_bytes", "saving_bytes", "ratio")
        self.results_tree = self._ttk.Treeview(result_frame, columns=columns, show="headings", height=8)
        headings = {
            "optimizer": "Optimizer",
            "status": "Status",
            "raw_bytes": "Raw B",
            "total_bytes": "Est B",
            "saving_bytes": "Saved B",
            "ratio": "Ratio",
        }
        widths = {
            "optimizer": 120,
            "status": 120,
            "raw_bytes": 80,
            "total_bytes": 80,
            "saving_bytes": 90,
            "ratio": 80,
        }
        for key in columns:
            self.results_tree.heading(key, text=headings[key])
            self.results_tree.column(key, width=widths[key], anchor="center", stretch=(key == "optimizer"))
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        self.results_tree.bind("<<TreeviewSelect>>", self._on_result_selected)

        tree_scroll = self._ttk.Scrollbar(result_frame, orient="vertical", command=self.results_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.results_tree.configure(yscrollcommand=tree_scroll.set)

        report_frame = self._ttk.LabelFrame(lower_frame, text="Detailed report", padding=12)
        report_frame.grid(row=0, column=1, sticky="nsew")
        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)
        self.output = self._tk.Text(report_frame, width=72, height=18, wrap="word")
        self.output.grid(row=0, column=0, sticky="nsew")

        text_scroll = self._ttk.Scrollbar(report_frame, orient="vertical", command=self.output.yview)
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=text_scroll.set)
        dataset_box.bind("<<ComboboxSelected>>", self._refresh_preview)
        preview_box.bind("<<ComboboxSelected>>", self._refresh_selected_view)

    def _build_panel(self, parent, column: int, title: str) -> _CanvasPanel:
        """Vytvori jeden obrazkovy panel s titulkom a canvasom."""

        title_var = self._tk.StringVar(value=title)
        self._ttk.Label(parent, textvariable=title_var).grid(row=0, column=column, sticky="w", pady=(0, 4))
        canvas = self._tk.Canvas(parent, width=280, height=280, bg="white", highlightthickness=1)
        canvas.grid(row=1, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 0))
        return _CanvasPanel(title_var=title_var, canvas=canvas)

    def _parse_state(self) -> _GuiState:
        """Nacita a validuje hodnoty z formulára."""

        return _GuiState(
            optimizer_name=self.optimizer_var.get(),
            dataset_name=self.dataset_var.get(),
            image_width=parse_positive_int(self.width_var.get()),
            image_height=parse_positive_int(self.height_var.get()),
            seed=int(self.seed_var.get().strip()),
            population_size=parse_positive_int(self.population_var.get()),
            generations=parse_positive_int(self.generations_var.get()),
            image_gplite_primitive_set=self.image_gplite_primitive_set_var.get(),
            max_index=parse_optional_int(self.max_index_var.get()),
            strict_lower=bool(self.strict_lower_var.get()),
        )

    def _load_image(self) -> None:
        """Nacita lokalny obrazok podporeny Tk PhotoImage a prevedie ho na grayscale."""

        path = self._filedialog.askopenfilename(
            title="Load image",
            filetypes=[
                ("Tk image files", "*.png *.gif *.pgm *.ppm"),
                ("PNG", "*.png"),
                ("GIF", "*.gif"),
                ("PGM", "*.pgm"),
                ("PPM", "*.ppm"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        try:
            image = self._load_tk_image(path)
        except Exception as exc:
            self._messagebox.showerror("Image load error", str(exc))
            return

        self.loaded_image = image
        self.source_var.set("file")
        self.loaded_path_var.set(str(Path(path).name))
        self.width_var.set(str(image.width))
        self.height_var.set(str(image.height))
        self.status_var.set(
            f"Loaded {Path(path).name} as {image.width}x{image.height} grayscale. "
            "Large images may be slow in this research UI."
        )
        self._refresh_preview()

    def _load_tk_image(self, path: str) -> GrayImage:
        """Nacita obrazok cez Tk a vrati grayscale pixely bez externych kniznic."""

        photo = self._tk.PhotoImage(file=path)
        width = int(photo.width())
        height = int(photo.height())
        pixels = bytearray()
        for y in range(height):
            for x in range(width):
                pixels.append(self._pixel_to_gray(photo.get(x, y)))
        return make_gray_image(Path(path).name, width, height, bytes(pixels))

    def _pixel_to_gray(self, value) -> int:
        """Prevedie Tk pixel na 8-bit grayscale."""

        if isinstance(value, tuple):
            if len(value) >= 3:
                red, green, blue = (int(channel) for channel in value[:3])
                return (299 * red + 587 * green + 114 * blue) // 1000
            if len(value) == 1:
                return int(value[0])

        if isinstance(value, str):
            if value.startswith("#") and len(value) == 7:
                red = int(value[1:3], 16)
                green = int(value[3:5], 16)
                blue = int(value[5:7], 16)
                return (299 * red + 587 * green + 114 * blue) // 1000
            red16, green16, blue16 = self.root.winfo_rgb(value)
            red = red16 // 257
            green = green16 // 257
            blue = blue16 // 257
            return (299 * red + 587 * green + 114 * blue) // 1000

        raise ValueError(f"Unsupported pixel format from Tk image loader: {value!r}")

    def _run_selected_optimizer(self) -> None:
        """Spusti iba aktualne vybrany optimizer."""

        self._run_optimizers([self.optimizer_var.get()])

    def _run_all_optimizers(self) -> None:
        """Spusti vsetky registrovane optimizery nad tym istym vstupom."""

        self._run_optimizers(get_optimizer_names())

    def _run_optimizers(self, optimizer_names: list[str]) -> None:
        """Spusti sadu optimizerov a naplni tabulku vysledkov."""

        try:
            state = self._parse_state()
            image = self._resolve_image(state)
        except Exception as exc:
            self._messagebox.showerror("Simulation error", str(exc))
            return

        self.active_image = image
        self.status_var.set(f"Running {len(optimizer_names)} optimizer(s) on {image.name} ({image.width}x{image.height})...")
        self.root.update_idletasks()

        results = []
        for optimizer_name in optimizer_names:
            try:
                result = run_gray_image_simulation(
                    optimizer_name,
                    image,
                    seed=state.seed,
                    population_size=state.population_size,
                    generations=state.generations,
                    image_gplite_primitive_set=state.image_gplite_primitive_set,
                    max_index=state.max_index,
                    strict_lower=state.strict_lower,
                )
            except Exception as exc:
                result = self._error_result(optimizer_name, image, str(exc))
            results.append(result)

        self._store_results(results)
        best = min(results, key=lambda item: (item["total_bits"], item["optimizer_name"]))
        self._select_result(best["optimizer_name"])
        self.status_var.set(
            f"Finished {len(results)} optimizer(s). "
            f"Best total_bits={best['total_bits']} with {best['optimizer_name']}."
        )

    def _error_result(self, optimizer_name: str, image: GrayImage, message: str) -> dict:
        """Vrati stabilny error vysledok, aby GUI ostalo citatelne."""

        raw_bits = len(image.pixels) * 8
        raw_bytes = len(image.pixels)
        return {
            "optimizer_name": optimizer_name,
            "status": "error",
            "dataset_name": image.name,
            "image_width": image.width,
            "image_height": image.height,
            "raw_bits": raw_bits,
            "total_bits": raw_bits,
            "saving_bits": 0,
            "ratio_vs_raw": 1.0,
            "raw_bytes": raw_bytes,
            "total_bytes_estimate": raw_bytes,
            "saving_bytes_estimate": 0,
            "best_model": "error",
            "history": [],
            "details": {"message": message},
        }

    def _resolve_image(self, state: _GuiState) -> GrayImage:
        """Vrati aktivny vstupny obrazok podla zvoleneho zdroja."""

        if self.source_var.get() == "file":
            if self.loaded_image is None:
                raise ValueError("No file image is loaded.")
            return self.loaded_image
        return make_image_dataset(state.dataset_name, state.image_width, state.image_height, state.seed)

    def _refresh_preview(self, _event=None, clear_results: bool = True) -> None:
        """Prekresli vstupny obrazok a pripadne zneplatni stare vysledky."""

        try:
            state = self._parse_state()
            image = self._resolve_image(state)
        except Exception:
            return

        self.active_image = image
        if self.original_panel is not None:
            self.original_panel.title_var.set(f"Input image: {image.name} ({image.width}x{image.height})")
            self._draw_image(self.original_panel.canvas, image)
        if clear_results:
            self._clear_results()

    def _refresh_selected_view(self, _event=None) -> None:
        """Prekresli coded panel pre aktualne vybrany vysledok bez resetu."""

        if self.results_tree is None:
            return
        selection = self.results_tree.selection()
        if not selection:
            return
        optimizer_name = selection[0]
        result = self._results_by_name.get(optimizer_name)
        if result is not None:
            self._draw_result_images(result)

    def _store_results(self, results: list[dict]) -> None:
        """Nahradi tabulku vysledkov novym behom."""

        self._results_by_name = {result["optimizer_name"]: result for result in results}
        self._clear_tree()
        for result in results:
            self.results_tree.insert(
                "",
                "end",
                iid=result["optimizer_name"],
                values=(
                    result["optimizer_name"],
                    result["status"],
                    result["raw_bytes"],
                    result["total_bytes_estimate"],
                    result["saving_bytes_estimate"],
                    f"{result['ratio_vs_raw']:.3f}",
                ),
            )

    def _clear_results(self) -> None:
        """Vymaze stare vysledky a necha iba vstupny preview."""

        self._results_by_name = {}
        self._clear_tree()
        if self.output is not None:
            self.output.delete("1.0", self._tk.END)
        self._draw_history(None)
        if self.coded_panel is not None:
            self.coded_panel.title_var.set("Residuals / anchors")
            self._draw_placeholder(self.coded_panel.canvas, "Run an optimizer to inspect the coded view.")
        if self.decoded_panel is not None:
            self.decoded_panel.title_var.set("Decoded image")
            self._draw_placeholder(self.decoded_panel.canvas, "Run an optimizer to inspect exact reconstruction.")

    def _clear_tree(self) -> None:
        """Vymaze vsetky riadky v tabulke vysledkov."""

        if self.results_tree is None:
            return
        for item_id in self.results_tree.get_children():
            self.results_tree.delete(item_id)

    def _select_result(self, optimizer_name: str) -> None:
        """Programovo vyberie riadok a zobrazi detail vysledku."""

        if self.results_tree is None or optimizer_name not in self._results_by_name:
            return
        self.results_tree.selection_set(optimizer_name)
        self.results_tree.focus(optimizer_name)
        self._show_result(self._results_by_name[optimizer_name])

    def _on_result_selected(self, _event=None) -> None:
        """Zareaguje na manualny vyber riadku v tabulke."""

        if self.results_tree is None:
            return
        selection = self.results_tree.selection()
        if not selection:
            return
        optimizer_name = selection[0]
        result = self._results_by_name.get(optimizer_name)
        if result is not None:
            self._show_result(result)

    def _show_result(self, result: dict) -> None:
        """Zobrazi detail vybraneho optimizera."""

        if self.output is not None:
            self.output.delete("1.0", self._tk.END)
            self.output.insert(self._tk.END, format_simulation_report(result))
        self._draw_history(result)
        self._draw_result_images(result)

    def _draw_result_images(self, result: dict) -> None:
        """Prekresli coded a decoded pohlad pre vybrany vysledok."""

        preview = result.get("preview")
        if self.active_image is not None and self.original_panel is not None:
            self._draw_image(self.original_panel.canvas, self.active_image)

        if not isinstance(preview, dict):
            self._draw_fallback_result_images(result)
            return

        coded_key = "residual_image" if self.preview_mode_var.get() == "Residuals" else "anchor_image"
        coded_title = str(preview.get("residual_label", "Residuals"))
        if coded_key == "anchor_image":
            coded_title = str(preview.get("anchor_label", "Anchors"))

        coded_image = preview[coded_key]
        decoded_image = preview["decoded_image"]
        residual_codec = result.get("details", {}).get("residual_codec")

        if self.coded_panel is not None:
            codec_suffix = f" codec={residual_codec}" if residual_codec else ""
            self.coded_panel.title_var.set(
                f"{coded_title}{codec_suffix}: min_residual={preview['min_residual']} max_residual={preview['max_residual']} escapes={preview['escaped_count']}"
            )
            self._draw_image(self.coded_panel.canvas, coded_image)
        if self.decoded_panel is not None:
            self.decoded_panel.title_var.set(
                f"Decoded: exact_roundtrip={preview['roundtrip_ok']}"
            )
            self._draw_image(self.decoded_panel.canvas, decoded_image)

    def _draw_fallback_result_images(self, result: dict) -> None:
        """Zobrazi placeholder alebo raw fallback, ked preview nie je dostupny."""

        if self.active_image is None:
            return

        if self.coded_panel is not None:
            self.coded_panel.title_var.set("Coded view unavailable")
            self._draw_placeholder(
                self.coded_panel.canvas,
                "This optimizer does not expose a law-based coded image preview.",
            )

        if self.decoded_panel is None:
            return

        if result["best_model"] == "raw_fallback":
            self.decoded_panel.title_var.set("Decoded image: raw fallback")
            self._draw_image(self.decoded_panel.canvas, self.active_image)
            return

        self.decoded_panel.title_var.set("Decoded image unavailable")
        self._draw_placeholder(
            self.decoded_panel.canvas,
            "No exact decoded preview is available for this result.",
        )

    def _draw_history(self, result: dict | None) -> None:
        """Nakresli priebeh total_bits pre vybrany search."""

        if self.history_canvas is None:
            return

        canvas = self.history_canvas
        canvas.delete("all")
        width = int(canvas.cget("width"))
        height = int(canvas.cget("height"))

        left = 48
        right = width - 16
        top = 16
        bottom = height - 28
        canvas.create_rectangle(left, top, right, bottom, outline="#999999")

        if result is None:
            self._draw_placeholder(canvas, "Run an optimizer to see total_bits history.")
            return

        history = result.get("history", [])
        raw_bits = int(result["raw_bits"])
        canvas.create_line(left, top, right, top, fill="#ffffff")

        if not history:
            self._draw_placeholder(canvas, "No search history is available for this optimizer.")
            return

        totals = [int(item.get("total_bits", raw_bits)) for item in history]
        generations = [int(item.get("generation", index)) for index, item in enumerate(history)]
        max_bits = max(max(totals), raw_bits)
        min_bits = min(min(totals), raw_bits)
        span = max(1, max_bits - min_bits)

        def project_x(index: int) -> float:
            if len(generations) == 1:
                return (left + right) / 2
            return left + ((right - left) * index / (len(generations) - 1))

        def project_y(bits: int) -> float:
            return bottom - ((bits - min_bits) * (bottom - top) / span)

        raw_y = project_y(raw_bits)
        canvas.create_line(left, raw_y, right, raw_y, fill="#cc3333", dash=(4, 4), width=2)
        canvas.create_text(left, raw_y - 10, anchor="w", text=f"raw_bits={raw_bits}", fill="#aa2222")

        points = []
        for index, total_bits in enumerate(totals):
            points.extend((project_x(index), project_y(total_bits)))
        if len(points) >= 4:
            canvas.create_line(*points, fill="#1f5d9b", width=3, smooth=False)

        for index, total_bits in enumerate(totals):
            x_coord = project_x(index)
            y_coord = project_y(total_bits)
            canvas.create_oval(x_coord - 3, y_coord - 3, x_coord + 3, y_coord + 3, fill="#1f5d9b", outline="#1f5d9b")
            canvas.create_text(x_coord, bottom + 12, text=str(generations[index]), fill="#333333")

        canvas.create_text(left, top - 8, anchor="w", text=f"best total_bits={min(totals)}", fill="#333333")
        canvas.create_text(right, top - 8, anchor="e", text=result["optimizer_name"], fill="#333333")
        canvas.create_text(left, bottom + 12, anchor="w", text="generation", fill="#333333")

    def _draw_placeholder(self, canvas, text: str) -> None:
        """Vymaze canvas a zobrazi textovy placeholder."""

        canvas.delete("all")
        width = int(canvas.cget("width"))
        height = int(canvas.cget("height"))
        canvas.create_text(width // 2, height // 2, width=max(120, width - 24), text=text, fill="#666666")

    def _draw_image(self, canvas, image: GrayImage) -> None:
        """Nakresli grayscale obrazok ako siet malych stvorcov."""

        max_canvas = 280
        scale = max(1, min(8, max_canvas // max(image.width, image.height)))
        canvas_width = image.width * scale
        canvas_height = image.height * scale
        canvas.config(width=canvas_width, height=canvas_height)
        canvas.delete("all")

        for y in range(image.height):
            for x in range(image.width):
                pixel = image.pixels[(y * image.width) + x]
                color = f"#{pixel:02x}{pixel:02x}{pixel:02x}"
                canvas.create_rectangle(
                    x * scale,
                    y * scale,
                    (x + 1) * scale,
                    (y + 1) * scale,
                    outline=color,
                    fill=color,
                )


def main() -> None:
    """Spusti GUI alebo zlyha s jasnou hlaskou pri chybajucom Tk."""

    try:
        ResearchCockpit().run()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/huge_anchor_binary_demo.py`

```python
"""CLI demo pre skutocne huge-anchor binarne payloady."""

from __future__ import annotations

from .huge_anchor_binary import compress_best_huge_anchor_binary
from .huge_anchor_datasets import make_huge_anchor_dataset


def run_demo() -> list[dict]:
    """Spusti malu deterministicku sadu benchmarkov nad binarnym kontajnerom."""

    datasets = (
        "linear_shift_generated",
        "square_generated",
        "multiple_generated",
        "random_bytes",
        "ascii_small",
        "repeating_pattern",
    )
    widths = (16, 32, 64)

    results: list[dict] = []
    for dataset_name in datasets:
        for width_bits in widths:
            data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
            result = compress_best_huge_anchor_binary(data, width_bits=width_bits, allow_raw_fallback=True)
            results.append(
                {
                    "dataset": dataset_name,
                    **result,
                }
            )
    return results


def format_huge_anchor_binary_result(result: dict) -> str:
    """Vrati stabilny textovy report jedneho binarneho benchmarku."""

    lines = [
        f"dataset: {result['dataset']}",
        f"width_bits: {result['width_bits']}",
        f"estimated_best_model: {result['estimated_best_model_string']} radius={result['estimated_best_search_radius']}",
        f"actual_best_model: {result['best_model_string']} radius={result['search_radius']}",
        f"actual_rerank_changed_winner: {result['actual_rerank_changed_winner']}",
        f"actual_rerank_top_n: {result['actual_rerank_top_n']}",
        f"raw_bytes: {result['raw_bytes']}",
        f"compressed_bytes: {result['compressed_bytes']}",
        f"raw_bits: {result['raw_bits']}",
        f"actual_bits: {result['actual_bits']}",
        f"actual_best_estimated_total_bits: {result['estimated_total_bits']}",
        f"estimated_best_total_bits: {result['estimated_best_total_bits']}",
        f"actual_saving_bytes: {result['actual_saving_bytes']}",
        f"actual_saving_bits: {result['actual_saving_bits']}",
        f"roundtrip_ok: {result['roundtrip_ok']}",
        f"decision: {result['decision']}",
        f"estimated_decision: {result['estimated_decision']}",
        f"residual_codec: {result['residual_codec']}",
        f"escape_count: {result['escape_count']}",
        "actual_top_3_candidates:",
    ]
    for index, candidate in enumerate(result["actual_rerank_candidates"][:3], start=1):
        if candidate["status"] == "ok":
            lines.append(
                f"{index}. {candidate['model']} radius={candidate['search_radius']} compressed_bytes={candidate['compressed_bytes']} "
                f"actual_bits={candidate['actual_bits']} estimated_total_bits={candidate['estimated_total_bits']} decision={candidate['decision']}"
            )
            continue
        lines.append(
            f"{index}. {candidate['model']} radius={candidate['search_radius']} status=error error={candidate.get('error', 'unknown')}"
        )
    return "\n".join(lines)


def main() -> None:
    """Vypise binarny huge-anchor report do stdout."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_huge_anchor_binary_result(result))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/huge_anchor_binary.py`

```python
"""Prvy skutocny binarny container pre huge-anchor payloady.

Format je deterministicky a repo-friendly:

- magic `PSMDLHA1`
- 1 bajt version
- unsigned varint `width_bits`
- unsigned varint `original_size`
- unsigned varint `block_count`
- model family id a family-specific parametre
- unsigned varint `search_radius`
- unsigned varint `flag_blob_length` + MSB-first flag bity
- unsigned varint `index_width`
- unsigned varint `index_count`
- unsigned varint `index_blob_length` + MSB-first packed indices
- unsigned varint `residual_count`
- unsigned varint `residual_blob_length` + residual binary blob
- unsigned varint `raw_escape_count`
- unsigned varint `raw_blob_length` + big-endian raw escape bloky
"""

from __future__ import annotations

from .bitstream import BitReader, BitWriter, decode_unsigned_varint, encode_unsigned_varint, zigzag_decode, zigzag_encode
from .huge_anchor_branch import encode_block_huge_anchor
from .huge_anchor_models import (
    HugeAnchorModel,
    SUPPORTED_HUGE_ANCHOR_FAMILIES,
    anchor_from_index,
    huge_anchor_model_from_dict,
    huge_anchor_model_bits,
    huge_anchor_parameter_bits,
)
from .huge_anchor_search import search_best_huge_anchor_model
from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks, huge_blocks_to_bytes
from .residual_binary import decode_residuals_binary, encode_residuals_binary
from .residual_codecs import choose_best_residual_codec, unsigned_width_for_max

_MAGIC = b"PSMDLHA1"
_VERSION = 1
_FAMILY_TO_ID = {family: index for index, family in enumerate(SUPPORTED_HUGE_ANCHOR_FAMILIES)}
_ID_TO_FAMILY = {value: key for key, value in _FAMILY_TO_ID.items()}


def encode_huge_anchor_binary(
    data: bytes,
    width_bits: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> bytes:
    """Zakoduje data do skutocneho huge-anchor binarneho blobu."""

    _validate_width_bits(width_bits)
    if not isinstance(search_radius, int) or search_radius < 0:
        raise ValueError("search_radius must be a non-negative integer")

    payload = bytes(data)
    blocks = bytes_to_huge_blocks(payload, width_bits)
    encoded_blocks = [encode_block_huge_anchor(block, width_bits, model, search_radius=search_radius) for block in blocks]

    flags = [bool(entry["escaped"]) for entry in encoded_blocks]
    indices = [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    raw_blocks = [int(block) for block, entry in zip(blocks, encoded_blocks) if entry["escaped"]]

    residual_codec = choose_best_residual_codec(residuals)
    residual_blob = encode_residuals_binary(residuals, codec_name=residual_codec.codec_name)
    flag_blob = _pack_flags(flags)
    index_width = unsigned_width_for_max(max(indices)) if indices else 0
    index_blob = _pack_fixed_width_values(indices, index_width, "indices")
    raw_blob = _encode_raw_blocks(raw_blocks, width_bits)

    output = bytearray()
    output.extend(_MAGIC)
    output.append(_VERSION)
    output.extend(encode_unsigned_varint(width_bits))
    output.extend(encode_unsigned_varint(len(payload)))
    output.extend(encode_unsigned_varint(len(blocks)))
    output.extend(_encode_model(model))
    output.extend(encode_unsigned_varint(search_radius))
    output.extend(encode_unsigned_varint(len(flag_blob)))
    output.extend(flag_blob)
    output.extend(encode_unsigned_varint(index_width))
    output.extend(encode_unsigned_varint(len(indices)))
    output.extend(encode_unsigned_varint(len(index_blob)))
    output.extend(index_blob)
    output.extend(encode_unsigned_varint(len(residuals)))
    output.extend(encode_unsigned_varint(len(residual_blob)))
    output.extend(residual_blob)
    output.extend(encode_unsigned_varint(len(raw_blocks)))
    output.extend(encode_unsigned_varint(len(raw_blob)))
    output.extend(raw_blob)
    return bytes(output)


def decode_huge_anchor_binary(blob: bytes) -> bytes:
    """Dekoduje huge-anchor binarny blob spat na povodne bajty."""

    payload = bytes(blob)
    if not payload.startswith(_MAGIC):
        raise ValueError("Unsupported huge-anchor binary magic")
    if len(payload) <= len(_MAGIC):
        raise ValueError("Huge-anchor binary payload is truncated")

    version = payload[len(_MAGIC)]
    if version != _VERSION:
        raise ValueError(f"Unsupported huge-anchor binary version: {version}")

    offset = len(_MAGIC) + 1
    width_bits, offset = decode_unsigned_varint(payload, offset)
    original_size, offset = decode_unsigned_varint(payload, offset)
    block_count, offset = decode_unsigned_varint(payload, offset)
    model, offset = _decode_model(payload, offset)
    search_radius, offset = decode_unsigned_varint(payload, offset)
    del search_radius

    flag_blob_length, offset = decode_unsigned_varint(payload, offset)
    flag_blob, offset = _take_bytes(payload, offset, flag_blob_length, "flag blob")
    flags = _unpack_flags(flag_blob, block_count)

    index_width, offset = decode_unsigned_varint(payload, offset)
    index_count, offset = decode_unsigned_varint(payload, offset)
    index_blob_length, offset = decode_unsigned_varint(payload, offset)
    index_blob, offset = _take_bytes(payload, offset, index_blob_length, "index blob")
    indices = _unpack_fixed_width_values(index_blob, index_count, index_width, "indices")

    residual_count, offset = decode_unsigned_varint(payload, offset)
    residual_blob_length, offset = decode_unsigned_varint(payload, offset)
    residual_blob, offset = _take_bytes(payload, offset, residual_blob_length, "residual blob")
    residuals = decode_residuals_binary(residual_blob, residual_count)

    raw_escape_count, offset = decode_unsigned_varint(payload, offset)
    raw_blob_length, offset = decode_unsigned_varint(payload, offset)
    raw_blob, offset = _take_bytes(payload, offset, raw_blob_length, "raw escape blob")
    raw_blocks = _decode_raw_blocks(raw_blob, raw_escape_count, width_bits)

    if offset != len(payload):
        raise ValueError("Huge-anchor binary payload has trailing bytes")

    escape_count = sum(1 for flag in flags if flag)
    non_escape_count = block_count - escape_count
    if escape_count != raw_escape_count:
        raise ValueError("raw escape count does not match flag stream")
    if non_escape_count != index_count:
        raise ValueError("index count does not match non-escape blocks")
    if non_escape_count != residual_count:
        raise ValueError("residual count does not match non-escape blocks")

    index_position = 0
    residual_position = 0
    raw_position = 0
    decoded_blocks: list[int] = []

    for escaped in flags:
        if escaped:
            decoded_blocks.append(raw_blocks[raw_position])
            raw_position += 1
            continue

        index = indices[index_position]
        residual = residuals[residual_position]
        index_position += 1
        residual_position += 1

        anchor = anchor_from_index(index, model, width_bits)
        if anchor is None:
            raise ValueError("Stored index cannot reconstruct a valid anchor")
        block_value = anchor + residual
        if block_value < 0 or block_value >= (1 << width_bits):
            raise ValueError("Decoded block falls outside the declared width")
        decoded_blocks.append(block_value)

    return huge_blocks_to_bytes(decoded_blocks, width_bits, original_size)


def compress_best_huge_anchor_binary(
    data: bytes,
    width_bits: int = 32,
    allow_raw_fallback: bool = True,
    actual_rerank_top_n: int = 16,
) -> dict:
    """Najde najmensi skutocny binarny blob medzi top estimated kandidatmi."""

    payload = bytes(data)
    search_result = search_best_huge_anchor_model(payload, width_bits=width_bits)
    actual_rerank_candidates = rerank_huge_anchor_candidates_by_actual_size(
        payload,
        width_bits,
        search_result,
        top_n=actual_rerank_top_n,
    )

    successful_candidates = [candidate for candidate in actual_rerank_candidates if candidate["status"] == "ok"]
    if not successful_candidates:
        raise RuntimeError("Actual-size reranking did not produce any decodable huge-anchor candidate")

    actual_winner = successful_candidates[0]
    best_model = huge_anchor_model_from_dict(actual_winner["model_dict"])
    search_radius = int(actual_winner["search_radius"])
    binary_blob = encode_huge_anchor_binary(payload, width_bits, best_model, search_radius=search_radius)
    roundtrip_ok = decode_huge_anchor_binary(binary_blob) == payload

    raw_bytes = len(payload)
    compressed_bytes = int(actual_winner["compressed_bytes"])
    raw_bits = raw_bytes * 8
    actual_bits = int(actual_winner["actual_bits"])
    decision = "compressed" if compressed_bytes < raw_bytes else "raw_fallback"
    if not allow_raw_fallback and decision == "raw_fallback":
        decision = "model_blob"

    estimated_best_key = (search_result["best_model_string"], int(search_result["search_radius"]))
    actual_best_key = (actual_winner["model"], search_radius)

    return {
        "best_model": best_model,
        "best_model_string": actual_winner["model"],
        "width_bits": width_bits,
        "search_radius": search_radius,
        "estimated_best_model": search_result["best_model"],
        "estimated_best_model_dict": dict(search_result["best_model_dict"]),
        "estimated_best_model_string": search_result["best_model_string"],
        "estimated_best_search_radius": search_result["search_radius"],
        "estimated_best_total_bits": search_result["total_bits"],
        "actual_rerank_top_n": actual_rerank_top_n,
        "actual_rerank_candidates": actual_rerank_candidates,
        "actual_rerank_changed_winner": actual_best_key != estimated_best_key,
        "raw_bytes": raw_bytes,
        "compressed_bytes": compressed_bytes,
        "raw_bits": raw_bits,
        "actual_bits": actual_bits,
        "estimated_total_bits": actual_winner["estimated_total_bits"],
        "estimated_saving_bits": actual_winner["estimated_saving_bits"],
        "actual_saving_bytes": actual_winner["actual_saving_bytes"],
        "actual_saving_bits": actual_winner["actual_saving_bits"],
        "roundtrip_ok": roundtrip_ok,
        "decision": decision,
        "estimated_decision": search_result["decision"],
        "residual_codec": actual_winner["residual_codec"],
        "escape_count": actual_winner["escape_count"],
        "binary_blob": binary_blob,
    }


def rerank_huge_anchor_candidates_by_actual_size(
    data: bytes,
    width_bits: int,
    search_result: dict,
    top_n: int = 16,
) -> list[dict]:
    """Zoradi top estimated kandidatov podla skutocnej serializovanej velkosti."""

    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer")

    payload = bytes(data)
    history = search_result.get("history")
    if not isinstance(history, list) or not history:
        raise ValueError("search_result must contain non-empty history")

    raw_bytes = len(payload)
    raw_bits = raw_bytes * 8
    selected_rows: list[dict] = []
    seen_identities: set[tuple[str, tuple[tuple[str, int], ...], int]] = set()

    for row in history:
        model_dict = row.get("model_dict")
        if not isinstance(model_dict, dict):
            raise ValueError("search history row is missing model_dict")
        search_radius = row.get("search_radius")
        if not isinstance(search_radius, int):
            raise ValueError("search history row has invalid search_radius")

        identity = _candidate_identity_key(model_dict, search_radius)
        if identity in seen_identities:
            continue
        seen_identities.add(identity)
        selected_rows.append(row)
        if len(selected_rows) >= top_n:
            break

    reranked: list[dict] = []
    for estimated_rank, row in enumerate(selected_rows, start=1):
        model_dict = dict(row["model_dict"])
        candidate = {
            "status": "error",
            "estimated_rank": estimated_rank,
            "model": row["model"],
            "model_dict": model_dict,
            "search_radius": int(row["search_radius"]),
            "estimated_total_bits": int(row["total_bits"]),
            "estimated_saving_bits": int(row["saving_bits"]),
            "residual_codec": row["residual_codec"],
            "escape_count": int(row["escape_count"]),
            "raw_bytes": raw_bytes,
            "raw_bits": raw_bits,
            "roundtrip_ok": False,
            "decision": "error",
        }
        try:
            model = huge_anchor_model_from_dict(model_dict)
            blob = encode_huge_anchor_binary(payload, width_bits, model, search_radius=candidate["search_radius"])
            roundtrip_ok = decode_huge_anchor_binary(blob) == payload
            if not roundtrip_ok:
                raise ValueError("Binary rerank roundtrip failed")

            compressed_bytes = len(blob)
            actual_bits = compressed_bytes * 8
            candidate.update(
                {
                    "status": "ok",
                    "compressed_bytes": compressed_bytes,
                    "actual_bits": actual_bits,
                    "actual_saving_bytes": raw_bytes - compressed_bytes,
                    "actual_saving_bits": raw_bits - actual_bits,
                    "roundtrip_ok": True,
                    "decision": "compressed" if compressed_bytes < raw_bytes else "raw_fallback",
                }
            )
        except Exception as error:  # pragma: no cover - defensive path exercised indirectly
            candidate["error"] = str(error)
        reranked.append(candidate)

    reranked.sort(
        key=lambda row: (
            0 if row["status"] == "ok" else 1,
            row.get("compressed_bytes", float("inf")),
            row["estimated_total_bits"],
            row["model"],
            row["search_radius"],
        )
    )
    return reranked


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze huge-block sirka patri medzi podporovane hodnoty."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")


def _encode_model(model: HugeAnchorModel) -> bytes:
    """Zakoduje family identifikator a jej parametre."""

    huge_anchor_model_bits(model)
    huge_anchor_parameter_bits(model)

    family = model.family
    params = dict(model.params)
    output = bytearray()
    try:
        family_id = _FAMILY_TO_ID[family]
    except KeyError as error:
        raise ValueError(f"Unsupported huge anchor family: {family}") from error

    output.extend(encode_unsigned_varint(family_id))
    if family == "linear_shift":
        output.extend(encode_unsigned_varint(int(params["shift"])))
    elif family == "affine_shift":
        output.extend(encode_unsigned_varint(int(params["shift"])))
        output.extend(encode_unsigned_varint(zigzag_encode(int(params["bias"]))))
    elif family == "multiple":
        output.extend(encode_unsigned_varint(int(params["step"])))
    elif family == "square":
        pass
    elif family == "scaled_prime":
        output.extend(encode_unsigned_varint(int(params["shift"])))
        output.extend(encode_unsigned_varint(int(params.get("search_radius", 0))))
    else:
        raise ValueError(f"Unsupported huge anchor family: {family}")
    return bytes(output)


def _decode_model(payload: bytes, offset: int) -> tuple[HugeAnchorModel, int]:
    """Dekoduje family identifikator a family-specific parametre."""

    family_id, offset = decode_unsigned_varint(payload, offset)
    family = _ID_TO_FAMILY.get(family_id)
    if family is None:
        raise ValueError(f"Unsupported huge anchor family id: {family_id}")

    if family == "linear_shift":
        shift, offset = decode_unsigned_varint(payload, offset)
        return HugeAnchorModel(family, {"shift": shift}), offset
    if family == "affine_shift":
        shift, offset = decode_unsigned_varint(payload, offset)
        bias_encoded, offset = decode_unsigned_varint(payload, offset)
        return HugeAnchorModel(family, {"shift": shift, "bias": zigzag_decode(bias_encoded)}), offset
    if family == "multiple":
        step, offset = decode_unsigned_varint(payload, offset)
        return HugeAnchorModel(family, {"step": step}), offset
    if family == "square":
        return HugeAnchorModel(family, {}), offset

    shift, offset = decode_unsigned_varint(payload, offset)
    model_search_radius, offset = decode_unsigned_varint(payload, offset)
    return HugeAnchorModel(family, {"shift": shift, "search_radius": model_search_radius}), offset


def _candidate_identity_key(model_dict: dict, search_radius: int) -> tuple[str, tuple[tuple[str, int], ...], int]:
    """Vrati hashovatelny identifikator modelu a search radiusu."""

    normalized = huge_anchor_model_from_dict(model_dict)
    return (
        normalized.family,
        tuple(sorted(normalized.params.items())),
        search_radius,
    )


def _pack_flags(flags: list[bool]) -> bytes:
    """Zabali escape flagy do MSB-first bitstreamu."""

    writer = BitWriter()
    for flag in flags:
        writer.write_bool(flag)
    return writer.to_bytes()


def _unpack_flags(blob: bytes, count: int) -> list[bool]:
    """Rozbali escape flagy z bitstreamu."""

    reader = BitReader(blob)
    flags = [reader.read_bool() for _ in range(count)]
    _validate_zero_padding(blob, count, "flag stream")
    return flags


def _pack_fixed_width_values(values: list[int], width: int, label: str) -> bytes:
    """Zabali zoznam nezapornych hodnot s fixnou bitovou sirkou."""

    if width == 0:
        if any(value != 0 for value in values):
            raise ValueError(f"{label} require non-zero width")
        return b""

    writer = BitWriter()
    for value in values:
        if value < 0:
            raise ValueError(f"{label} must be non-negative")
        writer.write_bits(value, width)
    return writer.to_bytes()


def _unpack_fixed_width_values(blob: bytes, count: int, width: int, label: str) -> list[int]:
    """Rozbali zoznam hodnot s fixnou bitovou sirkou."""

    if width == 0:
        if blob:
            raise ValueError(f"{label} with zero width must not contain bytes")
        return [0] * count

    reader = BitReader(blob)
    values = [reader.read_bits(width) for _ in range(count)]
    _validate_zero_padding(blob, count * width, label)
    return values


def _encode_raw_blocks(raw_blocks: list[int], width_bits: int) -> bytes:
    """Zakoduje raw escape bloky ako big-endian bajty."""

    width_bytes = width_bits // 8
    output = bytearray()
    for block in raw_blocks:
        if block < 0 or block >= (1 << width_bits):
            raise ValueError(f"Raw block out of range for {width_bits} bits: {block}")
        output.extend(int(block).to_bytes(width_bytes, "big"))
    return bytes(output)


def _decode_raw_blocks(blob: bytes, raw_escape_count: int, width_bits: int) -> list[int]:
    """Dekoduje raw escape bloky z big-endian bajtov."""

    width_bytes = width_bits // 8
    expected_length = raw_escape_count * width_bytes
    if len(blob) != expected_length:
        raise ValueError("raw escape blob length does not match raw_escape_count")

    blocks: list[int] = []
    for start in range(0, len(blob), width_bytes):
        blocks.append(int.from_bytes(blob[start : start + width_bytes], "big"))
    return blocks


def _take_bytes(payload: bytes, offset: int, length: int, label: str) -> tuple[bytes, int]:
    """Vrati rez `length` bajtov alebo vyhodi chybu pri orezani."""

    if offset + length > len(payload):
        raise ValueError(f"Truncated {label}")
    return payload[offset : offset + length], offset + length


def _validate_zero_padding(payload: bytes, used_bits: int, label: str) -> None:
    """Overi, ze padding za skutocnymi bitmi je nulovy."""

    total_bits = len(payload) * 8
    if used_bits > total_bits:
        raise ValueError(f"{label} is shorter than declared")
    if used_bits == total_bits:
        return

    full_bytes, used_tail_bits = divmod(used_bits, 8)
    if used_tail_bits:
        mask = (1 << (8 - used_tail_bits)) - 1
        if payload[full_bytes] & mask:
            raise ValueError(f"{label} contains non-zero padding bits")
        full_bytes += 1

    for byte_value in payload[full_bytes:]:
        if byte_value:
            raise ValueError(f"{label} contains non-zero trailing bytes")
```

## File: `src/primesymbolicmdl/huge_anchor_branch.py`

```python
"""Vseobecna huge-anchor vetva nad index-plus-diff reprezentaciou."""

from __future__ import annotations

import math
from math import isqrt

from .huge_anchor_models import (
    HugeAnchorModel,
    anchor_from_index,
    huge_anchor_model_bits,
    huge_anchor_parameter_bits,
    render_huge_anchor_model,
)
from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks, huge_blocks_to_bytes
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    unsigned_width_for_max,
)

_FIXED_HEADER_BITS = 32


def encode_block_huge_anchor(
    x: int,
    width_bits: int,
    model: HugeAnchorModel,
    max_index: int | None = None,
    search_radius: int = 0,
) -> dict:
    """Najde najlepsi index pre zvolenu anchor family alebo vrati escape."""

    _validate_width_bits(width_bits)
    _validate_block_value(x, width_bits)
    if max_index is not None and max_index < 0:
        raise ValueError("max_index must be non-negative")
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")

    estimated_index = _estimate_index(x, model)
    effective_radius = _effective_search_radius(model, search_radius)
    lower_index = max(0, estimated_index - effective_radius)
    upper_index = estimated_index + effective_radius
    if max_index is not None:
        upper_index = min(upper_index, max_index)

    best: tuple[int, int, int, int] | None = None

    for index in range(lower_index, upper_index + 1):
        anchor = anchor_from_index(index, model, width_bits)
        if anchor is None or anchor > x:
            continue

        diff = x - anchor
        local_cost = unsigned_width_for_max(index) + unsigned_width_for_max(diff)
        candidate = (diff, local_cost, index, anchor)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return {
            "index": None,
            "anchor": 0,
            "diff": x,
            "escaped": True,
            "estimated_index": estimated_index,
        }

    _, _, index, anchor = best
    return {
        "index": index,
        "anchor": anchor,
        "diff": x - anchor,
        "escaped": False,
        "estimated_index": estimated_index,
    }


def estimate_huge_anchor_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> dict:
    """Spocita plny MDL-style cost vseobecnej huge-anchor vetvy."""

    _validate_width_bits(width_bits)
    if original_size < 0:
        raise ValueError("original_size must be non-negative")
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")

    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")
    for block in blocks:
        _validate_block_value(int(block), width_bits)

    raw_bits = original_size * 8
    block_count = len(blocks)
    flag_bits = block_count
    encoded_blocks = [encode_block_huge_anchor(int(block), width_bits, model, search_radius=search_radius) for block in blocks]

    indices = [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    escape_count = sum(1 for entry in encoded_blocks if entry["escaped"])

    if indices:
        index_width = unsigned_width_for_max(max(indices))
        index_bits = index_width * len(indices)
    else:
        index_bits = 0

    residual_codec = choose_best_residual_codec(residuals)
    residual_bits = residual_codec.bits
    model_bits = huge_anchor_model_bits(model)
    parameter_bits = huge_anchor_parameter_bits(model)
    escape_bits = width_bits * escape_count
    total_bits = (
        model_bits
        + parameter_bits
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )
    saving_bits = raw_bits - total_bits

    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "block_count": block_count,
        "model": render_huge_anchor_model(model),
        "search_radius": search_radius,
    }


def encode_huge_anchor_payload(
    data: bytes,
    width_bits: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> dict:
    """Zakoduje data do exact payloadu vseobecnej huge-anchor vetvy."""

    _validate_width_bits(width_bits)
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")

    payload = bytes(data)
    blocks = bytes_to_huge_blocks(payload, width_bits)
    encoded_blocks = [encode_block_huge_anchor(block, width_bits, model, search_radius=search_radius) for block in blocks]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    residual_codec = choose_best_residual_codec(residuals)

    return {
        "codec": "huge_anchor_index",
        "width_bits": width_bits,
        "original_size": len(payload),
        "block_count": len(blocks),
        "model": {
            "family": model.family,
            "params": dict(model.params),
        },
        "flags": [bool(entry["escaped"]) for entry in encoded_blocks],
        "indices": [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None],
        "raw_blocks": [int(block) for block, entry in zip(blocks, encoded_blocks) if entry["escaped"]],
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "residual_payload": residual_codec.payload,
    }


def decode_huge_anchor_payload(payload: dict) -> bytes:
    """Dekoduje payload huge-anchor vetvy spat na povodne bajty."""

    if payload.get("codec") not in {None, "huge_anchor_index"}:
        raise ValueError("Unsupported huge-anchor payload codec")

    width_bits = payload.get("width_bits")
    original_size = payload.get("original_size")
    block_count = payload.get("block_count")
    flags = payload.get("flags")
    indices = payload.get("indices")
    raw_blocks = payload.get("raw_blocks")
    model_payload = payload.get("model")
    residual_payload = payload.get("residual_payload")

    if not isinstance(width_bits, int):
        raise ValueError("width_bits must be an integer")
    if not isinstance(original_size, int) or original_size < 0:
        raise ValueError("original_size must be a non-negative integer")
    if not isinstance(block_count, int) or block_count < 0:
        raise ValueError("block_count must be a non-negative integer")
    if not isinstance(flags, list):
        raise ValueError("flags must be a list")
    if not isinstance(indices, list):
        raise ValueError("indices must be a list")
    if not isinstance(raw_blocks, list):
        raise ValueError("raw_blocks must be a list")
    if not isinstance(model_payload, dict):
        raise ValueError("model must be a dict")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")

    _validate_width_bits(width_bits)
    if len(flags) != block_count:
        raise ValueError("flags length does not match block_count")

    raw_model_params = model_payload.get("params")
    if not isinstance(raw_model_params, dict):
        raise ValueError("model.params must be a dict")
    model = HugeAnchorModel(family=str(model_payload.get("family")), params={str(key): int(value) for key, value in raw_model_params.items()})

    residuals = _decode_residual_payload(residual_payload)
    index_position = 0
    residual_position = 0
    raw_position = 0
    decoded_blocks: list[int] = []

    for flag in flags:
        escaped = _coerce_flag(flag)
        if escaped:
            if raw_position >= len(raw_blocks):
                raise ValueError("raw_blocks are shorter than escape flags")
            decoded_blocks.append(int(raw_blocks[raw_position]))
            raw_position += 1
            continue

        if index_position >= len(indices):
            raise ValueError("indices are shorter than non-escape flags")
        if residual_position >= len(residuals):
            raise ValueError("residual stream is shorter than non-escape flags")

        index = int(indices[index_position])
        residual = int(residuals[residual_position])
        index_position += 1
        residual_position += 1

        anchor = anchor_from_index(index, model, width_bits)
        if anchor is None:
            raise ValueError("Stored index cannot reconstruct a valid anchor")
        decoded_blocks.append(anchor + residual)

    if index_position != len(indices):
        raise ValueError("Unused indices remain after decoding")
    if residual_position != len(residuals):
        raise ValueError("Unused residual values remain after decoding")
    if raw_position != len(raw_blocks):
        raise ValueError("Unused raw blocks remain after decoding")

    return huge_blocks_to_bytes(decoded_blocks, width_bits, original_size)


def roundtrip_huge_anchor(
    data: bytes,
    width_bits: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> bytes:
    """Zakoduje a spatne dekoduje data cez huge-anchor payload."""

    return decode_huge_anchor_payload(encode_huge_anchor_payload(bytes(data), width_bits, model, search_radius=search_radius))


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze sirka blokov patri medzi podporovane huge bloky."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")


def _validate_block_value(x: int, width_bits: int) -> None:
    """Overi rozsah jedneho bloku pre danu sirku."""

    if x < 0 or x >= (1 << width_bits):
        raise ValueError(f"Block out of range for {width_bits} bits: {x}")


def _estimate_index(x: int, model: HugeAnchorModel) -> int:
    """Vrati analyticky odhad indexu pre danu family."""

    family = model.family
    params = model.params

    if family == "linear_shift":
        return x >> params["shift"]
    if family == "affine_shift":
        shifted = x - params["bias"]
        if shifted <= 0:
            return 0
        return shifted >> params["shift"]
    if family == "multiple":
        return x // params["step"]
    if family == "square":
        return isqrt(x)
    if family == "scaled_prime":
        return x >> params["shift"]
    raise ValueError(f"Unsupported huge anchor family: {family}")


def _effective_search_radius(model: HugeAnchorModel, search_radius: int) -> int:
    """Vrati skutocny encoder-side search radius pre kandidata."""

    model_radius = int(model.params.get("search_radius", 0))
    return max(search_radius, model_radius)


def _decode_residual_payload(payload: dict) -> list[int]:
    """Dekoduje residual payload podla ulozeneho codec mena."""

    codec_name = payload.get("codec")
    if codec_name in {None, "fixed_signed"}:
        return decode_fixed_signed_residual_payload(payload)
    if codec_name == "zero_rle":
        return decode_zero_rle_residual_payload(payload)
    raise ValueError(f"Unsupported residual payload codec: {codec_name}")


def _coerce_flag(flag: object) -> bool:
    """Prevedie payload flag na bool s kontrolou povoleneho tvaru."""

    if isinstance(flag, bool):
        return flag
    if isinstance(flag, int) and flag in {0, 1}:
        return bool(flag)
    raise ValueError("Flag values must be bool or 0/1 integers")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer ceny huge-anchor vetvy voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
```

## File: `src/primesymbolicmdl/huge_anchor_datasets.py`

```python
"""Kontrolovane datasety pre huge-anchor portfolio experimenty."""

from __future__ import annotations

from .experiments import dataset_random
from .huge_blocks import huge_blocks_to_bytes

_DATASET_NAMES = [
    "linear_shift_generated",
    "square_generated",
    "multiple_generated",
    "random_bytes",
    "ascii_small",
    "repeating_pattern",
]


def get_huge_anchor_dataset_names() -> list[str]:
    """Vrati stabilny zoznam podporovanych nazvov datasetov."""

    return list(_DATASET_NAMES)


def make_huge_anchor_dataset(name: str, width_bits: int, count: int = 32, seed: int = 1234) -> bytes:
    """Vrati jeden deterministicky dataset pre zvolenu sirku a pocet blokov."""

    if count < 0:
        raise ValueError("count must be non-negative")
    width_bytes = width_bits // 8
    total_size = count * width_bytes

    if name == "linear_shift_generated":
        shift = _generated_shift(width_bits)
        blocks = [((index << shift) + _small_positive_diff(index)) % (1 << width_bits) for index in range(count)]
        return huge_blocks_to_bytes(blocks, width_bits, total_size)

    if name == "square_generated":
        blocks = [((index * index) + _small_positive_diff(index)) % (1 << width_bits) for index in range(count)]
        return huge_blocks_to_bytes(blocks, width_bits, total_size)

    if name == "multiple_generated":
        step = _generated_step(width_bits)
        blocks = [((index * step) + _small_positive_diff(index)) % (1 << width_bits) for index in range(count)]
        return huge_blocks_to_bytes(blocks, width_bits, total_size)

    if name == "random_bytes":
        return dataset_random(total_size, seed=seed)

    if name == "ascii_small":
        phrase = b"PrimeSymbolicMDL-huge-anchor-demo|"
        return _repeat_to_length(phrase, total_size)

    if name == "repeating_pattern":
        pattern = b"ABCD"
        return _repeat_to_length(pattern, total_size)

    raise ValueError(f"Unknown huge-anchor dataset: {name}")


def _generated_shift(width_bits: int) -> int:
    """Vrati shift pouzity pre synthetic linear dataset."""

    return max(1, min(8, width_bits // 4))


def _generated_step(width_bits: int) -> int:
    """Vrati step pouzity pre synthetic multiple dataset."""

    del width_bits
    return 31


def _small_positive_diff(index: int) -> int:
    """Vrati malu deterministicku odchylku bez zapornych diffov."""

    return (index * 3) % 3


def _repeat_to_length(pattern: bytes, total_size: int) -> bytes:
    """Opakuje bajtovy vzor na presnu pozadovanu dlzku."""

    if total_size == 0:
        return b""
    repeats = (total_size + len(pattern) - 1) // len(pattern)
    return (pattern * repeats)[:total_size]
```

## File: `src/primesymbolicmdl/huge_anchor_demo.py`

```python
"""Sirsie CLI porovnanie huge-anchor portfolia a scaled-prime baseline."""

from __future__ import annotations

from .huge_anchor_datasets import make_huge_anchor_dataset
from .huge_anchor_search import search_best_huge_anchor_model
from .scaled_prime_search import search_best_scaled_prime_model


def run_demo() -> list[dict]:
    """Spusti malu deterministicku benchmark sadu nad portfolio branchom."""

    datasets = (
        "linear_shift_generated",
        "square_generated",
        "multiple_generated",
        "random_bytes",
        "ascii_small",
        "repeating_pattern",
    )
    widths = (16, 32, 64)

    results: list[dict] = []
    for dataset_name in datasets:
        for width_bits in widths:
            data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
            portfolio = search_best_huge_anchor_model(data, width_bits=width_bits)
            scaled_prime = search_best_scaled_prime_model(data, width_bits=width_bits) if width_bits <= 64 else None
            results.append(
                {
                    "dataset": dataset_name,
                    "width_bits": width_bits,
                    "best_model": portfolio["best_model"],
                    "best_model_string": portfolio["best_model_string"],
                    "raw_bits": portfolio["raw_bits"],
                    "total_bits": portfolio["total_bits"],
                    "saving_bits": portfolio["saving_bits"],
                    "ratio_vs_raw": portfolio["ratio_vs_raw"],
                    "residual_codec": portfolio["residual_codec"],
                    "escape_count": portfolio["escape_count"],
                    "roundtrip_ok": portfolio["roundtrip_ok"],
                    "decision": portfolio["decision"],
                    "search_radius": portfolio["search_radius"],
                    "top_candidates": portfolio["top_candidates"],
                    "scaled_prime_baseline": scaled_prime,
                }
            )
    return results


def format_huge_anchor_result(result: dict) -> str:
    """Vrati stabilny textovy report jedneho benchmark behu."""

    ratio = result["ratio_vs_raw"]
    lines = [
        f"dataset: {result['dataset']}",
        f"width_bits: {result['width_bits']}",
        f"best_model: {result['best_model_string']}",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"ratio_vs_raw: {ratio:.3f}" if ratio != float("inf") else "ratio_vs_raw: inf",
        f"residual_codec: {result['residual_codec']}",
        f"escape_count: {result['escape_count']}",
        f"roundtrip_ok: {result['roundtrip_ok']}",
        f"decision: {result['decision']}",
        f"search_radius: {result['search_radius']}",
        "top_3_candidates:",
    ]
    for index, candidate in enumerate(result["top_candidates"], start=1):
        lines.append(
            f"{index}. {candidate['model']} radius={candidate['search_radius']} total_bits={candidate['total_bits']} "
            f"saving_bits={candidate['saving_bits']} residual_codec={candidate['residual_codec']} escapes={candidate['escape_count']}"
        )

    scaled_prime = result.get("scaled_prime_baseline")
    if scaled_prime is None:
        lines.append("scaled_prime_baseline: n/a")
    else:
        lines.append(
            "scaled_prime_baseline: "
            f"{scaled_prime['best_model_string']} total_bits={scaled_prime['total_bits']} "
            f"saving_bits={scaled_prime['saving_bits']} residual_codec={scaled_prime['residual_codec']} "
            f"decision={'win' if scaled_prime['total_bits'] < scaled_prime['raw_bits'] else 'raw_fallback'}"
        )
    return "\n".join(lines)


def main() -> None:
    """Vypise portfolio benchmark reporty do stdout."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_huge_anchor_result(result))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/huge_anchor_file_benchmark.py`

```python
"""Deterministicky benchmark pre `.psmdl` file CLI bez univerzalnych tvrdeni."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

from .huge_anchor_datasets import make_huge_anchor_dataset
from .huge_anchor_file import PsmdlCompressionRefusedError, compress_file, decompress_file


@dataclass(frozen=True)
class BenchmarkRow:
    """Jeden riadok honest actual-size benchmarku."""

    name: str
    raw_bytes: int
    psmdl_bytes: int
    decision: str
    file_format: str
    roundtrip_ok: bool
    require_compression: str
    note: str = ""


def _benchmark_one(
    name: str,
    data: bytes,
    *,
    width_bits: int = 32,
    note: str = "",
) -> BenchmarkRow:
    """Skomprimuje jeden vstup do docasneho suboru a overi roundtrip."""

    with tempfile.TemporaryDirectory(prefix="psmdl-bench-") as tmp_dir:
        tmp = Path(tmp_dir)
        input_path = tmp / "input.bin"
        psmdl_path = tmp / "output.psmdl"
        restored_path = tmp / "restored.bin"
        input_path.write_bytes(data)

        result = compress_file(input_path, psmdl_path, width_bits=width_bits)
        restored = decompress_file(psmdl_path, restored_path)
        roundtrip_ok = restored == data

        require_status = "ok"
        try:
            refused_path = tmp / "refused.psmdl"
            compress_file(input_path, refused_path, width_bits=width_bits, require_compression=True)
            if result.decision != "compressed":
                require_status = "unexpected_ok"
        except PsmdlCompressionRefusedError:
            if result.decision == "compressed":
                require_status = "unexpected_refused"
            else:
                require_status = "refused"
        except Exception as error:  # pragma: no cover - defensive
            require_status = f"error:{error}"

        return BenchmarkRow(
            name=name,
            raw_bytes=len(data),
            psmdl_bytes=result.compressed_bytes,
            decision=result.decision,
            file_format=result.file_format,
            roundtrip_ok=roundtrip_ok,
            require_compression=require_status,
            note=note,
        )


def run_benchmark() -> list[BenchmarkRow]:
    """Spusti maly deterministicky benchmark nad repozitarnymi a syntetickymi vstupmi."""

    repo_root = Path(__file__).resolve().parents[2]
    rows: list[BenchmarkRow] = []

    rows.append(
        _benchmark_one(
            "random_bytes_128",
            make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234),
            note="deterministic random sanity",
        )
    )
    rows.append(
        _benchmark_one(
            "repeating_pattern",
            make_huge_anchor_dataset("repeating_pattern", 32, count=32, seed=1234),
            note="ABCD repeat",
        )
    )

    for rel_path in ("README.md", "AGENTS.md"):
        source = repo_root / rel_path
        rows.append(
            _benchmark_one(
                rel_path,
                source.read_bytes(),
                note="repo text file",
            )
        )

    py_source = repo_root / "src" / "primesymbolicmdl" / "huge_anchor_file.py"
    rows.append(
        _benchmark_one(
            "src/primesymbolicmdl/huge_anchor_file.py",
            py_source.read_bytes(),
            note="repo python source",
        )
    )
    rows.append(
        _benchmark_one(
            "square_generated_64",
            make_huge_anchor_dataset("square_generated", 64, count=32, seed=1234),
            width_bits=64,
            note="synthetic structure-compatible dataset",
        )
    )
    return rows


def format_benchmark_table(rows: list[BenchmarkRow]) -> str:
    """Vrati citatelnu tabulku actual byte sizes."""

    header = (
        "name | raw_bytes | psmdl_bytes | decision | file_format | roundtrip_ok | require_compression | note"
    )
    lines = [header, "-" * len(header)]
    for row in rows:
        lines.append(
            f"{row.name} | {row.raw_bytes} | {row.psmdl_bytes} | {row.decision} | "
            f"{row.file_format} | {row.roundtrip_ok} | {row.require_compression} | {row.note}"
        )
    return "\n".join(lines)


def main() -> None:
    """Vypise honest benchmark tabulku do stdout."""

    print(format_benchmark_table(run_benchmark()))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/huge_anchor_file_cli.py`

```python
"""CLI pre huge-anchor `.psmdl` kompresiu a dekompresiu suborov."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .huge_anchor_file import PsmdlCompressionRefusedError, compress_file, decompress_file
from .huge_blocks import SUPPORTED_HUGE_WIDTHS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PrimeSymbolicMDL huge-anchor file compression and decompression.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    compress_parser = subparsers.add_parser("compress", help="Compress an input file to .psmdl")
    compress_parser.add_argument("--input", required=True, help="Path to the raw input file")
    compress_parser.add_argument("--output", required=True, help="Path to the output .psmdl file")
    compress_parser.add_argument(
        "--width-bits",
        type=int,
        default=32,
        choices=sorted(SUPPORTED_HUGE_WIDTHS),
        help="Huge block width in bits",
    )
    compress_parser.add_argument(
        "--require-compression",
        action="store_true",
        help="Refuse to write output when the huge-anchor blob is not smaller than raw",
    )
    compress_parser.add_argument(
        "--actual-rerank-top-n",
        type=int,
        default=16,
        help="How many estimated candidates to rerank by actual serialized size",
    )

    decompress_parser = subparsers.add_parser("decompress", help="Decompress a .psmdl file")
    decompress_parser.add_argument("--input", required=True, help="Path to the input .psmdl file")
    decompress_parser.add_argument("--output", required=True, help="Path to the restored output file")
    return parser


def _format_compress_summary(result) -> str:
    return (
        f"decision={result.decision} "
        f"file_format={result.file_format} "
        f"width_bits={result.width_bits} "
        f"raw_bytes={result.raw_bytes} "
        f"compressed_bytes={result.compressed_bytes} "
        f"roundtrip_ok={result.roundtrip_ok} "
        f"best_model={result.best_model_string} "
        f"search_radius={result.search_radius}"
    )


def main(argv: list[str] | None = None) -> int:
    """Spusti CLI pre compress alebo decompress."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "compress":
            result = compress_file(
                args.input,
                args.output,
                width_bits=args.width_bits,
                require_compression=args.require_compression,
                actual_rerank_top_n=args.actual_rerank_top_n,
            )
            print(_format_compress_summary(result))
            return 0

        decompress_file(args.input, args.output)
        print(f"restored_bytes={Path(args.output).stat().st_size}")
        return 0
    except PsmdlCompressionRefusedError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (ValueError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## File: `src/primesymbolicmdl/huge_anchor_file.py`

```python
"""Súborový `.psmdl` wrapper pre huge-anchor binárnu kompresiu."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .bitstream import decode_unsigned_varint, encode_unsigned_varint
from .huge_anchor_binary import (
    _MAGIC as _HUGE_ANCHOR_MAGIC,
    compress_best_huge_anchor_binary,
    decode_huge_anchor_binary,
)

_RAW_MAGIC = b"PSMDLRAW1"
_RAW_VERSION = 1


class PsmdlCompressionRefusedError(RuntimeError):
    """Vznika, ked CLI odmietne zapis, lebo kompresia nie je mensia ako raw."""


@dataclass(frozen=True)
class PsmdlCompressResult:
    """Vysledok kompresie pred zapisom do suboru."""

    file_bytes: bytes
    width_bits: int
    raw_bytes: int
    compressed_bytes: int
    decision: str
    file_format: str
    roundtrip_ok: bool
    best_model_string: str
    search_radius: int
    estimated_best_model_string: str
    actual_rerank_changed_winner: bool


def encode_raw_psmdl(data: bytes) -> bytes:
    """Zabali povodne bajty do bezpecneho raw-fallback `.psmdl` kontajnera."""

    payload = bytes(data)
    output = bytearray()
    output.extend(_RAW_MAGIC)
    output.append(_RAW_VERSION)
    output.extend(encode_unsigned_varint(len(payload)))
    output.extend(payload)
    return bytes(output)


def decode_raw_psmdl(blob: bytes) -> bytes:
    """Dekoduje raw-fallback `.psmdl` kontajner."""

    payload = bytes(blob)
    if not payload.startswith(_RAW_MAGIC):
        raise ValueError("Unsupported raw .psmdl magic")
    if len(payload) <= len(_RAW_MAGIC):
        raise ValueError("Raw .psmdl payload is truncated")

    version = payload[len(_RAW_MAGIC)]
    if version != _RAW_VERSION:
        raise ValueError(f"Unsupported raw .psmdl version: {version}")

    offset = len(_RAW_MAGIC) + 1
    original_size, offset = decode_unsigned_varint(payload, offset)
    if offset + original_size > len(payload):
        raise ValueError("Truncated raw .psmdl payload")
    if offset + original_size < len(payload):
        raise ValueError("Raw .psmdl payload has trailing bytes")

    return payload[offset : offset + original_size]


def decode_psmdl_bytes(blob: bytes) -> bytes:
    """Dekoduje `.psmdl` subor bez ohladu na to, ci ide o huge-anchor alebo raw fallback."""

    payload = bytes(blob)
    if payload.startswith(_HUGE_ANCHOR_MAGIC):
        return decode_huge_anchor_binary(payload)
    if payload.startswith(_RAW_MAGIC):
        return decode_raw_psmdl(payload)
    raise ValueError("Unsupported .psmdl file magic")


def compress_to_psmdl_bytes(
    data: bytes,
    width_bits: int = 32,
    *,
    require_compression: bool = False,
    actual_rerank_top_n: int = 16,
) -> PsmdlCompressResult:
    """Skomprimuje bajty do `.psmdl` reprezentacie s uctivym raw fallbackom."""

    payload = bytes(data)
    search_result = compress_best_huge_anchor_binary(
        payload,
        width_bits=width_bits,
        allow_raw_fallback=True,
        actual_rerank_top_n=actual_rerank_top_n,
    )

    if search_result["decision"] == "compressed":
        file_bytes = bytes(search_result["binary_blob"])
        file_format = "huge_anchor"
        decision = "compressed"
    elif require_compression:
        raise PsmdlCompressionRefusedError(
            "Huge-anchor binary blob is not smaller than raw input; refusing to write output"
        )
    else:
        file_bytes = encode_raw_psmdl(payload)
        file_format = "raw_fallback"
        decision = "raw_fallback"

    roundtrip_ok = decode_psmdl_bytes(file_bytes) == payload
    if not roundtrip_ok:
        raise RuntimeError("PSMDL compress roundtrip verification failed")

    return PsmdlCompressResult(
        file_bytes=file_bytes,
        width_bits=width_bits,
        raw_bytes=len(payload),
        compressed_bytes=len(file_bytes),
        decision=decision,
        file_format=file_format,
        roundtrip_ok=roundtrip_ok,
        best_model_string=str(search_result["best_model_string"]),
        search_radius=int(search_result["search_radius"]),
        estimated_best_model_string=str(search_result["estimated_best_model_string"]),
        actual_rerank_changed_winner=bool(search_result["actual_rerank_changed_winner"]),
    )


def compress_file(
    input_path: str | Path,
    output_path: str | Path,
    *,
    width_bits: int = 32,
    require_compression: bool = False,
    actual_rerank_top_n: int = 16,
) -> PsmdlCompressResult:
    """Precita vstupny subor, zapise `.psmdl` vystup a overi presny roundtrip."""

    source = Path(input_path)
    destination = Path(output_path)
    payload = source.read_bytes()
    result = compress_to_psmdl_bytes(
        payload,
        width_bits=width_bits,
        require_compression=require_compression,
        actual_rerank_top_n=actual_rerank_top_n,
    )
    destination.write_bytes(result.file_bytes)
    return result


def decompress_file(input_path: str | Path, output_path: str | Path) -> bytes:
    """Dekoduje `.psmdl` subor a zapise obnovene bajty."""

    source = Path(input_path)
    destination = Path(output_path)
    restored = decode_psmdl_bytes(source.read_bytes())
    destination.write_bytes(restored)
    return restored
```

## File: `src/primesymbolicmdl/huge_anchor_models.py`

```python
"""Vseobecne index-plus-diff anchor modely pre vacsie bloky."""

from __future__ import annotations

from dataclasses import dataclass

from .huge_blocks import SUPPORTED_HUGE_WIDTHS
from .prime_bigint import prev_prime_64
from .residual_codecs import unsigned_width_for_max, zigzag_encode

SUPPORTED_HUGE_ANCHOR_FAMILIES = (
    "linear_shift",
    "affine_shift",
    "multiple",
    "square",
    "scaled_prime",
)
_FIXED_MODEL_BITS = 12
_FAMILY_BITS = unsigned_width_for_max(len(SUPPORTED_HUGE_ANCHOR_FAMILIES) - 1)
_MAX_UINT64 = 1 << 64


@dataclass(frozen=True, order=True)
class HugeAnchorModel:
    """Popis jednej anchor family a jej parametrov."""

    family: str
    params: dict[str, int]


def huge_anchor_model_to_dict(model: HugeAnchorModel) -> dict:
    """Vrati stabilny serializovatelny slovnik modelu."""

    normalized = _normalize_model(model)
    return {
        "family": normalized.family,
        "params": dict(normalized.params),
    }


def huge_anchor_model_from_dict(data: dict) -> HugeAnchorModel:
    """Vytvori a znormalizuje model zo slovnikovej reprezentacie."""

    if not isinstance(data, dict):
        raise ValueError("model data must be a dict")

    family = data.get("family")
    params = data.get("params")
    if not isinstance(family, str):
        raise ValueError("model data must contain string family")
    if not isinstance(params, dict):
        raise ValueError("model data must contain dict params")

    normalized_params: dict[str, int] = {}
    for key, value in params.items():
        normalized_params[str(key)] = int(value)
    return _normalize_model(HugeAnchorModel(family=family, params=normalized_params))


def render_huge_anchor_model(model: HugeAnchorModel) -> str:
    """Vrati stabilnu textualnu reprezentaciu anchor modelu."""

    normalized = _normalize_model(model)
    if not normalized.params:
        return normalized.family
    rendered_params = ", ".join(f"{key}={normalized.params[key]}" for key in sorted(normalized.params))
    return f"{normalized.family}({rendered_params})"


def huge_anchor_model_bits(model: HugeAnchorModel) -> int:
    """Vrati fixnu cenu identifikacie vseobecnej huge-anchor vetvy."""

    _normalize_model(model)
    return _FIXED_MODEL_BITS


def huge_anchor_parameter_bits(model: HugeAnchorModel) -> int:
    """Vrati cenu family taga a jej ciselnych parametrov."""

    normalized = _normalize_model(model)
    parameter_bits = _FAMILY_BITS
    for key, value in normalized.params.items():
        if _is_signed_param(normalized.family, key):
            parameter_bits += unsigned_width_for_max(zigzag_encode(value))
        else:
            parameter_bits += unsigned_width_for_max(value)
    return parameter_bits


def anchor_from_index(index: int, model: HugeAnchorModel, width_bits: int) -> int | None:
    """Vrati deterministicky anchor pre dany index alebo None."""

    normalized = _normalize_model(model)
    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")
    if index < 0:
        return None

    anchor: int | None
    if normalized.family == "linear_shift":
        anchor = index << normalized.params["shift"]
    elif normalized.family == "affine_shift":
        anchor = (index << normalized.params["shift"]) + normalized.params["bias"]
    elif normalized.family == "multiple":
        anchor = index * normalized.params["step"]
    elif normalized.family == "square":
        anchor = index * index
    elif normalized.family == "scaled_prime":
        if width_bits > 64:
            return None
        base = index << normalized.params["shift"]
        if base >= _MAX_UINT64:
            return None
        anchor = prev_prime_64(base)
    else:
        raise ValueError(f"Unsupported huge anchor family: {normalized.family}")

    if anchor is None or anchor < 0 or anchor >= (1 << width_bits):
        return None
    return int(anchor)


def _normalize_model(model: HugeAnchorModel) -> HugeAnchorModel:
    """Overi family a vrati normalizovanu kopiu s ocakavanymi parametrami."""

    if model.family not in SUPPORTED_HUGE_ANCHOR_FAMILIES:
        raise ValueError(f"Unsupported huge anchor family: {model.family}")

    raw_params = dict(model.params)

    if model.family == "linear_shift":
        shift = _require_non_negative_int(raw_params, "shift")
        _reject_extra_params(model.family, raw_params, {"shift"})
        return HugeAnchorModel(model.family, {"shift": shift})

    if model.family == "affine_shift":
        shift = _require_non_negative_int(raw_params, "shift")
        bias = _require_int(raw_params, "bias")
        _reject_extra_params(model.family, raw_params, {"shift", "bias"})
        return HugeAnchorModel(model.family, {"shift": shift, "bias": bias})

    if model.family == "multiple":
        step = _require_positive_int(raw_params, "step")
        _reject_extra_params(model.family, raw_params, {"step"})
        return HugeAnchorModel(model.family, {"step": step})

    if model.family == "square":
        _reject_extra_params(model.family, raw_params, set())
        return HugeAnchorModel(model.family, {})

    shift = _require_positive_int(raw_params, "shift")
    search_radius = int(raw_params.pop("search_radius", 0))
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")
    _reject_extra_params(model.family, raw_params, {"shift", "search_radius"})
    return HugeAnchorModel(model.family, {"shift": shift, "search_radius": search_radius})


def _require_int(params: dict[str, int], key: str) -> int:
    """Vrati integer parameter alebo vyhodi chybu."""

    if key not in params or not isinstance(params[key], int):
        raise ValueError(f"Missing or invalid integer parameter: {key}")
    return int(params[key])


def _require_non_negative_int(params: dict[str, int], key: str) -> int:
    """Vrati nezaporny integer parameter alebo vyhodi chybu."""

    value = _require_int(params, key)
    if value < 0:
        raise ValueError(f"{key} must be non-negative")
    return value


def _require_positive_int(params: dict[str, int], key: str) -> int:
    """Vrati kladny integer parameter alebo vyhodi chybu."""

    value = _require_int(params, key)
    if value <= 0:
        raise ValueError(f"{key} must be positive")
    return value


def _reject_extra_params(family: str, params: dict[str, int], expected: set[str]) -> None:
    """Overi, ze family nedostala necakane parametre."""

    unknown = set(params) - expected
    if unknown:
        raise ValueError(f"Unexpected parameters for {family}: {sorted(unknown)}")


def _is_signed_param(family: str, key: str) -> bool:
    """Vrati pravdu pre parametre, ktore mozu byt podpisane."""

    return family == "affine_shift" and key == "bias"
```

## File: `src/primesymbolicmdl/huge_anchor_search.py`

```python
"""Portfolio search nad viacerymi huge-anchor families."""

from __future__ import annotations

from .huge_anchor_branch import estimate_huge_anchor_cost, roundtrip_huge_anchor
from .huge_anchor_models import HugeAnchorModel, huge_anchor_model_to_dict, render_huge_anchor_model
from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks

_FAMILY_RANK = {
    "linear_shift": 0,
    "multiple": 1,
    "square": 2,
    "affine_shift": 3,
    "scaled_prime": 4,
}


def candidate_huge_anchor_models(width_bits: int) -> list[HugeAnchorModel]:
    """Vrati malu deterministicku mriezku kandidatov pre danu sirku."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")

    models: list[HugeAnchorModel] = []
    shift_values = _general_shift_values(width_bits)
    bias_values = (-16, -1, 0, 1, 16)
    step_values = (2, 3, 4, 5, 7, 8, 16, 31, 64, 127, 256)

    for shift in shift_values:
        models.append(HugeAnchorModel("linear_shift", {"shift": shift}))
    for shift in shift_values:
        for bias in bias_values:
            models.append(HugeAnchorModel("affine_shift", {"shift": shift, "bias": bias}))
    for step in step_values:
        models.append(HugeAnchorModel("multiple", {"step": step}))
    models.append(HugeAnchorModel("square", {}))

    if width_bits <= 64:
        for shift in _scaled_prime_shift_values(width_bits):
            models.append(HugeAnchorModel("scaled_prime", {"shift": shift, "search_radius": 0}))

    return models


def search_best_huge_anchor_model(
    data: bytes,
    width_bits: int = 32,
    search_radius_values: tuple[int, ...] = (0, 1, 2, 4),
    seed: int = 1234,
) -> dict:
    """Vyskusa portfolio huge-anchor families a vrati najlepsi model."""

    del seed

    payload = bytes(data)
    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")
    if not search_radius_values:
        raise ValueError("search_radius_values must not be empty")

    blocks = bytes_to_huge_blocks(payload, width_bits)
    history: list[dict] = []
    best_model: HugeAnchorModel | None = None
    best_cost: dict | None = None
    best_radius = 0
    best_key: tuple[int, int, int, str, int] | None = None

    for model in candidate_huge_anchor_models(width_bits):
        model_string = render_huge_anchor_model(model)
        model_dict = huge_anchor_model_to_dict(model)
        for search_radius in search_radius_values:
            cost = estimate_huge_anchor_cost(blocks, width_bits, len(payload), model, search_radius=search_radius)
            history.append(
                {
                    "family": model.family,
                    "model_dict": dict(model_dict),
                    "model": model_string,
                    "search_radius": search_radius,
                    "total_bits": cost["total_bits"],
                    "saving_bits": cost["saving_bits"],
                    "residual_codec": cost["residual_codec"],
                    "escape_count": cost["escape_count"],
                }
            )
            candidate_key = (
                cost["total_bits"],
                cost["parameter_bits"],
                _FAMILY_RANK[model.family],
                model_string,
                search_radius,
            )
            if best_key is None or candidate_key < best_key:
                best_key = candidate_key
                best_model = model
                best_cost = cost
                best_radius = search_radius

    if best_model is None or best_cost is None:
        raise RuntimeError("Huge-anchor portfolio search did not produce any candidate model")

    ordered_history = sorted(
        history,
        key=lambda row: (row["total_bits"], _FAMILY_RANK[row["family"]], row["model"], row["search_radius"]),
    )
    top_candidates = _top_unique_models(ordered_history, limit=3)
    roundtrip_ok = roundtrip_huge_anchor(payload, width_bits, best_model, search_radius=best_radius) == payload

    return {
        "best_model": best_model,
        "best_model_dict": huge_anchor_model_to_dict(best_model),
        "best_model_string": render_huge_anchor_model(best_model),
        "raw_bits": best_cost["raw_bits"],
        "total_bits": best_cost["total_bits"],
        "saving_bits": best_cost["saving_bits"],
        "ratio_vs_raw": best_cost["ratio_vs_raw"],
        "history": ordered_history,
        "width_bits": width_bits,
        "search_radius": best_radius,
        "roundtrip_ok": roundtrip_ok,
        "decision": "win" if best_cost["total_bits"] < best_cost["raw_bits"] else "raw_fallback",
        "residual_codec": best_cost["residual_codec"],
        "escape_count": best_cost["escape_count"],
        "top_candidates": top_candidates,
    }


def _general_shift_values(width_bits: int) -> tuple[int, ...]:
    """Vrati rozumne, ale obmedzene, shift kandidaty pre linear/affine family."""

    preferred = (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 112, 120)
    return tuple(value for value in preferred if 0 <= value < width_bits)


def _scaled_prime_shift_values(width_bits: int) -> tuple[int, ...]:
    """Vrati mensiu sadu shift kandidatov pre scaled-prime family."""

    if width_bits == 8:
        return (1, 2, 3, 4, 5, 6)
    if width_bits == 16:
        return tuple(range(1, 13))
    if width_bits == 24:
        return (1, 2, 4, 6, 8, 10, 12, 16, 20)
    if width_bits == 32:
        return (1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 28)
    if width_bits == 40:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36)
    if width_bits == 48:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40)
    if width_bits == 56:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    if width_bits == 64:
        return (8, 12, 16, 20, 24, 28, 32)
    raise ValueError(f"Scaled-prime family is unsupported for width {width_bits}")


def _top_unique_models(history: list[dict], limit: int) -> list[dict]:
    """Vrati prvych N kandidatov s jedinecnym model stringom."""

    selected: list[dict] = []
    seen_models: set[str] = set()
    for row in history:
        if row["model"] in seen_models:
            continue
        selected.append(row)
        seen_models.add(row["model"])
        if len(selected) >= limit:
            break
    return selected
```

## File: `src/primesymbolicmdl/huge_blocks.py`

```python
"""Pomocne funkcie pre balenie vacsich blokov do Python int."""

from __future__ import annotations

SUPPORTED_HUGE_WIDTHS = {8, 16, 24, 32, 40, 48, 56, 64, 96, 128}


def _width_bytes(width_bits: int) -> int:
    """Vrati sirku bloku v bajtoch alebo vyhodi chybu."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")
    return width_bits // 8


def bytes_to_huge_blocks(data: bytes, width_bits: int) -> list[int]:
    """Prevedie bajty na big-endian bloky a posledny blok nulovo doplni."""

    width_bytes = _width_bytes(width_bits)
    payload = bytes(data)
    if not payload:
        return []

    blocks: list[int] = []
    for start in range(0, len(payload), width_bytes):
        chunk = payload[start : start + width_bytes]
        if len(chunk) < width_bytes:
            chunk = chunk + (b"\x00" * (width_bytes - len(chunk)))
        blocks.append(int.from_bytes(chunk, "big"))
    return blocks


def huge_blocks_to_bytes(blocks: list[int], width_bits: int, original_size: int) -> bytes:
    """Zlozi bloky spat na bajty a oreze nulove doplnenie na povodnu dlzku."""

    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    width_bytes = _width_bytes(width_bits)
    upper_bound = 1 << width_bits
    output = bytearray()

    for block in blocks:
        if int(block) < 0 or int(block) >= upper_bound:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")
        output.extend(int(block).to_bytes(width_bytes, "big"))

    if original_size > len(output):
        raise ValueError("original_size exceeds decoded byte length")

    return bytes(output[:original_size])
```

## File: `src/primesymbolicmdl/image_ablation.py`

```python
"""Rychle ablation benchmarky pre Image-GP-lite primitive sety."""

from __future__ import annotations

from .simulation import run_image_simulation

_ABLATION_PRIMITIVE_SETS = ("local", "ramp", "structure")


def run_image_gplite_ablation(
    dataset_name: str,
    width: int = 16,
    height: int = 16,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 10,
) -> list[dict]:
    """Spusti Image-GP-lite nad vsetkymi hlavnymi primitive setmi."""

    rows = []
    for primitive_set in _ABLATION_PRIMITIVE_SETS:
        result = run_image_simulation(
            "Image-GP-lite",
            dataset_name=dataset_name,
            image_width=width,
            image_height=height,
            seed=seed,
            population_size=population_size,
            generations=generations,
            max_index=31,
            strict_lower=False,
            image_gplite_primitive_set=primitive_set,
        )
        preview = result.get("preview", {})
        details = result.get("details", {})
        rows.append(
            {
                "dataset_name": dataset_name,
                "primitive_set": primitive_set,
                "raw_bits": result["raw_bits"],
                "total_bits": result["total_bits"],
                "saving_bits": result["saving_bits"],
                "ratio_vs_raw": result["ratio_vs_raw"],
                "best_model": result["best_model"],
                "residual_codec": details.get("residual_codec", "n/a"),
                "roundtrip_preview_ok": bool(preview.get("roundtrip_ok", False)),
            }
        )
    return rows


def format_image_ablation_table(rows: list[dict]) -> str:
    """Vrati markdown tabulku s vysledkami primitive-set ablationu."""

    header = (
        "| dataset | primitive_set | raw_bits | total_bits | saving_bits | ratio_vs_raw | "
        "best_model | residual_codec | roundtrip_preview_ok |"
    )
    divider = "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |"
    body = [header, divider]
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                [
                    str(row["dataset_name"]),
                    str(row["primitive_set"]),
                    str(row["raw_bits"]),
                    str(row["total_bits"]),
                    str(row["saving_bits"]),
                    f"{float(row['ratio_vs_raw']):.3f}",
                    str(row["best_model"]),
                    str(row["residual_codec"]),
                    str(bool(row["roundtrip_preview_ok"])),
                ]
            )
            + " |"
        )
    return "\n".join(body)


def main() -> None:
    """Vypise rychle markdown tabuľky pre hlavne synteticke datasety."""

    for index, dataset_name in enumerate(("gradient", "diagonal_ramp", "checker")):
        if index:
            print()
        print(f"## Image-GP-lite ablation: {dataset_name}")
        rows = run_image_gplite_ablation(dataset_name, width=16, height=16, seed=1234, population_size=16, generations=8)
        print(format_image_ablation_table(rows))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/image_context_laws.py`

```python
"""Male expression-tree prediktory nad 2D grayscale kontextom."""

from __future__ import annotations

from dataclasses import dataclass

from .bitcost import bits_unsigned_range

_TERMINAL_KINDS = (
    "col",
    "row",
    "left",
    "up",
    "up_left",
    "x_ramp",
    "y_ramp",
    "diag_ramp",
)
_NODE_KINDS = _TERMINAL_KINDS + (
    "const",
    "add",
    "sub",
    "avg",
    "gradient",
    "mul_small",
    "floordiv_pow2",
    "mod_const",
    "floordiv_const",
    "eq_const",
    "parity_byte",
    "checker_parity",
    "clamp_byte",
)
_NODE_KIND_BITS = bits_unsigned_range(len(_NODE_KINDS) - 1)
_MOD_DIV_CONST_VALUES = (2, 4, 8, 16)
_EQ_CONST_VALUES = tuple(range(17))
_CHECKER_BLOCKS = (1, 2, 4, 8, 16)


@dataclass(frozen=True)
class ImageLawNode:
    """Nemenny uzol maleho obrazkoveho expression stromu."""

    kind: str
    value: int | None = None
    children: tuple["ImageLawNode", ...] = ()


def terminal_law(name: str) -> ImageLawNode:
    """Vytvori terminal reprezentujuci decoder-znamy kontext."""

    law = ImageLawNode(str(name))
    _validate_law(law)
    return law


def const_law(value: int) -> ImageLawNode:
    """Vytvori konstantny terminal."""

    law = ImageLawNode("const", int(value))
    _validate_law(law)
    return law


def add_law(left: ImageLawNode, right: ImageLawNode) -> ImageLawNode:
    """Vytvori binarny sucet."""

    law = ImageLawNode("add", None, (left, right))
    _validate_law(law)
    return law


def sub_law(left: ImageLawNode, right: ImageLawNode) -> ImageLawNode:
    """Vytvori binarny rozdiel."""

    law = ImageLawNode("sub", None, (left, right))
    _validate_law(law)
    return law


def avg_law(left: ImageLawNode, right: ImageLawNode) -> ImageLawNode:
    """Vytvori celociselny priemer dvoch podstromov."""

    law = ImageLawNode("avg", None, (left, right))
    _validate_law(law)
    return law


def gradient_law(a: ImageLawNode, b: ImageLawNode, c: ImageLawNode) -> ImageLawNode:
    """Vytvori trojargumentovy gradient zakon a + b - c."""

    law = ImageLawNode("gradient", None, (a, b, c))
    _validate_law(law)
    return law


def mul_small_law(child: ImageLawNode, factor: int) -> ImageLawNode:
    """Vytvori male celociselne nasobenie."""

    law = ImageLawNode("mul_small", int(factor), (child,))
    _validate_law(law)
    return law


def floordiv_pow2_law(child: ImageLawNode, shift: int) -> ImageLawNode:
    """Vytvori floor delenie mocninou dvojky."""

    law = ImageLawNode("floordiv_pow2", int(shift), (child,))
    _validate_law(law)
    return law


def clamp_byte_law(child: ImageLawNode) -> ImageLawNode:
    """Vytvori explicitne byte clampnutie podstromu."""

    law = ImageLawNode("clamp_byte", None, (child,))
    _validate_law(law)
    return law


def mod_const_law(child: ImageLawNode, modulus: int) -> ImageLawNode:
    """Vytvori modulo uzol s malym pevnym delitelom."""

    law = ImageLawNode("mod_const", int(modulus), (child,))
    _validate_law(law)
    return law


def floordiv_const_law(child: ImageLawNode, divisor: int) -> ImageLawNode:
    """Vytvori floor delenie malou pevnou konstantou."""

    law = ImageLawNode("floordiv_const", int(divisor), (child,))
    _validate_law(law)
    return law


def eq_const_law(child: ImageLawNode, constant: int) -> ImageLawNode:
    """Vytvori porovnanie s malou konstantou vracajuce 0 alebo 255."""

    law = ImageLawNode("eq_const", int(constant), (child,))
    _validate_law(law)
    return law


def parity_byte_law(child: ImageLawNode) -> ImageLawNode:
    """Vytvori parity primitive vracajucu 0 alebo 255."""

    law = ImageLawNode("parity_byte", None, (child,))
    _validate_law(law)
    return law


def checker_parity_law(block: int) -> ImageLawNode:
    """Vytvori explicitnu checker primitive nad col a row kontextom."""

    law = ImageLawNode("checker_parity", int(block))
    _validate_law(law)
    return law


def evaluate_image_law(law: ImageLawNode, context: dict[str, int]) -> int:
    """Vyhodnoti zakon nad decoder-znamym kontextom a vrati byte predikciu."""

    _validate_law(law)
    raw_value = _evaluate_raw(law, context)
    return _clamp_byte(raw_value)


def render_image_law(law: ImageLawNode) -> str:
    """Vrati stabilnu citatelnu textualnu podobu zakona."""

    _validate_law(law)

    if law.kind in _TERMINAL_KINDS:
        return law.kind
    if law.kind == "const":
        return f"const({int(law.value or 0)})"
    if law.kind in {"add", "sub", "avg"}:
        left, right = law.children
        return f"{law.kind}({render_image_law(left)}, {render_image_law(right)})"
    if law.kind == "gradient":
        first, second, third = law.children
        return (
            "gradient("
            f"{render_image_law(first)}, "
            f"{render_image_law(second)}, "
            f"{render_image_law(third)})"
        )
    if law.kind == "mul_small":
        return f"mul_small({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "floordiv_pow2":
        return f"floordiv_pow2({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "mod_const":
        return f"mod_const({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "floordiv_const":
        return f"floordiv_const({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "eq_const":
        return f"eq_const({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "parity_byte":
        return f"parity_byte({render_image_law(law.children[0])})"
    if law.kind == "checker_parity":
        return f"checker_parity(block={int(law.value or 0)})"
    if law.kind == "clamp_byte":
        return f"clamp_byte({render_image_law(law.children[0])})"
    raise ValueError(f"Unsupported image law kind: {law.kind}")


def image_law_model_bits(law: ImageLawNode) -> int:
    """Vrati konzervativnu modelovu cenu stromu bez jeho parametrov."""

    _validate_law(law)
    return sum(_NODE_KIND_BITS for _ in _iter_nodes(law))


def image_law_parameter_bits(law: ImageLawNode) -> int:
    """Vrati konzervativnu cenu vsetkych ciselnych parametrov stromu."""

    _validate_law(law)
    total = 0
    for node in _iter_nodes(law):
        if node.kind == "const":
            total += _signed_parameter_bits(int(node.value or 0))
        elif node.kind == "mul_small":
            total += _signed_parameter_bits(int(node.value or 0))
        elif node.kind == "floordiv_pow2":
            total += 1 if int(node.value or 0) == 0 else bits_unsigned_range(int(node.value or 0))
        elif node.kind in {"mod_const", "floordiv_const", "checker_parity"}:
            total += bits_unsigned_range(int(node.value or 0))
        elif node.kind == "eq_const":
            total += bits_unsigned_range(int(node.value or 0))
    return total


def serialize_image_law(law: ImageLawNode) -> dict:
    """Serializuje zakon do research dict payloadu."""

    _validate_law(law)
    return {
        "kind": law.kind,
        "value": law.value,
        "children": [serialize_image_law(child) for child in law.children],
    }


def deserialize_image_law(payload: dict) -> ImageLawNode:
    """Obnovi zakon zo serializovaneho dict payloadu."""

    if not isinstance(payload, dict):
        raise ValueError("image law payload must be a dict")
    kind = payload.get("kind")
    value = payload.get("value")
    children_payload = payload.get("children", [])
    if not isinstance(kind, str):
        raise ValueError("image law kind must be a string")
    if not isinstance(children_payload, list):
        raise ValueError("image law children must be a list")
    children = tuple(deserialize_image_law(child) for child in children_payload)
    law = ImageLawNode(kind, None if value is None else int(value), children)
    _validate_law(law)
    return law


def _evaluate_raw(law: ImageLawNode, context: dict[str, int]) -> int:
    """Vrati neorezanu hodnotu podstromu pred finalnym byte clampom."""

    if law.kind in _TERMINAL_KINDS:
        return _context_value(context, law.kind)
    if law.kind == "const":
        return int(law.value or 0)
    if law.kind == "add":
        return _evaluate_raw(law.children[0], context) + _evaluate_raw(law.children[1], context)
    if law.kind == "sub":
        return _evaluate_raw(law.children[0], context) - _evaluate_raw(law.children[1], context)
    if law.kind == "avg":
        return (_evaluate_raw(law.children[0], context) + _evaluate_raw(law.children[1], context)) // 2
    if law.kind == "gradient":
        return (
            _evaluate_raw(law.children[0], context)
            + _evaluate_raw(law.children[1], context)
            - _evaluate_raw(law.children[2], context)
        )
    if law.kind == "mul_small":
        return _evaluate_raw(law.children[0], context) * int(law.value or 0)
    if law.kind == "floordiv_pow2":
        return _evaluate_raw(law.children[0], context) // (1 << int(law.value or 0))
    if law.kind == "mod_const":
        return _evaluate_raw(law.children[0], context) % int(law.value or 0)
    if law.kind == "floordiv_const":
        return _evaluate_raw(law.children[0], context) // int(law.value or 0)
    if law.kind == "eq_const":
        return 255 if _evaluate_raw(law.children[0], context) == int(law.value or 0) else 0
    if law.kind == "parity_byte":
        return 255 if (_evaluate_raw(law.children[0], context) % 2) == 1 else 0
    if law.kind == "checker_parity":
        block = int(law.value or 0)
        col = _context_value(context, "col")
        row = _context_value(context, "row")
        return 255 if (((col // block) + (row // block)) % 2) else 0
    if law.kind == "clamp_byte":
        return _clamp_byte(_evaluate_raw(law.children[0], context))
    raise ValueError(f"Unsupported image law kind: {law.kind}")


def _context_value(context: dict[str, int], key: str) -> int:
    """Bezpecne vyberie integer zo vstupneho kontextu."""

    if key not in context:
        raise ValueError(f"Missing image context key: {key}")
    value = context[key]
    if not isinstance(value, int):
        raise ValueError(f"Image context value must be an integer: {key}")
    return int(value)


def _validate_law(law: ImageLawNode) -> None:
    """Overi aritu, kind aj parametre uzla."""

    if law.kind not in _NODE_KINDS:
        raise ValueError(f"Unsupported image law kind: {law.kind}")

    arity = len(law.children)
    if law.kind in _TERMINAL_KINDS:
        if law.value is not None or arity != 0:
            raise ValueError(f"Terminal {law.kind} must not have parameters or children")
        return
    if law.kind == "const":
        if not isinstance(law.value, int) or arity != 0:
            raise ValueError("const law requires an integer value and no children")
        return
    if law.kind in {"add", "sub", "avg"}:
        if law.value is not None or arity != 2:
            raise ValueError(f"{law.kind} requires exactly two children")
        return
    if law.kind == "gradient":
        if law.value is not None or arity != 3:
            raise ValueError("gradient requires exactly three children")
        return
    if law.kind == "mul_small":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("mul_small requires one child and an integer factor")
        if int(law.value) < -4 or int(law.value) > 4:
            raise ValueError("mul_small factor must be in range -4..4")
        return
    if law.kind == "floordiv_pow2":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("floordiv_pow2 requires one child and an integer shift")
        if int(law.value) < 0 or int(law.value) > 8:
            raise ValueError("floordiv_pow2 shift must be in range 0..8")
        return
    if law.kind == "mod_const":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("mod_const requires one child and an integer modulus")
        if int(law.value) not in _MOD_DIV_CONST_VALUES:
            raise ValueError(f"mod_const modulus must be one of {_MOD_DIV_CONST_VALUES}")
        return
    if law.kind == "floordiv_const":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("floordiv_const requires one child and an integer divisor")
        if int(law.value) not in _MOD_DIV_CONST_VALUES:
            raise ValueError(f"floordiv_const divisor must be one of {_MOD_DIV_CONST_VALUES}")
        return
    if law.kind == "eq_const":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("eq_const requires one child and an integer constant")
        if int(law.value) not in _EQ_CONST_VALUES:
            raise ValueError(f"eq_const constant must be in range {_EQ_CONST_VALUES[0]}..{_EQ_CONST_VALUES[-1]}")
        return
    if law.kind == "parity_byte":
        if law.value is not None or arity != 1:
            raise ValueError("parity_byte requires exactly one child")
        return
    if law.kind == "checker_parity":
        if not isinstance(law.value, int) or arity != 0:
            raise ValueError("checker_parity requires a block parameter and no children")
        if int(law.value) not in _CHECKER_BLOCKS:
            raise ValueError(f"checker_parity block must be one of {_CHECKER_BLOCKS}")
        return
    if law.kind == "clamp_byte":
        if law.value is not None or arity != 1:
            raise ValueError("clamp_byte requires exactly one child")
        return


def _iter_nodes(law: ImageLawNode):
    """Prejde cely strom v preorder poradi."""

    yield law
    for child in law.children:
        yield from _iter_nodes(child)


def _signed_parameter_bits(value: int) -> int:
    """Vrati konzervativny pocet bitov pre jedno podpisane cele cislo."""

    if value == 0:
        return 1
    return 1 + bits_unsigned_range(abs(int(value)))


def _clamp_byte(value: int) -> int:
    """Oreze lubovolne cele cislo na grayscale rozsah 0..255."""

    return max(0, min(255, int(value)))
```

## File: `src/primesymbolicmdl/image_datasets.py`

```python
"""Male generovane grayscale datasety bez externych kniznic."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class GrayImage:
    """Jednoducha grayscale reprezentacia obrazka."""

    name: str
    width: int
    height: int
    pixels: bytes


def make_gray_image(name: str, width: int, height: int, pixels: bytes) -> GrayImage:
    """Vytvori grayscale obrazok aj pre externe nacitane pixely."""

    return _image(name, width, height, bytes(pixels))


def make_gradient_image(width: int = 32, height: int = 32) -> GrayImage:
    """Vrati vodorovny gradient od ciernej po bielu."""

    pixels = bytes(
        _scale_255(x, max(1, width - 1))
        for _y in range(height)
        for x in range(width)
    )
    return _image("gradient", width, height, pixels)


def make_checker_image(width: int = 32, height: int = 32, block: int = 4) -> GrayImage:
    """Vrati sachovnicovy grayscale obrazok."""

    if block <= 0:
        raise ValueError("block must be positive")
    pixels = bytes(
        255 if ((x // block) + (y // block)) % 2 else 0
        for y in range(height)
        for x in range(width)
    )
    return _image("checker", width, height, pixels)


def make_diagonal_ramp_image(width: int = 32, height: int = 32) -> GrayImage:
    """Vrati diagonaly grayscale ramp."""

    scale = max(1, (width - 1) + (height - 1))
    pixels = bytes(
        _scale_255(x + y, scale)
        for y in range(height)
        for x in range(width)
    )
    return _image("diagonal_ramp", width, height, pixels)


def make_noise_image(width: int = 32, height: int = 32, seed: int = 1234) -> GrayImage:
    """Vrati deterministicky sumovy grayscale obrazok."""

    rng = Random(seed)
    pixels = bytes(rng.randrange(256) for _ in range(width * height))
    return _image("noise", width, height, pixels)


def get_image_dataset_names() -> list[str]:
    """Vrati stabilny zoznam mien obrazkovych datasetov."""

    return ["gradient", "checker", "diagonal_ramp", "noise"]


def make_image_dataset(name: str, width: int, height: int, seed: int = 1234) -> GrayImage:
    """Vytvori obrazok podla mena datasetu."""

    if name == "gradient":
        return make_gradient_image(width, height)
    if name == "checker":
        return make_checker_image(width, height)
    if name == "diagonal_ramp":
        return make_diagonal_ramp_image(width, height)
    if name == "noise":
        return make_noise_image(width, height, seed)
    raise ValueError(f"Unknown image dataset: {name}")


def _image(name: str, width: int, height: int, pixels: bytes) -> GrayImage:
    """Overi rozmery a vrati immutable objekt obrazka."""

    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if len(pixels) != width * height:
        raise ValueError("pixel count does not match image size")
    return GrayImage(name=name, width=width, height=height, pixels=pixels)


def _scale_255(value: int, max_value: int) -> int:
    """Preskaluje integer do rozsahu 0..255."""

    return (255 * value) // max_value
```

## File: `src/primesymbolicmdl/image_law_branch.py`

```python
"""Lossless 2D image-law branch nad decoder-znamym pixel kontextom."""

from __future__ import annotations

import math

from .image_context_laws import (
    ImageLawNode,
    deserialize_image_law,
    evaluate_image_law,
    image_law_model_bits,
    image_law_parameter_bits,
    render_image_law,
    serialize_image_law,
)
from .image_datasets import GrayImage
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
)

_HEADER_BITS = 64


def estimate_image_law_cost(image: GrayImage, law: ImageLawNode) -> dict:
    """Odhadne cenu image-law vetvy pre konkretny grayscale obrazok."""

    trace = build_image_law_trace(image, law)
    raw_bits = image.width * image.height * 8
    model_bits = image_law_model_bits(law)
    parameter_bits = image_law_parameter_bits(law)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    residual_bits = residual_codec.bits
    residual_width = signed_width_for_range(trace["min_residual"], trace["max_residual"])
    total_bits = _HEADER_BITS + model_bits + parameter_bits + residual_bits
    saving_bits = raw_bits - total_bits
    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _HEADER_BITS,
        "residual_bits": residual_bits,
        "residual_width": residual_width,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "pixel_count": trace["pixel_count"],
        "model": law,
    }


def encode_image_law_payload(image: GrayImage, law: ImageLawNode) -> dict:
    """Zakoduje obrazok cez 2D expression-law prediktor."""

    trace = build_image_law_trace(image, law)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    return {
        "codec": "image_law",
        "width": image.width,
        "height": image.height,
        "law": serialize_image_law(law),
        "residual_codec": residual_codec.codec_name,
        "residual_payload": residual_codec.payload,
        "metadata": {
            "estimated_costs": estimate_image_law_cost(image, law),
            "model_string": render_image_law(law),
            "experimental": True,
        },
    }


def decode_image_law_payload(payload: dict) -> bytes:
    """Dekoduje payload iba z law modelu, rozmerov a residual streamu."""

    width = payload.get("width")
    height = payload.get("height")
    law_payload = payload.get("law")
    residual_codec = payload.get("residual_codec")
    residual_payload = payload.get("residual_payload")
    explicit_residuals = payload.get("residuals")

    if payload.get("codec") not in {None, "image_law"}:
        raise ValueError("Unsupported image law codec")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")

    law = deserialize_image_law(law_payload)
    residuals = _decode_residual_stream(residual_codec, residual_payload, explicit_residuals)
    if len(residuals) != width * height:
        raise ValueError("residual count does not match image size")

    decoded: list[int] = []
    for index, residual in enumerate(residuals):
        if not isinstance(residual, int):
            raise ValueError("residuals must contain integers")
        row = index // width
        col = index % width
        context = _build_context(decoded, col, row, width, height)
        prediction = evaluate_image_law(law, context)
        value = prediction + residual
        if value < 0 or value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        decoded.append(value)

    return bytes(decoded)


def roundtrip_image_law(image: GrayImage, law: ImageLawNode) -> bytes:
    """Zakoduje a spatne dekoduje obrazok bez straty informacie."""

    return decode_image_law_payload(encode_image_law_payload(image, law))


def build_image_law_trace(image: GrayImage, law: ImageLawNode) -> dict:
    """Vrati predikovane pixely, rezidua a decoded kontrolu pre obrazok."""

    predicted: list[int] = []
    residuals: list[int] = []
    decoded: list[int] = []

    for index, original in enumerate(image.pixels):
        row = index // image.width
        col = index % image.width
        context = _build_context(decoded, col, row, image.width, image.height)
        prediction = evaluate_image_law(law, context)
        residual = int(original) - prediction
        decoded_value = prediction + residual
        if decoded_value < 0 or decoded_value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        predicted.append(prediction)
        residuals.append(residual)
        decoded.append(decoded_value)

    min_residual = min(residuals, default=0)
    max_residual = max(residuals, default=0)
    return {
        "predicted_pixels": bytes(predicted),
        "residuals": residuals,
        "decoded_pixels": bytes(decoded),
        "min_residual": min_residual,
        "max_residual": max_residual,
        "pixel_count": len(image.pixels),
        "model_string": render_image_law(law),
    }


def _build_context(decoded: list[int], col: int, row: int, width: int, height: int) -> dict[str, int]:
    """Posklada decoder-znamy 2D kontext bez pristupu k aktualnemu pixelu."""

    left = decoded[-1] if col > 0 else 0
    up = decoded[(row - 1) * width + col] if row > 0 else 0
    up_left = decoded[(row - 1) * width + col - 1] if row > 0 and col > 0 else 0
    return {
        "col": col,
        "row": row,
        "width": width,
        "height": height,
        "left": left,
        "up": up,
        "up_left": up_left,
        "x_ramp": (255 * col) // max(1, width - 1),
        "y_ramp": (255 * row) // max(1, height - 1),
        "diag_ramp": (255 * (col + row)) // max(1, width + height - 2),
    }


def _decode_residual_stream(
    residual_codec: object,
    residual_payload: object,
    explicit_residuals: object,
) -> list[int]:
    """Dekoduje residual stream z codec payloadu alebo zo starsieho fallback pola."""

    if isinstance(explicit_residuals, list):
        if not all(isinstance(value, int) for value in explicit_residuals):
            raise ValueError("residuals must contain integers")
        return [int(value) for value in explicit_residuals]

    if not isinstance(residual_codec, str):
        raise ValueError("residual_codec must be a string")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")

    if residual_codec == "fixed_signed":
        return decode_fixed_signed_residual_payload(residual_payload)
    if residual_codec == "zero_rle":
        return decode_zero_rle_residual_payload(residual_payload)
    raise ValueError(f"Unsupported residual codec: {residual_codec}")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer total_bits voci raw_bits."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
```

## File: `src/primesymbolicmdl/image_predictor_branch.py`

```python
"""Lossless 2D predictor branch pre grayscale obrazky."""

from __future__ import annotations

import math

from .image_datasets import GrayImage
from .image_predictors import (
    ImagePredictorModel,
    image_predictor_model_bits,
    image_predictor_parameter_bits,
    predict_pixel,
    render_image_predictor,
)
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
)

_HEADER_BITS = 64


def estimate_image_predictor_cost(image: GrayImage, model: ImagePredictorModel) -> dict:
    """Odhadne cenu 2D predictor vetvy pre konkretny grayscale obrazok."""

    trace = build_image_predictor_trace(image, model)
    raw_bits = image.width * image.height * 8
    model_bits = image_predictor_model_bits(model)
    parameter_bits = image_predictor_parameter_bits(model)
    residual_width = signed_width_for_range(trace["min_residual"], trace["max_residual"])
    residual_codec = choose_best_residual_codec(trace["residuals"])
    residual_bits = residual_codec.bits
    total_bits = _HEADER_BITS + model_bits + parameter_bits + residual_bits
    saving_bits = raw_bits - total_bits
    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _HEADER_BITS,
        "residual_bits": residual_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "residual_width": residual_width,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "pixel_count": trace["pixel_count"],
        "model": model,
    }


def encode_image_predictor_payload(image: GrayImage, model: ImagePredictorModel) -> dict:
    """Zakoduje obrazok cez 2D prediktor a ulozi rezidua."""

    trace = build_image_predictor_trace(image, model)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    return {
        "codec": "image_predictor",
        "width": image.width,
        "height": image.height,
        "model_name": model.name,
        "model_params": dict(model.params),
        "residual_codec": residual_codec.codec_name,
        "residual_payload": residual_codec.payload,
        "metadata": {
            "estimated_costs": estimate_image_predictor_cost(image, model),
            "experimental": True,
        },
    }


def decode_image_predictor_payload(payload: dict) -> bytes:
    """Dekoduje lossless payload iba z modelu, rozmerov a rezidui."""

    width = payload.get("width")
    height = payload.get("height")
    model_name = payload.get("model_name")
    model_params = payload.get("model_params", {})
    residual_codec = payload.get("residual_codec")
    residual_payload = payload.get("residual_payload")
    explicit_residuals = payload.get("residuals")

    if payload.get("codec") not in {None, "image_predictor"}:
        raise ValueError("Unsupported image predictor codec")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")
    if not isinstance(model_name, str):
        raise ValueError("model_name must be a string")
    if not isinstance(model_params, dict):
        raise ValueError("model_params must be a dict")

    model = ImagePredictorModel(model_name, {str(key): int(value) for key, value in model_params.items()})
    residuals = _decode_residual_stream(residual_codec, residual_payload, explicit_residuals)
    if len(residuals) != width * height:
        raise ValueError("residual count does not match image size")
    decoded: list[int] = []

    for index, residual in enumerate(residuals):
        if not isinstance(residual, int):
            raise ValueError("residuals must contain integers")
        row = index // width
        col = index % width
        left = decoded[index - 1] if col > 0 else 0
        up = decoded[index - width] if row > 0 else 0
        up_left = decoded[index - width - 1] if row > 0 and col > 0 else 0
        prediction = predict_pixel(model, col, row, width, height, left, up, up_left)
        value = prediction + residual
        if value < 0 or value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        decoded.append(value)

    return bytes(decoded)


def roundtrip_image_predictor(image: GrayImage, model: ImagePredictorModel) -> bytes:
    """Zakoduje a spatne dekoduje obrazok bez straty informacie."""

    return decode_image_predictor_payload(encode_image_predictor_payload(image, model))


def build_image_predictor_trace(image: GrayImage, model: ImagePredictorModel) -> dict:
    """Vrati predikovane pixely, rezidua a decoded kontrolu pre obrazok."""

    predicted: list[int] = []
    residuals: list[int] = []
    decoded: list[int] = []

    for index, original in enumerate(image.pixels):
        row = index // image.width
        col = index % image.width
        left = decoded[index - 1] if col > 0 else 0
        up = decoded[index - image.width] if row > 0 else 0
        up_left = decoded[index - image.width - 1] if row > 0 and col > 0 else 0
        prediction = predict_pixel(model, col, row, image.width, image.height, left, up, up_left)
        residual = int(original) - prediction
        decoded_value = prediction + residual
        if decoded_value < 0 or decoded_value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        predicted.append(prediction)
        residuals.append(residual)
        decoded.append(decoded_value)

    min_residual = min(residuals, default=0)
    max_residual = max(residuals, default=0)
    return {
        "predicted_pixels": bytes(predicted),
        "residuals": residuals,
        "decoded_pixels": bytes(decoded),
        "min_residual": min_residual,
        "max_residual": max_residual,
        "pixel_count": len(image.pixels),
        "model_string": render_image_predictor(model),
    }

def _decode_residual_stream(
    residual_codec: object,
    residual_payload: object,
    explicit_residuals: object,
) -> list[int]:
    """Dekoduje residual stream z codec payloadu alebo zo starsieho fallback pola."""

    if isinstance(explicit_residuals, list):
        if not all(isinstance(value, int) for value in explicit_residuals):
            raise ValueError("residuals must contain integers")
        return [int(value) for value in explicit_residuals]

    if not isinstance(residual_codec, str):
        raise ValueError("residual_codec must be a string")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")

    if residual_codec == "fixed_signed":
        return decode_fixed_signed_residual_payload(residual_payload)
    if residual_codec == "zero_rle":
        return decode_zero_rle_residual_payload(residual_payload)
    raise ValueError(f"Unsupported residual codec: {residual_codec}")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer total_bits voci raw_bits."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
```

## File: `src/primesymbolicmdl/image_predictors.py`

```python
"""Deterministicke 2D prediktory pre grayscale obrazky."""

from __future__ import annotations

from dataclasses import dataclass, field

from .bitcost import bits_unsigned_range

_CHECKER_BLOCKS = (1, 2, 4, 8, 16)
_MODEL_NAMES = (
    "zero",
    "left",
    "up",
    "avg_left_up",
    "gradient",
    "x_ramp",
    "y_ramp",
    "diagonal_ramp",
    "checker",
)
_MODEL_BITS = bits_unsigned_range(len(_MODEL_NAMES) - 1)


@dataclass(frozen=True)
class ImagePredictorModel:
    """Malý nemenny popis jedneho obrazkoveho prediktora."""

    name: str
    params: dict[str, int] = field(default_factory=dict)


def predict_pixel(
    model: ImagePredictorModel,
    col: int,
    row: int,
    width: int,
    height: int,
    left: int,
    up: int,
    up_left: int,
) -> int:
    """Vrati predikovanu hodnotu pixelu iba z decoder-znameho kontextu."""

    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    _validate_model(model)

    if model.name == "zero":
        value = 0
    elif model.name == "left":
        value = left
    elif model.name == "up":
        value = up
    elif model.name == "avg_left_up":
        value = (left + up) // 2
    elif model.name == "gradient":
        value = left + up - up_left
    elif model.name == "x_ramp":
        value = (255 * col) // max(1, width - 1)
    elif model.name == "y_ramp":
        value = (255 * row) // max(1, height - 1)
    elif model.name == "diagonal_ramp":
        value = (255 * (col + row)) // max(1, width + height - 2)
    elif model.name == "checker":
        block = int(model.params["block"])
        value = 255 if ((col // block) + (row // block)) % 2 else 0
    else:
        raise ValueError(f"Unknown image predictor: {model.name}")

    return _clamp_byte(value)


def default_image_predictor_models() -> list[ImagePredictorModel]:
    """Vrati stabilny zoznam malych baseline obrazkovych prediktorov."""

    models = [
        ImagePredictorModel("zero"),
        ImagePredictorModel("left"),
        ImagePredictorModel("up"),
        ImagePredictorModel("avg_left_up"),
        ImagePredictorModel("gradient"),
        ImagePredictorModel("x_ramp"),
        ImagePredictorModel("y_ramp"),
        ImagePredictorModel("diagonal_ramp"),
    ]
    models.extend(ImagePredictorModel("checker", {"block": block}) for block in _CHECKER_BLOCKS)
    return models


def render_image_predictor(model: ImagePredictorModel) -> str:
    """Vrati stabilnu textualnu reprezentaciu modelu."""

    _validate_model(model)
    if not model.params:
        return model.name
    params = ", ".join(f"{key}={model.params[key]}" for key in sorted(model.params))
    return f"{model.name}({params})"


def image_predictor_model_bits(model: ImagePredictorModel) -> int:
    """Vrati konzervativnu cenu identifikatora rodiny modelu."""

    _validate_model(model)
    return _MODEL_BITS


def image_predictor_parameter_bits(model: ImagePredictorModel) -> int:
    """Vrati konzervativnu cenu ciselnych parametrov modelu."""

    _validate_model(model)
    total = 0
    for key in sorted(model.params):
        value = int(model.params[key])
        if value < 0:
            total += 1 + bits_unsigned_range(abs(value))
        else:
            total += bits_unsigned_range(value)
    return total


def _validate_model(model: ImagePredictorModel) -> None:
    """Overi, ze model patri medzi podporovane prediktory."""

    if model.name not in _MODEL_NAMES:
        raise ValueError(f"Unknown image predictor: {model.name}")

    params = dict(model.params)
    if model.name == "checker":
        if set(params) != {"block"}:
            raise ValueError("checker predictor requires exactly one 'block' parameter")
        block = int(params["block"])
        if block not in _CHECKER_BLOCKS:
            raise ValueError(f"Unsupported checker block: {block}")
        return

    if params:
        raise ValueError(f"Predictor {model.name} does not accept parameters")


def _clamp_byte(value: int) -> int:
    """Oreze hodnotu na 8-bitovy grayscale rozsah."""

    return max(0, min(255, int(value)))
```

## File: `src/primesymbolicmdl/index_branch.py`

```python
"""Indexova vetva pre zakon A(i) plus reziduum."""

from __future__ import annotations

import math

from .anchor_laws import LawNode, anchor_value, law_model_bits, law_parameter_bits, render_law
from .bitcost import bits_raw, bits_unsigned_range
from .blocks import SUPPORTED_WIDTHS, bytes_to_uint_blocks, uint_blocks_to_bytes
from .residual_codecs import choose_best_residual_codec

_FIXED_HEADER_BITS = 32


def encode_block_with_law(x: int, law, max_index: int, strict_lower: bool = False) -> dict:
    """Najde najlepsi index pre anchor zakon alebo vrati escape."""

    if x < 0:
        raise ValueError("x must be non-negative")
    if max_index < 0:
        raise ValueError("max_index must be non-negative")

    best: tuple[int, int, int] | None = None

    for index in range(max_index + 1):
        anchor = _anchor_from_law(law, index)
        if not _is_valid_anchor(anchor, x, strict_lower):
            continue

        residual = x - anchor
        candidate = (residual, -anchor, index)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return {
            "index": None,
            "anchor": 0,
            "residual": x,
            "escaped": True,
        }

    residual, negative_anchor, index = best
    return {
        "index": index,
        "anchor": -negative_anchor,
        "residual": residual,
        "escaped": False,
    }


def estimate_law_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    law,
    max_index: int,
    strict_lower: bool = False,
) -> dict:
    """Spocita odhad ceny indexovej vetvy pre zadany anchor zakon."""

    if width_bits not in SUPPORTED_WIDTHS:
        raise ValueError(f"Unsupported block width: {width_bits}")
    if original_size < 0:
        raise ValueError("original_size must be non-negative")
    if max_index < 0:
        raise ValueError("max_index must be non-negative")

    upper_bound = 1 << width_bits
    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")

    for block in blocks:
        if block < 0 or block >= upper_bound:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")

    raw_bits = bits_raw(original_size)
    block_count = len(blocks)
    flag_bits = block_count
    encoded_blocks = [encode_block_with_law(block, law, max_index, strict_lower) for block in blocks]

    used_indices = [entry["index"] for entry in encoded_blocks if not entry["escaped"]]
    residuals = [entry["residual"] for entry in encoded_blocks if not entry["escaped"]]
    escape_count = sum(1 for entry in encoded_blocks if entry["escaped"])

    if used_indices:
        index_width = bits_unsigned_range(max(int(index) for index in used_indices))
        index_bits = index_width * len(used_indices)
    else:
        index_bits = 0

    residual_codec = choose_best_residual_codec([int(value) for value in residuals])
    residual_bits = residual_codec.bits

    model_bits = _law_model_bits(law)
    parameter_bits = _law_parameter_bits(law)
    escape_bits = width_bits * escape_count
    total_bits = (
        model_bits
        + parameter_bits
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )
    saving_bits = raw_bits - total_bits

    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "block_count": block_count,
        "max_index": max_index,
        "strict_lower": strict_lower,
        "law": _render_law(law),
    }


def roundtrip_law_payload(
    data: bytes,
    width_bits: int,
    law,
    max_index: int,
    strict_lower: bool = False,
) -> bytes:
    """Zakoduje a spatne dekoduje data cez law branch bez straty informacie."""

    blocks = bytes_to_uint_blocks(bytes(data), width_bits)
    decoded_blocks: list[int] = []

    for block in blocks:
        encoded = encode_block_with_law(block, law, max_index, strict_lower)
        if encoded["escaped"]:
            decoded_blocks.append(int(encoded["residual"]))
            continue

        index = encoded["index"]
        if index is None:
            raise ValueError("Non-escaped block must have an index")
        anchor = _anchor_from_law(law, int(index))
        decoded_blocks.append(anchor + int(encoded["residual"]))

    return uint_blocks_to_bytes(decoded_blocks, width_bits, len(data))


def _is_valid_anchor(anchor: int, x: int, strict_lower: bool) -> bool:
    """Overi platnost anchoru pre konkretny blok."""

    if strict_lower:
        return 0 <= anchor < x
    return 0 <= anchor <= x


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer ceny law vetvy voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits


def _anchor_from_law(law, index: int) -> int:
    """Vrati anchor z GP-lite stromu alebo z ineho kompatibilneho modelu."""

    if isinstance(law, LawNode):
        return anchor_value(law, index)
    if hasattr(law, "anchor_at"):
        return int(law.anchor_at(index))
    raise TypeError("Unsupported law object for anchor evaluation")


def _law_model_bits(law) -> int:
    """Vrati modelovu cenu zakona alebo kompatibilneho modelu."""

    if isinstance(law, LawNode):
        return law_model_bits(law)
    if hasattr(law, "model_bits"):
        return int(law.model_bits())
    raise TypeError("Unsupported law object for model bit accounting")


def _law_parameter_bits(law) -> int:
    """Vrati parameter bit cost zakona alebo kompatibilneho modelu."""

    if isinstance(law, LawNode):
        return law_parameter_bits(law)
    if hasattr(law, "parameter_bits"):
        return int(law.parameter_bits())
    raise TypeError("Unsupported law object for parameter bit accounting")


def _render_law(law) -> str:
    """Vrati stabilnu textualnu reprezentaciu zakona alebo modelu."""

    if isinstance(law, LawNode):
        return render_law(law)
    if hasattr(law, "render"):
        return str(law.render())
    raise TypeError("Unsupported law object for rendering")
```

## File: `src/primesymbolicmdl/__init__.py`

```python
"""Minimalny verejny povrch pre experimentalny codec."""

from .codec import compress_experimental, decompress_experimental

__all__ = ["compress_experimental", "decompress_experimental"]
```

## File: `src/primesymbolicmdl/law_demo.py`

```python
"""Maly CLI demo beh GP-lite searchu nad zakonmi A(i)."""

from __future__ import annotations

from .experiments import dataset_ramp_u16
from .law_search import search_best_law_for_bytes


def run_demo() -> dict:
    """Spusti maly deterministicky demo search a vrati vysledok."""

    data = dataset_ramp_u16(32)
    result = search_best_law_for_bytes(
        data,
        width_bits=16,
        seed=1234,
        population_size=24,
        generations=10,
        max_depth=4,
        max_index=31,
        strict_lower=False,
    )
    return {
        "dataset_name": "ramp_u16_32",
        "result": result,
    }


def main() -> None:
    """Vypise kratke zhrnutie demo behu."""

    demo = run_demo()
    result = demo["result"]
    print(f"dataset: {demo['dataset_name']}")
    print(f"raw_bits: {result['raw_bits']}")
    print(f"best_total_bits: {result['total_bits']}")
    print(f"saving_bits: {result['saving_bits']}")
    print(f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}")
    print(f"best_law: {result['best_law_string']}")
    print(f"max_index: {result['max_index']}")
    print("history:")
    for item in result["history"][:5]:
        print(
            f"  gen={item['generation']} total_bits={item['total_bits']} "
            f"saving_bits={item['saving_bits']} law={item['best_law']}"
        )


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/law_search.py`

```python
"""Male deterministicke GP-lite hladanie anchor zakonov A(i)."""

from __future__ import annotations

from random import Random

from .anchor_laws import (
    LawNode,
    add_law,
    clamp_nonnegative_law,
    const_law,
    floordiv_pow2_law,
    idx_law,
    mul_small_law,
    render_law,
    square_law,
    sub_law,
)
from .blocks import bytes_to_uint_blocks
from .index_branch import estimate_law_cost


def search_best_law_for_bytes(
    data: bytes,
    width_bits: int = 16,
    seed: int = 1234,
    population_size: int = 64,
    generations: int = 40,
    max_depth: int = 4,
    max_index: int | None = None,
    strict_lower: bool = False,
) -> dict:
    """Spusti male deterministicke GP-lite hladanie nad zakonmi A(i)."""

    payload = bytes(data)
    blocks = bytes_to_uint_blocks(payload, width_bits)
    resolved_max_index = _resolve_max_index(blocks, max_index)
    rng = Random(seed)

    population = _seed_population(max_depth)
    attempts = 0
    while len(population) < population_size and attempts < population_size * 20:
        candidate = _random_law(rng, max_depth)
        population[_law_key(candidate)] = candidate
        attempts += 1

    history: list[dict] = []
    best_law: LawNode | None = None
    best_cost: dict | None = None

    for generation_index in range(generations):
        scored = _score_population(
            list(population.values()),
            blocks,
            width_bits,
            len(payload),
            resolved_max_index,
            strict_lower,
        )
        best_law = scored[0]["law"]
        best_cost = scored[0]["cost"]
        history.append(
            {
                "generation": generation_index,
                "best_law": render_law(best_law),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
            }
        )

        elite_count = max(2, min(len(scored), population_size // 8 or 1))
        next_population = {
            _law_key(item["law"]): item["law"]
            for item in scored[:elite_count]
        }

        fill_attempts = 0
        while len(next_population) < population_size and fill_attempts < population_size * 40:
            parent = _tournament_select(scored, rng)
            if rng.random() < 0.35:
                donor = _tournament_select(scored, rng)
                child = _crossover_laws(parent["law"], donor["law"], rng, max_depth)
            else:
                child = _mutate_law(parent["law"], rng, max_depth)
            next_population[_law_key(child)] = child
            fill_attempts += 1

        extra_attempts = 0
        while len(next_population) < population_size and extra_attempts < population_size * 20:
            extra = _random_law(rng, max_depth)
            next_population[_law_key(extra)] = extra
            extra_attempts += 1

        population = next_population

    if best_law is None or best_cost is None:
        raise RuntimeError("Law search did not produce a best candidate")

    return {
        "best_law": best_law,
        "best_law_string": render_law(best_law),
        "best_cost": best_cost,
        "raw_bits": best_cost["raw_bits"],
        "total_bits": best_cost["total_bits"],
        "saving_bits": best_cost["saving_bits"],
        "ratio_vs_raw": best_cost["ratio_vs_raw"],
        "generations": generations,
        "population_size": population_size,
        "seed": seed,
        "history": history,
        "max_index": resolved_max_index,
        "strict_lower": strict_lower,
    }


def _resolve_max_index(blocks: list[int], max_index: int | None) -> int:
    """Vrati maly predvoleny limit indexu pre rychly lokalny search."""

    if max_index is not None:
        if max_index < 0:
            raise ValueError("max_index must be non-negative")
        return max_index
    if not blocks:
        return 0
    return min(31, max(blocks))


def _seed_population(max_depth: int) -> dict[str, LawNode]:
    """Vrati malu sadu rozumnych startovacich zakonov."""

    laws = [
        idx_law(),
        const_law(0),
        const_law(1),
        add_law(idx_law(), const_law(1)),
        sub_law(idx_law(), const_law(1)),
        mul_small_law(idx_law(), 2),
        floordiv_pow2_law(idx_law(), 1),
        square_law(idx_law()),
        clamp_nonnegative_law(sub_law(idx_law(), const_law(1))),
    ]
    return {_law_key(_prune_law(law, max_depth)): _prune_law(law, max_depth) for law in laws}


def _score_population(
    population: list[LawNode],
    blocks: list[int],
    width_bits: int,
    original_size: int,
    max_index: int,
    strict_lower: bool,
) -> list[dict]:
    """Ohodnoti populaciu podla total_bits a stabilne ju utriedi."""

    scored = []
    for law in population:
        cost = estimate_law_cost(blocks, width_bits, original_size, law, max_index, strict_lower)
        scored.append({"law": law, "cost": cost, "law_string": render_law(law)})

    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return scored


def _tournament_select(scored: list[dict], rng: Random, size: int = 3) -> dict:
    """Vyberie rodica cez maly turnaj."""

    sample_size = min(size, len(scored))
    candidates = rng.sample(scored, sample_size)
    candidates.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return candidates[0]


def _random_law(rng: Random, max_depth: int) -> LawNode:
    """Vygeneruje nahodny zakon malej hlbky."""

    if max_depth <= 0 or rng.random() < 0.3:
        return _random_terminal(rng)

    choice = rng.choice(("add", "sub", "mul_small", "floordiv_pow2", "square", "clamp_nonnegative"))
    if choice == "add":
        return add_law(_random_law(rng, max_depth - 1), _random_law(rng, max_depth - 1))
    if choice == "sub":
        return sub_law(_random_law(rng, max_depth - 1), _random_law(rng, max_depth - 1))
    if choice == "mul_small":
        return mul_small_law(_random_law(rng, max_depth - 1), rng.randint(1, 8))
    if choice == "floordiv_pow2":
        return floordiv_pow2_law(_random_law(rng, max_depth - 1), rng.randint(0, 4))
    if choice == "square":
        return square_law(_random_law(rng, max_depth - 1))
    return clamp_nonnegative_law(_random_law(rng, max_depth - 1))


def _random_terminal(rng: Random) -> LawNode:
    """Vygeneruje terminal idx alebo malu konstantu."""

    if rng.random() < 0.5:
        return idx_law()
    return const_law(rng.randint(-8, 16))


def _mutate_law(law: LawNode, rng: Random, max_depth: int) -> LawNode:
    """Aplikuje malu deterministicku mutaciu podstromu."""

    paths = _subtree_paths(law)
    target_path = rng.choice(paths)
    target = _get_subtree(law, target_path)
    mode = rng.choice(("replace", "wrap", "tweak"))

    if mode == "replace":
        replacement = _random_law(rng, 2)
    elif mode == "wrap":
        replacement = _wrap_subtree(target, rng)
    else:
        replacement = _tweak_subtree(target, rng)

    return _prune_law(_replace_subtree(law, target_path, replacement), max_depth)


def _crossover_laws(left: LawNode, right: LawNode, rng: Random, max_depth: int) -> LawNode:
    """Zlozi dieta nahradenim podstromu darcovskym podstromom."""

    left_path = rng.choice(_subtree_paths(left))
    right_subtree = _get_subtree(right, rng.choice(_subtree_paths(right)))
    return _prune_law(_replace_subtree(left, left_path, right_subtree), max_depth)


def _wrap_subtree(law: LawNode, rng: Random) -> LawNode:
    """Obali podstrom jednoduchym operatorom."""

    choice = rng.choice(("add", "sub", "mul_small", "floordiv_pow2", "square", "clamp_nonnegative"))
    if choice == "add":
        return add_law(law, _random_terminal(rng))
    if choice == "sub":
        return sub_law(law, _random_terminal(rng))
    if choice == "mul_small":
        return mul_small_law(law, rng.randint(1, 8))
    if choice == "floordiv_pow2":
        return floordiv_pow2_law(law, rng.randint(0, 4))
    if choice == "square":
        return square_law(law)
    return clamp_nonnegative_law(law)


def _tweak_subtree(law: LawNode, rng: Random) -> LawNode:
    """Jemne upravi operator alebo jeho parameter."""

    if law.kind == "idx":
        return const_law(rng.randint(-4, 8))
    if law.kind == "const":
        return const_law(int(law.value or 0) + rng.choice((-3, -1, 1, 3)))
    if law.kind == "mul_small":
        return mul_small_law(_require_left(law), max(1, int(law.value or 1) + rng.choice((-2, -1, 1, 2))))
    if law.kind == "floordiv_pow2":
        return floordiv_pow2_law(_require_left(law), min(8, max(0, int(law.value or 0) + rng.choice((-1, 1)))))
    if law.kind == "add":
        return sub_law(_require_left(law), _require_right(law))
    if law.kind == "sub":
        return add_law(_require_left(law), _require_right(law))
    if law.kind == "square":
        return clamp_nonnegative_law(_require_left(law))
    if law.kind == "clamp_nonnegative":
        return square_law(_require_left(law))
    return law


def _subtree_paths(law: LawNode, prefix: tuple[int, ...] = ()) -> list[tuple[int, ...]]:
    """Vrati vsetky cesty k podstromom."""

    paths = [prefix]
    if law.left is not None:
        paths.extend(_subtree_paths(law.left, prefix + (0,)))
    if law.right is not None:
        paths.extend(_subtree_paths(law.right, prefix + (1,)))
    return paths


def _get_subtree(law: LawNode, path: tuple[int, ...]) -> LawNode:
    """Vrati podstrom na zadanej ceste."""

    node = law
    for step in path:
        if step == 0:
            node = _require_left(node)
        else:
            node = _require_right(node)
    return node


def _replace_subtree(law: LawNode, path: tuple[int, ...], replacement: LawNode) -> LawNode:
    """Vrati novy strom s nahradenym podstromom."""

    if not path:
        return replacement

    step = path[0]
    if step == 0:
        return LawNode(law.kind, law.value, _replace_subtree(_require_left(law), path[1:], replacement), law.right)
    return LawNode(law.kind, law.value, law.left, _replace_subtree(_require_right(law), path[1:], replacement))


def _prune_law(law: LawNode, max_depth: int) -> LawNode:
    """Oreze strom na povolenu hlbku, aby search ostal maly."""

    if max_depth <= 0:
        if law.kind == "const":
            return law
        return idx_law()

    if law.kind in {"idx", "const"}:
        return law
    if law.kind == "add":
        return add_law(_prune_law(_require_left(law), max_depth - 1), _prune_law(_require_right(law), max_depth - 1))
    if law.kind == "sub":
        return sub_law(_prune_law(_require_left(law), max_depth - 1), _prune_law(_require_right(law), max_depth - 1))
    if law.kind == "mul_small":
        return mul_small_law(_prune_law(_require_left(law), max_depth - 1), max(1, int(law.value or 1)))
    if law.kind == "floordiv_pow2":
        return floordiv_pow2_law(_prune_law(_require_left(law), max_depth - 1), min(8, max(0, int(law.value or 0))))
    if law.kind == "square":
        return square_law(_prune_law(_require_left(law), max_depth - 1))
    if law.kind == "clamp_nonnegative":
        return clamp_nonnegative_law(_prune_law(_require_left(law), max_depth - 1))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def _law_key(law: LawNode) -> str:
    """Vrati stabilny kluc pre deduplikaciu populacie."""

    return render_law(law)


def _require_left(law: LawNode) -> LawNode:
    """Overi pritomnost laveho potomka."""

    if law.left is None:
        raise ValueError("law node is missing a left child")
    return law.left


def _require_right(law: LawNode) -> LawNode:
    """Overi pritomnost praveho potomka."""

    if law.right is None:
        raise ValueError("law node is missing a right child")
    return law.right
```

## File: `src/primesymbolicmdl/optimizers/base.py`

```python
"""Zakladne typy pre spustanie optimizerov."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class OptimizerRequest:
    """Vstupne nastavenia jedneho optimalizacneho behu."""

    data: bytes
    width_bits: int
    seed: int
    population_size: int
    generations: int
    max_index: int | None
    strict_lower: bool
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class OptimizerResult:
    """Stabilne zhrnutie vysledku optimizera."""

    optimizer_name: str
    status: str
    best_model: str
    raw_bits: int
    total_bits: int
    saving_bits: int
    ratio_vs_raw: float
    history: list[dict]
    details: dict


class Optimizer(Protocol):
    """Minimalne rozhranie pre optimizer v registry."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

    def available(self) -> bool:
        """Vrati pravdu iba pre realne implementovany optimizer."""

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti optimizer nad zadanymi bytmi."""
```

## File: `src/primesymbolicmdl/optimizers/gplite_adapter.py`

```python
"""Adapter medzi povodnym GP-lite searchom a registry optimizerov."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult
from ..law_search import search_best_law_for_bytes


class GPLiteOptimizer:
    """Tenký adapter pre existujuci stromovy GP-lite search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "GP-lite"

    def available(self) -> bool:
        """GP-lite je plne dostupny v tomto repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti povodny GP-lite search a normalizuje vysledok."""

        result = search_best_law_for_bytes(
            request.data,
            width_bits=request.width_bits,
            seed=request.seed,
            population_size=request.population_size,
            generations=request.generations,
            max_index=request.max_index,
            strict_lower=request.strict_lower,
        )
        details = dict(result)
        details["decoder_model"] = details.pop("best_law", None)
        best_cost = result.get("best_cost", {})
        if isinstance(best_cost, dict):
            details["residual_bits"] = best_cost.get("residual_bits")
            details["residual_codec"] = best_cost.get("residual_codec")
            details["residual_codec_details"] = best_cost.get("residual_codec_details")
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=result["best_law_string"],
            raw_bits=result["raw_bits"],
            total_bits=result["total_bits"],
            saving_bits=result["saving_bits"],
            ratio_vs_raw=result["ratio_vs_raw"],
            history=result["history"],
            details=details,
        )
```

## File: `src/primesymbolicmdl/optimizers/image_gplite.py`

```python
"""Deterministicky Image-GP-lite search nad 2D pixel kontextom."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .base import OptimizerRequest, OptimizerResult
from ..image_context_laws import (
    ImageLawNode,
    add_law,
    avg_law,
    checker_parity_law,
    clamp_byte_law,
    eq_const_law,
    floordiv_const_law,
    gradient_law,
    mod_const_law,
    parity_byte_law,
    render_image_law,
    sub_law,
    terminal_law,
)
from ..image_datasets import GrayImage, make_gray_image
from ..image_law_branch import encode_image_law_payload, estimate_image_law_cost

_MAX_DEPTH = 4
_PRIMITIVE_SET_ALIASES = {
    "local": "local",
    "ramp": "ramp",
    "structure": "structure",
    "full": "structure",
}
_STRUCTURE_BLOCKS = (1, 2, 4, 8, 16)
_EQ_CONST_VALUES = tuple(range(17))
_MOD_DIV_VALUES = (2, 4, 8, 16)


@dataclass(frozen=True)
class PrimitiveSetSpec:
    """Popis dostupnych terminalov a operatorov pre jeden primitive set."""

    name: str
    terminals: tuple[str, ...]
    allows_structure_primitives: bool


_PRIMITIVE_SPECS = {
    "local": PrimitiveSetSpec(
        name="local",
        terminals=("left", "up", "up_left"),
        allows_structure_primitives=False,
    ),
    "ramp": PrimitiveSetSpec(
        name="ramp",
        terminals=("left", "up", "up_left", "x_ramp", "y_ramp", "diag_ramp"),
        allows_structure_primitives=False,
    ),
    "structure": PrimitiveSetSpec(
        name="structure",
        terminals=("col", "row", "left", "up", "up_left", "x_ramp", "y_ramp", "diag_ramp"),
        allows_structure_primitives=True,
    ),
}


class ImageGPLiteOptimizer:
    """Registry adapter pre maly 2D expression-tree search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "Image-GP-lite"

    def available(self) -> bool:
        """Image-aware GP-lite je plne implementovany v repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti maly deterministicky search nad 2D image law stromami."""

        width = request.metadata.get("image_width")
        height = request.metadata.get("image_height")
        dataset_name = request.metadata.get("dataset_name", "external")
        primitive_set_name = request.metadata.get("image_gplite_primitive_set", "full")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Image-GP-lite requires positive metadata['image_width']")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Image-GP-lite requires positive metadata['image_height']")

        image_name = str(dataset_name) if isinstance(dataset_name, str) else "external"
        image = make_gray_image(image_name, width, height, bytes(request.data))
        search = search_best_image_law(
            image,
            seed=request.seed,
            population_size=request.population_size,
            generations=request.generations,
            primitive_set=str(primitive_set_name),
        )
        best_law = search["best_law"]
        best_cost = search["best_cost"]
        payload = encode_image_law_payload(image, best_law)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=render_image_law(best_law),
            raw_bits=best_cost["raw_bits"],
            total_bits=best_cost["total_bits"],
            saving_bits=best_cost["saving_bits"],
            ratio_vs_raw=best_cost["ratio_vs_raw"],
            history=search["history"],
            details={
                "image_law_model": best_law,
                "payload": payload,
                "residual_bits": best_cost["residual_bits"],
                "residual_codec": best_cost["residual_codec"],
                "residual_codec_details": best_cost["residual_codec_details"],
                "min_residual": best_cost["min_residual"],
                "max_residual": best_cost["max_residual"],
                "would_use_fallback": best_cost["total_bits"] >= best_cost["raw_bits"],
                "best_cost": best_cost,
                "search_seed": request.seed,
                "primitive_set": search["requested_primitive_set"],
                "resolved_primitive_set": search["resolved_primitive_set"],
            },
        )


def available_image_gplite_primitive_sets() -> list[str]:
    """Vrati stabilny zoznam akceptovanych primitive set mien."""

    return ["local", "ramp", "structure", "full"]


def search_best_image_law(
    image: GrayImage,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
    max_depth: int = _MAX_DEPTH,
    primitive_set: str = "full",
) -> dict:
    """Spusti malu deterministicku GP-lite search smycku nad image law stromami."""

    resolved_name, spec = _resolve_primitive_set(primitive_set)
    rng = Random(seed)
    resolved_population = max(1, population_size)
    resolved_generations = max(1, generations)

    population = _seed_population(spec, max_depth)
    attempts = 0
    while len(population) < resolved_population and attempts < resolved_population * 20:
        candidate = _random_law(rng, spec, max_depth)
        population[_law_key(candidate)] = candidate
        attempts += 1

    history: list[dict] = []
    best_law: ImageLawNode | None = None
    best_cost: dict | None = None

    for generation_index in range(resolved_generations):
        scored = _score_population(list(population.values()), image)
        best_law = scored[0]["law"]
        best_cost = scored[0]["cost"]
        history.append(
            {
                "generation": generation_index,
                "best_model": render_image_law(best_law),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
                "primitive_set": resolved_name,
            }
        )

        elite_count = max(2, min(len(scored), resolved_population // 8 or 1))
        next_population = {
            _law_key(item["law"]): item["law"]
            for item in scored[:elite_count]
        }

        fill_attempts = 0
        while len(next_population) < resolved_population and fill_attempts < resolved_population * 40:
            parent = _tournament_select(scored, rng)
            if rng.random() < 0.35:
                donor = _tournament_select(scored, rng)
                child = _crossover_laws(parent["law"], donor["law"], rng, spec, max_depth)
            else:
                child = _mutate_law(parent["law"], rng, spec, max_depth)
            next_population[_law_key(child)] = child
            fill_attempts += 1

        extra_attempts = 0
        while len(next_population) < resolved_population and extra_attempts < resolved_population * 20:
            extra = _random_law(rng, spec, max_depth)
            next_population[_law_key(extra)] = extra
            extra_attempts += 1

        population = next_population

    if best_law is None or best_cost is None:
        raise RuntimeError("Image-GP-lite did not produce a best candidate")

    return {
        "best_law": best_law,
        "best_cost": best_cost,
        "history": history,
        "generations": resolved_generations,
        "population_size": resolved_population,
        "seed": seed,
        "requested_primitive_set": primitive_set,
        "resolved_primitive_set": resolved_name,
    }


def _resolve_primitive_set(name: str) -> tuple[str, PrimitiveSetSpec]:
    """Prevedie alias primitive setu na internu specifikaciu."""

    normalized = str(name).strip()
    resolved = _PRIMITIVE_SET_ALIASES.get(normalized)
    if resolved is None:
        raise ValueError(f"Unknown Image-GP-lite primitive set: {name}")
    return resolved, _PRIMITIVE_SPECS[resolved]


def _seed_population(spec: PrimitiveSetSpec, max_depth: int) -> dict[str, ImageLawNode]:
    """Vrati malu sadu rozumnych startovacich stromov pre dany primitive set."""

    laws: list[ImageLawNode] = [
        terminal_law("left"),
        terminal_law("up"),
        terminal_law("up_left"),
        avg_law(terminal_law("left"), terminal_law("up")),
        gradient_law(terminal_law("left"), terminal_law("up"), terminal_law("up_left")),
        clamp_byte_law(gradient_law(terminal_law("left"), terminal_law("up"), terminal_law("up_left"))),
    ]

    if "x_ramp" in spec.terminals:
        laws.extend(
            [
                terminal_law("x_ramp"),
                terminal_law("y_ramp"),
                terminal_law("diag_ramp"),
            ]
        )

    if spec.allows_structure_primitives:
        laws.extend(checker_parity_law(block) for block in _STRUCTURE_BLOCKS)
        laws.extend(
            [
                parity_byte_law(terminal_law("col")),
                parity_byte_law(terminal_law("row")),
                mod_const_law(terminal_law("col"), 2),
                mod_const_law(terminal_law("row"), 2),
                floordiv_const_law(terminal_law("col"), 4),
                floordiv_const_law(terminal_law("row"), 4),
                eq_const_law(mod_const_law(terminal_law("col"), 2), 1),
            ]
        )

    return {_law_key(_prune_law(law, spec, max_depth)): _prune_law(law, spec, max_depth) for law in laws}


def _score_population(population: list[ImageLawNode], image: GrayImage) -> list[dict]:
    """Ohodnoti populaciu podla total_bits a stabilne ju utriedi."""

    scored = []
    for law in population:
        cost = estimate_image_law_cost(image, law)
        scored.append({"law": law, "cost": cost, "law_string": render_image_law(law)})
    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return scored


def _tournament_select(scored: list[dict], rng: Random, size: int = 3) -> dict:
    """Vyberie rodica cez maly deterministicky turnaj."""

    sample_size = min(size, len(scored))
    candidates = rng.sample(scored, sample_size)
    candidates.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return candidates[0]


def _random_law(rng: Random, spec: PrimitiveSetSpec, max_depth: int) -> ImageLawNode:
    """Vygeneruje nahodny zakon malej hlbky v ramci primitive setu."""

    if max_depth <= 0 or rng.random() < 0.28:
        return _random_terminal(rng, spec)

    choices = ["add", "sub", "avg", "gradient", "clamp_byte"]
    if spec.allows_structure_primitives:
        choices.extend(["mod_const", "floordiv_const", "eq_const", "parity_byte", "checker_parity"])

    choice = rng.choice(choices)
    if choice == "add":
        return add_law(_random_law(rng, spec, max_depth - 1), _random_law(rng, spec, max_depth - 1))
    if choice == "sub":
        return sub_law(_random_law(rng, spec, max_depth - 1), _random_law(rng, spec, max_depth - 1))
    if choice == "avg":
        return avg_law(_random_law(rng, spec, max_depth - 1), _random_law(rng, spec, max_depth - 1))
    if choice == "gradient":
        return gradient_law(
            _random_law(rng, spec, max_depth - 1),
            _random_law(rng, spec, max_depth - 1),
            _random_law(rng, spec, max_depth - 1),
        )
    if choice == "mod_const":
        return mod_const_law(_random_law(rng, spec, max_depth - 1), rng.choice(_MOD_DIV_VALUES))
    if choice == "floordiv_const":
        return floordiv_const_law(_random_law(rng, spec, max_depth - 1), rng.choice(_MOD_DIV_VALUES))
    if choice == "eq_const":
        return eq_const_law(_random_law(rng, spec, max_depth - 1), rng.choice(_EQ_CONST_VALUES))
    if choice == "parity_byte":
        return parity_byte_law(_random_law(rng, spec, max_depth - 1))
    if choice == "checker_parity":
        return checker_parity_law(rng.choice(_STRUCTURE_BLOCKS))
    return clamp_byte_law(_random_law(rng, spec, max_depth - 1))


def _random_terminal(rng: Random, spec: PrimitiveSetSpec) -> ImageLawNode:
    """Vygeneruje terminal alebo explicitnu checker primitive."""

    if spec.allows_structure_primitives and rng.random() < 0.18:
        return checker_parity_law(rng.choice(_STRUCTURE_BLOCKS))
    return terminal_law(rng.choice(spec.terminals))


def _mutate_law(law: ImageLawNode, rng: Random, spec: PrimitiveSetSpec, max_depth: int) -> ImageLawNode:
    """Aplikuje malu deterministicku mutaciu podstromu."""

    paths = _subtree_paths(law)
    target_path = rng.choice(paths)
    target = _get_subtree(law, target_path)
    mode = rng.choice(("replace", "wrap", "tweak"))

    if mode == "replace":
        replacement = _random_law(rng, spec, 2)
    elif mode == "wrap":
        replacement = _wrap_subtree(target, rng, spec)
    else:
        replacement = _tweak_subtree(target, rng, spec)

    return _prune_law(_replace_subtree(law, target_path, replacement), spec, max_depth)


def _crossover_laws(
    left: ImageLawNode,
    right: ImageLawNode,
    rng: Random,
    spec: PrimitiveSetSpec,
    max_depth: int,
) -> ImageLawNode:
    """Zlozi dieta nahradenim podstromu darcovskym podstromom."""

    left_path = rng.choice(_subtree_paths(left))
    right_subtree = _get_subtree(right, rng.choice(_subtree_paths(right)))
    return _prune_law(_replace_subtree(left, left_path, right_subtree), spec, max_depth)


def _wrap_subtree(law: ImageLawNode, rng: Random, spec: PrimitiveSetSpec) -> ImageLawNode:
    """Obali podstrom jednoduchym operatorom dostupnym v primitive sete."""

    choices = ["add", "sub", "avg", "clamp_byte"]
    if spec.allows_structure_primitives:
        choices.extend(["mod_const", "floordiv_const", "eq_const", "parity_byte"])

    choice = rng.choice(choices)
    if choice == "add":
        return add_law(law, _random_terminal(rng, spec))
    if choice == "sub":
        return sub_law(law, _random_terminal(rng, spec))
    if choice == "avg":
        return avg_law(law, _random_terminal(rng, spec))
    if choice == "mod_const":
        return mod_const_law(law, rng.choice(_MOD_DIV_VALUES))
    if choice == "floordiv_const":
        return floordiv_const_law(law, rng.choice(_MOD_DIV_VALUES))
    if choice == "eq_const":
        return eq_const_law(law, rng.choice(_EQ_CONST_VALUES))
    if choice == "parity_byte":
        return parity_byte_law(law)
    return clamp_byte_law(law)


def _tweak_subtree(law: ImageLawNode, rng: Random, spec: PrimitiveSetSpec) -> ImageLawNode:
    """Jemne upravi operator alebo jeho parameter."""

    if law.kind in spec.terminals:
        return _random_terminal(rng, spec)
    if law.kind == "add":
        return sub_law(law.children[0], law.children[1])
    if law.kind == "sub":
        return avg_law(law.children[0], law.children[1])
    if law.kind == "avg":
        return add_law(law.children[0], law.children[1])
    if law.kind == "gradient":
        return clamp_byte_law(law)
    if law.kind == "clamp_byte":
        return law.children[0]
    if law.kind == "mod_const":
        current = int(law.value or _MOD_DIV_VALUES[0])
        return mod_const_law(law.children[0], _next_value(_MOD_DIV_VALUES, current, rng))
    if law.kind == "floordiv_const":
        current = int(law.value or _MOD_DIV_VALUES[0])
        return floordiv_const_law(law.children[0], _next_value(_MOD_DIV_VALUES, current, rng))
    if law.kind == "eq_const":
        current = int(law.value or 0)
        return eq_const_law(law.children[0], _next_value(_EQ_CONST_VALUES, current, rng))
    if law.kind == "parity_byte":
        return law.children[0]
    if law.kind == "checker_parity":
        current = int(law.value or _STRUCTURE_BLOCKS[0])
        return checker_parity_law(_next_value(_STRUCTURE_BLOCKS, current, rng))
    return _random_terminal(rng, spec)


def _subtree_paths(law: ImageLawNode, prefix: tuple[int, ...] = ()) -> list[tuple[int, ...]]:
    """Vrati vsetky cesty k podstromom."""

    paths = [prefix]
    for index, child in enumerate(law.children):
        paths.extend(_subtree_paths(child, prefix + (index,)))
    return paths


def _get_subtree(law: ImageLawNode, path: tuple[int, ...]) -> ImageLawNode:
    """Vrati podstrom na zadanej ceste."""

    node = law
    for step in path:
        node = node.children[step]
    return node


def _replace_subtree(law: ImageLawNode, path: tuple[int, ...], replacement: ImageLawNode) -> ImageLawNode:
    """Vrati novy strom s nahradenym podstromom."""

    if not path:
        return replacement

    step = path[0]
    children = list(law.children)
    children[step] = _replace_subtree(children[step], path[1:], replacement)
    return ImageLawNode(law.kind, law.value, tuple(children))


def _prune_law(law: ImageLawNode, spec: PrimitiveSetSpec, max_depth: int) -> ImageLawNode:
    """Oreze strom na malu hlbku, aby search ostal rychly a validny."""

    if max_depth <= 0:
        if law.kind in spec.terminals or law.kind == "checker_parity":
            return law
        if law.children:
            return _prune_law(law.children[0], spec, 0)
        return terminal_law(spec.terminals[0])

    if law.kind in spec.terminals or law.kind == "checker_parity":
        return law

    if law.kind in {"add", "sub", "avg"}:
        return ImageLawNode(
            law.kind,
            None,
            (_prune_law(law.children[0], spec, max_depth - 1), _prune_law(law.children[1], spec, max_depth - 1)),
        )
    if law.kind == "gradient":
        return ImageLawNode(
            law.kind,
            None,
            (
                _prune_law(law.children[0], spec, max_depth - 1),
                _prune_law(law.children[1], spec, max_depth - 1),
                _prune_law(law.children[2], spec, max_depth - 1),
            ),
        )
    if law.kind in {"clamp_byte", "mod_const", "floordiv_const", "eq_const", "parity_byte"}:
        return ImageLawNode(law.kind, law.value, (_prune_law(law.children[0], spec, max_depth - 1),))

    if law.children:
        return _prune_law(law.children[0], spec, max_depth - 1)
    return terminal_law(spec.terminals[0])


def _next_value(options: tuple[int, ...], current: int, rng: Random) -> int:
    """Vrati iny validny parameter z konecnej mnoziny hodnôt."""

    if current not in options:
        return options[0]
    candidates = [value for value in options if value != current]
    if not candidates:
        return current
    return rng.choice(candidates)


def _law_key(law: ImageLawNode) -> str:
    """Vrati stabilny kluc pre deduplikaciu populacie."""

    return render_image_law(law)
```

## File: `src/primesymbolicmdl/optimizers/image_predictor.py`

```python
"""Adapter optimizera pre deterministicke 2D obrazkove prediktory."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult
from ..image_datasets import make_gray_image
from ..image_predictor_branch import encode_image_predictor_payload, estimate_image_predictor_cost
from ..image_predictors import default_image_predictor_models, render_image_predictor


class ImagePredictorOptimizer:
    """Registry adapter pre 2D grayscale predictor baseline."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "Image-predictor"

    def available(self) -> bool:
        """Tento baseline je plne implementovany v repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Vyhodnoti malu sadu decoder-znamych 2D prediktorov."""

        width = request.metadata.get("image_width")
        height = request.metadata.get("image_height")
        dataset_name = request.metadata.get("dataset_name", "external")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Image-predictor requires positive metadata['image_width']")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Image-predictor requires positive metadata['image_height']")

        image_name = str(dataset_name) if isinstance(dataset_name, str) else "external"
        image = make_gray_image(image_name, width, height, bytes(request.data))

        history: list[dict] = []
        best_model = None
        best_cost = None

        for index, model in enumerate(default_image_predictor_models()):
            cost = estimate_image_predictor_cost(image, model)
            if best_cost is None or (cost["total_bits"], render_image_predictor(model)) < (
                best_cost["total_bits"],
                render_image_predictor(best_model),
            ):
                best_model = model
                best_cost = cost

            history.append(
                {
                    "generation": index,
                    "best_model": render_image_predictor(best_model),
                    "candidate_model": render_image_predictor(model),
                    "total_bits": best_cost["total_bits"],
                    "saving_bits": best_cost["saving_bits"],
                }
            )

        if best_model is None or best_cost is None:
            raise RuntimeError("Image-predictor did not evaluate any models")

        payload = encode_image_predictor_payload(image, best_model)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=render_image_predictor(best_model),
            raw_bits=best_cost["raw_bits"],
            total_bits=best_cost["total_bits"],
            saving_bits=best_cost["saving_bits"],
            ratio_vs_raw=best_cost["ratio_vs_raw"],
            history=history,
            details={
                "predictor_model": best_model,
                "payload": payload,
                "residual_width": best_cost["residual_width"],
                "residual_bits": best_cost["residual_bits"],
                "residual_codec": best_cost["residual_codec"],
                "residual_codec_details": best_cost["residual_codec_details"],
                "min_residual": best_cost["min_residual"],
                "max_residual": best_cost["max_residual"],
                "would_use_fallback": best_cost["total_bits"] >= best_cost["raw_bits"],
                "best_cost": best_cost,
            },
        )
```

## File: `src/primesymbolicmdl/optimizers/image_soma.py`

```python
"""Deterministicky fixed-point Image-SOMA search nad 2D pixel kontextom."""

from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

from .base import OptimizerRequest, OptimizerResult
from ..bitcost import bits_unsigned_range
from ..image_datasets import GrayImage, make_gray_image
from ..residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
)

_HEADER_BITS = 64
_MODEL_BITS = 16
_SCALE = 256
_WEIGHT_BOUNDS = (-512, 512)
_BIAS_BOUNDS = (-65536, 65536)
_PATH_STEPS = ((1, 2), (1, 1), (3, 2))
_PRT = 0.6
_DIMENSION_NAMES = ("w_left", "w_up", "w_up_left", "w_x", "w_y", "w_diag", "bias")


@dataclass(frozen=True)
class ImageSomaModel:
    """Malý fixed-point linear predictor pre grayscale obrazky."""

    w_left: int
    w_up: int
    w_up_left: int
    w_x: int
    w_y: int
    w_diag: int
    bias: int

    def predict(self, context: dict[str, int]) -> int:
        """Vrati clampnutu predikciu iba z decoder-znameho kontextu."""

        total = (
            (self.w_left * context["left"])
            + (self.w_up * context["up"])
            + (self.w_up_left * context["up_left"])
            + (self.w_x * context["x_ramp"])
            + (self.w_y * context["y_ramp"])
            + (self.w_diag * context["diag_ramp"])
            + self.bias
        )
        return _clamp_byte(total // _SCALE)

    def parameter_bits(self) -> int:
        """Vrati konzervativnu cenu vsetkych integer parametrov modelu."""

        values = (
            self.w_left,
            self.w_up,
            self.w_up_left,
            self.w_x,
            self.w_y,
            self.w_diag,
            self.bias,
        )
        return sum(_signed_parameter_bits(value) for value in values)

    def render(self) -> str:
        """Vrati stabilnu textualnu podobu fixed-point modelu."""

        return (
            "image_soma("
            f"w_left={self.w_left}, "
            f"w_up={self.w_up}, "
            f"w_up_left={self.w_up_left}, "
            f"w_x={self.w_x}, "
            f"w_y={self.w_y}, "
            f"w_diag={self.w_diag}, "
            f"bias={self.bias}, "
            f"scale={_SCALE})"
        )

    def as_tuple(self) -> tuple[int, int, int, int, int, int, int]:
        """Vrati model ako stabilny integer vektor."""

        return (
            self.w_left,
            self.w_up,
            self.w_up_left,
            self.w_x,
            self.w_y,
            self.w_diag,
            self.bias,
        )


class ImageSomaOptimizer:
    """Registry adapter pre image-aware fixed-point SOMA search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "Image-SOMA"

    def available(self) -> bool:
        """Image-SOMA je plne implementovany v tomto repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti maly deterministicky fixed-point SOMA search."""

        width = request.metadata.get("image_width")
        height = request.metadata.get("image_height")
        dataset_name = request.metadata.get("dataset_name", "external")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Image-SOMA requires positive metadata['image_width']")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Image-SOMA requires positive metadata['image_height']")

        image_name = str(dataset_name) if isinstance(dataset_name, str) else "external"
        image = make_gray_image(image_name, width, height, bytes(request.data))
        search = search_best_image_soma_model(
            image,
            seed=request.seed,
            population_size=request.population_size,
            generations=request.generations,
        )
        best_model = search["best_model"]
        best_cost = search["best_cost"]
        payload = encode_image_soma_payload(image, best_model)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=best_model.render(),
            raw_bits=best_cost["raw_bits"],
            total_bits=best_cost["total_bits"],
            saving_bits=best_cost["saving_bits"],
            ratio_vs_raw=best_cost["ratio_vs_raw"],
            history=search["history"],
            details={
                "image_soma_model": best_model,
                "payload": payload,
                "residual_bits": best_cost["residual_bits"],
                "residual_codec": best_cost["residual_codec"],
                "residual_codec_details": best_cost["residual_codec_details"],
                "min_residual": best_cost["min_residual"],
                "max_residual": best_cost["max_residual"],
                "would_use_fallback": best_cost["total_bits"] >= best_cost["raw_bits"],
                "best_cost": best_cost,
                "scale": _SCALE,
                "search_seed": request.seed,
            },
        )


def estimate_image_soma_cost(image: GrayImage, model: ImageSomaModel) -> dict:
    """Odhadne cenu fixed-point Image-SOMA vetvy pre obrazok."""

    trace = build_image_soma_trace(image, model)
    raw_bits = image.width * image.height * 8
    residual_codec = choose_best_residual_codec(trace["residuals"])
    residual_bits = residual_codec.bits
    residual_width = signed_width_for_range(trace["min_residual"], trace["max_residual"])
    total_bits = _HEADER_BITS + _MODEL_BITS + model.parameter_bits() + residual_bits
    saving_bits = raw_bits - total_bits
    return {
        "raw_bits": raw_bits,
        "model_bits": _MODEL_BITS,
        "parameter_bits": model.parameter_bits(),
        "header_bits": _HEADER_BITS,
        "residual_bits": residual_bits,
        "residual_width": residual_width,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "pixel_count": trace["pixel_count"],
        "model": model,
    }


def encode_image_soma_payload(image: GrayImage, model: ImageSomaModel) -> dict:
    """Zakoduje obrazok cez fixed-point Image-SOMA model."""

    trace = build_image_soma_trace(image, model)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    return {
        "codec": "image_soma",
        "width": image.width,
        "height": image.height,
        "model": {
            "w_left": model.w_left,
            "w_up": model.w_up,
            "w_up_left": model.w_up_left,
            "w_x": model.w_x,
            "w_y": model.w_y,
            "w_diag": model.w_diag,
            "bias": model.bias,
            "scale": _SCALE,
        },
        "residual_codec": residual_codec.codec_name,
        "residual_payload": residual_codec.payload,
        "metadata": {
            "estimated_costs": estimate_image_soma_cost(image, model),
            "model_string": model.render(),
            "experimental": True,
        },
    }


def decode_image_soma_payload(payload: dict) -> bytes:
    """Dekoduje exact-lossless fixed-point Image-SOMA payload."""

    width = payload.get("width")
    height = payload.get("height")
    model_payload = payload.get("model")
    residual_codec = payload.get("residual_codec")
    residual_payload = payload.get("residual_payload")
    explicit_residuals = payload.get("residuals")

    if payload.get("codec") not in {None, "image_soma"}:
        raise ValueError("Unsupported image soma codec")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")
    if not isinstance(model_payload, dict):
        raise ValueError("model must be a dict")

    model = ImageSomaModel(
        w_left=int(model_payload.get("w_left", 0)),
        w_up=int(model_payload.get("w_up", 0)),
        w_up_left=int(model_payload.get("w_up_left", 0)),
        w_x=int(model_payload.get("w_x", 0)),
        w_y=int(model_payload.get("w_y", 0)),
        w_diag=int(model_payload.get("w_diag", 0)),
        bias=int(model_payload.get("bias", 0)),
    )
    residuals = _decode_residual_stream(residual_codec, residual_payload, explicit_residuals)
    if len(residuals) != width * height:
        raise ValueError("residual count does not match image size")

    decoded: list[int] = []
    for index, residual in enumerate(residuals):
        row = index // width
        col = index % width
        context = _build_context(decoded, col, row, width, height)
        prediction = model.predict(context)
        value = prediction + int(residual)
        if value < 0 or value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        decoded.append(value)
    return bytes(decoded)


def roundtrip_image_soma(image: GrayImage, model: ImageSomaModel) -> bytes:
    """Zakoduje a spatne dekoduje obrazok bez straty informacie."""

    return decode_image_soma_payload(encode_image_soma_payload(image, model))


def build_image_soma_trace(image: GrayImage, model: ImageSomaModel) -> dict:
    """Vrati predikcie, rezidua a decoded kontrolu pre dany model."""

    predicted: list[int] = []
    residuals: list[int] = []
    decoded: list[int] = []

    for index, original in enumerate(image.pixels):
        row = index // image.width
        col = index % image.width
        context = _build_context(decoded, col, row, image.width, image.height)
        prediction = model.predict(context)
        residual = int(original) - prediction
        decoded_value = prediction + residual
        if decoded_value < 0 or decoded_value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        predicted.append(prediction)
        residuals.append(residual)
        decoded.append(decoded_value)

    min_residual = min(residuals, default=0)
    max_residual = max(residuals, default=0)
    return {
        "predicted_pixels": bytes(predicted),
        "residuals": residuals,
        "decoded_pixels": bytes(decoded),
        "min_residual": min_residual,
        "max_residual": max_residual,
        "pixel_count": len(image.pixels),
        "model_string": model.render(),
    }


def search_best_image_soma_model(
    image: GrayImage,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
) -> dict:
    """Spusti malu deterministicku fixed-point SOMA search smycku."""

    rng = Random(seed)
    resolved_population = max(1, population_size)
    resolved_generations = max(1, generations)

    population = _initial_population(rng, resolved_population)
    history: list[dict] = []
    best_model: ImageSomaModel | None = None
    best_cost: dict | None = None

    for generation in range(resolved_generations):
        scored = _score_population(population, image)
        leader = scored[0]
        best_model = leader["model"]
        best_cost = leader["cost"]
        history.append(
            {
                "generation": generation,
                "best_model": best_model.render(),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
            }
        )

        elite_count = max(2, min(len(scored), resolved_population // 8 or 1))
        next_population = [item["model"] for item in scored[:elite_count]]
        for item in scored[elite_count:]:
            next_population.append(_migrate_individual(item["model"], best_model, image, rng))

        while len(next_population) < resolved_population:
            next_population.append(_random_model(rng))
        population = next_population[:resolved_population]

    if best_model is None or best_cost is None:
        raise RuntimeError("Image-SOMA did not produce a best candidate")

    return {
        "best_model": best_model,
        "best_cost": best_cost,
        "history": history,
        "generations": resolved_generations,
        "population_size": resolved_population,
        "seed": seed,
    }


def _initial_population(rng: Random, population_size: int) -> list[ImageSomaModel]:
    """Vytvori uvodnu populaciu s rozumnymi fixed-point baseline modelmi."""

    population = [
        ImageSomaModel(0, 0, 0, _SCALE, 0, 0, 0),
        ImageSomaModel(0, 0, 0, 0, _SCALE, 0, 0),
        ImageSomaModel(0, 0, 0, 0, 0, _SCALE, 0),
        ImageSomaModel(_SCALE, 0, 0, 0, 0, 0, 0),
        ImageSomaModel(0, _SCALE, 0, 0, 0, 0, 0),
        ImageSomaModel(_SCALE // 2, _SCALE // 2, 0, 0, 0, 0, 0),
        ImageSomaModel(_SCALE, _SCALE, -_SCALE, 0, 0, 0, 0),
        ImageSomaModel(0, 0, 0, 0, 0, 0, 128 * _SCALE),
    ]
    while len(population) < max(1, population_size):
        population.append(_random_model(rng))
    return population[: max(1, population_size)]


def _score_population(population: list[ImageSomaModel], image: GrayImage) -> list[dict]:
    """Ohodnoti populaciu a utriedi ju podla total_bits."""

    scored = []
    for model in population:
        cost = estimate_image_soma_cost(image, model)
        scored.append({"model": model, "cost": cost})
    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["model"].render()))
    return scored


def _migrate_individual(current: ImageSomaModel, leader: ImageSomaModel, image: GrayImage, rng: Random) -> ImageSomaModel:
    """Presunie jedinca po ceste smerom k liderovi a ponecha najlepsi bod."""

    best_model = current
    best_cost = estimate_image_soma_cost(image, current)
    current_values = list(current.as_tuple())
    leader_values = list(leader.as_tuple())

    for numerator, denominator in _PATH_STEPS:
        mask = _prt_mask(rng, len(current_values))
        candidate_values = []
        for index, (value, target) in enumerate(zip(current_values, leader_values)):
            if mask[index] == 0:
                candidate_values.append(value)
                continue
            delta = target - value
            migrated = value + _round_div(delta * numerator, denominator)
            candidate_values.append(_clip_dimension(index, migrated))
        candidate = _model_from_values(candidate_values)
        candidate_cost = estimate_image_soma_cost(image, candidate)
        if (candidate_cost["total_bits"], candidate.render()) < (best_cost["total_bits"], best_model.render()):
            best_model = candidate
            best_cost = candidate_cost

    if rng.random() < 0.2:
        mutated = _random_perturbation(best_model, rng)
        mutated_cost = estimate_image_soma_cost(image, mutated)
        if (mutated_cost["total_bits"], mutated.render()) < (best_cost["total_bits"], best_model.render()):
            best_model = mutated

    return best_model


def _prt_mask(rng: Random, dimensions: int) -> list[int]:
    """Vrati PRT masku a zaruci aspon jednu aktivnu dimenziu."""

    mask = [1 if rng.random() < _PRT else 0 for _ in range(dimensions)]
    if any(mask):
        return mask
    mask[rng.randrange(dimensions)] = 1
    return mask


def _random_model(rng: Random) -> ImageSomaModel:
    """Vrati nahodny model v povolenych integer hraniciach."""

    return ImageSomaModel(
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_BIAS_BOUNDS),
    )


def _random_perturbation(model: ImageSomaModel, rng: Random) -> ImageSomaModel:
    """Vykona malu lokalnu mutaciu jedneho integer parametra."""

    values = list(model.as_tuple())
    index = rng.randrange(len(values))
    if index < 6:
        values[index] = _clip_dimension(index, values[index] + rng.choice((-64, -32, -16, 16, 32, 64)))
    else:
        values[index] = _clip_dimension(index, values[index] + rng.choice((-4096, -1024, -256, 256, 1024, 4096)))
    return _model_from_values(values)


def _build_context(decoded: list[int], col: int, row: int, width: int, height: int) -> dict[str, int]:
    """Posklada decoder-znamy 2D kontext bez pristupu k aktualnemu pixelu."""

    left = decoded[-1] if col > 0 else 0
    up = decoded[(row - 1) * width + col] if row > 0 else 0
    up_left = decoded[(row - 1) * width + col - 1] if row > 0 and col > 0 else 0
    return {
        "left": left,
        "up": up,
        "up_left": up_left,
        "x_ramp": (255 * col) // max(1, width - 1),
        "y_ramp": (255 * row) // max(1, height - 1),
        "diag_ramp": (255 * (col + row)) // max(1, width + height - 2),
    }


def _decode_residual_stream(
    residual_codec: object,
    residual_payload: object,
    explicit_residuals: object,
) -> list[int]:
    """Dekoduje residual stream z codec payloadu alebo zo starsieho fallback pola."""

    if isinstance(explicit_residuals, list):
        if not all(isinstance(value, int) for value in explicit_residuals):
            raise ValueError("residuals must contain integers")
        return [int(value) for value in explicit_residuals]

    if not isinstance(residual_codec, str):
        raise ValueError("residual_codec must be a string")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")
    if residual_codec == "fixed_signed":
        return decode_fixed_signed_residual_payload(residual_payload)
    if residual_codec == "zero_rle":
        return decode_zero_rle_residual_payload(residual_payload)
    raise ValueError(f"Unsupported residual codec: {residual_codec}")


def _model_from_values(values: list[int]) -> ImageSomaModel:
    """Posklada immutable model z integer zoznamu."""

    return ImageSomaModel(*[int(value) for value in values])


def _clip_dimension(index: int, value: int) -> int:
    """Oreze jednu dimenziu vektora na jej povoleny rozsah."""

    if index < 6:
        return max(_WEIGHT_BOUNDS[0], min(_WEIGHT_BOUNDS[1], int(value)))
    return max(_BIAS_BOUNDS[0], min(_BIAS_BOUNDS[1], int(value)))


def _round_div(value: int, divisor: int) -> int:
    """Zaokruhli integer po deleni smerom k najblizsiemu celemu."""

    if divisor <= 0:
        raise ValueError("divisor must be positive")
    if value >= 0:
        return (value + (divisor // 2)) // divisor
    return -(((-value) + (divisor // 2)) // divisor)


def _signed_parameter_bits(value: int) -> int:
    """Vrati konzervativnu bitovu cenu jedneho podpisaneho parametra."""

    if value == 0:
        return 1
    return 1 + bits_unsigned_range(abs(int(value)))


def _clamp_byte(value: int) -> int:
    """Oreze lubovolne cele cislo na grayscale rozsah."""

    return max(0, min(255, int(value)))


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer total_bits voci raw_bits."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
```

## File: `src/primesymbolicmdl/optimizers/__init__.py`

```python
"""Abstrakcie a registry optimizerov pre vyskumne behy."""

from .base import Optimizer, OptimizerRequest, OptimizerResult
from .registry import get_optimizer, get_optimizer_names, run_optimizer

__all__ = [
    "Optimizer",
    "OptimizerRequest",
    "OptimizerResult",
    "get_optimizer",
    "get_optimizer_names",
    "run_optimizer",
]
```

## File: `src/primesymbolicmdl/optimizers/placeholders.py`

```python
"""Cestne placeholder implementacie pre buduce optimizery."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult


class PlaceholderOptimizer:
    """Jednoduchy neimplementovany optimizer s honest fallbackom."""

    def __init__(self, optimizer_name: str, explanation: str) -> None:
        self._optimizer_name = optimizer_name
        self._explanation = explanation

    def name(self) -> str:
        """Vrati registrovany nazov placeholdera."""

        return self._optimizer_name

    def available(self) -> bool:
        """Placeholder sa zobrazuje v GUI, ale nie je plne implementovany."""

        return False

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Vrati honest raw fallback namiesto predstieranej optimalizacie."""

        raw_bits = len(request.data) * 8
        return OptimizerResult(
            optimizer_name=self._optimizer_name,
            status="not_implemented",
            best_model="raw_fallback",
            raw_bits=raw_bits,
            total_bits=raw_bits,
            saving_bits=0,
            ratio_vs_raw=1.0,
            history=[],
            details={
                "message": self._explanation,
                "experimental": True,
            },
        )


def make_gp_placeholder() -> PlaceholderOptimizer:
    """Vrati placeholder pre buduci bohaty geneticky program."""

    return PlaceholderOptimizer(
        "GP",
        "GP will later search richer expression trees and topologies beyond the current GP-lite branch.",
    )


def make_adam_placeholder() -> PlaceholderOptimizer:
    """Vrati placeholder pre buduci diferencovatelny optimizer."""

    return PlaceholderOptimizer(
        "ADAM",
        "ADAM will later tune differentiable continuous parameters once a suitable differentiable law family exists.",
    )
```

## File: `src/primesymbolicmdl/optimizers/registry.py`

```python
"""Registry optimizerov pouzitelnych v CLI aj GUI."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult
from .gplite_adapter import GPLiteOptimizer
from .image_gplite import ImageGPLiteOptimizer
from .image_predictor import ImagePredictorOptimizer
from .image_soma import ImageSomaOptimizer
from .placeholders import make_adam_placeholder, make_gp_placeholder
from .soma import SomaOptimizer

_OPTIMIZERS = {
    "GP-lite": GPLiteOptimizer(),
    "SOMA": SomaOptimizer(),
    "GP": make_gp_placeholder(),
    "ADAM": make_adam_placeholder(),
    "Image-predictor": ImagePredictorOptimizer(),
    "Image-GP-lite": ImageGPLiteOptimizer(),
    "Image-SOMA": ImageSomaOptimizer(),
}

_ORDER = ["GP-lite", "SOMA", "GP", "ADAM", "Image-predictor", "Image-GP-lite", "Image-SOMA"]


def get_optimizer_names() -> list[str]:
    """Vrati stabilny zoznam mien pre dropdown a CLI."""

    return list(_ORDER)


def get_optimizer(name: str):
    """Vrati optimizer registrovany pod zadanym menom."""

    try:
        return _OPTIMIZERS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown optimizer: {name}") from exc


def run_optimizer(name: str, request: OptimizerRequest) -> OptimizerResult:
    """Spusti optimizer podla mena a vrati normalizovany vysledok."""

    return get_optimizer(name).run(request)
```

## File: `src/primesymbolicmdl/optimizers/soma.py`

```python
"""Maly deterministicky SOMA-like optimizer pre spojite parametre."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor
from random import Random

from .base import OptimizerRequest, OptimizerResult
from ..bitcost import bits_unsigned_range
from ..blocks import bytes_to_uint_blocks
from ..index_branch import estimate_law_cost

_PARAMETER_SCALE = 1000
_FAMILY_MODEL_BITS = {"affine": 10, "quadratic": 14}
_BOUNDS = (-16.0, 16.0)
_PATH_LENGTH = 1.5
_STEP = 0.5
_PRT = 0.6


@dataclass(frozen=True)
class ContinuousLaw:
    """Spojity zakon s malym poctom parametrov pre SOMA vetvu."""

    family: str
    params: tuple[float, float, float]

    def anchor_at(self, index: int) -> int:
        """Vyhodnoti anchor zakon A(i) a oreze ho na nezaporny rozsah."""

        if self.family == "affine":
            a, b, _ = self.params
            return max(0, floor((a * index) + b))
        if self.family == "quadratic":
            a, b, c = self.params
            return max(0, floor((a * index * index) + (b * index) + c))
        raise ValueError(f"Unsupported SOMA family: {self.family}")

    def model_bits(self) -> int:
        """Vrati konzervativnu modelovu cenu rodiny bez parametrov."""

        return _FAMILY_MODEL_BITS[self.family]

    def parameter_bits(self) -> int:
        """Vrati konzervativny pocet bitov pre kvantizovane parametre."""

        count = 2 if self.family == "affine" else 3
        total = 0
        for value in self.params[:count]:
            scaled = abs(int(round(value * _PARAMETER_SCALE)))
            total += 1 if scaled == 0 else 1 + bits_unsigned_range(scaled)
        return total

    def render(self) -> str:
        """Vrati stabilnu textualnu podobu zakona."""

        if self.family == "affine":
            return f"affine(a={self.params[0]:.3f}, b={self.params[1]:.3f})"
        return (
            f"quadratic(a={self.params[0]:.3f}, "
            f"b={self.params[1]:.3f}, c={self.params[2]:.3f})"
        )


class SomaOptimizer:
    """Registry adapter pre SOMA-like search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "SOMA"

    def available(self) -> bool:
        """SOMA implementacia je dostupna v tomto repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti SOMA-like search nad malou rodinou spojitych zakonov."""

        return run_soma_search(request)


def run_soma_search(request: OptimizerRequest) -> OptimizerResult:
    """Spusti maly deterministicky SOMA-like optimizer."""

    payload = bytes(request.data)
    blocks = bytes_to_uint_blocks(payload, request.width_bits)
    resolved_max_index = _resolve_max_index(blocks, request.max_index)
    rng = Random(request.seed)

    population = _initial_population(rng, request.population_size)
    history: list[dict] = []
    best_law: ContinuousLaw | None = None
    best_cost: dict | None = None

    for generation in range(request.generations):
        scored = _score_population(
            population,
            blocks,
            request.width_bits,
            len(payload),
            resolved_max_index,
            request.strict_lower,
        )
        leader = scored[0]
        best_law = leader["law"]
        best_cost = leader["cost"]
        history.append(
            {
                "generation": generation,
                "best_model": best_law.render(),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
            }
        )

        next_population = [best_law]
        for item in scored[1:]:
            next_population.append(
                _migrate_individual(
                    item["law"],
                    best_law,
                    blocks,
                    request.width_bits,
                    len(payload),
                    resolved_max_index,
                    request.strict_lower,
                    rng,
                )
            )

        while len(next_population) < request.population_size:
            next_population.append(_random_law(rng))

        population = next_population[: request.population_size]

    if best_law is None or best_cost is None:
        fallback = ContinuousLaw("affine", (0.0, 0.0, 0.0))
        best_cost = estimate_law_cost(blocks, request.width_bits, len(payload), fallback, resolved_max_index, request.strict_lower)
        best_law = fallback

    return OptimizerResult(
        optimizer_name="SOMA",
        status="ok",
        best_model=best_law.render(),
        raw_bits=best_cost["raw_bits"],
        total_bits=best_cost["total_bits"],
        saving_bits=best_cost["saving_bits"],
        ratio_vs_raw=best_cost["ratio_vs_raw"],
        history=history,
        details={
            "decoder_model": best_law,
            "best_cost": best_cost,
            "residual_bits": best_cost.get("residual_bits"),
            "residual_codec": best_cost.get("residual_codec"),
            "residual_codec_details": best_cost.get("residual_codec_details"),
            "max_index": resolved_max_index,
            "strict_lower": request.strict_lower,
            "note": "Float parameters are estimated research parameters, not a final codec format.",
        },
    )


def _resolve_max_index(blocks: list[int], max_index: int | None) -> int:
    """Vrati maly bezpecny limit indexu."""

    if max_index is not None:
        return max(0, max_index)
    if not blocks:
        return 0
    return min(31, max(blocks), max(0, len(blocks) - 1))


def _initial_population(rng: Random, population_size: int) -> list[ContinuousLaw]:
    """Vytvori uvodnu populaciu s oboma rodinami."""

    population = [
        ContinuousLaw("affine", (1.0, 0.0, 0.0)),
        ContinuousLaw("affine", (0.5, 0.0, 0.0)),
        ContinuousLaw("quadratic", (0.0, 1.0, 0.0)),
        ContinuousLaw("quadratic", (0.0, 0.5, 0.0)),
    ]
    while len(population) < max(1, population_size):
        population.append(_random_law(rng))
    return population[: max(1, population_size)]


def _score_population(
    population: list[ContinuousLaw],
    blocks: list[int],
    width_bits: int,
    original_size: int,
    max_index: int,
    strict_lower: bool,
) -> list[dict]:
    """Ohodnoti a stabilne utriedi populaciu."""

    scored = []
    for law in population:
        cost = estimate_law_cost(blocks, width_bits, original_size, law, max_index, strict_lower)
        scored.append({"law": law, "cost": cost})
    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law"].render()))
    return scored


def _migrate_individual(
    current: ContinuousLaw,
    leader: ContinuousLaw,
    blocks: list[int],
    width_bits: int,
    original_size: int,
    max_index: int,
    strict_lower: bool,
    rng: Random,
) -> ContinuousLaw:
    """Presunie jedinca po ceste smerom k liderovi a ponecha najlepsiu poziciu."""

    best_law = current
    best_cost = estimate_law_cost(blocks, width_bits, original_size, current, max_index, strict_lower)
    current_vector = list(current.params)
    leader_vector = list(leader.params)

    if current.family != leader.family and rng.random() < 0.25:
        current = ContinuousLaw(leader.family, current.params)
        best_law = current
        best_cost = estimate_law_cost(blocks, width_bits, original_size, current, max_index, strict_lower)

    step_count = int(_PATH_LENGTH / _STEP)
    for step_index in range(1, step_count + 1):
        t = step_index * _STEP
        mask = _prt_mask(rng, 3)
        candidate_vector = []
        for value, target, use_dim in zip(current_vector, leader_vector, mask):
            migrated = value + ((target - value) * t * use_dim)
            candidate_vector.append(_clip(migrated))
        candidate = ContinuousLaw(current.family, tuple(candidate_vector))
        candidate_cost = estimate_law_cost(blocks, width_bits, original_size, candidate, max_index, strict_lower)
        if (candidate_cost["total_bits"], candidate.render()) < (best_cost["total_bits"], best_law.render()):
            best_law = candidate
            best_cost = candidate_cost

    if rng.random() < 0.15:
        mutated = _random_perturbation(best_law, rng)
        mutated_cost = estimate_law_cost(blocks, width_bits, original_size, mutated, max_index, strict_lower)
        if (mutated_cost["total_bits"], mutated.render()) < (best_cost["total_bits"], best_law.render()):
            best_law = mutated

    return best_law


def _prt_mask(rng: Random, dimensions: int) -> list[int]:
    """Vrati PRT masku a zaruci, ze aspon jedna dimenzia ostane aktivna."""

    mask = [1 if rng.random() < _PRT else 0 for _ in range(dimensions)]
    if any(mask):
        return mask
    mask[rng.randrange(dimensions)] = 1
    return mask


def _random_law(rng: Random) -> ContinuousLaw:
    """Vrati nahodneho jedinca v povolenych hraniciach."""

    family = rng.choice(("affine", "quadratic"))
    values = tuple(rng.uniform(*_BOUNDS) for _ in range(3))
    if family == "affine":
        return ContinuousLaw(family, (values[0], values[1], 0.0))
    return ContinuousLaw(family, values)


def _random_perturbation(law: ContinuousLaw, rng: Random) -> ContinuousLaw:
    """Vykona malu lokalnu mutaciu spojitych parametrov."""

    values = list(law.params)
    index = rng.randrange(2 if law.family == "affine" else 3)
    values[index] = _clip(values[index] + rng.uniform(-1.5, 1.5))
    if law.family == "affine":
        values[2] = 0.0
    return ContinuousLaw(law.family, tuple(values))


def _clip(value: float) -> float:
    """Oreze parameter do bezpecnych hranic."""

    return max(_BOUNDS[0], min(_BOUNDS[1], value))
```

## File: `src/primesymbolicmdl/prime_anchors.py`

```python
"""Jednoduche deterministicke prvociselne kotvy."""

from __future__ import annotations

from functools import lru_cache
from math import isqrt


def is_prime(n: int) -> bool:
    """Vrati pravdu iba pre prvocisla."""

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limit = isqrt(n)
    for candidate in range(3, limit + 1, 2):
        if n % candidate == 0:
            return False
    return True


def primes_up_to(n: int) -> list[int]:
    """Vrati zoznam vsetkych prvocisel mensich alebo rovnych n."""

    if n < 2:
        return []

    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"

    for candidate in range(2, isqrt(n) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            count = ((n - start) // candidate) + 1
            sieve[start : n + 1 : candidate] = b"\x00" * count

    return [index for index, flag in enumerate(sieve) if flag]


def _integer_cuberoot(n: int) -> int:
    """Vrati celu tretiu odmocninu zaokruhlenu nadol."""

    if n < 0:
        raise ValueError("n must be non-negative")

    candidate = int(round(n ** (1.0 / 3.0)))
    while (candidate + 1) ** 3 <= n:
        candidate += 1
    while candidate**3 > n:
        candidate -= 1
    return candidate


@lru_cache(maxsize=None)
def _phi(x: int, a: int) -> int:
    """Vrati pocet cisel do x nesudelitelnych prvymi a prvocislami."""

    if a == 0:
        return x
    return _phi(x, a - 1) - _phi(x // _SMALL_PRIMES[a - 1], a - 1)


_SMALL_PRIMES = tuple(primes_up_to(10_000))
_DIRECT_COUNT_LIMIT = 1_000_000


@lru_cache(maxsize=None)
def prime_count(n: int) -> int:
    """Vrati presny pocet prvocisel mensich alebo rovnych n."""

    if n < 2:
        return 0
    if n <= _DIRECT_COUNT_LIMIT:
        return len(primes_up_to(n))

    fourth_root = isqrt(isqrt(n))
    square_root = isqrt(n)
    cube_root = _integer_cuberoot(n)

    a = prime_count(fourth_root)
    b = prime_count(square_root)
    c = prime_count(cube_root)
    primes = primes_up_to(square_root)

    total = _phi(n, a) + ((b + a - 2) * (b - a + 1) // 2)

    for i in range(a + 1, b + 1):
        prime_i = primes[i - 1]
        quotient = n // prime_i
        total -= prime_count(quotient)

        if i <= c:
            quotient_root = isqrt(quotient)
            quotient_root_count = prime_count(quotient_root)
            for j in range(i, quotient_root_count + 1):
                total -= prime_count(quotient // primes[j - 1]) - (j - 1)

    return total


def nearest_lower_prime(n: int) -> int | None:
    """Vrati najblizsie prvocislo zdola alebo None, ak neexistuje."""

    if n < 2:
        return None
    if n == 2:
        return 2

    candidate = n if n % 2 == 1 else n - 1
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 2
    return None


def nearest_upper_prime(n: int) -> int:
    """Vrati najblizsie prvocislo zhora."""

    if n <= 2:
        return 2
    if n == 3:
        return 3

    candidate = n if n % 2 == 1 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def nearest_prime(n: int) -> int:
    """Vrati najblizsie prvocislo, pri remize preferuje spodnu kotvu."""

    lower = nearest_lower_prime(n)
    upper = nearest_upper_prime(n)

    if lower is None:
        return upper
    if (n - lower) <= (upper - n):
        return lower
    return upper


def prime_anchor_residual(x: int, mode: str) -> tuple[int, int]:
    """Vrati kotvu a reziduum tak, aby platilo x == kotva + reziduum."""

    if mode == "lower":
        anchor = nearest_lower_prime(x)
        if anchor is None:
            anchor = 2
    elif mode == "upper":
        anchor = nearest_upper_prime(x)
    elif mode == "nearest":
        anchor = nearest_prime(x)
    else:
        raise ValueError(f"Unsupported prime-anchor mode: {mode}")

    return anchor, x - anchor
```

## File: `src/primesymbolicmdl/prime_bigint.py`

```python
"""Deterministicke 64-bit prvociselne utility bez probabilistickych skratiek."""

from __future__ import annotations

from functools import lru_cache

_MAX_UINT64 = 1 << 64
_MR_BASES_64 = (2, 325, 9_375, 28_178, 450_775, 9_780_504, 1_795_265_022)
_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _validate_uint64_domain(n: int) -> None:
    """Overi, ze vstup patri do podporovaneho 64-bit priestoru."""

    if n >= _MAX_UINT64:
        raise ValueError("Exact prime utilities currently support only n < 2**64.")


@lru_cache(maxsize=131072)
def is_probably_prime_deterministic_64(n: int) -> bool:
    """Vrati presny vysledok pre prvociselnost v rozsahu n < 2**64."""

    if n < 2:
        return False
    _validate_uint64_domain(n)

    if n in _SMALL_PRIMES:
        return True
    for prime in _SMALL_PRIMES:
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for base in _MR_BASES_64:
        if base % n == 0:
            continue
        witness = pow(base, d, n)
        if witness in {1, n - 1}:
            continue
        for _ in range(s - 1):
            witness = pow(witness, 2, n)
            if witness == n - 1:
                break
        else:
            return False
    return True


@lru_cache(maxsize=131072)
def prev_prime_64(n: int) -> int | None:
    """Vrati najvacsie prvocislo mensie alebo rovne n, inak None."""

    if n < 2:
        return None
    _validate_uint64_domain(n)

    if n == 2:
        return 2

    candidate = n if n % 2 == 1 else n - 1
    while candidate >= 3:
        if is_probably_prime_deterministic_64(candidate):
            return candidate
        candidate -= 2
    return 2


@lru_cache(maxsize=131072)
def next_prime_64(n: int) -> int:
    """Vrati najmensie prvocislo vacsie alebo rovne n v 64-bit priestore."""

    if n <= 2:
        return 2
    _validate_uint64_domain(n)

    candidate = n if n % 2 == 1 else n + 1
    while candidate < _MAX_UINT64:
        if is_probably_prime_deterministic_64(candidate):
            return candidate
        candidate += 2

    raise ValueError("No exact 64-bit prime exists at or above the requested value.")
```

## File: `src/primesymbolicmdl/residual_binary.py`

```python
"""Binarna serializacia residual streamov pre exact-lossless roundtrip."""

from __future__ import annotations

from .bitstream import BitReader, BitWriter, decode_unsigned_varint, encode_unsigned_varint, zigzag_decode, zigzag_encode
from .residual_codecs import choose_best_residual_codec, signed_width_for_range

_CODEC_NAME_TO_ID = {
    "fixed_signed": 0,
    "zero_rle": 1,
    "varint_residuals": 2,
}
_CODEC_ID_TO_NAME = {value: key for key, value in _CODEC_NAME_TO_ID.items()}


def encode_residuals_binary(residuals: list[int], codec_name: str | None = None) -> bytes:
    """Zakoduje residual stream do realnych bytes."""

    values = [int(value) for value in residuals]
    chosen_codec = _select_codec_name(values, codec_name)

    if chosen_codec == "fixed_signed":
        return _encode_fixed_signed(values)
    if chosen_codec == "zero_rle":
        return _encode_zero_rle(values)
    return _encode_varint_residuals(values)


def decode_residuals_binary(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje residual stream z binarneho payloadu."""

    if not isinstance(residual_count, int) or residual_count < 0:
        raise ValueError("residual_count must be a non-negative integer")

    payload = bytes(blob)
    codec_id, offset = decode_unsigned_varint(payload, 0)
    codec_name = _CODEC_ID_TO_NAME.get(codec_id)
    if codec_name is None:
        raise ValueError(f"Unsupported residual binary codec id: {codec_id}")

    body = payload[offset:]
    if codec_name == "fixed_signed":
        return _decode_fixed_signed(body, residual_count)
    if codec_name == "zero_rle":
        return _decode_zero_rle(body, residual_count)
    return _decode_varint_residuals(body, residual_count)


def _select_codec_name(residuals: list[int], codec_name: str | None) -> str:
    """Vyberie finalne meno codec-u pre binarnu serializaciu."""

    if codec_name is None:
        return choose_best_residual_codec(residuals).codec_name
    if codec_name in _CODEC_NAME_TO_ID:
        return codec_name
    return "varint_residuals"


def _encode_fixed_signed(residuals: list[int]) -> bytes:
    """Zakoduje residualy do fixed-width zigzag bitstreamu."""

    if residuals:
        width = signed_width_for_range(min(residuals), max(residuals))
    else:
        width = 0

    output = bytearray()
    output.extend(encode_unsigned_varint(_CODEC_NAME_TO_ID["fixed_signed"]))
    output.extend(encode_unsigned_varint(width))
    if width == 0:
        return bytes(output)

    writer = BitWriter()
    for value in residuals:
        writer.write_bits(zigzag_encode(value), width)
    output.extend(writer.to_bytes())
    return bytes(output)


def _decode_fixed_signed(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje fixed-width residual stream."""

    width, offset = decode_unsigned_varint(blob, 0)
    payload = blob[offset:]

    if width == 0:
        if payload:
            raise ValueError("Zero-width fixed_signed payload must not contain extra bytes")
        return [0] * residual_count

    reader = BitReader(payload)
    values = [zigzag_decode(reader.read_bits(width)) for _ in range(residual_count)]
    _validate_zero_padding(payload, residual_count * width, "fixed_signed payload")
    return values


def _encode_zero_rle(residuals: list[int]) -> bytes:
    """Zakoduje residualy cez jednoduchy zero-run varint stream."""

    output = bytearray()
    output.extend(encode_unsigned_varint(_CODEC_NAME_TO_ID["zero_rle"]))

    index = 0
    while index < len(residuals):
        if residuals[index] == 0:
            run_length = 1
            index += 1
            while index < len(residuals) and residuals[index] == 0:
                run_length += 1
                index += 1
            output.extend(encode_unsigned_varint((run_length - 1) << 1))
            continue

        output.extend(encode_unsigned_varint((zigzag_encode(residuals[index]) << 1) | 1))
        index += 1

    return bytes(output)


def _decode_zero_rle(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje zero-run varint stream na povodne residualy."""

    values: list[int] = []
    offset = 0

    while len(values) < residual_count:
        token, offset = decode_unsigned_varint(blob, offset)
        if token & 1:
            values.append(zigzag_decode(token >> 1))
            continue

        run_length = (token >> 1) + 1
        if len(values) + run_length > residual_count:
            raise ValueError("zero_rle payload exceeds declared residual_count")
        values.extend([0] * run_length)

    if offset != len(blob):
        raise ValueError("zero_rle payload has trailing bytes")
    return values


def _encode_varint_residuals(residuals: list[int]) -> bytes:
    """Zakoduje residualy cez fallback zigzag varinty."""

    output = bytearray()
    output.extend(encode_unsigned_varint(_CODEC_NAME_TO_ID["varint_residuals"]))
    for value in residuals:
        output.extend(encode_unsigned_varint(zigzag_encode(value)))
    return bytes(output)


def _decode_varint_residuals(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje fallback varint residual stream."""

    offset = 0
    values: list[int] = []
    for _ in range(residual_count):
        encoded, offset = decode_unsigned_varint(blob, offset)
        values.append(zigzag_decode(encoded))
    if offset != len(blob):
        raise ValueError("varint_residuals payload has trailing bytes")
    return values


def _validate_zero_padding(payload: bytes, used_bits: int, label: str) -> None:
    """Overi, ze padding za skutocnymi datami zostal nulovy."""

    total_bits = len(payload) * 8
    if used_bits > total_bits:
        raise ValueError(f"{label} is shorter than required")
    if used_bits == total_bits:
        return

    full_bytes, used_tail_bits = divmod(used_bits, 8)
    if used_tail_bits:
        mask = (1 << (8 - used_tail_bits)) - 1
        if payload[full_bytes] & mask:
            raise ValueError(f"{label} contains non-zero padding bits")
        full_bytes += 1

    for byte_value in payload[full_bytes:]:
        if byte_value:
            raise ValueError(f"{label} contains non-zero trailing bytes")
```

## File: `src/primesymbolicmdl/residual_codecs.py`

```python
"""Male deterministicke codec baseline vrstvy pre rezidua a bajtove streamy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResidualCodecResult:
    """Stabilny vysledok jedneho residual alebo byte codec kandidata."""

    codec_name: str
    bits: int
    payload: dict
    details: dict


def zigzag_encode(n: int) -> int:
    """Prevedie podpisane cele cislo na nezaporny zigzag tvar."""

    value = int(n)
    return (value << 1) if value >= 0 else ((-value << 1) - 1)


def zigzag_decode(z: int) -> int:
    """Vrati povodne podpisane cele cislo zo zigzag reprezentacie."""

    value = int(z)
    if value < 0:
        raise ValueError("zigzag value must be non-negative")
    if value % 2 == 0:
        return value // 2
    return -((value + 1) // 2)


def signed_width_for_range(min_value: int, max_value: int) -> int:
    """Vrati minimalnu signed fixed-width sirku pre zadany rozsah."""

    if min_value > max_value:
        raise ValueError("min_value must not exceed max_value")
    if min_value == 0 and max_value == 0:
        return 0

    width = 1
    while min_value < -(1 << (width - 1)) or max_value > ((1 << (width - 1)) - 1):
        width += 1
    return width


def unsigned_width_for_max(max_value: int) -> int:
    """Vrati minimalnu unsigned fixed-width sirku pre rozsah 0..max_value."""

    if max_value < 0:
        raise ValueError("max_value must be non-negative")
    if max_value == 0:
        return 0

    width = 0
    limit = 1
    while limit <= max_value:
        width += 1
        limit <<= 1
    return width


def estimate_fixed_signed_residual_bits(residuals: list[int]) -> ResidualCodecResult:
    """Vrati fixed-width signed baseline pre residual stream."""

    values = [int(value) for value in residuals]
    if not values:
        return ResidualCodecResult(
            codec_name="fixed_signed",
            bits=0,
            payload={"codec": "fixed_signed", "count": 0, "residual_width": 0, "values": []},
            details={"count": 0, "min_residual": 0, "max_residual": 0, "residual_width": 0},
        )

    min_residual = min(values)
    max_residual = max(values)
    residual_width = signed_width_for_range(min_residual, max_residual)
    bits = residual_width * len(values)
    payload_values = [] if residual_width == 0 else [zigzag_encode(value) for value in values]
    return ResidualCodecResult(
        codec_name="fixed_signed",
        bits=bits,
        payload={
            "codec": "fixed_signed",
            "count": len(values),
            "residual_width": residual_width,
            "values": payload_values,
        },
        details={
            "count": len(values),
            "min_residual": min_residual,
            "max_residual": max_residual,
            "residual_width": residual_width,
        },
    )


def decode_fixed_signed_residual_payload(payload: dict) -> list[int]:
    """Dekoduje research payload fixed signed residual codec-u."""

    count = payload.get("count")
    residual_width = payload.get("residual_width")
    values = payload.get("values")

    if payload.get("codec") not in {None, "fixed_signed"}:
        raise ValueError("Unsupported fixed signed payload codec")
    if not isinstance(count, int) or count < 0:
        raise ValueError("count must be a non-negative integer")
    if not isinstance(residual_width, int) or residual_width < 0:
        raise ValueError("residual_width must be a non-negative integer")
    if not isinstance(values, list):
        raise ValueError("values must be a list")

    if residual_width == 0:
        return [0] * count
    if len(values) != count:
        raise ValueError("values length does not match count")
    return [zigzag_decode(value) for value in values]


def estimate_zero_rle_residual_bits(residuals: list[int]) -> ResidualCodecResult:
    """Vrati zero-run-length codec baseline pre residual stream."""

    values = [int(value) for value in residuals]
    if not values:
        return ResidualCodecResult(
            codec_name="zero_rle",
            bits=0,
            payload={
                "codec": "zero_rle",
                "count": 0,
                "tokens": [],
                "run_length_width": 0,
                "literal_width": 0,
            },
            details={
                "count": 0,
                "token_count": 0,
                "zero_token_count": 0,
                "literal_token_count": 0,
                "max_run_length": 0,
                "run_length_width": 0,
                "literal_width": 0,
            },
        )

    tokens: list[dict] = []
    index = 0
    while index < len(values):
        if values[index] == 0:
            run_length = 1
            index += 1
            while index < len(values) and values[index] == 0:
                run_length += 1
                index += 1
            tokens.append({"kind": "zero_run", "run_length": run_length})
            continue

        tokens.append({"kind": "literal", "value": zigzag_encode(values[index])})
        index += 1

    run_lengths = [token["run_length"] for token in tokens if token["kind"] == "zero_run"]
    literal_values = [value for value in values if value != 0]
    max_run_length = max(run_lengths, default=0)
    run_length_width = unsigned_width_for_max(max_run_length)
    if literal_values:
        literal_width = signed_width_for_range(min(literal_values), max(literal_values))
    else:
        literal_width = 0

    bits = 0
    for token in tokens:
        bits += 1
        if token["kind"] == "zero_run":
            bits += run_length_width
        else:
            bits += literal_width

    return ResidualCodecResult(
        codec_name="zero_rle",
        bits=bits,
        payload={
            "codec": "zero_rle",
            "count": len(values),
            "tokens": tokens,
            "run_length_width": run_length_width,
            "literal_width": literal_width,
        },
        details={
            "count": len(values),
            "token_count": len(tokens),
            "zero_token_count": len(run_lengths),
            "literal_token_count": len(literal_values),
            "max_run_length": max_run_length,
            "run_length_width": run_length_width,
            "literal_width": literal_width,
        },
    )


def decode_zero_rle_residual_payload(payload: dict) -> list[int]:
    """Dekoduje research payload zero-RLE residual codec-u."""

    count = payload.get("count")
    tokens = payload.get("tokens")

    if payload.get("codec") not in {None, "zero_rle"}:
        raise ValueError("Unsupported zero_rle payload codec")
    if not isinstance(count, int) or count < 0:
        raise ValueError("count must be a non-negative integer")
    if not isinstance(tokens, list):
        raise ValueError("tokens must be a list")

    decoded: list[int] = []
    for token in tokens:
        if not isinstance(token, dict):
            raise ValueError("token must be a dict")
        kind = token.get("kind")
        if kind == "zero_run":
            run_length = token.get("run_length")
            if not isinstance(run_length, int) or run_length <= 0:
                raise ValueError("zero_run token requires a positive run_length")
            decoded.extend([0] * run_length)
            continue
        if kind == "literal":
            value = token.get("value")
            if not isinstance(value, int):
                raise ValueError("literal token requires an integer value")
            decoded.append(zigzag_decode(value))
            continue
        raise ValueError(f"Unsupported token kind: {kind}")

    if len(decoded) != count:
        raise ValueError("Decoded residual count does not match payload count")
    return decoded


def estimate_byte_rle_bits(data: bytes) -> ResidualCodecResult:
    """Vrati byte-run-length baseline pre bajtovy stream."""

    payload = bytes(data)
    if not payload:
        return ResidualCodecResult(
            codec_name="byte_rle",
            bits=0,
            payload={"codec": "byte_rle", "length": 0, "tokens": [], "run_length_width": 0},
            details={"length": 0, "token_count": 0, "max_run_length": 0, "run_length_width": 0},
        )

    tokens: list[dict] = []
    index = 0
    while index < len(payload):
        value = payload[index]
        run_length = 1
        index += 1
        while index < len(payload) and payload[index] == value:
            run_length += 1
            index += 1
        tokens.append({"run_length": run_length, "byte_value": value})

    max_run_length = max(token["run_length"] for token in tokens)
    run_length_width = unsigned_width_for_max(max_run_length)
    bits = len(tokens) * (run_length_width + 8)
    return ResidualCodecResult(
        codec_name="byte_rle",
        bits=bits,
        payload={
            "codec": "byte_rle",
            "length": len(payload),
            "tokens": tokens,
            "run_length_width": run_length_width,
        },
        details={
            "length": len(payload),
            "token_count": len(tokens),
            "max_run_length": max_run_length,
            "run_length_width": run_length_width,
            "token_bits": run_length_width + 8,
        },
    )


def decode_byte_rle_payload(payload: dict) -> bytes:
    """Dekoduje research payload byte-RLE codec-u."""

    length = payload.get("length")
    tokens = payload.get("tokens")

    if payload.get("codec") not in {None, "byte_rle"}:
        raise ValueError("Unsupported byte_rle payload codec")
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if not isinstance(tokens, list):
        raise ValueError("tokens must be a list")

    decoded = bytearray()
    for token in tokens:
        if not isinstance(token, dict):
            raise ValueError("token must be a dict")
        run_length = token.get("run_length")
        byte_value = token.get("byte_value")
        if not isinstance(run_length, int) or run_length <= 0:
            raise ValueError("run_length must be a positive integer")
        if not isinstance(byte_value, int) or byte_value < 0 or byte_value > 255:
            raise ValueError("byte_value must be in range 0..255")
        decoded.extend([byte_value] * run_length)

    if len(decoded) != length:
        raise ValueError("Decoded byte length does not match payload length")
    return bytes(decoded)


def choose_best_residual_codec(residuals: list[int]) -> ResidualCodecResult:
    """Vyberie najlacnejsi residual codec kandidat pre zadany stream."""

    candidates = [
        estimate_fixed_signed_residual_bits(residuals),
        estimate_zero_rle_residual_bits(residuals),
    ]
    return min(enumerate(candidates), key=lambda item: (item[1].bits, item[0]))[1]


def choose_best_byte_codec(data: bytes) -> ResidualCodecResult:
    """Vyberie najlacnejsi byte codec kandidat pre zadany bajtovy stream."""

    payload = bytes(data)
    candidates = [
        ResidualCodecResult(
            codec_name="raw_bytes",
            bits=len(payload) * 8,
            payload={"codec": "raw_bytes", "data": payload},
            details={"length": len(payload)},
        ),
        estimate_byte_rle_bits(payload),
    ]
    return min(enumerate(candidates), key=lambda item: (item[1].bits, item[0]))[1]
```

## File: `src/primesymbolicmdl/scaled_prime_demo.py`

```python
"""Kratke CLI demo pre scaled prime-index branch."""

from __future__ import annotations

from .experiments import dataset_random
from .scaled_prime_search import search_best_scaled_prime_model


def run_demo() -> list[dict]:
    """Spusti malu deterministicku sadu scaled-prime experimentov."""

    datasets = [
        ("ascii_small", b"prime-index-demo", (16, 24, 32, 64)),
        ("ramp_bytes", bytes(range(24)), (16, 24, 32)),
        ("random_bytes", dataset_random(24, seed=1234), (16, 24, 32)),
        ("repeating_pattern", b"ABCDABCDABCDABCD", (16, 24, 32, 64)),
    ]

    results: list[dict] = []
    for dataset_name, data, widths in datasets:
        for width_bits in widths:
            search = search_best_scaled_prime_model(data, width_bits=width_bits)
            results.append(
                {
                    "dataset": dataset_name,
                    "size_bytes": len(data),
                    "width_bits": width_bits,
                    "best_model": search["best_model"],
                    "best_model_string": search["best_model_string"],
                    "raw_bits": search["raw_bits"],
                    "total_bits": search["total_bits"],
                    "saving_bits": search["saving_bits"],
                    "ratio_vs_raw": search["ratio_vs_raw"],
                    "residual_codec": search["residual_codec"],
                    "escape_count": search["escape_count"],
                    "roundtrip_ok": search["roundtrip_ok"],
                    "decision": "win" if search["total_bits"] < search["raw_bits"] else "raw_fallback",
                }
            )
    return results


def format_scaled_prime_result(result: dict) -> str:
    """Vrati stabilny textovy report jedneho demo vysledku."""

    lines = [
        f"dataset: {result['dataset']}",
        f"size_bytes: {result['size_bytes']}",
        f"width_bits: {result['width_bits']}",
        f"best_model: {result['best_model_string']}",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}" if result["ratio_vs_raw"] != float("inf") else "ratio_vs_raw: inf",
        f"residual_codec: {result['residual_codec']}",
        f"escape_count: {result['escape_count']}",
        f"roundtrip_ok: {result['roundtrip_ok']}",
        f"decision: {result['decision']}",
    ]
    return "\n".join(lines)


def main() -> None:
    """Vypise scaled-prime demo reporty do stdout."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_scaled_prime_result(result))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/scaled_prime_index.py`

```python
"""Scaled prime-index branch s exact 64-bit prvociselnymi anchor-mi."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks, huge_blocks_to_bytes
from .prime_bigint import prev_prime_64
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
    unsigned_width_for_max,
)

_FIXED_MODEL_BITS = 12
_FIXED_HEADER_BITS = 32
_MAX_UINT64 = 1 << 64


@dataclass(frozen=True, order=True)
class ScaledPrimeModel:
    """Parametre scaled prime-index modelu."""

    shift: int
    direction: str
    search_radius: int


def render_scaled_prime_model(model: ScaledPrimeModel) -> str:
    """Vrati stabilnu textualnu reprezentaciu modelu."""

    _validate_model(model)
    return f"scaled_prime(direction={model.direction}, shift={model.shift}, search_radius={model.search_radius})"


def model_bits_scaled_prime(model: ScaledPrimeModel) -> int:
    """Vrati fixnu cenu identifikacie scaled-prime vetvy."""

    _validate_model(model)
    return _FIXED_MODEL_BITS


def parameter_bits_scaled_prime(model: ScaledPrimeModel) -> int:
    """Vrati konzervativny odhad ceny parametrov modelu."""

    _validate_model(model)
    direction_bits = 2
    return direction_bits + unsigned_width_for_max(model.shift) + unsigned_width_for_max(model.search_radius)


def encode_block_scaled_prime(x: int, width_bits: int, model: ScaledPrimeModel) -> dict:
    """Zakoduje jeden blok cez scaled prime-index anchor alebo vrati escape."""

    _validate_width_bits(width_bits)
    _validate_model(model)
    _validate_block_value(x, width_bits)

    base_index = x >> model.shift
    lower_index = max(0, base_index - model.search_radius)
    upper_index = base_index + model.search_radius

    best: tuple[int, int, int, int] | None = None

    for index in range(lower_index, upper_index + 1):
        anchor = _anchor_from_index(index, model)
        if anchor is None or anchor > x:
            continue

        diff = x - anchor
        candidate = (abs(diff), _rough_local_cost(index, diff), index, anchor)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return {
            "index": None,
            "anchor": 0,
            "diff": x,
            "escaped": True,
            "base_index": base_index,
        }

    _, _, index, anchor = best
    return {
        "index": index,
        "anchor": anchor,
        "diff": x - anchor,
        "escaped": False,
        "base_index": base_index,
    }


def estimate_scaled_prime_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    model: ScaledPrimeModel,
) -> dict:
    """Spocita plny MDL-style cost scaled-prime vetvy bez auto fallbacku."""

    _validate_width_bits(width_bits)
    _validate_model(model)
    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")

    for block in blocks:
        _validate_block_value(int(block), width_bits)

    raw_bits = original_size * 8
    block_count = len(blocks)
    flag_bits = block_count
    encoded_blocks = [encode_block_scaled_prime(int(block), width_bits, model) for block in blocks]

    indices = [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    escape_count = sum(1 for entry in encoded_blocks if entry["escaped"])

    if indices:
        index_width = unsigned_width_for_max(max(indices))
        index_bits = index_width * len(indices)
    else:
        index_bits = 0

    residual_codec = choose_best_residual_codec(residuals)
    residual_bits = residual_codec.bits
    model_bits = model_bits_scaled_prime(model)
    parameter_bits = parameter_bits_scaled_prime(model)
    escape_bits = width_bits * escape_count
    total_bits = (
        model_bits
        + parameter_bits
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )
    saving_bits = raw_bits - total_bits

    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "block_count": block_count,
        "model": render_scaled_prime_model(model),
    }


def encode_scaled_prime_payload(data: bytes, width_bits: int, model: ScaledPrimeModel) -> dict:
    """Zakoduje data do exact payloadu scaled-prime vetvy."""

    _validate_width_bits(width_bits)
    _validate_model(model)

    payload = bytes(data)
    blocks = bytes_to_huge_blocks(payload, width_bits)
    encoded_blocks = [encode_block_scaled_prime(block, width_bits, model) for block in blocks]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    residual_codec = choose_best_residual_codec(residuals)

    return {
        "codec": "scaled_prime_index",
        "width_bits": width_bits,
        "original_size": len(payload),
        "block_count": len(blocks),
        "model": {
            "shift": model.shift,
            "direction": model.direction,
            "search_radius": model.search_radius,
        },
        "flags": [bool(entry["escaped"]) for entry in encoded_blocks],
        "indices": [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None],
        "raw_blocks": [int(block) for block, entry in zip(blocks, encoded_blocks) if entry["escaped"]],
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "residual_payload": residual_codec.payload,
    }


def decode_scaled_prime_payload(payload: dict) -> bytes:
    """Dekoduje payload scaled-prime vetvy spat na povodne bajty."""

    if payload.get("codec") not in {None, "scaled_prime_index"}:
        raise ValueError("Unsupported scaled-prime payload codec")

    width_bits = payload.get("width_bits")
    original_size = payload.get("original_size")
    block_count = payload.get("block_count")
    flags = payload.get("flags")
    indices = payload.get("indices")
    raw_blocks = payload.get("raw_blocks")
    model_payload = payload.get("model")
    residual_payload = payload.get("residual_payload")

    if not isinstance(width_bits, int):
        raise ValueError("width_bits must be an integer")
    if not isinstance(original_size, int) or original_size < 0:
        raise ValueError("original_size must be a non-negative integer")
    if not isinstance(block_count, int) or block_count < 0:
        raise ValueError("block_count must be a non-negative integer")
    if not isinstance(flags, list):
        raise ValueError("flags must be a list")
    if not isinstance(indices, list):
        raise ValueError("indices must be a list")
    if not isinstance(raw_blocks, list):
        raise ValueError("raw_blocks must be a list")
    if not isinstance(model_payload, dict):
        raise ValueError("model must be a dict")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")

    _validate_width_bits(width_bits)
    if len(flags) != block_count:
        raise ValueError("flags length does not match block_count")

    model = ScaledPrimeModel(
        shift=int(model_payload.get("shift")),
        direction=str(model_payload.get("direction")),
        search_radius=int(model_payload.get("search_radius")),
    )
    _validate_model(model)

    residuals = _decode_residual_payload(residual_payload)
    index_position = 0
    residual_position = 0
    raw_position = 0
    decoded_blocks: list[int] = []

    for flag in flags:
        escaped = _coerce_flag(flag)
        if escaped:
            if raw_position >= len(raw_blocks):
                raise ValueError("raw_blocks are shorter than escape flags")
            block = int(raw_blocks[raw_position])
            raw_position += 1
            decoded_blocks.append(block)
            continue

        if index_position >= len(indices):
            raise ValueError("indices are shorter than non-escape flags")
        if residual_position >= len(residuals):
            raise ValueError("residual stream is shorter than non-escape flags")

        index = int(indices[index_position])
        residual = int(residuals[residual_position])
        index_position += 1
        residual_position += 1

        anchor = _anchor_from_index(index, model)
        if anchor is None:
            raise ValueError("Stored index cannot reconstruct a valid prime anchor")
        decoded_blocks.append(anchor + residual)

    if index_position != len(indices):
        raise ValueError("Unused indices remain after decoding")
    if residual_position != len(residuals):
        raise ValueError("Unused residual values remain after decoding")
    if raw_position != len(raw_blocks):
        raise ValueError("Unused raw blocks remain after decoding")

    return huge_blocks_to_bytes(decoded_blocks, width_bits, original_size)


def roundtrip_scaled_prime(data: bytes, width_bits: int, model: ScaledPrimeModel) -> bytes:
    """Zakoduje a spatne dekoduje data cez scaled-prime payload."""

    return decode_scaled_prime_payload(encode_scaled_prime_payload(bytes(data), width_bits, model))


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze sirka blokov patri medzi podporovane hodnoty vetvy."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS or width_bits > 64:
        raise ValueError(f"Scaled-prime branch supports only width_bits <= 64 from {sorted(value for value in SUPPORTED_HUGE_WIDTHS if value <= 64)}.")


def _validate_model(model: ScaledPrimeModel) -> None:
    """Overi, ze model patri do zatial podporovanej podmnoziny."""

    if not isinstance(model.shift, int) or model.shift < 1:
        raise ValueError("shift must be a positive integer")
    if model.direction != "lower":
        raise ValueError('Only direction="lower" is currently supported')
    if not isinstance(model.search_radius, int) or model.search_radius < 0:
        raise ValueError("search_radius must be a non-negative integer")


def _validate_block_value(x: int, width_bits: int) -> None:
    """Overi rozsah jedneho bloku pre danu sirku."""

    if x < 0 or x >= (1 << width_bits):
        raise ValueError(f"Block out of range for {width_bits} bits: {x}")


def _rough_local_cost(index: int, diff: int) -> int:
    """Vrati hruby lokalny cost pre rozlisovanie remiz kandidatov."""

    return unsigned_width_for_max(index) + signed_width_for_range(diff, diff)


def _anchor_from_index(index: int, model: ScaledPrimeModel) -> int | None:
    """Rekonstruuje lower-prime anchor z indexu a modelu."""

    if index < 0:
        raise ValueError("index must be non-negative")

    base = index << model.shift
    if base >= _MAX_UINT64:
        return None
    return prev_prime_64(base)


def _decode_residual_payload(payload: dict) -> list[int]:
    """Dekoduje residual payload podla ulozeneho codec mena."""

    codec_name = payload.get("codec")
    if codec_name in {None, "fixed_signed"}:
        return decode_fixed_signed_residual_payload(payload)
    if codec_name == "zero_rle":
        return decode_zero_rle_residual_payload(payload)
    raise ValueError(f"Unsupported residual payload codec: {codec_name}")


def _coerce_flag(flag: object) -> bool:
    """Prevedie payload flag na bool s kontrolou povoleneho tvaru."""

    if isinstance(flag, bool):
        return flag
    if isinstance(flag, int) and flag in {0, 1}:
        return bool(flag)
    raise ValueError("Flag values must be bool or 0/1 integers")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer ceny modelu voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
```

## File: `src/primesymbolicmdl/scaled_prime_search.py`

```python
"""Deterministicke hladanie najlepsieho scaled-prime modelu."""

from __future__ import annotations

from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks
from .scaled_prime_index import (
    ScaledPrimeModel,
    estimate_scaled_prime_cost,
    render_scaled_prime_model,
    roundtrip_scaled_prime,
)


def search_best_scaled_prime_model(
    data: bytes,
    width_bits: int = 32,
    shifts: tuple[int, ...] | None = None,
    search_radii: tuple[int, ...] = (0, 1, 2, 4),
    seed: int = 1234,
) -> dict:
    """Vyskusa malu deterministicku mriezku scaled-prime modelov."""

    del seed

    payload = bytes(data)
    _validate_search_width(width_bits)
    if not search_radii:
        raise ValueError("search_radii must not be empty")

    resolved_shifts = shifts if shifts is not None else _default_shifts(width_bits)
    if not resolved_shifts:
        raise ValueError("No shifts are available for the selected width")

    blocks = bytes_to_huge_blocks(payload, width_bits)
    history: list[dict] = []
    best_model: ScaledPrimeModel | None = None
    best_cost: dict | None = None
    best_key: tuple[int, int, int, int] | None = None

    candidate_index = 0
    for shift in resolved_shifts:
        for search_radius in search_radii:
            model = ScaledPrimeModel(shift=shift, direction="lower", search_radius=search_radius)
            cost = estimate_scaled_prime_cost(blocks, width_bits, len(payload), model)
            history.append(
                {
                    "candidate_index": candidate_index,
                    "shift": shift,
                    "search_radius": search_radius,
                    "model": render_scaled_prime_model(model),
                    "total_bits": cost["total_bits"],
                    "saving_bits": cost["saving_bits"],
                    "ratio_vs_raw": cost["ratio_vs_raw"],
                    "escape_count": cost["escape_count"],
                    "residual_codec": cost["residual_codec"],
                }
            )
            candidate_index += 1

            candidate_key = (cost["total_bits"], cost["parameter_bits"], shift, search_radius)
            if best_key is None or candidate_key < best_key:
                best_key = candidate_key
                best_model = model
                best_cost = cost

    if best_model is None or best_cost is None:
        raise RuntimeError("Scaled-prime search did not produce any candidate model")

    roundtrip_ok = roundtrip_scaled_prime(payload, width_bits, best_model) == payload
    return {
        "best_model": best_model,
        "best_model_string": render_scaled_prime_model(best_model),
        "raw_bits": best_cost["raw_bits"],
        "total_bits": best_cost["total_bits"],
        "saving_bits": best_cost["saving_bits"],
        "ratio_vs_raw": best_cost["ratio_vs_raw"],
        "history": history,
        "width_bits": width_bits,
        "roundtrip_ok": roundtrip_ok,
        "residual_codec": best_cost["residual_codec"],
        "escape_count": best_cost["escape_count"],
        "block_count": best_cost["block_count"],
        "cost_details": best_cost,
    }


def _validate_search_width(width_bits: int) -> None:
    """Overi, ze hladanie bezi iba v presne podporovanom rozsahu."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS or width_bits > 64:
        raise ValueError("Scaled-prime search currently supports only exact widths up to 64 bits.")


def _default_shifts(width_bits: int) -> tuple[int, ...]:
    """Vrati rozumne default shift kandidaty pre danu sirku bloku."""

    if width_bits == 8:
        return tuple(range(1, 7))
    if width_bits == 16:
        return tuple(range(1, 13))
    if width_bits == 24:
        return tuple(range(1, 21))
    if width_bits == 32:
        return tuple(range(1, 29))
    if width_bits == 40:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36)
    if width_bits == 48:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40)
    if width_bits == 56:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    if width_bits == 64:
        return (8, 12, 16, 20, 24, 28, 32)
    raise ValueError(f"Unsupported width for default shift selection: {width_bits}")
```

## File: `src/primesymbolicmdl/sim_demo.py`

```python
"""Krátke CLI demo simulacie optimizerov nad obrazkami."""

from __future__ import annotations

from .image_ablation import format_image_ablation_table, run_image_gplite_ablation
from .simulation import format_simulation_report, run_image_simulation


def run_demo() -> list[dict]:
    """Spusti malu sadu rychlych demo behov nad obrazkami."""

    shared = {
        "image_width": 16,
        "image_height": 16,
        "seed": 1234,
        "population_size": 12,
        "generations": 8,
        "max_index": 15,
        "strict_lower": False,
    }
    return [
        run_image_simulation("Image-predictor", dataset_name="gradient", **shared),
        run_image_simulation("Image-GP-lite", dataset_name="gradient", **shared),
        run_image_simulation("Image-SOMA", dataset_name="gradient", **shared),
        run_image_simulation("Image-predictor", dataset_name="checker", **shared),
        run_image_simulation("Image-GP-lite", dataset_name="checker", **shared),
        run_image_simulation("GP-lite", dataset_name="gradient", **shared),
        run_image_simulation("SOMA", dataset_name="gradient", **shared),
    ]


def main() -> None:
    """Vypise reporty pre rychlu sadu obrazkovych demo behov."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_simulation_report(result))

    print()
    print("## Image-GP-lite primitive ablation summary: gradient")
    print(format_image_ablation_table(run_image_gplite_ablation("gradient", width=16, height=16, seed=1234, population_size=16, generations=8)))
    print()
    print("## Image-GP-lite primitive ablation summary: checker")
    print(format_image_ablation_table(run_image_gplite_ablation("checker", width=16, height=16, seed=1234, population_size=16, generations=8)))


if __name__ == "__main__":
    main()
```

## File: `src/primesymbolicmdl/simulation.py`

```python
"""Headless simulacia optimizerov nad malymi grayscale datasetmi."""

from __future__ import annotations

from .image_datasets import GrayImage, make_gray_image, make_image_dataset
from .image_law_branch import build_image_law_trace, decode_image_law_payload
from .image_predictor_branch import build_image_predictor_trace, decode_image_predictor_payload
from .index_branch import encode_block_with_law, roundtrip_law_payload
from .optimizers import OptimizerRequest, run_optimizer
from .optimizers.image_soma import build_image_soma_trace, decode_image_soma_payload
from .residual_codecs import choose_best_byte_codec


def bits_to_bytes_ceil(bit_count: int) -> int:
    """Prevedie bitovy odhad na konzervativny pocet bajtov."""

    if bit_count < 0:
        raise ValueError("bit_count must be non-negative")
    return (bit_count + 7) // 8


def run_gray_image_simulation(
    optimizer_name: str,
    image: GrayImage,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
    max_index: int | None = None,
    strict_lower: bool = False,
    image_gplite_primitive_set: str | None = None,
) -> dict:
    """Spusti vybrany optimizer nad konkretnym grayscale obrazkom."""

    metadata = {
        "image_width": image.width,
        "image_height": image.height,
        "dataset_name": image.name,
    }
    if image_gplite_primitive_set is not None:
        metadata["image_gplite_primitive_set"] = image_gplite_primitive_set

    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=seed,
        population_size=population_size,
        generations=generations,
        max_index=max_index,
        strict_lower=strict_lower,
        metadata=metadata,
    )
    result = run_optimizer(optimizer_name, request)
    details = dict(result.details)
    best_cost = details.get("best_cost")
    if isinstance(best_cost, dict):
        for key in ("residual_bits", "residual_codec", "residual_codec_details"):
            if key not in details and key in best_cost:
                details[key] = best_cost[key]
    raw_byte_codec = choose_best_byte_codec(image.pixels)
    details["raw_byte_codec"] = raw_byte_codec.codec_name
    details["raw_byte_codec_bits"] = raw_byte_codec.bits
    details["raw_byte_codec_ratio_vs_raw"] = _ratio(raw_byte_codec.bits, result.raw_bits)
    details["raw_byte_codec_details"] = dict(raw_byte_codec.details)
    preview = build_result_preview(image, details)
    raw_bytes = len(image.pixels)
    total_bytes_estimate = bits_to_bytes_ceil(result.total_bits)
    saving_bytes_estimate = raw_bytes - total_bytes_estimate
    payload = {
        "optimizer_name": result.optimizer_name,
        "status": result.status,
        "dataset_name": image.name,
        "image_width": image.width,
        "image_height": image.height,
        "raw_bits": result.raw_bits,
        "total_bits": result.total_bits,
        "saving_bits": result.saving_bits,
        "ratio_vs_raw": result.ratio_vs_raw,
        "raw_bytes": raw_bytes,
        "total_bytes_estimate": total_bytes_estimate,
        "saving_bytes_estimate": saving_bytes_estimate,
        "best_model": result.best_model,
        "history": result.history,
        "details": details,
    }
    if preview is not None:
        payload["preview"] = preview
    return payload


def run_image_simulation(
    optimizer_name: str,
    dataset_name: str = "gradient",
    image_width: int = 32,
    image_height: int = 32,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
    max_index: int | None = None,
    strict_lower: bool = False,
    image_gplite_primitive_set: str | None = None,
) -> dict:
    """Spusti vybrany optimizer nad generovanym grayscale datasetom."""

    image = make_image_dataset(dataset_name, image_width, image_height, seed)
    return run_gray_image_simulation(
        optimizer_name,
        image,
        seed=seed,
        population_size=population_size,
        generations=generations,
        max_index=max_index,
        strict_lower=strict_lower,
        image_gplite_primitive_set=image_gplite_primitive_set,
    )


def build_result_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati preview pre law-based alebo image-predictor branch."""

    preview = build_law_image_preview(image, details)
    if preview is not None:
        return preview
    preview = build_image_law_preview(image, details)
    if preview is not None:
        return preview
    preview = build_image_soma_preview(image, details)
    if preview is not None:
        return preview
    return build_image_predictor_preview(image, details)


def build_law_image_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati anchor, residual a decoded preview pre law-based vysledok."""

    decoder_model = details.get("decoder_model")
    max_index = details.get("max_index")
    if decoder_model is None or not isinstance(max_index, int):
        return None

    strict_lower = bool(details.get("strict_lower", False))
    encoded = [
        encode_block_with_law(pixel, decoder_model, max_index, strict_lower)
        for pixel in image.pixels
    ]
    anchor_pixels = bytes(entry["anchor"] for entry in encoded)
    residual_pixels = bytes(entry["residual"] for entry in encoded)
    decoded_pixels = roundtrip_law_payload(image.pixels, 8, decoder_model, max_index, strict_lower)
    return {
        "anchor_image": make_gray_image(f"{image.name}:anchors", image.width, image.height, anchor_pixels),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_pixels),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Anchors",
        "residual_label": "Residuals",
        "escaped_count": sum(1 for entry in encoded if entry["escaped"]),
        "min_residual": min(residual_pixels, default=0),
        "max_residual": max(residual_pixels, default=0),
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def build_image_predictor_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati predictor, residual a decoded preview pre image predictor."""

    model = details.get("predictor_model")
    if model is None:
        return None

    trace = build_image_predictor_trace(image, model)
    payload = details.get("payload")
    if isinstance(payload, dict):
        decoded_pixels = decode_image_predictor_payload(payload)
    else:
        decoded_pixels = trace["decoded_pixels"]

    residual_visual = bytes(_signed_residual_to_visual(value) for value in trace["residuals"])
    return {
        "anchor_image": make_gray_image(f"{image.name}:predictor", image.width, image.height, trace["predicted_pixels"]),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_visual),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Predictor",
        "residual_label": "Residuals+128",
        "escaped_count": 0,
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def build_image_law_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati predictor, residual a decoded preview pre image-law branch."""

    law = details.get("image_law_model")
    if law is None:
        return None

    trace = build_image_law_trace(image, law)
    payload = details.get("payload")
    if isinstance(payload, dict):
        decoded_pixels = decode_image_law_payload(payload)
    else:
        decoded_pixels = trace["decoded_pixels"]

    residual_visual = bytes(_signed_residual_to_visual(value) for value in trace["residuals"])
    return {
        "anchor_image": make_gray_image(f"{image.name}:predictor_law", image.width, image.height, trace["predicted_pixels"]),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_visual),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Predictor law",
        "residual_label": "Residuals+128",
        "escaped_count": 0,
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def build_image_soma_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati predictor, residual a decoded preview pre fixed-point Image-SOMA."""

    model = details.get("image_soma_model")
    if model is None:
        return None

    trace = build_image_soma_trace(image, model)
    payload = details.get("payload")
    if isinstance(payload, dict):
        decoded_pixels = decode_image_soma_payload(payload)
    else:
        decoded_pixels = trace["decoded_pixels"]

    residual_visual = bytes(_signed_residual_to_visual(value) for value in trace["residuals"])
    return {
        "anchor_image": make_gray_image(f"{image.name}:predictor_soma", image.width, image.height, trace["predicted_pixels"]),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_visual),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Predictor soma",
        "residual_label": "Residuals+128",
        "escaped_count": 0,
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def format_simulation_report(result: dict) -> str:
    """Vrati citatelny textovy report pre CLI alebo GUI."""

    details = result.get("details", {})
    lines = [
        f"optimizer: {result['optimizer_name']}",
        f"status: {result['status']}",
        f"dataset: {result['dataset_name']} ({result['image_width']}x{result['image_height']})",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"raw_bytes: {result.get('raw_bytes', bits_to_bytes_ceil(result['raw_bits']))}",
        f"total_bytes_estimate: {result.get('total_bytes_estimate', bits_to_bytes_ceil(result['total_bits']))}",
        f"saving_bytes_estimate: {result.get('saving_bytes_estimate', 0)}",
        f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}",
        f"best_model: {result['best_model']}",
    ]
    if result["total_bits"] < result["raw_bits"]:
        lines.append("decision: WIN beats raw under current accounting")
    else:
        lines.append("decision: use raw fallback; current model loses to raw")
    would_use_fallback = details.get("would_use_fallback")
    if not isinstance(would_use_fallback, bool):
        would_use_fallback = result["total_bits"] >= result["raw_bits"]
    lines.append(
        "fallback_recommendation: "
        + ("use_raw_fallback" if would_use_fallback else "use_model_under_current_accounting")
    )
    history = result.get("history", [])
    if history:
        lines.append("history:")
        for item in history[:5]:
            best_label = item.get("best_law") or item.get("best_model") or "n/a"
            lines.append(
                f"  gen={item.get('generation', '?')} total_bits={item.get('total_bits', '?')} "
                f"saving_bits={item.get('saving_bits', '?')} best={best_label}"
            )
    if details.get("message"):
        lines.append(f"note: {details['message']}")
    if details.get("note"):
        lines.append(f"note: {details['note']}")
    if details.get("primitive_set"):
        primitive_label = str(details["primitive_set"])
        resolved = details.get("resolved_primitive_set")
        if isinstance(resolved, str) and resolved != primitive_label:
            primitive_label = f"{primitive_label} -> {resolved}"
        lines.append(f"primitive_set: {primitive_label}")
    if details.get("residual_codec"):
        lines.append(f"residual_codec: {details['residual_codec']}")
    if details.get("residual_bits") is not None:
        lines.append(f"residual_bits: {details['residual_bits']}")
    if details.get("raw_byte_codec"):
        lines.append(f"raw_byte_codec: {details['raw_byte_codec']}")
        lines.append(f"raw_byte_codec_bits: {details['raw_byte_codec_bits']}")
        lines.append(f"raw_byte_codec_ratio_vs_raw: {details['raw_byte_codec_ratio_vs_raw']:.3f}")
    preview = result.get("preview")
    if isinstance(preview, dict):
        lines.append(f"roundtrip_preview_ok: {preview.get('roundtrip_ok', False)}")
        lines.append(f"escaped_pixels: {preview.get('escaped_count', 0)}")
        lines.append(f"min_residual: {preview.get('min_residual', 0)}")
        lines.append(f"max_residual: {preview.get('max_residual', 0)}")
    return "\n".join(lines)


def _signed_residual_to_visual(value: int) -> int:
    """Prevedie signed residual na zobrazitelny grayscale proxy."""

    return max(0, min(255, int(value) + 128))


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer bitovej ceny voci raw baseline."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else float("inf")
    return total_bits / raw_bits
```

## File: `tests/conftest.py`

```python
"""Minimalna konfiguracia testov pre src layout bez externych pluginov."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
```

## File: `tests/test_anchor_laws.py`

```python
from primesymbolicmdl.anchor_laws import (
    add_law,
    anchor_value,
    clamp_nonnegative_law,
    const_law,
    floordiv_pow2_law,
    idx_law,
    law_model_bits,
    law_parameter_bits,
    mul_small_law,
    render_law,
    square_law,
    sub_law,
)


def test_idx_terminal_evaluates_to_index() -> None:
    assert anchor_value(idx_law(), 7) == 7


def test_constant_terminal_evaluates() -> None:
    assert anchor_value(const_law(5), 12) == 5


def test_add_and_sub_evaluate() -> None:
    law = sub_law(add_law(idx_law(), const_law(3)), const_law(1))

    assert anchor_value(law, 4) == 6


def test_mul_small_evaluates() -> None:
    assert anchor_value(mul_small_law(idx_law(), 3), 5) == 15


def test_floordiv_pow2_evaluates() -> None:
    assert anchor_value(floordiv_pow2_law(mul_small_law(idx_law(), 3), 2), 5) == 3


def test_square_evaluates() -> None:
    assert anchor_value(square_law(idx_law()), 6) == 36


def test_clamp_nonnegative_evaluates() -> None:
    law = clamp_nonnegative_law(sub_law(idx_law(), const_law(5)))

    assert anchor_value(law, 2) == 0
    assert anchor_value(law, 9) == 4


def test_render_is_deterministic_and_readable() -> None:
    law = clamp_nonnegative_law(add_law(idx_law(), const_law(2)))

    assert render_law(law) == "clamp_nonnegative(add(idx, 2))"
    assert render_law(law) == render_law(law)


def test_model_and_parameter_bits_are_reported() -> None:
    law = mul_small_law(add_law(idx_law(), const_law(2)), 3)

    assert law_model_bits(law) > 0
    assert law_parameter_bits(law) > 0
```

## File: `tests/test_ap_rpc.py`

```python
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest

from primesymbolicmdl.ap_rpc import build_request, handle_request, validate_repo_relative_path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_request_contains_required_metadata() -> None:
    request = build_request("repo.get_file", {"path": "AP.md", "max_bytes": 1234})

    assert request["id"]
    assert request["type"] == "rpc_request"
    assert request["from"] == "ORCHESTRATOR"
    assert request["to"] == "WORKER"
    assert request["method"] == "repo.get_file"
    assert request["params"] == {"path": "AP.md", "max_bytes": 1234}
    assert request["created_at"]


def test_validate_repo_relative_path_allows_safe_relative_file() -> None:
    validate_repo_relative_path("AP.md")


@pytest.mark.parametrize(
    "bad_path",
    [
        "/etc/passwd",
        "../secret.txt",
        ".git/config",
        ".venv/bin/python",
        "image.png",
        "cache/module.pyc",
    ],
)
def test_validate_repo_relative_path_rejects_forbidden_inputs(bad_path: str) -> None:
    with pytest.raises(ValueError):
        validate_repo_relative_path(bad_path)


def test_repo_get_file_returns_sha_and_truncation(tmp_path: Path) -> None:
    sample = tmp_path / "notes.txt"
    content = "alpha-beta-gamma-delta"
    sample.write_text(content, encoding="utf-8")
    request = {
        "id": "demo-request",
        "type": "rpc_request",
        "from": "ORCHESTRATOR",
        "to": "WORKER",
        "method": "repo.get_file",
        "params": {"path": "notes.txt", "max_bytes": 5},
        "created_at": "2026-06-11T20:00:00+02:00",
    }

    response = handle_request(request, tmp_path)

    assert response["status"] == "ok"
    assert response["result"] == {
        "path": "notes.txt",
        "content": "alpha",
        "size_bytes": len(content.encode("utf-8")),
        "truncated": True,
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
    }


def test_unknown_method_returns_error_response(tmp_path: Path) -> None:
    request = {
        "id": "unknown-request",
        "type": "rpc_request",
        "from": "ORCHESTRATOR",
        "to": "WORKER",
        "method": "repo.unknown",
        "params": {},
        "created_at": "2026-06-11T20:00:00+02:00",
    }

    response = handle_request(request, tmp_path)

    assert response["status"] == "error"
    assert "Unknown RPC method" in response["error"]


def test_ap_rpc_call_fish_smoke() -> None:
    if shutil.which("fish") is None:
        pytest.skip("fish is not available")

    completed = subprocess.run(
        ["fish", "scripts/ap_rpc_call.fish", "--method", "repo.status"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "RESPONSE_STATUS=ok" in completed.stdout
    assert "RESPONSE_PATH=" in completed.stdout
```

## File: `tests/test_bitcost.py`

```python
from primesymbolicmdl.bitcost import estimate_prime_anchor_cost
from primesymbolicmdl.blocks import bytes_to_uint_blocks


def test_cost_accounting_uses_original_size_bits() -> None:
    data = b"\x00\x01\x02"
    blocks = bytes_to_uint_blocks(data, 16)
    costs = estimate_prime_anchor_cost(blocks, 16, len(data), "nearest")

    assert costs["raw_bits"] == len(data) * 8
    assert costs["width_bits"] == 16
    assert isinstance(costs["ratio_vs_raw"], (int, float))


def test_cost_accounting_handles_empty_data() -> None:
    costs = estimate_prime_anchor_cost([], 8, 0, "nearest")

    assert costs["raw_bits"] == 0
    assert costs["block_count"] == 0
    assert costs["escape_count"] == 0


def test_lower_mode_counts_escaped_blocks_below_two() -> None:
    data = b"\x00\x01\x02\x03"
    blocks = bytes_to_uint_blocks(data, 8)
    costs = estimate_prime_anchor_cost(blocks, 8, len(data), "lower")

    assert costs["escape_count"] == 2
    assert costs["escape_bits"] == 16
    assert costs["block_count"] == 4
```

## File: `tests/test_bitstream.py`

```python
from primesymbolicmdl.bitstream import (
    BitReader,
    BitWriter,
    decode_unsigned_varint,
    encode_unsigned_varint,
    zigzag_decode,
    zigzag_encode,
)


def test_bit_writer_and_reader_use_stable_msb_first_order() -> None:
    writer = BitWriter()
    for bit in (1, 0, 1, 1):
        writer.write_bit(bit)

    payload = writer.to_bytes()

    assert payload == b"\xb0"

    reader = BitReader(payload)
    assert [reader.read_bit() for _ in range(4)] == [1, 0, 1, 1]


def test_write_bits_and_read_bits_roundtrip_for_mixed_widths() -> None:
    values = (
        (0, 0),
        (1, 1),
        (2, 2),
        (5, 3),
        (0xAB, 8),
        (0x1234, 16),
        (0x12345, 20),
    )

    writer = BitWriter()
    for value, width in values:
        writer.write_bits(value, width)

    reader = BitReader(writer.to_bytes())
    decoded = [reader.read_bits(width) for value, width in values]

    assert decoded == [value for value, width in values]


def test_unsigned_varint_roundtrip_is_deterministic() -> None:
    values = [0, 1, 2, 127, 128, 255, 300, 16384, (1 << 32) + 5]

    decoded = []
    for value in values:
        encoded = encode_unsigned_varint(value)
        roundtrip, offset = decode_unsigned_varint(encoded)
        assert offset == len(encoded)
        decoded.append(roundtrip)

    assert encode_unsigned_varint(300) == b"\xac\x02"
    assert decoded == values


def test_zigzag_roundtrip_handles_negative_and_positive_values() -> None:
    values = [-99, -3, -1, 0, 1, 3, 99]

    assert [zigzag_decode(zigzag_encode(value)) for value in values] == values
```

## File: `tests/test_blocks.py`

```python
import pytest

from primesymbolicmdl.blocks import bytes_to_uint_blocks, uint_blocks_to_bytes


@pytest.mark.parametrize("width_bits", [8, 16, 24, 32])
def test_blocks_roundtrip_supported_widths(width_bits: int) -> None:
    data = bytes(range(1, 40))
    blocks = bytes_to_uint_blocks(data, width_bits)

    assert uint_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_blocks_roundtrip_empty_bytes() -> None:
    assert bytes_to_uint_blocks(b"", 16) == []
    assert uint_blocks_to_bytes([], 16, 0) == b""


@pytest.mark.parametrize(
    ("width_bits", "data"),
    [
        (8, b"\x01\x02\x03"),
        (16, b"\x01"),
        (24, b"\x01\x02\x03\x04"),
        (32, b"\x10\x20\x30"),
    ],
)
def test_blocks_roundtrip_non_multiple_sizes(width_bits: int, data: bytes) -> None:
    blocks = bytes_to_uint_blocks(data, width_bits)

    assert uint_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_unsupported_width_raises() -> None:
    with pytest.raises(ValueError):
        bytes_to_uint_blocks(b"\x00", 12)
```

## File: `tests/test_codec_roundtrip.py`

```python
import random

from primesymbolicmdl.codec import compress_experimental, decompress_experimental


def _u16_bytes(values: list[int]) -> bytes:
    return b"".join(value.to_bytes(2, "big") for value in values)


def test_codec_roundtrip_empty_data() -> None:
    data = b""
    payload = compress_experimental(data)

    assert payload["codec"] == "raw"
    assert decompress_experimental(payload) == data


def test_codec_roundtrip_short_ascii_data() -> None:
    data = b"PrimeSymbolicMDL"
    payload = compress_experimental(data, width_bits=8)

    assert decompress_experimental(payload) == data


def test_codec_roundtrip_deterministic_random_bytes() -> None:
    rng = random.Random(1234)
    data = bytes(rng.randrange(256) for _ in range(513))
    payload = compress_experimental(data, width_bits=16)

    assert decompress_experimental(payload) == data


def test_codec_roundtrip_structured_integer_like_bytes() -> None:
    values = [2, 3, 5, 7, 11, 13, 17, 19] * 8
    data = _u16_bytes(values)
    payload = compress_experimental(data, width_bits=16, mode="nearest")

    assert payload["codec"] == "prime_anchor"
    assert payload["metadata"]["estimated_costs"]["total_bits"] < payload["metadata"]["estimated_costs"]["raw_bits"]
    assert decompress_experimental(payload) == data
```

## File: `tests/test_evolution.py`

```python
from primesymbolicmdl.evolution import (
    AnchorGenome,
    encode_block_with_genome,
    estimate_genome_cost,
    search_best_genome_for_bytes,
)
from primesymbolicmdl.experiments import dataset_random, dataset_zeros


def test_encode_block_with_genome_reconstructs_exactly() -> None:
    for genome in (
        AnchorGenome("prime_lower", 0),
        AnchorGenome("multiple", 4),
        AnchorGenome("power", 2),
        AnchorGenome("square", 0),
    ):
        encoded = encode_block_with_genome(37, genome)

        if encoded["escaped"]:
            continue

        assert encoded["anchor"] <= 37
        assert encoded["anchor"] + encoded["residual"] == 37


def test_estimate_genome_cost_reports_numeric_fitness() -> None:
    costs = estimate_genome_cost([0, 0, 0, 0], 8, 4, AnchorGenome("multiple", 1))

    assert isinstance(costs["fitness"], int)
    assert costs["fitness"] == costs["raw_bits"] - costs["total_bits"]


def test_evolution_search_is_deterministic_for_same_seed() -> None:
    data = dataset_zeros(128)
    left = search_best_genome_for_bytes(data, 8, generations=8, population_size=16, seed=1234)
    right = search_best_genome_for_bytes(data, 8, generations=8, population_size=16, seed=1234)

    assert left["best_genome"] == right["best_genome"]
    assert left["best_costs"]["total_bits"] == right["best_costs"]["total_bits"]


def test_evolution_search_finds_improvement_on_zero_data() -> None:
    result = search_best_genome_for_bytes(dataset_zeros(256), 8, generations=8, population_size=16, seed=1234)

    assert result["best_costs"]["fitness"] > 0
    assert result["best_costs"]["total_bits"] < result["best_costs"]["raw_bits"]


def test_evolution_search_does_not_crash_on_random_data() -> None:
    result = search_best_genome_for_bytes(dataset_random(128, 1234), 8, generations=6, population_size=12, seed=1234)

    assert "best_genome" in result
    assert "history" in result
```

## File: `tests/test_experiments.py`

```python
import importlib
import io
from contextlib import redirect_stdout

from primesymbolicmdl.experiments import (
    default_datasets,
    format_markdown_table,
    run_prime_anchor_matrix,
)


def test_default_experiment_matrix_produces_rows() -> None:
    rows = run_prime_anchor_matrix(
        datasets=default_datasets(),
        widths=(8, 16, 24, 32),
        modes=("lower", "upper", "nearest"),
    )

    assert rows


def test_all_requested_widths_and_modes_appear() -> None:
    rows = run_prime_anchor_matrix(
        datasets={"tiny": b"\x00\x01\x02"},
        widths=(8, 16, 24, 32),
        modes=("lower", "upper", "nearest"),
    )

    assert {row["width_bits"] for row in rows} == {8, 16, 24, 32}
    assert {row["mode"] for row in rows} == {"lower", "upper", "nearest"}


def test_markdown_table_contains_header() -> None:
    table = format_markdown_table(
        [
            {
                "dataset": "tiny",
                "size_bytes": 3,
                "width_bits": 8,
                "mode": "nearest",
                "raw_bits": 24,
                "total_bits": 40,
                "ratio_vs_raw": 1.5,
                "escape_count": 0,
                "block_count": 3,
            }
        ]
    )

    assert "| dataset " in table
    assert "| ratio_vs_raw " in table


def test_cli_module_is_importable_and_prints_table() -> None:
    module = importlib.import_module("primesymbolicmdl.experiments")
    assert hasattr(module, "run_prime_anchor_matrix")

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        module.main()

    output = stdout.getvalue()
    assert "| dataset " in output
```

## File: `tests/test_gui_import.py`

```python
import importlib

from primesymbolicmdl.optimizers.image_gplite import available_image_gplite_primitive_sets


def test_gui_module_imports_headlessly() -> None:
    module = importlib.import_module("primesymbolicmdl.gui")

    assert hasattr(module, "main")
    assert hasattr(module, "parse_optional_int")


def test_gui_registry_names_include_image_aware_optimizers() -> None:
    module = importlib.import_module("primesymbolicmdl.gui")
    names = module.get_optimizer_names()

    assert "Image-GP-lite" in names
    assert "Image-SOMA" in names


def test_gui_supports_image_gplite_primitive_set_choices() -> None:
    assert available_image_gplite_primitive_sets() == ["local", "ramp", "structure", "full"]
```

## File: `tests/test_huge_anchor_binary_demo.py`

```python
import io
from contextlib import redirect_stdout

from primesymbolicmdl import huge_anchor_binary_demo


def test_huge_anchor_binary_demo_runs_and_prints_actual_fields() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        huge_anchor_binary_demo.main()

    output = stdout.getvalue()
    assert "dataset: linear_shift_generated" in output
    assert "actual_bits:" in output
    assert "decision:" in output
    assert "estimated_best_model:" in output
    assert "actual_best_model:" in output
    assert "actual_top_3_candidates:" in output


def test_huge_anchor_binary_demo_results_include_actual_compression_or_honest_fallback() -> None:
    results = huge_anchor_binary_demo.run_demo()

    assert results
    assert all(result["roundtrip_ok"] for result in results)
    assert any(result["decision"] == "compressed" for result in results if result["dataset"].endswith("_generated"))
    assert all(result["actual_rerank_candidates"] for result in results)
```

## File: `tests/test_huge_anchor_binary.py`

```python
import pytest

from primesymbolicmdl.huge_anchor_binary import (
    compress_best_huge_anchor_binary,
    decode_huge_anchor_binary,
    encode_huge_anchor_binary,
    rerank_huge_anchor_candidates_by_actual_size,
)
from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset
from primesymbolicmdl.huge_anchor_models import HugeAnchorModel
from primesymbolicmdl.huge_anchor_search import search_best_huge_anchor_model


@pytest.mark.parametrize(
    ("dataset_name", "width_bits"),
    [
        ("linear_shift_generated", 16),
        ("square_generated", 64),
        ("multiple_generated", 32),
    ],
)
def test_huge_anchor_binary_exact_roundtrip_for_generated_datasets(dataset_name: str, width_bits: int) -> None:
    data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
    model = compress_best_huge_anchor_binary(data, width_bits=width_bits)["best_model"]
    blob = encode_huge_anchor_binary(data, width_bits, model)

    assert decode_huge_anchor_binary(blob) == data


def test_huge_anchor_binary_random_data_decodes_exactly() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=32)

    assert decode_huge_anchor_binary(result["binary_blob"]) == data
    assert result["roundtrip_ok"] is True


def test_huge_anchor_binary_rejects_corrupt_magic() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=8, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=16)
    corrupt = b"BADMAGIC" + result["binary_blob"][8:]

    with pytest.raises(ValueError, match="magic"):
        decode_huge_anchor_binary(corrupt)


def test_huge_anchor_binary_rejects_unsupported_family() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=8, seed=1234)

    with pytest.raises(ValueError, match="Unsupported huge anchor family"):
        encode_huge_anchor_binary(data, 16, HugeAnchorModel("imaginary_family", {}))


def test_compress_best_huge_anchor_binary_roundtrips_square_generated() -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=64)

    assert result["roundtrip_ok"] is True
    assert decode_huge_anchor_binary(result["binary_blob"]) == data
    assert result["actual_rerank_candidates"]
    assert result["estimated_best_model_string"]


def test_at_least_one_synthetic_dataset_is_truly_smaller_in_actual_bytes() -> None:
    results = []
    for dataset_name in ("linear_shift_generated", "square_generated", "multiple_generated"):
        for width_bits in (16, 32, 64):
            data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
            results.append(compress_best_huge_anchor_binary(data, width_bits=width_bits))

    assert any(result["decision"] == "compressed" for result in results)
    assert any(result["compressed_bytes"] < result["raw_bytes"] for result in results)


def test_random_data_is_not_reported_as_fake_actual_win() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=32)

    assert result["roundtrip_ok"] is True
    if result["decision"] == "compressed":
        assert result["compressed_bytes"] < result["raw_bytes"]
    else:
        assert result["compressed_bytes"] >= result["raw_bytes"]


def test_actual_rerank_candidates_are_exact_and_use_actual_bytes() -> None:
    data = make_huge_anchor_dataset("repeating_pattern", 32, count=32, seed=1234)
    search_result = search_best_huge_anchor_model(data, width_bits=32)
    candidates = rerank_huge_anchor_candidates_by_actual_size(data, 32, search_result, top_n=4)

    successful = [candidate for candidate in candidates if candidate["status"] == "ok"]

    assert len(successful) >= 2
    assert all(candidate["roundtrip_ok"] is True for candidate in successful)
    assert all(candidate["actual_bits"] == candidate["compressed_bytes"] * 8 for candidate in successful)
    for candidate in successful:
        if candidate["decision"] == "compressed":
            assert candidate["compressed_bytes"] < candidate["raw_bytes"]
        else:
            assert candidate["compressed_bytes"] >= candidate["raw_bytes"]


def test_compress_best_huge_anchor_binary_reports_estimated_vs_actual_winner() -> None:
    data = make_huge_anchor_dataset("repeating_pattern", 32, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=32, actual_rerank_top_n=4)

    assert result["actual_rerank_top_n"] == 4
    assert result["best_model_string"]
    assert result["estimated_best_model_string"]
    assert isinstance(result["actual_rerank_changed_winner"], bool)
```

## File: `tests/test_huge_anchor_branch.py`

```python
import pytest

from primesymbolicmdl.huge_anchor_branch import (
    decode_huge_anchor_payload,
    encode_block_huge_anchor,
    encode_huge_anchor_payload,
    estimate_huge_anchor_cost,
    roundtrip_huge_anchor,
)
from primesymbolicmdl.huge_anchor_models import HugeAnchorModel
from primesymbolicmdl.huge_blocks import bytes_to_huge_blocks


@pytest.mark.parametrize(
    ("model", "x", "width_bits"),
    [
        (HugeAnchorModel("linear_shift", {"shift": 3}), 41, 16),
        (HugeAnchorModel("affine_shift", {"shift": 3, "bias": 1}), 41, 16),
        (HugeAnchorModel("multiple", {"step": 7}), 43, 16),
        (HugeAnchorModel("square", {}), 83, 16),
        (HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0}), 53, 16),
    ],
)
def test_encode_block_huge_anchor_reconstructs_block(model: HugeAnchorModel, x: int, width_bits: int) -> None:
    encoded = encode_block_huge_anchor(x, width_bits, model, search_radius=2)

    assert encoded["anchor"] + encoded["diff"] == x


def test_encode_block_huge_anchor_escape_works_for_unreachable_prime_case() -> None:
    model = HugeAnchorModel("scaled_prime", {"shift": 1, "search_radius": 0})
    encoded = encode_block_huge_anchor(0, 8, model)

    assert encoded["escaped"]
    assert encoded["index"] is None
    assert encoded["diff"] == 0


def test_estimate_huge_anchor_cost_returns_required_fields() -> None:
    model = HugeAnchorModel("linear_shift", {"shift": 4})
    data = b"\x00\x10\x00\x20\x00\x30\x00\x40"
    blocks = bytes_to_huge_blocks(data, 16)
    costs = estimate_huge_anchor_cost(blocks, 16, len(data), model, search_radius=1)

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "flag_bits",
        "index_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "escape_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "escape_count",
        "block_count",
        "model",
    }

    assert required.issubset(costs)
    assert costs["raw_bits"] == len(data) * 8


@pytest.mark.parametrize(
    ("model", "width_bits", "data"),
    [
        (HugeAnchorModel("linear_shift", {"shift": 4}), 16, b"\x00\x10\x00\x20\x00\x30\x00\x40"),
        (HugeAnchorModel("multiple", {"step": 31}), 32, b"\x00\x00\x00\x1f\x00\x00\x00>\x00\x00\x00]"),
        (HugeAnchorModel("square", {}), 64, b"\x00\x00\x00\x00\x00\x00\x00\x04"),
        (HugeAnchorModel("linear_shift", {"shift": 8}), 128, b"\x00" * 16 + b"\x01" * 16),
        (HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0}), 16, b"\x00/\x003\x005\x007"),
    ],
)
def test_huge_anchor_payload_roundtrip_is_exact(model: HugeAnchorModel, width_bits: int, data: bytes) -> None:
    payload = encode_huge_anchor_payload(data, width_bits, model, search_radius=2)

    assert decode_huge_anchor_payload(payload) == data
    assert roundtrip_huge_anchor(data, width_bits, model, search_radius=2) == data


def test_huge_anchor_roundtrip_supports_width_96_for_non_prime_family() -> None:
    model = HugeAnchorModel("multiple", {"step": 31})
    data = (31).to_bytes(12, "big") + (62).to_bytes(12, "big")

    assert roundtrip_huge_anchor(data, 96, model, search_radius=1) == data
```

## File: `tests/test_huge_anchor_datasets.py`

```python
from primesymbolicmdl.huge_anchor_datasets import get_huge_anchor_dataset_names, make_huge_anchor_dataset


def test_huge_anchor_dataset_names_are_stable() -> None:
    assert get_huge_anchor_dataset_names() == [
        "linear_shift_generated",
        "square_generated",
        "multiple_generated",
        "random_bytes",
        "ascii_small",
        "repeating_pattern",
    ]


def test_huge_anchor_datasets_are_deterministic_for_same_seed() -> None:
    left = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=1234)
    right = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=1234)

    assert left == right


def test_generated_dataset_respects_requested_size() -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=10, seed=1234)

    assert len(data) == 10 * (64 // 8)
```

## File: `tests/test_huge_anchor_demo.py`

```python
import io
from contextlib import redirect_stdout

from primesymbolicmdl import huge_anchor_demo


def test_huge_anchor_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        huge_anchor_demo.main()

    output = stdout.getvalue()
    assert "dataset: linear_shift_generated" in output
    assert "dataset: random_bytes" in output
    assert "best_model:" in output
    assert "top_3_candidates:" in output
    assert "scaled_prime_baseline:" in output


def test_huge_anchor_demo_results_include_at_least_one_win() -> None:
    results = huge_anchor_demo.run_demo()

    assert results
    assert all(result["roundtrip_ok"] for result in results)
    assert any(result["decision"] == "win" for result in results if result["dataset"].endswith("_generated"))
```

## File: `tests/test_huge_anchor_file_benchmark.py`

```python
from primesymbolicmdl.huge_anchor_file_benchmark import format_benchmark_table, run_benchmark


def test_huge_anchor_file_benchmark_runs_and_reports_honest_sizes() -> None:
  rows = run_benchmark()
  table = format_benchmark_table(rows)

  assert len(rows) >= 5
  assert all(row.roundtrip_ok for row in rows)
  assert any(row.decision == "raw_fallback" for row in rows)
  assert any(row.decision == "compressed" for row in rows)
  assert "random_bytes_128" in table
  assert "square_generated_64" in table
  assert "README.md" in table

  random_row = next(row for row in rows if row.name == "random_bytes_128")
  assert random_row.decision == "raw_fallback"
  assert random_row.psmdl_bytes >= random_row.raw_bytes
  assert random_row.require_compression == "refused"

  square_row = next(row for row in rows if row.name == "square_generated_64")
  assert square_row.decision == "compressed"
  assert square_row.psmdl_bytes < square_row.raw_bytes
  assert square_row.require_compression == "ok"
```

## File: `tests/test_huge_anchor_file_cli.py`

```python
import subprocess
import sys
from pathlib import Path

import pytest

from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset
from primesymbolicmdl.huge_anchor_file import (
    PsmdlCompressionRefusedError,
    compress_file,
    compress_to_psmdl_bytes,
    decode_psmdl_bytes,
    decompress_file,
    encode_raw_psmdl,
)
from primesymbolicmdl.huge_anchor_file_cli import main as cli_main


def test_compress_to_psmdl_bytes_roundtrips_square_generated() -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=32, seed=1234)
    result = compress_to_psmdl_bytes(data, width_bits=64)

    assert result.roundtrip_ok is True
    assert decode_psmdl_bytes(result.file_bytes) == data
    assert result.decision == "compressed"
    assert result.file_format == "huge_anchor"
    assert result.compressed_bytes < result.raw_bytes


def test_compress_to_psmdl_bytes_uses_raw_fallback_for_random_data() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    result = compress_to_psmdl_bytes(data, width_bits=32)

    assert result.roundtrip_ok is True
    assert decode_psmdl_bytes(result.file_bytes) == data
    assert result.decision == "raw_fallback"
    assert result.file_format == "raw_fallback"
    assert result.compressed_bytes >= result.raw_bytes


def test_compress_to_psmdl_bytes_can_refuse_non_winning_compression() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)

    with pytest.raises(PsmdlCompressionRefusedError, match="not smaller than raw"):
        compress_to_psmdl_bytes(data, width_bits=32, require_compression=True)


def test_encode_raw_psmdl_roundtrips() -> None:
    data = b"hello-psmdl-raw-fallback"

    assert decode_psmdl_bytes(encode_raw_psmdl(data)) == data


def test_temp_file_cli_roundtrip_for_square_generated(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("square_generated", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    result = compress_file(input_path, psmdl_path, width_bits=32)
    assert result.roundtrip_ok is True
    assert psmdl_path.exists()

    restored = decompress_file(psmdl_path, restored_path)
    assert restored == data
    assert restored_path.read_bytes() == data


def test_temp_file_cli_roundtrip_for_random_bytes_with_raw_fallback(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    result = compress_file(input_path, psmdl_path, width_bits=32)
    assert result.decision == "raw_fallback"
    assert result.file_format == "raw_fallback"

    restored = decompress_file(psmdl_path, restored_path)
    assert restored == data


def test_cli_module_compress_and_decompress_roundtrip(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    exit_code = cli_main(
        [
            "compress",
            "--input",
            str(input_path),
            "--output",
            str(psmdl_path),
            "--width-bits",
            "16",
        ]
    )
    assert exit_code == 0
    assert psmdl_path.exists()

    exit_code = cli_main(
        [
            "decompress",
            "--input",
            str(psmdl_path),
            "--output",
            str(restored_path),
        ]
    )
    assert exit_code == 0
    assert restored_path.read_bytes() == data


def test_cli_refuses_compression_when_required_and_no_win(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    input_path.write_bytes(data)

    exit_code = cli_main(
        [
            "compress",
            "--input",
            str(input_path),
            "--output",
            str(psmdl_path),
            "--width-bits",
            "32",
            "--require-compression",
        ]
    )
    assert exit_code == 2
    assert not psmdl_path.exists()


def test_subprocess_cli_roundtrip(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("multiple_generated", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    compress = subprocess.run(
        [
            sys.executable,
            "-m",
            "primesymbolicmdl.huge_anchor_file_cli",
            "compress",
            "--input",
            str(input_path),
            "--output",
            str(psmdl_path),
            "--width-bits",
            "32",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert compress.returncode == 0, compress.stderr

    decompress = subprocess.run(
        [
            sys.executable,
            "-m",
            "primesymbolicmdl.huge_anchor_file_cli",
            "decompress",
            "--input",
            str(psmdl_path),
            "--output",
            str(restored_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert decompress.returncode == 0, decompress.stderr
    assert restored_path.read_bytes() == data
```

## File: `tests/test_huge_anchor_models.py`

```python
import pytest

from primesymbolicmdl.huge_anchor_models import (
    HugeAnchorModel,
    anchor_from_index,
    huge_anchor_model_bits,
    huge_anchor_parameter_bits,
    render_huge_anchor_model,
)


def test_render_huge_anchor_model_is_stable() -> None:
    model = HugeAnchorModel("affine_shift", {"shift": 4, "bias": -1})

    assert render_huge_anchor_model(model) == "affine_shift(bias=-1, shift=4)"


def test_huge_anchor_model_bits_and_parameters_are_positive() -> None:
    model = HugeAnchorModel("linear_shift", {"shift": 3})

    assert huge_anchor_model_bits(model) > 0
    assert huge_anchor_parameter_bits(model) > 0


@pytest.mark.parametrize(
    ("model", "index", "width_bits", "expected"),
    [
        (HugeAnchorModel("linear_shift", {"shift": 3}), 5, 16, 40),
        (HugeAnchorModel("affine_shift", {"shift": 2, "bias": 3}), 4, 16, 19),
        (HugeAnchorModel("multiple", {"step": 7}), 6, 16, 42),
        (HugeAnchorModel("square", {}), 9, 16, 81),
        (HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0}), 3, 16, 47),
    ],
)
def test_anchor_from_index_returns_expected_values(
    model: HugeAnchorModel,
    index: int,
    width_bits: int,
    expected: int,
) -> None:
    assert anchor_from_index(index, model, width_bits) == expected


def test_scaled_prime_anchor_returns_none_above_64_bits() -> None:
    model = HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0})

    assert anchor_from_index(3, model, 96) is None


def test_unknown_family_raises() -> None:
    model = HugeAnchorModel("unknown_family", {})

    with pytest.raises(ValueError):
        render_huge_anchor_model(model)
```

## File: `tests/test_huge_anchor_search.py`

```python
from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset
from primesymbolicmdl.huge_anchor_models import huge_anchor_model_from_dict, huge_anchor_model_to_dict
from primesymbolicmdl.huge_anchor_search import candidate_huge_anchor_models, search_best_huge_anchor_model


def test_candidate_huge_anchor_models_include_expected_families() -> None:
    families = {model.family for model in candidate_huge_anchor_models(32)}

    assert {"linear_shift", "affine_shift", "multiple", "square", "scaled_prime"}.issubset(families)


def test_huge_anchor_search_runs_on_tiny_deterministic_data() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=16, seed=1234)
    result = search_best_huge_anchor_model(data, width_bits=16)

    assert result["best_model_string"]
    assert result["raw_bits"] == len(data) * 8
    assert result["roundtrip_ok"] is True
    assert result["history"]
    first_candidate = result["history"][0]
    assert first_candidate["model_dict"]
    assert huge_anchor_model_to_dict(huge_anchor_model_from_dict(first_candidate["model_dict"])) == first_candidate["model_dict"]


def test_huge_anchor_search_is_deterministic_for_same_seed() -> None:
    data = make_huge_anchor_dataset("multiple_generated", 32, count=16, seed=1234)
    left = search_best_huge_anchor_model(data, width_bits=32, seed=1234)
    right = search_best_huge_anchor_model(data, width_bits=32, seed=1234)

    assert left["best_model"] == right["best_model"]
    assert left["best_model_dict"] == right["best_model_dict"]
    assert left["best_model_string"] == right["best_model_string"]
    assert left["total_bits"] == right["total_bits"]
    assert left["history"] == right["history"]


def test_huge_anchor_search_handles_random_data_without_crashing() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=1234)
    result = search_best_huge_anchor_model(data, width_bits=32)

    assert result["roundtrip_ok"] is True
    assert isinstance(result["total_bits"], int)
    assert isinstance(result["saving_bits"], int)


def test_huge_anchor_search_finds_synthetic_win() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 32, count=32, seed=1234)
    result = search_best_huge_anchor_model(data, width_bits=32)

    assert result["roundtrip_ok"] is True
    assert result["decision"] == "win"
    assert result["saving_bits"] > 0
```

## File: `tests/test_huge_blocks.py`

```python
import random

import pytest

from primesymbolicmdl.huge_blocks import bytes_to_huge_blocks, huge_blocks_to_bytes


@pytest.mark.parametrize("width_bits", [8, 16, 24, 32, 40, 48, 56, 64, 96, 128])
def test_huge_blocks_roundtrip_supported_widths(width_bits: int) -> None:
    data = bytes(range(1, 80))
    blocks = bytes_to_huge_blocks(data, width_bits)

    assert huge_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_huge_blocks_roundtrip_empty_bytes() -> None:
    assert bytes_to_huge_blocks(b"", 64) == []
    assert huge_blocks_to_bytes([], 64, 0) == b""


@pytest.mark.parametrize(
    ("width_bits", "data"),
    [
        (8, b"\x01\x02\x03"),
        (16, b"\x01"),
        (24, b"\x01\x02\x03\x04"),
        (40, b"\x10\x20\x30"),
        (64, b"\x10\x20\x30\x40\x50"),
        (128, b"\xAA\xBB\xCC"),
    ],
)
def test_huge_blocks_roundtrip_non_multiple_sizes(width_bits: int, data: bytes) -> None:
    blocks = bytes_to_huge_blocks(data, width_bits)

    assert huge_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_huge_blocks_roundtrip_deterministic_random_bytes() -> None:
    rng = random.Random(1234)
    data = bytes(rng.randrange(256) for _ in range(257))
    blocks = bytes_to_huge_blocks(data, 96)

    assert huge_blocks_to_bytes(blocks, 96, len(data)) == data


def test_huge_blocks_unsupported_width_raises() -> None:
    with pytest.raises(ValueError):
        bytes_to_huge_blocks(b"\x00", 72)
```

## File: `tests/test_image_ablation.py`

```python
import io
from contextlib import redirect_stdout

from primesymbolicmdl import image_ablation


def test_run_image_gplite_ablation_returns_all_primitive_sets() -> None:
    rows = image_ablation.run_image_gplite_ablation("gradient", width=8, height=8, population_size=8, generations=4)

    assert [row["primitive_set"] for row in rows] == ["local", "ramp", "structure"]
    assert all("residual_codec" in row for row in rows)


def test_format_image_ablation_table_returns_markdown_header() -> None:
    rows = image_ablation.run_image_gplite_ablation("checker", width=8, height=8, population_size=8, generations=4)
    table = image_ablation.format_image_ablation_table(rows)

    assert "| dataset | primitive_set |" in table
    assert "structure" in table


def test_image_ablation_cli_main_runs() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        image_ablation.main()

    output = stdout.getvalue()
    assert "## Image-GP-lite ablation: gradient" in output
    assert "## Image-GP-lite ablation: checker" in output
    assert "| dataset | primitive_set |" in output
```

## File: `tests/test_image_context_laws.py`

```python
from primesymbolicmdl.image_context_laws import (
    add_law,
    avg_law,
    checker_parity_law,
    clamp_byte_law,
    const_law,
    eq_const_law,
    evaluate_image_law,
    floordiv_const_law,
    floordiv_pow2_law,
    gradient_law,
    image_law_model_bits,
    image_law_parameter_bits,
    mod_const_law,
    mul_small_law,
    parity_byte_law,
    render_image_law,
    sub_law,
    terminal_law,
)
from primesymbolicmdl.image_datasets import make_checker_image


def _context() -> dict[str, int]:
    return {
        "col": 3,
        "row": 2,
        "width": 8,
        "height": 8,
        "left": 50,
        "up": 70,
        "up_left": 20,
        "x_ramp": 109,
        "y_ramp": 72,
        "diag_ramp": 91,
    }


def test_terminals_return_decoder_known_context() -> None:
    context = _context()

    assert evaluate_image_law(terminal_law("left"), context) == 50
    assert evaluate_image_law(terminal_law("up"), context) == 70
    assert evaluate_image_law(terminal_law("x_ramp"), context) == 109


def test_basic_image_law_operators_work() -> None:
    context = _context()

    assert evaluate_image_law(add_law(terminal_law("left"), const_law(5)), context) == 55
    assert evaluate_image_law(sub_law(terminal_law("up"), terminal_law("left")), context) == 20
    assert evaluate_image_law(avg_law(terminal_law("left"), terminal_law("up")), context) == 60
    assert evaluate_image_law(
        gradient_law(terminal_law("left"), terminal_law("up"), terminal_law("up_left")),
        context,
    ) == 100
    assert evaluate_image_law(mul_small_law(terminal_law("row"), 3), context) == 6
    assert evaluate_image_law(floordiv_pow2_law(const_law(40), 3), context) == 5


def test_clamp_byte_keeps_prediction_in_byte_range() -> None:
    context = _context()

    assert evaluate_image_law(clamp_byte_law(const_law(999)), context) == 255
    assert evaluate_image_law(sub_law(const_law(0), const_law(999)), context) == 0


def test_render_and_bit_helpers_are_stable() -> None:
    law = clamp_byte_law(
        gradient_law(
            terminal_law("left"),
            terminal_law("up"),
            floordiv_pow2_law(terminal_law("up_left"), 1),
        )
    )

    assert render_image_law(law) == "clamp_byte(gradient(left, up, floordiv_pow2(up_left, 1)))"
    assert isinstance(image_law_model_bits(law), int)
    assert isinstance(image_law_parameter_bits(law), int)
    assert image_law_model_bits(law) > 0


def test_structure_primitives_are_deterministic() -> None:
    context = _context()

    assert evaluate_image_law(mod_const_law(terminal_law("col"), 4), context) == 3
    assert evaluate_image_law(floordiv_const_law(terminal_law("left"), 4), context) == 12
    assert evaluate_image_law(eq_const_law(terminal_law("row"), 2), context) == 255
    assert evaluate_image_law(eq_const_law(terminal_law("row"), 3), context) == 0
    assert evaluate_image_law(parity_byte_law(terminal_law("col")), context) == 255


def test_checker_parity_matches_checker_dataset_for_block_four() -> None:
    image = make_checker_image(8, 8, 4)
    law = checker_parity_law(4)
    predicted = bytes(
        evaluate_image_law(
            law,
            {
                "col": col,
                "row": row,
                "width": image.width,
                "height": image.height,
                "left": 0,
                "up": 0,
                "up_left": 0,
                "x_ramp": (255 * col) // max(1, image.width - 1),
                "y_ramp": (255 * row) // max(1, image.height - 1),
                "diag_ramp": (255 * (col + row)) // max(1, image.width + image.height - 2),
            },
        )
        for row in range(image.height)
        for col in range(image.width)
    )

    assert predicted == image.pixels


def test_structure_primitive_render_strings_are_stable() -> None:
    law = clamp_byte_law(
        add_law(
            checker_parity_law(4),
            parity_byte_law(floordiv_const_law(terminal_law("col"), 2)),
        )
    )

    assert (
        render_image_law(law)
        == "clamp_byte(add(checker_parity(block=4), parity_byte(floordiv_const(col, 2))))"
    )
    assert isinstance(image_law_model_bits(law), int)
    assert isinstance(image_law_parameter_bits(law), int)
```

## File: `tests/test_image_datasets.py`

```python
from primesymbolicmdl.image_datasets import (
    get_image_dataset_names,
    make_checker_image,
    make_diagonal_ramp_image,
    make_gradient_image,
    make_image_dataset,
    make_noise_image,
)


def test_generated_images_have_expected_pixel_length() -> None:
    for image in (
        make_gradient_image(8, 8),
        make_checker_image(8, 8, 2),
        make_diagonal_ramp_image(8, 8),
        make_noise_image(8, 8, 1234),
    ):
        assert len(image.pixels) == image.width * image.height


def test_generated_pixels_are_bytes() -> None:
    image = make_gradient_image(4, 4)

    assert isinstance(image.pixels, bytes)


def test_dataset_names_are_stable() -> None:
    assert get_image_dataset_names() == ["gradient", "checker", "diagonal_ramp", "noise"]


def test_make_image_dataset_dispatches() -> None:
    image = make_image_dataset("noise", 8, 8, 1234)

    assert image.name == "noise"
```

## File: `tests/test_image_gplite_optimizer.py`

```python
from primesymbolicmdl.image_datasets import make_checker_image, make_gradient_image, make_noise_image
from primesymbolicmdl.optimizers import OptimizerRequest, run_optimizer


def test_image_gplite_runs_on_tiny_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-GP-lite"
    assert result.total_bits < result.raw_bits
    assert result.details["residual_codec"] == "fixed_signed"
    assert isinstance(result.details["would_use_fallback"], bool)


def test_image_gplite_is_deterministic_for_same_seed() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=2024,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    left = run_optimizer("Image-GP-lite", request)
    right = run_optimizer("Image-GP-lite", request)

    assert left.best_model == right.best_model
    assert left.total_bits == right.total_bits


def test_image_gplite_accepts_named_primitive_sets() -> None:
    image = make_gradient_image(8, 8)
    for primitive_set in ("local", "ramp", "structure", "full"):
        request = OptimizerRequest(
            data=image.pixels,
            width_bits=8,
            seed=1234,
            population_size=8,
            generations=4,
            max_index=7,
            strict_lower=False,
            metadata={
                "image_width": image.width,
                "image_height": image.height,
                "dataset_name": image.name,
                "image_gplite_primitive_set": primitive_set,
            },
        )
        result = run_optimizer("Image-GP-lite", request)
        assert result.status == "ok"


def test_image_gplite_rejects_unknown_primitive_set() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=7,
        strict_lower=False,
        metadata={
            "image_width": image.width,
            "image_height": image.height,
            "dataset_name": image.name,
            "image_gplite_primitive_set": "mystery",
        },
    )

    try:
        run_optimizer("Image-GP-lite", request)
    except ValueError as exc:
        assert "primitive set" in str(exc)
    else:
        raise AssertionError("Unknown primitive set should raise ValueError")


def test_structure_primitive_set_finds_checker_like_model() -> None:
    image = make_checker_image(8, 8, 4)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_index=7,
        strict_lower=False,
        metadata={
            "image_width": image.width,
            "image_height": image.height,
            "dataset_name": image.name,
            "image_gplite_primitive_set": "structure",
        },
    )

    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert "checker_parity" in result.best_model
    assert result.total_bits < result.raw_bits


def test_image_gplite_runs_on_noise_without_promising_a_win() -> None:
    image = make_noise_image(8, 8, 1234)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert isinstance(result.best_model, str)
    assert isinstance(result.total_bits, int)
```

## File: `tests/test_image_law_branch.py`

```python
from primesymbolicmdl.image_context_laws import terminal_law
from primesymbolicmdl.image_datasets import make_checker_image, make_diagonal_ramp_image, make_gradient_image
from primesymbolicmdl.image_law_branch import (
    decode_image_law_payload,
    encode_image_law_payload,
    estimate_image_law_cost,
    roundtrip_image_law,
)


def test_x_ramp_law_can_exactly_match_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    law = terminal_law("x_ramp")
    cost = estimate_image_law_cost(image, law)

    assert roundtrip_image_law(image, law) == image.pixels
    assert cost["residual_codec"] == "fixed_signed"
    assert cost["raw_bits"] == image.width * image.height * 8
    assert cost["total_bits"] < cost["raw_bits"]


def test_diagonal_ramp_law_roundtrips_diagonal_image() -> None:
    image = make_diagonal_ramp_image(8, 8)
    law = terminal_law("diag_ramp")

    assert roundtrip_image_law(image, law) == image.pixels


def test_image_law_payload_roundtrips_checker_even_without_win() -> None:
    image = make_checker_image(8, 8, 4)
    payload = encode_image_law_payload(image, terminal_law("x_ramp"))

    assert decode_image_law_payload(payload) == image.pixels


def test_image_law_cost_report_contains_required_fields() -> None:
    image = make_gradient_image(4, 4)
    cost = estimate_image_law_cost(image, terminal_law("x_ramp"))

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "min_residual",
        "max_residual",
        "pixel_count",
        "model",
    }

    assert required.issubset(cost)
```

## File: `tests/test_image_predictor_branch.py`

```python
from primesymbolicmdl.image_datasets import make_checker_image, make_diagonal_ramp_image, make_gradient_image, make_noise_image
from primesymbolicmdl.image_datasets import make_gray_image
from primesymbolicmdl.image_predictor_branch import (
    decode_image_predictor_payload,
    encode_image_predictor_payload,
    estimate_image_predictor_cost,
    roundtrip_image_predictor,
)
from primesymbolicmdl.image_predictors import ImagePredictorModel


def test_x_ramp_predictor_can_exactly_match_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    cost = estimate_image_predictor_cost(image, ImagePredictorModel("x_ramp"))

    assert cost["residual_width"] == 0
    assert cost["residual_codec"] == "fixed_signed"
    assert cost["total_bits"] < cost["raw_bits"]


def test_diagonal_ramp_predictor_roundtrips_diagonal_ramp() -> None:
    image = make_diagonal_ramp_image(8, 8)
    model = ImagePredictorModel("diagonal_ramp")

    assert roundtrip_image_predictor(image, model) == image.pixels


def test_checker_predictor_roundtrips_checker_image() -> None:
    image = make_checker_image(8, 8, 4)
    payload = encode_image_predictor_payload(image, ImagePredictorModel("checker", {"block": 4}))

    assert decode_image_predictor_payload(payload) == image.pixels


def test_zero_predictor_roundtrips_noise_even_without_compression_win() -> None:
    image = make_noise_image(8, 8, 1234)
    model = ImagePredictorModel("zero")
    cost = estimate_image_predictor_cost(image, model)

    assert roundtrip_image_predictor(image, model) == image.pixels
    assert isinstance(cost["ratio_vs_raw"], float)


def test_cost_report_contains_required_fields() -> None:
    image = make_gradient_image(4, 4)
    cost = estimate_image_predictor_cost(image, ImagePredictorModel("x_ramp"))

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "min_residual",
        "max_residual",
        "residual_width",
        "pixel_count",
        "model",
    }

    assert required.issubset(cost)


def test_nonzero_constant_residuals_still_need_positive_width() -> None:
    image = make_gray_image("constant", 4, 4, bytes([5] * 16))
    cost = estimate_image_predictor_cost(image, ImagePredictorModel("zero"))

    assert cost["min_residual"] == 5
    assert cost["max_residual"] == 5
    assert cost["residual_width"] > 0


def test_predictor_payload_carries_residual_codec_metadata() -> None:
    image = make_gradient_image(8, 8)
    payload = encode_image_predictor_payload(image, ImagePredictorModel("x_ramp"))

    assert payload["residual_codec"] == "fixed_signed"
    assert isinstance(payload["residual_payload"], dict)
```

## File: `tests/test_image_predictor_optimizer.py`

```python
from primesymbolicmdl.optimizers import OptimizerRequest, run_optimizer


def test_image_predictor_optimizer_runs_on_gradient_image() -> None:
    width = 8
    height = 8
    pixels = bytes((255 * col) // max(1, width - 1) for _row in range(height) for col in range(width))
    request = OptimizerRequest(
        data=pixels,
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": width, "image_height": height, "dataset_name": "gradient"},
    )

    result = run_optimizer("Image-predictor", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-predictor"
    assert result.best_model == "x_ramp"
    assert result.total_bits < result.raw_bits
    assert result.details["would_use_fallback"] is False
    assert result.details["residual_codec"] == "fixed_signed"


def test_image_predictor_requires_image_metadata() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01\x02\x03",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
    )

    try:
        run_optimizer("Image-predictor", request)
    except ValueError as exc:
        assert "image_width" in str(exc)
    else:
        raise AssertionError("Image-predictor should require image metadata")
```

## File: `tests/test_image_predictors.py`

```python
from primesymbolicmdl.image_predictors import (
    ImagePredictorModel,
    default_image_predictor_models,
    image_predictor_model_bits,
    image_predictor_parameter_bits,
    predict_pixel,
    render_image_predictor,
)


def test_default_image_predictor_models_are_stable() -> None:
    models = default_image_predictor_models()

    assert [render_image_predictor(model) for model in models] == [
        "zero",
        "left",
        "up",
        "avg_left_up",
        "gradient",
        "x_ramp",
        "y_ramp",
        "diagonal_ramp",
        "checker(block=1)",
        "checker(block=2)",
        "checker(block=4)",
        "checker(block=8)",
        "checker(block=16)",
    ]


def test_predict_pixel_supports_context_predictors() -> None:
    assert predict_pixel(ImagePredictorModel("zero"), 2, 3, 8, 8, 11, 22, 33) == 0
    assert predict_pixel(ImagePredictorModel("left"), 2, 3, 8, 8, 11, 22, 33) == 11
    assert predict_pixel(ImagePredictorModel("up"), 2, 3, 8, 8, 11, 22, 33) == 22
    assert predict_pixel(ImagePredictorModel("avg_left_up"), 2, 3, 8, 8, 11, 22, 33) == 16
    assert predict_pixel(ImagePredictorModel("gradient"), 2, 3, 8, 8, 11, 22, 33) == 0


def test_predict_pixel_supports_geometric_predictors() -> None:
    assert predict_pixel(ImagePredictorModel("x_ramp"), 7, 0, 8, 8, 0, 0, 0) == 255
    assert predict_pixel(ImagePredictorModel("y_ramp"), 0, 7, 8, 8, 0, 0, 0) == 255
    assert predict_pixel(ImagePredictorModel("diagonal_ramp"), 7, 7, 8, 8, 0, 0, 0) == 255
    assert predict_pixel(ImagePredictorModel("checker", {"block": 2}), 3, 0, 8, 8, 0, 0, 0) == 255


def test_predict_pixel_clamps_gradient_to_byte_range() -> None:
    assert predict_pixel(ImagePredictorModel("gradient"), 1, 1, 8, 8, 255, 255, 0) == 255


def test_image_predictor_bit_helpers_are_deterministic() -> None:
    assert image_predictor_model_bits(ImagePredictorModel("zero")) == 4
    assert image_predictor_parameter_bits(ImagePredictorModel("zero")) == 0
    assert image_predictor_parameter_bits(ImagePredictorModel("checker", {"block": 16})) > 0
```

## File: `tests/test_image_soma_optimizer.py`

```python
from primesymbolicmdl.image_datasets import make_gradient_image, make_noise_image
from primesymbolicmdl.optimizers import OptimizerRequest, run_optimizer
from primesymbolicmdl.optimizers.image_soma import ImageSomaModel


def test_image_soma_runs_on_tiny_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    result = run_optimizer("Image-SOMA", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-SOMA"
    assert result.total_bits < result.raw_bits
    assert result.details["residual_codec"] == "fixed_signed"
    assert isinstance(result.details["would_use_fallback"], bool)


def test_image_soma_is_deterministic_for_same_seed() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=2025,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    left = run_optimizer("Image-SOMA", request)
    right = run_optimizer("Image-SOMA", request)

    assert left.best_model == right.best_model
    assert left.total_bits == right.total_bits


def test_image_soma_rendering_is_stable() -> None:
    model = ImageSomaModel(256, 0, 0, 256, 0, 0, 0)

    assert (
        model.render()
        == "image_soma(w_left=256, w_up=0, w_up_left=0, w_x=256, w_y=0, w_diag=0, bias=0, scale=256)"
    )


def test_image_soma_runs_on_noise_without_promising_a_win() -> None:
    image = make_noise_image(8, 8, 1234)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    result = run_optimizer("Image-SOMA", request)

    assert result.status == "ok"
    assert isinstance(result.best_model, str)
    assert isinstance(result.total_bits, int)
```

## File: `tests/test_index_branch.py`

```python
from primesymbolicmdl.anchor_laws import const_law, idx_law, sub_law
from primesymbolicmdl.index_branch import (
    encode_block_with_law,
    estimate_law_cost,
    roundtrip_law_payload,
)


def test_encode_block_with_law_reconstructs_x() -> None:
    encoded = encode_block_with_law(7, idx_law(), max_index=10)

    assert not encoded["escaped"]
    assert encoded["anchor"] + encoded["residual"] == 7


def test_strict_lower_false_allows_equal_anchor() -> None:
    encoded = encode_block_with_law(7, idx_law(), max_index=10, strict_lower=False)

    assert encoded["anchor"] == 7
    assert encoded["residual"] == 0


def test_strict_lower_true_disallows_equal_anchor() -> None:
    encoded = encode_block_with_law(7, idx_law(), max_index=10, strict_lower=True)

    assert encoded["anchor"] == 6
    assert encoded["residual"] == 1


def test_escape_case_works() -> None:
    encoded = encode_block_with_law(3, const_law(10), max_index=0)

    assert encoded["escaped"]
    assert encoded["index"] is None
    assert encoded["anchor"] == 0
    assert encoded["residual"] == 3


def test_estimate_law_cost_returns_required_fields() -> None:
    costs = estimate_law_cost([0, 1, 2, 3], 8, 4, idx_law(), max_index=3)

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "flag_bits",
        "index_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "escape_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "escape_count",
        "block_count",
        "max_index",
        "strict_lower",
        "law",
    }

    assert required.issubset(costs)
    assert costs["raw_bits"] == 32
    assert isinstance(costs["total_bits"], int)
    assert isinstance(costs["saving_bits"], int)
    assert isinstance(costs["ratio_vs_raw"], float)


def test_roundtrip_law_payload_width_8() -> None:
    data = b"\x00\x01\x02\x03\x04"

    assert roundtrip_law_payload(data, 8, idx_law(), max_index=4) == data


def test_roundtrip_law_payload_width_16() -> None:
    data = b"\x00\x00\x00\x01\x00\x02\x00\x03"
    law = sub_law(idx_law(), const_law(0))

    assert roundtrip_law_payload(data, 16, law, max_index=3) == data
```

## File: `tests/test_law_demo.py`

```python
import importlib
import io
from contextlib import redirect_stdout

from primesymbolicmdl import law_demo


def test_law_demo_module_is_importable() -> None:
    module = importlib.import_module("primesymbolicmdl.law_demo")

    assert hasattr(module, "main")


def test_law_demo_runs_and_prints_summary() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        law_demo.main()

    output = stdout.getvalue()
    assert "dataset:" in output
    assert "best_law:" in output
```

## File: `tests/test_law_search.py`

```python
from primesymbolicmdl.experiments import dataset_random, dataset_zeros
from primesymbolicmdl.law_search import search_best_law_for_bytes


def test_search_result_includes_required_fields() -> None:
    result = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )

    required = {
        "best_law",
        "best_law_string",
        "best_cost",
        "raw_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "generations",
        "population_size",
        "seed",
        "history",
        "max_index",
        "strict_lower",
    }

    assert required.issubset(result)
    assert result["history"]


def test_search_is_deterministic_for_same_seed() -> None:
    left = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )
    right = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )

    assert left["best_law_string"] == right["best_law_string"]
    assert left["total_bits"] == right["total_bits"]


def test_search_finishes_and_can_improve_on_zero_data() -> None:
    result = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )

    assert result["saving_bits"] > 0


def test_search_does_not_need_to_beat_random_data() -> None:
    result = search_best_law_for_bytes(
        dataset_random(64, 1234),
        width_bits=8,
        seed=1234,
        population_size=10,
        generations=5,
        max_depth=3,
        max_index=7,
    )

    assert "best_law_string" in result
    assert isinstance(result["total_bits"], int)
```

## File: `tests/test_optimizers.py`

```python
from primesymbolicmdl.optimizers import OptimizerRequest, get_optimizer_names, run_optimizer


def test_optimizer_registry_names_are_stable() -> None:
    assert get_optimizer_names() == ["GP-lite", "SOMA", "GP", "ADAM", "Image-predictor", "Image-GP-lite", "Image-SOMA"]


def test_can_run_gplite_optimizer_on_tiny_data() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01\x02\x03",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
    )
    result = run_optimizer("GP-lite", request)

    assert result.status == "ok"
    assert result.optimizer_name == "GP-lite"


def test_can_run_soma_optimizer_on_tiny_data() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01\x02\x03",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
    )
    result = run_optimizer("SOMA", request)

    assert result.status == "ok"
    assert result.optimizer_name == "SOMA"


def test_placeholders_return_not_implemented() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01",
        width_bits=8,
        seed=1234,
        population_size=4,
        generations=2,
        max_index=1,
        strict_lower=False,
    )

    gp_result = run_optimizer("GP", request)
    adam_result = run_optimizer("ADAM", request)

    assert gp_result.status == "not_implemented"
    assert adam_result.status == "not_implemented"


def test_can_run_image_predictor_optimizer_on_tiny_image() -> None:
    request = OptimizerRequest(
        data=b"\x00\x40\x80\xc0",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
        metadata={"image_width": 2, "image_height": 2, "dataset_name": "tiny"},
    )
    result = run_optimizer("Image-predictor", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-predictor"


def test_can_run_image_gplite_optimizer_on_tiny_image() -> None:
    request = OptimizerRequest(
        data=b"\x00\x40\x80\xc0",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
        metadata={"image_width": 2, "image_height": 2, "dataset_name": "tiny"},
    )
    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-GP-lite"


def test_can_run_image_soma_optimizer_on_tiny_image() -> None:
    request = OptimizerRequest(
        data=b"\x00\x40\x80\xc0",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
        metadata={"image_width": 2, "image_height": 2, "dataset_name": "tiny"},
    )
    result = run_optimizer("Image-SOMA", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-SOMA"
```

## File: `tests/test_prime_anchors.py`

```python
import pytest

from primesymbolicmdl.prime_anchors import (
    is_prime,
    nearest_lower_prime,
    nearest_prime,
    nearest_upper_prime,
    prime_anchor_residual,
    primes_up_to,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (21, False),
    ],
)
def test_is_prime_known_values(value: int, expected: bool) -> None:
    assert is_prime(value) is expected


def test_primes_up_to_small_limit() -> None:
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]


@pytest.mark.parametrize(
    ("value", "lower", "upper", "nearest"),
    [
        (1, None, 2, 2),
        (2, 2, 2, 2),
        (4, 3, 5, 3),
        (8, 7, 11, 7),
        (12, 11, 13, 11),
        (14, 13, 17, 13),
    ],
)
def test_nearest_prime_helpers(value: int, lower: int | None, upper: int, nearest: int) -> None:
    assert nearest_lower_prime(value) == lower
    assert nearest_upper_prime(value) == upper
    assert nearest_prime(value) == nearest


@pytest.mark.parametrize(
    ("value", "mode"),
    [
        (0, "nearest"),
        (1, "lower"),
        (1, "upper"),
        (2, "nearest"),
        (10, "lower"),
        (10, "upper"),
        (10, "nearest"),
        (255, "nearest"),
    ],
)
def test_prime_anchor_residual_reconstructs_exactly(value: int, mode: str) -> None:
    anchor, residual = prime_anchor_residual(value, mode)

    assert is_prime(anchor)
    assert value == anchor + residual
```

## File: `tests/test_prime_bigint.py`

```python
import pytest

from primesymbolicmdl.prime_bigint import (
    is_probably_prime_deterministic_64,
    next_prime_64,
    prev_prime_64,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (21, False),
        (2**31 - 1, True),
    ],
)
def test_is_probably_prime_deterministic_64_known_values(value: int, expected: bool) -> None:
    assert is_probably_prime_deterministic_64(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, None),
        (1, None),
        (2, 2),
        (3, 3),
        (4, 3),
        (20, 19),
        (30, 29),
    ],
)
def test_prev_prime_64_returns_expected_values(value: int, expected: int | None) -> None:
    assert prev_prime_64(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 3),
        (4, 5),
        (20, 23),
        (30, 31),
    ],
)
def test_next_prime_64_returns_expected_values(value: int, expected: int) -> None:
    assert next_prime_64(value) == expected


def test_prime_bigint_rejects_values_at_or_above_two_to_the_64() -> None:
    limit = 1 << 64
    with pytest.raises(ValueError):
        is_probably_prime_deterministic_64(limit)
    with pytest.raises(ValueError):
        prev_prime_64(limit)
    with pytest.raises(ValueError):
        next_prime_64(limit)
```

## File: `tests/test_random_sanity.py`

```python
import random

from primesymbolicmdl.codec import compress_experimental, decompress_experimental


def test_random_bytes_prefer_raw_fallback() -> None:
    rng = random.Random(1234)
    data = bytes(rng.randrange(256) for _ in range(1024))
    payload = compress_experimental(data, width_bits=16, mode="nearest")

    assert payload["codec"] == "raw"
    assert decompress_experimental(payload) == data
```

## File: `tests/test_repository_rules.py`

```python
from pathlib import Path


def test_no_local_pytest_shim_exists() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    assert not (repo_root / "pytest").exists()
```

## File: `tests/test_residual_binary.py`

```python
import random

from primesymbolicmdl.residual_binary import decode_residuals_binary, encode_residuals_binary


def test_fixed_signed_binary_roundtrip_for_all_zero_residuals() -> None:
    residuals = [0] * 32
    blob = encode_residuals_binary(residuals, codec_name="fixed_signed")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_fixed_signed_binary_roundtrip_for_mixed_values() -> None:
    residuals = [-7, -1, 0, 2, 9, -3, 4]
    blob = encode_residuals_binary(residuals, codec_name="fixed_signed")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_zero_rle_binary_roundtrip_for_zero_heavy_stream() -> None:
    residuals = [0, 0, 0, 5, 0, 0, -2, 0, 0, 0, 0, 8]
    blob = encode_residuals_binary(residuals, codec_name="zero_rle")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_unknown_codec_name_falls_back_to_varint_residuals() -> None:
    residuals = [-11, 0, 17, -3, 4]
    blob = encode_residuals_binary(residuals, codec_name="unsupported_codec_name")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_random_deterministic_residual_roundtrip_with_auto_codec() -> None:
    rng = random.Random(1234)
    residuals = [rng.randint(-20, 20) for _ in range(64)]
    blob = encode_residuals_binary(residuals, codec_name=None)

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals
```

## File: `tests/test_residual_codecs.py`

```python
from primesymbolicmdl.residual_codecs import (
    choose_best_byte_codec,
    choose_best_residual_codec,
    decode_byte_rle_payload,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    estimate_byte_rle_bits,
    estimate_fixed_signed_residual_bits,
    estimate_zero_rle_residual_bits,
    zigzag_decode,
    zigzag_encode,
)


def test_zigzag_roundtrip_for_signed_values() -> None:
    values = [-9, -2, -1, 0, 1, 2, 9]

    assert [zigzag_decode(zigzag_encode(value)) for value in values] == values


def test_fixed_signed_codec_roundtrips() -> None:
    residuals = [-3, 0, 4, -1, 2]
    result = estimate_fixed_signed_residual_bits(residuals)

    assert decode_fixed_signed_residual_payload(result.payload) == residuals


def test_all_zero_fixed_signed_codec_has_zero_bits() -> None:
    result = estimate_fixed_signed_residual_bits([0] * 12)

    assert result.bits == 0
    assert decode_fixed_signed_residual_payload(result.payload) == [0] * 12


def test_zero_rle_roundtrips_mixed_residuals() -> None:
    residuals = [0, 0, 5, 0, -3, 0, 0, 0, 7]
    result = estimate_zero_rle_residual_bits(residuals)

    assert decode_zero_rle_residual_payload(result.payload) == residuals


def test_zero_rle_has_low_cost_for_long_zero_run() -> None:
    residuals = [0] * 64
    result = estimate_zero_rle_residual_bits(residuals)

    assert result.bits > 0
    assert result.bits < (len(residuals) * 8)


def test_byte_rle_roundtrips_repeated_bytes() -> None:
    data = b"\x00\x00\x00\xff\xff\x01\x01\x01\x01"
    result = estimate_byte_rle_bits(data)

    assert decode_byte_rle_payload(result.payload) == data


def test_choose_best_byte_codec_is_stable_for_random_like_data() -> None:
    data = bytes(range(32))
    result = choose_best_byte_codec(data)

    assert result.codec_name in {"raw_bytes", "byte_rle"}
    assert isinstance(result.bits, int)


def test_residual_codec_selector_returns_required_fields() -> None:
    result = choose_best_residual_codec([0, 0, 1, 0, -1])

    assert result.codec_name in {"fixed_signed", "zero_rle"}
    assert isinstance(result.bits, int)
    assert isinstance(result.payload, dict)
    assert isinstance(result.details, dict)
```

## File: `tests/test_scaled_prime_demo.py`

```python
import io
from contextlib import redirect_stdout

from primesymbolicmdl import scaled_prime_demo


def test_scaled_prime_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        scaled_prime_demo.main()

    output = stdout.getvalue()
    assert "dataset: ascii_small" in output
    assert "dataset: random_bytes" in output
    assert "best_model:" in output
    assert "residual_codec:" in output
    assert "roundtrip_ok: True" in output
    assert "decision:" in output


def test_scaled_prime_demo_results_are_exact_roundtrips() -> None:
    results = scaled_prime_demo.run_demo()

    assert results
    assert all(result["roundtrip_ok"] for result in results)
```

## File: `tests/test_scaled_prime_index.py`

```python
import pytest

from primesymbolicmdl.huge_blocks import bytes_to_huge_blocks
from primesymbolicmdl.scaled_prime_index import (
    ScaledPrimeModel,
    decode_scaled_prime_payload,
    encode_block_scaled_prime,
    encode_scaled_prime_payload,
    estimate_scaled_prime_cost,
    model_bits_scaled_prime,
    parameter_bits_scaled_prime,
    render_scaled_prime_model,
    roundtrip_scaled_prime,
)


def test_encode_block_scaled_prime_reconstructs_block() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=2)
    encoded = encode_block_scaled_prime(37, 16, model)

    assert not encoded["escaped"]
    assert encoded["anchor"] + encoded["diff"] == 37


def test_encode_block_scaled_prime_escape_for_zero() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=0)
    encoded = encode_block_scaled_prime(0, 8, model)

    assert encoded["escaped"]
    assert encoded["index"] is None
    assert encoded["diff"] == 0


def test_scaled_prime_helpers_return_stable_metadata() -> None:
    model = ScaledPrimeModel(shift=4, direction="lower", search_radius=2)

    assert render_scaled_prime_model(model) == "scaled_prime(direction=lower, shift=4, search_radius=2)"
    assert model_bits_scaled_prime(model) > 0
    assert parameter_bits_scaled_prime(model) > 0


def test_estimate_scaled_prime_cost_returns_required_fields() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=2)
    data = b"\x00\x02\x00\x03\x00\x05\x00\x07"
    blocks = bytes_to_huge_blocks(data, 16)
    costs = estimate_scaled_prime_cost(blocks, 16, len(data), model)

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "flag_bits",
        "index_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "escape_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "escape_count",
        "block_count",
        "model",
    }

    assert required.issubset(costs)
    assert costs["raw_bits"] == len(data) * 8


@pytest.mark.parametrize(
    ("width_bits", "data"),
    [
        (16, b"\x00\x02\x00\x03\x00\x05\x00\x07"),
        (32, b"\x00\x00\x00\x11\x00\x00\x00\x13"),
        (64, b"\x00\x00\x00\x00\x00\x00\x00\x11"),
    ],
)
def test_scaled_prime_payload_roundtrip_is_exact(width_bits: int, data: bytes) -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=2)
    payload = encode_scaled_prime_payload(data, width_bits, model)

    assert decode_scaled_prime_payload(payload) == data
    assert roundtrip_scaled_prime(data, width_bits, model) == data


def test_scaled_prime_branch_rejects_width_above_64() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=0)

    with pytest.raises(ValueError):
        encode_scaled_prime_payload(b"\x00" * 12, 96, model)
```

## File: `tests/test_scaled_prime_search.py`

```python
from primesymbolicmdl.scaled_prime_search import search_best_scaled_prime_model


def test_scaled_prime_search_runs_on_tiny_deterministic_data() -> None:
    data = b"\x00\x02\x00\x03\x00\x05\x00\x07"
    result = search_best_scaled_prime_model(data, width_bits=16)

    assert result["best_model_string"]
    assert result["raw_bits"] == len(data) * 8
    assert result["roundtrip_ok"] is True
    assert result["history"]


def test_scaled_prime_search_is_deterministic_for_same_seed() -> None:
    data = b"\x00\x02\x00\x03\x00\x05\x00\x07"
    left = search_best_scaled_prime_model(data, width_bits=16, seed=1234)
    right = search_best_scaled_prime_model(data, width_bits=16, seed=1234)

    assert left["best_model"] == right["best_model"]
    assert left["best_model_string"] == right["best_model_string"]
    assert left["total_bits"] == right["total_bits"]
    assert left["history"] == right["history"]


def test_scaled_prime_search_handles_random_data_without_crashing() -> None:
    data = bytes(range(24))
    result = search_best_scaled_prime_model(data, width_bits=24)

    assert result["roundtrip_ok"] is True
    assert isinstance(result["total_bits"], int)
    assert isinstance(result["saving_bits"], int)


def test_scaled_prime_search_handles_structured_low_range_data() -> None:
    data = (b"\x00\x11" * 8) + (b"\x00\x13" * 8)
    result = search_best_scaled_prime_model(data, width_bits=16)

    assert result["roundtrip_ok"] is True
    assert result["best_model_string"].startswith("scaled_prime(")
```

## File: `tests/test_sim_demo.py`

```python
import io
from contextlib import redirect_stdout

from primesymbolicmdl import sim_demo


def test_sim_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        sim_demo.main()

    output = stdout.getvalue()
    assert "optimizer: Image-predictor" in output
    assert "optimizer: Image-GP-lite" in output
    assert "optimizer: Image-SOMA" in output
    assert "optimizer: GP-lite" in output
    assert "optimizer: SOMA" in output
    assert "residual_codec:" in output
    assert "raw_byte_codec:" in output
    assert "## Image-GP-lite primitive ablation summary: gradient" in output
    assert "primitive_set" in output
```

## File: `tests/test_simulation.py`

```python
from primesymbolicmdl.image_datasets import make_gray_image, make_image_dataset
from primesymbolicmdl.simulation import bits_to_bytes_ceil, format_simulation_report, run_gray_image_simulation, run_image_simulation


def test_run_image_simulation_returns_required_fields() -> None:
    result = run_image_simulation(
        "GP-lite",
        dataset_name="gradient",
        image_width=8,
        image_height=8,
        population_size=8,
        generations=4,
        max_index=7,
    )
    required = {
        "optimizer_name",
        "status",
        "dataset_name",
        "image_width",
        "image_height",
        "raw_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "raw_bytes",
        "total_bytes_estimate",
        "saving_bytes_estimate",
        "best_model",
        "history",
        "details",
    }

    assert required.issubset(result)


def test_format_simulation_report_returns_readable_text() -> None:
    result = run_image_simulation(
        "Image-predictor",
        dataset_name="gradient",
        image_width=8,
        image_height=8,
        population_size=8,
        generations=4,
        max_index=7,
    )
    report = format_simulation_report(result)

    assert "optimizer:" in report
    assert "raw_bits:" in report
    assert "raw_bytes:" in report
    assert "total_bytes_estimate:" in report
    assert "decision:" in report
    assert "fallback_recommendation:" in report
    assert "residual_codec:" in report
    assert "raw_byte_codec:" in report


def test_gplite_and_soma_both_run_on_tiny_gradient() -> None:
    left = run_image_simulation("GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    right = run_image_simulation("SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert left["status"] == "ok"
    assert right["status"] == "ok"


def test_image_gplite_and_image_soma_run_on_tiny_gradient() -> None:
    left = run_image_simulation("Image-GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    right = run_image_simulation("Image-SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert left["status"] == "ok"
    assert right["status"] == "ok"
    assert left["details"]["residual_codec"] == "fixed_signed"
    assert right["details"]["residual_codec"] == "fixed_signed"


def test_image_gplite_simulation_accepts_primitive_set_metadata() -> None:
    result = run_image_simulation(
        "Image-GP-lite",
        "checker",
        8,
        8,
        population_size=8,
        generations=4,
        max_index=7,
        image_gplite_primitive_set="structure",
    )

    assert result["status"] == "ok"
    assert result["details"]["resolved_primitive_set"] == "structure"
    assert "primitive_set:" in format_simulation_report(result)


def test_image_predictor_runs_on_tiny_gradient() -> None:
    result = run_image_simulation("Image-predictor", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert result["status"] == "ok"
    assert result["best_model"] == "x_ramp"
    assert result["details"]["residual_codec"] == "fixed_signed"
    assert result["details"]["raw_byte_codec"] in {"raw_bytes", "byte_rle"}
    assert result["preview"]["roundtrip_ok"] is True


def test_gp_placeholder_returns_not_implemented() -> None:
    result = run_image_simulation("GP", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert result["status"] == "not_implemented"


def test_bits_to_bytes_ceil_rounds_up() -> None:
    assert bits_to_bytes_ceil(0) == 0
    assert bits_to_bytes_ceil(8) == 1
    assert bits_to_bytes_ceil(9) == 2


def test_run_gray_image_simulation_accepts_external_image() -> None:
    image = make_gray_image("external", 4, 4, bytes(range(16)))
    result = run_gray_image_simulation(
        "GP-lite",
        image,
        population_size=8,
        generations=4,
        max_index=7,
    )

    assert result["dataset_name"] == "external"
    assert result["image_width"] == 4
    assert result["image_height"] == 4
    assert result["details"]["raw_byte_codec"] in {"raw_bytes", "byte_rle"}


def test_law_based_preview_roundtrips_for_gplite_and_soma() -> None:
    gplite_result = run_image_simulation("GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    soma_result = run_image_simulation("SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)

    for result in (gplite_result, soma_result):
        preview = result["preview"]
        assert preview["roundtrip_ok"] is True
        assert preview["decoded_image"].pixels == original.pixels
        assert len(preview["residual_image"].pixels) == 64


def test_image_predictor_preview_roundtrips_for_gradient() -> None:
    result = run_image_simulation("Image-predictor", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)
    preview = result["preview"]

    assert preview["anchor_label"] == "Predictor"
    assert preview["residual_label"] == "Residuals+128"
    assert preview["decoded_image"].pixels == original.pixels


def test_image_gplite_preview_roundtrips_for_gradient() -> None:
    result = run_image_simulation("Image-GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)
    preview = result["preview"]

    assert preview["roundtrip_ok"] is True
    assert preview["decoded_image"].pixels == original.pixels


def test_image_soma_preview_roundtrips_for_gradient() -> None:
    result = run_image_simulation("Image-SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)
    preview = result["preview"]

    assert preview["roundtrip_ok"] is True
    assert preview["decoded_image"].pixels == original.pixels
```

