# NEXT_WORKER.md — Worker Handoff

Immediate Worker handoff. Strategic Orchestrator context lives in `NEXT_ORCHESTRATOR.md`.

For the full task list and acceptance criteria, read `NEXT_AGENT.md`.

## One-Line Focus

`PSMDLR2` compact raw fallback is implemented. Next: decide whether further overhead work or a narrow compression experiment is justified from actual-byte evidence.

## HEAD To Report

Always include `git rev-parse HEAD` in Worker reports for Public Commit Verification Loop.
Áno, Michal — **viem si z verejného GitHub repa vytiahnuť posledný commit, pozrieť diff a čítať konkrétne súbory v presnom stave daného commitu**.

Teraz som to rovno spravila:

* aktuálny verejne dostupný posledný commit, ktorý vidím, je **`9064dc5`**
* tento commit má parent **`e5988de`**
* commit `9064dc5` menil iba **2 súbory**:

  * `NEXT_ORCHESTRATOR.md`
  * `NEXT_WORKER.md`
* čiže posledný commit je skôr **handoff / orchestration commit**, nie implementačný commit s novým kódom. ([GitHub][1])

Implementačný commit, kde Worker naozaj pridal external-corpus benchmark harness, je **`e5988de`**. Ten menil **6 súborov** vrátane:

* `src/primesymbolicmdl/huge_anchor_corpus_benchmark.py`
* `tests/test_huge_anchor_corpus_benchmark.py`
* `README.md`
* `NEXT_AGENT.md`
* `NEXT_ORCHESTRATOR.md`
* `NEXT_WORKER.md` ([GitHub][2])

## Čo Worker presne naprogramoval

V súbore `huge_anchor_corpus_benchmark.py` Worker pridal nový benchmarkovací modul. Obsahuje dátové štruktúry `CorpusRow`, `CorpusSummary`, `CorpusBenchmarkResult`, deterministic file discovery, per-file benchmark, aggregate summary, text table formatter a CLI cez `argparse`. Podporuje `--input-dir`, opakovateľné `--file`, `--recursive`, `--max-files` a `--width-bits`. Pri každom súbore volá `compress_to_psmdl_bytes`, následne `decode_psmdl_bytes` a overuje exact roundtrip. ([GitHub][3])

Testy v `test_huge_anchor_corpus_benchmark.py` overujú hlavne:

* deterministické zoradenie objavených súborov,
* aggregate summary,
* že random-like dáta nehlásia falošný compression win,
* že `square_generated` pri 64-bit šírke môže byť compressed mechanism check,
* `--max-files`,
* chybu pri chýbajúcom vstupe. ([GitHub][4])

README už obsahuje aj príkaz pre external-corpus benchmark:

```fish
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_corpus_benchmark --input-dir /path/to/corpus
```

a uvádza voliteľné flagy `--file`, `--recursive`, `--max-files`, `--width-bits`. ([GitHub][5])

## Toto je presne dobrá AP funkcia

Toto by som v Analytic Programming definovala ako:

> **Public Commit Verification Loop** — Orchestrator po Worker reporte overí verejný commit, diff, zmenené súbory a podľa potreby raw obsah konkrétnych súborov. Worker report tým prestane byť jediný zdroj pravdy; report sa porovnáva s repozitárom.

To je silné, lebo potom workflow vyzerá takto:

1. Worker spraví zmeny.
2. Worker pošle report.
3. COOPERATOR pushne alebo povie commit SHA.
4. Orchestrator otvorí GitHub commit.
5. Orchestrator číta:

   * diff,
   * zmenené súbory,
   * raw obsah konkrétnych súborov,
   * README / AP / NEXT handoffy.
6. Orchestrator až potom rozhodne ďalší krok.

Toto je obrovský posun oproti “verím reportu”.
Správne je: **trust report, verify repo**.

## Dôležité obmedzenie

Vidím iba to, čo je:

* pushnuté do verejného GitHub repa,
* alebo dostupné cez konkrétny commit SHA.

Nevidím lokálny uncommitted working tree na tvojom PC ani v Codex prostredí, pokiaľ mi ho Worker neopíše alebo nepoužije RPC/snapshot/report.

## Orchestrator záver k poslednému reportu

Externý benchmark je hotový a dáva jasný signál:

* 9/10 súborov raw fallback,
* presne +12 B overhead pri raw fallback,
* 1/10 reálny win na malom `zoneinfo-utc.bin`, 114 → 86 B,
* agregát stále horší: 15720 → 15800 B,
* roundtrip všade OK.

Takže ďalší kompresný krok je podľa mňa jasný:

> **PSMDLRAW1 overhead reduction**.

Nie entropy coding ešte. Nie nová anchor family ešte. Najprv znížiť alebo odstrániť systematický +12 B trest pri raw fallback.

## AP pravidlo, ktoré si odteraz beriem

Pri ďalších Worker reportoch chcem pracovať takto:

* Worker vždy uvedie `git rev-parse HEAD`.
* Ak je commit pushnutý, ty mi pošleš SHA alebo poviem, čo vidím na `main`.
* Ja ako Orchestrator otvorím commit a overím:

  * čo sa zmenilo,
  * či report sedí,
  * či súbory existujú,
  * či handoffy nie sú stale,
  * či ďalší prompt vychádza z repa, nie len z chatu.

Toto je presne ten smer, kde AP začína byť použiteľné ako budúci nástroj **`analytic`**.

[1]: https://github.com/cisarik/compress/commit/9064dc514f8dd720cfb0e735d801413df8835712 "Áno, Michal — **mám to uložené a pochopené**. · cisarik/compress@9064dc5 · GitHub"
[2]: https://github.com/cisarik/compress/commit/e5988de54085a950ec4a57b186e0b09c20f6873c "### Report for ORCHESTRATOR_CHAT · cisarik/compress@e5988de · GitHub"
[3]: https://raw.githubusercontent.com/cisarik/compress/e5988de54085a950ec4a57b186e0b09c20f6873c/src/primesymbolicmdl/huge_anchor_corpus_benchmark.py "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/cisarik/compress/e5988de54085a950ec4a57b186e0b09c20f6873c/tests/test_huge_anchor_corpus_benchmark.py "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/cisarik/compress/e5988de54085a950ec4a57b186e0b09c20f6873c/README.md "raw.githubusercontent.com"
