### Report for ORCHESTRATOR_CHAT

## 1. Summary

Audit a benchmark nového `.psmdl` file CLI sú **dokončené**. Implementácia je konzistentná, exact roundtrip funguje na všetkých testovaných vstupoch a správanie je úprimné: reálne súbory z repa aj náhodné/repeated dáta končia ako **raw fallback** (`.psmdl` je väčší kvôli kontajneru), jediný skutočný huge-anchor win v benchmarke je **syntetický** `square_generated_64` (256 → 49 B). Pridaný bol malý opakovateľný benchmark skript s jedným testom.

## 2. Files inspected

- `src/primesymbolicmdl/huge_anchor_file.py`
- `src/primesymbolicmdl/huge_anchor_file_cli.py`
- `tests/test_huge_anchor_file_cli.py`

**Audit zistenia:**

| Oblasť | Hodnotenie |
|--------|------------|
| Formát | `decode_psmdl_bytes` rozlišuje `PSMDLHA1` (huge-anchor) vs `PSMDLRAW1` (raw fallback) podľa magic |
| Raw fallback | Pri `decision != "compressed"` sa zapíše `PSMDLRAW1` wrapper, nie väčší huge-anchor blob |
| Roundtrip | `compress_to_psmdl_bytes` overí `decode_psmdl_bytes(file_bytes) == payload` pred návratom |
| `--require-compression` | `PsmdlCompressionRefusedError`, CLI exit code `2`, výstupný súbor sa nevytvorí |
| Chyby | Neplatný magic → `ValueError`; CLI chyby → exit `1` (súbor neexistuje, corrupt magic) |
| CLI výstup | Jednoriadkový súhrn s `decision`, `file_format`, actual `raw_bytes` / `compressed_bytes` — bez estimated-bit hype |

Žiadne zavádzajúce compression claims v kóde ani výstupe.

## 3. Files changed

- `src/primesymbolicmdl/huge_anchor_file_benchmark.py` — nový deterministický benchmark
- `tests/test_huge_anchor_file_benchmark.py` — minimálny test benchmarku

**Nezmenené:** `huge_anchor_file.py`, `huge_anchor_file_cli.py`, dokumentácia (`README.md` stále neobsahuje CLI usage).

## 4. Commands run

```fish
cd /home/agile/compress
.venv/bin/pytest -q
.venv/bin/pytest -q tests/test_huge_anchor_file_benchmark.py
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_benchmark
PYTHONPATH=src /usr/bin/python3.14 -c "..."  # audit error handling
```

**Poznámka k Python invokácii:**

- `.venv/bin/pytest` — funguje
- `.venv/bin/python -m ...` — `sys.executable` smeruje na Cursor appimage, **nefunguje** pre `-m pytest`
- `PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_file_benchmark` — **funguje**

## 5. Full test results

```
277 passed in 114.76s (0:01:54)
```

Predchádzajúci stav: 276 passed. Nový test: `test_huge_anchor_file_benchmark_runs_and_reports_honest_sizes`.

## 6. Benchmark table (actual byte sizes)

| name | raw_bytes | psmdl_bytes | decision | file_format | roundtrip | `--require-compression` | note |
|------|-----------|-------------|----------|-------------|-----------|-------------------------|------|
| random_bytes_128 | 128 | 140 | raw_fallback | raw_fallback | OK | refused | deterministic random sanity |
| repeating_pattern | 128 | 140 | raw_fallback | raw_fallback | OK | refused | ABCD repeat |
| README.md | 11548 | 11560 | raw_fallback | raw_fallback | OK | refused | repo text file |
| AGENTS.md | 9904 | 9916 | raw_fallback | raw_fallback | OK | refused | repo text file |
| huge_anchor_file.py | 5182 | 5194 | raw_fallback | raw_fallback | OK | refused | repo python source |
| square_generated_64 | 256 | 49 | **compressed** | huge_anchor | OK | ok | synthetic structure-compatible |

**Preklep v mene:** `random_bytes_128` = 128 B raw (32 blokov × 4 B pri `width_bits=32`).

## 7. Roundtrip verification

Všetkých **6/6** benchmark prípadov: `decompress_file` po `compress_file` vráti **presne rovnaké bajty** ako vstup.

Doplnkový audit error paths:
- `decode_psmdl_bytes(b'BADMAGIC...')` → `Unsupported .psmdl file magic`
- `decode_psmdl_bytes(b'PSMDLRAW1')` → `Raw .psmdl payload is truncated`
- CLI decompress na corrupt `.psmdl` → exit `1`

## 8. Raw fallback / `--require-compression` behavior

**Default (bez `--require-compression`):**
- Ak huge-anchor blob nie je menší ako raw → zapíše sa `PSMDLRAW1` kontajner
- Overhead: typicky **+12 B** oproti raw (magic 8 + version 1 + varint + padding efekt)
- Roundtrip zostáva exact, ale `.psmdl` je **väčší** než pôvodný súbor

**S `--require-compression`:**
- Pri raw_fallback: **odmietnutie**, exit code `2`, žiadny výstupný súbor
- Pri skutočnej kompresii (`square_generated_64`): **úspech**, exit code `0`

**Náhodné bajty:** `raw_fallback`, `.psmdl` väčší než raw — **žiadny falošný compression win**.

## 9. Warnings and limitations

- Raw fallback kontajner pridáva overhead; na reálnych textoch/Python zdrojoch `.psmdl` je vždy väčší než raw.
- `repeating_pattern` tiež raw_fallback — kontajnerový overhead preváži (známe z huge-anchor binary demo).
- Jediný actual win je na **syntetickom** `square_generated` — nie dôkaz všeobecnej kompresie.
- Benchmark beží ~90–115 s (search + rerank na každom vstupe).
- `README.md` ešte nepopisuje CLI príkazy.
- `ap_snapshot.fish` nebol spustený.
- Žiadne git operácie, žiadne nové závislosti, žiadne sieťové volania.

## 10. Suggested next smallest step

Pridať krátku sekciu do `README.md` s CLI príkazmi a upozornením na raw-fallback overhead; potom benchmarkovať na malom korpuse reálnych binárnych súborov mimo repa (temp files) a reportovať len actual bytes — bez tvrdenia o univerzálnej kompresii.