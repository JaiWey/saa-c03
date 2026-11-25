# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file offline practice app for the AWS SAA-C03 exam (1019 questions). There is no package manager, bundler, or lint setup — the repo is a pipeline of standalone Python scripts that turn a question-bank PDF into JSON and then inject that JSON into an HTML template. The shipped output is one self-contained `index.html` (data inlined) that you open directly in a browser.

## Data pipeline (in order)

1. `parse.py` / `parse2.py` — parse text extracted from the source PDF (`/tmp/bank.txt`, not in repo) into `bank.json`. `parse2.py` repairs PDF ligature loss (`Con gure`→`Configure`, `tra c`→`traffic`) using a spellchecker (`pyspellchecker`) plus manual regexes; `fix.log` records the corrections. Question 868 option A is missing in the source PDF.
2. `build_data.py` — reads `bank.json`, attaches base64 PNG images for the few image-based questions (96, 253, 423, 429, 477, 494; read from `img/`, which is gitignored) and writes `data.json` (Chinese-version data; fields `n,q,o,a,cv,cp,v,qi,oi`).
3. `sol/b001.json … b041.json` — independently authored answers + explanations (`{n, a, e}`) for every question, in batches. These are the app's source of truth for grading; the PDF key is kept only as reference.
4. `sol2/b001.json … b041.json` — per-option explanations (`{n, x:{A:..,B:..}}`, one entry per option letter, same 41 batches as `sol/`). `build_en.py` merges them into each question's `x` field and the template renders them under the explanation. `show_batch.py N` prints batch N for writing and `check_batch.py N` verifies every option letter is covered.
5. `build_en.py` — merges `data.json` with `sol/*.json` into `data_en.json` (`a` = own answer, `e` = explanation, `pa` = PDF answer when it differs, `v` = community vote) and writes `art_en/` (`index.html` + `bank.json`, data loaded separately) and `dist_en/index.html` (data inlined by replacing the `__DATA__` placeholder in `template_en.html`).
6. `mk_en.py` — one-off script that derived `template_en.html` from the Chinese `template.html` via asserted string replacements (fails loudly if a pattern is missing/ambiguous). Edit `template_en.html` directly now; only re-run `mk_en.py` if regenerating from `template.html`.

Run from repo root: `PYTHONUTF8=1 python build_en.py` to rebuild English output (the env var avoids Windows encoding errors). `build_en.py` also patches source-data defects: Q868 option A is missing, Q237 and Q756 have merged options. The Chinese variant (`template.html` → `dist/`, `art/`) is the older version; the English UI is the current one (see latest commit).

## Template architecture

`template*.html` is a single-file vanilla-JS SPA (no framework; DOM built with a small `h()` helper). State is persisted in `localStorage` under `saa-c03-practice-en-v1` (progress `prog`, favorites `fav`, settings `set`, importable/exportable as JSON). Modes (all started via `startSession(kind,list,opts)`): sequential (`seq`), reverse order (`rev`, resume pointer `S.rn`), browse (`browse`, resume pointer `S.bn`; answers and explanations always shown, nothing graded or recorded, options not clickable), random, unseen, wrong-answer review, favorites, search/jump to question, and a timed exam with answer sheet. Pages are served from `docs/index.html` (a copy of `dist_en/index.html`, GitHub Pages from main `/docs`) — after changing the template, rebuild and `cp dist_en/index.html docs/index.html`. Questions with `a.length > 1` are multi-select. A `mismatch` flag shows when the app's answer differs from the PDF key (`pa`).

## Testing

`test.py` / `test_en.py` are Playwright smoke tests (screenshots to `s_*.png`, gitignored). They hardcode Linux paths (`/usr/bin/google-chrome`, `file:///home/claude/work/dist*/index.html`), so adjust paths before running on Windows: `python test_en.py`. `show.py N M` prints questions N–M from `data.json` (also hardcoded path).
