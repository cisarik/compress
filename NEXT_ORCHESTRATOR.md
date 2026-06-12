# NEXT_ORCHESTRATOR.md — Strategic Handoff

This file is the handoff for the **next Orchestrator**, not the Worker.

## Recommended Read Order

1. `NEXT_ORCHESTRATOR.md`
2. `NEXT_AGENT.md` / `NEXT_WORKER.md`
3. `BOOT.md`
4. `BRAIN.md` only when deeper context is needed

## Current Phase

Compression practicalization. AP/meta is sufficient for this phase unless a blocking inconsistency appears.

Future product direction (not implemented): Linux CLI tool working name `analytic`.

## Verified Repo State

- `.psmdl` file CLI exists
- in-repo file benchmark exists
- external-corpus benchmark harness exists
- latest Worker target tests: `283 passed` before PSMDLRAW overhead work
- public commit verification loop: trust report, verify repo via SHA and diff

## Compression Evidence

External corpus (10 small files outside repo):

- 9/10 raw fallback with ~+12 B `PSMDLRAW1` overhead per file
- 1/10 compressed: `zoneinfo-utc.bin` 114 → 86 B (tiny structured file only)
- aggregate: 15720 → 15800 B (+80 B)
- exact roundtrip everywhere

Synthetic mechanism check still valid: `square_generated_64` can compress.

## Scientific Guardrails

- exact roundtrip mandatory
- raw fallback is normal
- actual bytes beat estimated bits
- no universal compression claims
- synthetic wins validate mechanism only

## Current Worker Direction

**PSMDLRAW overhead reduction** — reduce systematic raw-fallback container penalty before new anchor families or entropy coding.

## Recommended Strategy After Overhead Work

1. re-run the same 10-file external corpus and compare aggregate delta
2. only then consider narrow algorithm experiments or entropy coding

## Orchestrator Rules

- verify Worker reports against repo SHA and diff when possible
- keep `NEXT_AGENT.md` Worker-focused and `NEXT_ORCHESTRATOR.md` strategic
- do not let chat-style answers replace handoff files
### Report for ORCHESTRATOR_CHAT

## 1. Summary

Dokončené **obe požadované veci**: (1) vyčistené handoff súbory, (2) **PSMDLRAW overhead reduction** cez nový kompaktný formát **`PSMDLR2`**. Raw fallback overhead na malých súboroch klesol z **+12 B** na **+9 B**. Externý korpus: **15720 → 15773 B** (+53 B, predtým +80 B). Testy **285 passed**. Legacy `PSMDLRAW1` stále dekóduje.

`git rev-parse HEAD`: `d8f22b5777bc4e93263699e4357a52e7fedf1a55` (lokálne; zmeny zatiaľ uncommitted).

## 2. Handoff cleanup

| Súbor | Predtým | Teraz |
|-------|---------|-------|
| `NEXT_ORCHESTRATOR.md` | Worker benchmark report | Strategický Orchestrator handoff |
| `NEXT_AGENT.md` | Stale AP/meta prompt | Worker handoff + aktuálny stav |
| `NEXT_WORKER.md` | Orchestrator chat + GitHub linky | Krátky Worker pointer |

## 3. Files changed

| Súbor | Zmena |
|-------|--------|
| `src/primesymbolicmdl/huge_anchor_file.py` | `PSMDLR2` encode, `decode_raw_psmdl_v1/v2`, `raw_psmdl_container_overhead()` |
| `tests/test_huge_anchor_file_cli.py` | Testy overhead + legacy decode |
| `README.md` | Dokumentácia `PSMDLR2` / `PSMDLRAW1` |
| `NEXT_ORCHESTRATOR.md`, `NEXT_AGENT.md`, `NEXT_WORKER.md` | Vyčistené handoffy |

## 4. PSMDLR2 design

**Nový raw fallback (`PSMDLR2`):**
- magic `PSMDLR2` (7 B)
- `uint16_be` dĺžka pre payload ≤ 65535 B → **9 B overhead**
- pre väčšie súbory: marker `0xFF` + `uint32_be` → 12 B overhead

**Spätná kompatibilita:** `PSMDLRAW1` stále dekóduje cez `decode_raw_psmdl_v1`.

## 5. Commands run

```fish
cd /home/agile/compress
.venv/bin/pytest -q
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_corpus_benchmark \
  --input-dir /tmp/psmdl-external-corpus-7jJ9ig --recursive --width-bits 32
```

## 6. Test output

```
285 passed in 128.19s (0:02:08)
```

## 7. External corpus — pred / po

| metrika | PSMDLRAW1 | PSMDLR2 |
|---------|-----------|---------|
| raw fallback delta | +12 B/súbor | **+9 B/súbor** |
| total raw | 15720 B | 15720 B |
| total psmdl | 15800 B | **15773 B** |
| total delta | +80 B | **+53 B** |
| compressed | 1 (`zoneinfo-utc.bin` 114→86) | rovnaké |
| roundtrip failures | 0 | 0 |

## 8. Scientific framing

- Agregát stále **horší než raw** (+53 B) — žiadny hype
- Jediný win zostáva na miniatúrnom štruktúrovanom tzif súbore
- Exact roundtrip všade OK
- Úspora 27 B na korpuse je reálna, ale nedostačujúca na „kompressor“ claim

## 9. Warnings and limitations

- `.psmdl` na nekomprimovateľných súboroch je stále väčší než raw
- `ap_snapshot.fish` preskočený
- Žiadne git write / commit / push
- Huge-anchor `PSMDLHA1` kontajner nebol menený

## 10. Suggested next smallest step

**Jeden bounded smer:** buď ešte tenší raw passthrough (napr. odmietnuť zápis `.psmdl` keď nie je menší ako raw — už existuje `--require-compression`), alebo úzky experiment na konkrétnej triede dát, ak sa ukáže opakovaný actual-byte win. Entropy coding zatiaľ nie — aggregate stále negatívny.