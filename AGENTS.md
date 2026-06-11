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
- Do not run git commands.
- Do not create local shims for third-party tools such as pytest. If a required tool is missing, report the dependency and the exact install command.
- Report changed files and test results clearly.
- Use `NEXT_AGENT.md` as the single authoritative handoff file for the next Codex agent.
- Do not create `NEXT_PROMPT.md`, `NEXT_PROMPT2.md`, `NEXT_PROMPT3.md`, or similar chains of prompt files.
- When preparing a handoff, overwrite `NEXT_AGENT.md` with the current state and the current next task.
- After the handoff is consumed, the file may be deleted or replaced, but there should still be only one active handoff file at a time.

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

## Optimizer Architecture

- Keep optimizer names and registry wiring explicit and testable.
- Do not pretend placeholder optimizers are implemented.
- Reuse shared accounting and roundtrip machinery across optimizer families whenever possible.
- Compare optimizers on the same raw-bit baseline and the same MDL-style accounting.

## GUI Research Cockpit

- The GUI is for small deterministic research simulations, not benchmark theater.
- Prefer generated grayscale datasets first because they are cheap, reproducible, and headless-test friendly.
- If Tkinter is missing, report that the system package `tk` is needed instead of vendoring UI code.

## Handoff File

- `NEXT_AGENT.md` must contain the most important current context for the next Codex agent continuing this repository.
- The file should summarize architecture, hard rules, current test status, known limitations, and the exact next requested task.
- Keep it current. Replace stale handoff content instead of accumulating multiple prompt files.
