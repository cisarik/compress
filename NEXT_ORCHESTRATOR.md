### Report for ORCHESTRATOR_CHAT

## 1. Summary

Spustený **external-corpus benchmark** na 10 malých súboroch mimo repozitára (dočasný korpus v `/tmp`). Všetky súbory roundtripujú presne. **9/10 raw fallback** s konštantným **+12 B** overheadom; **1/10 skutočne skomprimovaný** (`zoneinfo-utc.bin`, 114→86 B). Agregát: **15720 → 15800 B** (+80 B). Testy: **283 passed**. Žiadne zmeny kódu ani AP docs.

## 2. Files inspected

- `README.md`, `NEXT_AGENT.md`, `NEXT_ORCHESTRATOR.md`
- `src/primesymbolicmdl/huge_anchor_corpus_benchmark.py`
- `tests/test_huge_anchor_corpus_benchmark.py`
- `git rev-parse HEAD` → `e5988de54085a950ec4a57b186e0b09c20f6873c`

## 3. Corpus selection

**Prístup:** dočasný adresár mimo repa (`/tmp/psmdl-external-corpus-CngaRx`), skopírované bezpečné systémové súbory — **žiadny rekurzívny crawl home**, žiadne citlivé dáta.

| Súbor | Typ | Raw B |
|-------|-----|-------|
| `os-release` | ASCII config | 361 |
| `hosts` | ASCII config | 332 |
| `fstab` | ASCII config | 692 |
| `desktop-wine.desktop` | UTF-8 text | 1469 |
| `desktop-kcm_wallpaper.desktop` | UTF-8 text | 1613 |
| `pixmap-archlinux-logo.svg` | SVG | 1102 |
| `pixmap-archlinux-logo-text-dark.svg` | SVG | 4548 |
| `pixmap-timeshift.png` | PNG 128×128 | 3188 |
| `zoneinfo-europe-bratislava.bin` | tzif timezone | 2301 |
| `zoneinfo-utc.bin` | tzif timezone | 114 |

**10 súborov**, celkom **15720 B raw**, runtime benchmarku ~29 s pri `--width-bits 32`.

## 4. Files changed

**Žiadne.** Harness fungoval bez úprav.

## 5. Commands run

```fish
cd /home/agile/compress
git status --short
git diff --stat
git rev-parse HEAD
# corpus: mktemp + cp z /etc, /usr/share/pixmaps, /usr/share/applications, /usr/share/zoneinfo
.venv/bin/pytest -q
PYTHONPATH=src /usr/bin/python3.14 -m primesymbolicmdl.huge_anchor_corpus_benchmark \
  --input-dir /tmp/psmdl-external-corpus-CngaRx --recursive --width-bits 32
```

## 6. Test output

```
283 passed in 118.79s (0:01:58)
```

## 7. Per-file benchmark results

| súbor | typ | raw | psmdl | delta | decision | format | roundtrip |
|-------|-----|-----|-------|-------|----------|--------|-----------|
| desktop-kcm_wallpaper.desktop | text | 1613 | 1625 | +12 | raw_fallback | raw_fallback | OK |
| desktop-wine.desktop | text | 1469 | 1481 | +12 | raw_fallback | raw_fallback | OK |
| fstab | text | 692 | 704 | +12 | raw_fallback | raw_fallback | OK |
| hosts | text | 332 | 344 | +12 | raw_fallback | raw_fallback | OK |
| os-release | text | 361 | 373 | +12 | raw_fallback | raw_fallback | OK |
| pixmap-archlinux-logo-text-dark.svg | SVG | 4548 | 4560 | +12 | raw_fallback | raw_fallback | OK |
| pixmap-archlinux-logo.svg | SVG | 1102 | 1114 | +12 | raw_fallback | raw_fallback | OK |
| pixmap-timeshift.png | PNG | 3188 | 3200 | +12 | raw_fallback | raw_fallback | OK |
| zoneinfo-europe-bratislava.bin | tzif | 2301 | 2313 | +12 | raw_fallback | raw_fallback | OK |
| zoneinfo-utc.bin | tzif | 114 | 86 | **−28** | **compressed** | huge_anchor | OK |

## 8. Aggregate benchmark summary

```
file_count=10
total_raw_bytes=15720
total_psmdl_bytes=15800
total_delta_bytes=+80
compressed_count=1
raw_fallback_count=9
roundtrip_failure_count=0
error_count=0
```

## 9. Evidence-based analysis

**1. Skomprimovali sa nejaké reálne externé súbory?**  
Áno — **jeden**: `zoneinfo-utc.bin` (114 B, veľmi štruktúrovaný tzif s nulami a opakovanými hlavičkami). To je **úzky mechanizmus-check na mikroskopickom súbore**, nie dôkaz všeobecnej kompresie textov, PNG ani väčších tzif.

**2. Dominantný problém?**  
Dva jasné faktory:

- **Raw-fallback container overhead:** 9 súborov má presne **+12 B** delta — konzistentný `PSMDLRAW1` wrapper. Pri nekomprimovateľných dátach je `.psmdl` vždy horší než raw.
- **Slabý match anchor rodín k reálnym dátam:** text, SVG, PNG, väčší tzif — huge-anchor search nevyhrá; žiadna rodina neprekoná raw okrem miniatúrneho UTC súboru.

**3. Odporúčaný ďalší krok (jeden smer):**  
**Overhead reduction** — zmenšiť `PSMDLRAW1` (a prípadne hlavičku huge-anchor kontajnera), aby raw fallback nebol systematicky drahší o ~12 B na súbor. Bez toho je `.psmdl` na bežných externých súboroch vždy horší než ponechať raw bajty; to je silnejší signál než ďalší anchor-family experiment na tomto korpuse.

## 10. Warnings and limitations

- Korpus je malý a skôr systémový než „reálny user corpus“; stále mimo repa a privacy-safe.
- Jediný win je na **114 B** súbore — neprezentovať ako všeobecný výsledok.
- `ap_snapshot.fish` **preskočený** (testy už prešli; úspora času).
- Žiadne git write, commit, network.
- AP/meta súbory **nezmenené** (podľa zadania).

## 11. Suggested next smallest step

**Bounded overhead-reduction task:** navrhnúť a implementovať tenší raw-fallback formát (alebo voliteľný „store raw bytes without wrapper when not smaller“ režim s explicitnou dekódovateľnosťou), s roundtrip testami a re-runom tohto istého 10-súborového korpusu na porovnanie aggregate `total_delta_bytes`. Až potom zvážiť úzky algoritmický experiment, ak overhead už nebude dominovať.