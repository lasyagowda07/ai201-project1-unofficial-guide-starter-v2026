# Project planner — AI201 Unit 1 (RAG pipeline)

Working checklist, not a graded deliverable. Grounded in an audit of this repo
on 2026-09-25. Update the checkboxes as we go.

## Status snapshot

This is a **pristine, unstarted starter checkout**. All 6 existing commits are
staff scaffolding (no student work yet). The pipeline code (`app.py`,
`ingest.py`, `store.py`, `gate.py`, `generate.py`) is fully built and
functional as shipped — nothing here is broken. What's still starter-default
or empty:

- `chunker.py::split_documents` — plain 800-char/120-overlap fallback, not yet customized (Milestone 3's job)
- `config.py::THRESHOLD` — default `0.6`, not yet calibrated (Milestone 4's job)
- `questions.py::QUESTIONS` — all 5 entries blank (`OUT_OF_SCOPE` is already filled in)
- `criteria.md` — criteria 1–3 have target numbers but zero "Why this target" reasons written; criteria 4–5 are entirely blank
- `README.md` — all 5 required section headers exist but are all placeholder text
- No index has ever been built, no `.env`/API key configured, no venv created

## Environment setup (blocking — do first)

- [x] Install a Python **3.11–3.13** interpreter — system default is 3.14.5, which `test.py` will reject (used Homebrew's `python@3.11`)
- [x] Create a virtualenv with that interpreter (`.venv`, Python 3.11.15)
- [x] `pip install -r requirements.txt`
- [x] `cp .env.example .env`
- [x] Get a free key at https://aistudio.google.com, paste into `.env` as `GEMINI_API_KEY`
- [x] Run `python test.py` — confirm all checks pass — **10/10 passed**, live Gemini call succeeded

## Milestone 1 — Pick corpus & run the starter (~25 min)

- [x] Read 3–4 documents from each candidate corpus in `corpora/*/documents/` (`campus_life` — 88 short posts; `advice_threads` — 23 messy multi-reply threads; `city_guides` — 14 long sectioned guides)
- [x] Pick one corpus: **campus_life** (already the `config.py` default — no change needed)
- [x] `python app.py index` — 88 documents → 88 chunks (800-char fallback chunker never splits these, since docs average 317 chars)
- [x] `python app.py ask "is the housing lottery random?"` — ran end to end: best distance 0.254 (well under 0.6 cutoff), grounded answer, cited `admin_housing_lottery.txt`
- [x] `python app.py --corpus campus_life chunks -n 1` — **88 chunks total** (write this number down for the end-of-session activity)
- [ ] Commit **(1 of 4 required)**

## Milestone 2 — Acceptance criteria (~75 min)

- [x] Write 5 specific test questions with right answers into `questions.py::QUESTIONS`, each with an `expects` phrase (wait times, CS 210 curving, Old Brewhouse noise, pass/fail deadline, printing rollover)
- [x] In `criteria.md`, write the "Why this target" reason under criteria 1, 2, and 3
- [x] Write criterion 4 (chunk-to-document ratio, grounded in the 88 docs -> 88 chunks index output)
- [x] Write criterion 5 (top-1 source-attribution precision — targets the templated near-duplicate docs risk)
- [x] Self-check: each criterion names a testable procedure from the sentence alone
- [ ] Commit **(2 of 4 required)** — `questions.py` and `criteria.md`

## Milestone 3 — Swap in your own chunker (~60 min)

- [ ] Read the `python app.py index` summary line (chunk count, avg/min/max length) for the chosen corpus and think about what it implies
- [ ] Decide chunk size + overlap for this corpus's shape, and write down *why* before coding
- [ ] Implement the new strategy in `chunker.py::split_documents` (not `fallback_split` — that stays as the fallback); update `produced_by` to reflect the new function name
- [ ] `python app.py chunks -n 5` — read the 5 sampled chunks, check each reads as a complete thought
- [ ] Paste those 5 chunks into README's **Sample Chunks** section, each labeled with source file + producing function
- [ ] Re-run `python app.py index` with the new chunker
- [ ] Commit **(3 of 4 required)**

## Milestone 4 — Tune retrieval & ground the answers (~85 min)

- [ ] `python app.py retrieve "<question>"` on 3 of the 5 test questions — read the returned chunks + distances for relevance
- [ ] Adjust `config.TOP_K` (starter default 5) if needed
- [ ] Run all 5 `QUESTIONS` and all 5 `OUT_OF_SCOPE` questions through `retrieve`, record the best distance for each
- [ ] Find the gap between the two groups; set `config.THRESHOLD` inside it (starter default 0.6, typical range 0.45–0.75)
- [ ] Review `GROUNDING_INSTRUCTION` in `generate.py` — use `python app.py ask "..." --show-prompt` to see the assembled prompt; tighten wording if answers drift from sources
- [ ] Paste one full question + grounded answer (with source line) into README's **Sample Answer** section, plus the chosen cutoff and a description of the two distance groups
- [ ] Commit **(4 of 4 required — minimum met)**

## Milestone 5 — Write it up & submit (~45 min)

- [ ] Fill README's **What This Does** section (corpus + kinds of questions answered)
- [ ] Fill README's **How I Used AI** section — two specific moments (what was asked, what came back, what was changed)
- [ ] Verify: `criteria.md` present with all 5 criteria + reasons; README has all 5 sections filled; ≥4 new commits exist
- [ ] Push to the `lasyagowda07` fork
- [ ] Submit the fork's URL through the Course Portal (write it down — Unit 2 reuses the same repo)

## Optional stretch features (not started)

- [ ] Metadata filtering (filter results by source/date)
- [ ] Conversational memory (follow-up questions build on prior ones)
- [ ] Second embedding model swap (needs `pip install 'sentence-transformers>=3.4,<3.5'` — large, install ahead of time; expect the relevance cutoff to shift)
