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
- [x] Commit **(1 of 4 required)**

## Milestone 2 — Acceptance criteria (~75 min)

- [x] Write 5 specific test questions with right answers into `questions.py::QUESTIONS`, each with an `expects` phrase (wait times, CS 210 curving, Old Brewhouse noise, pass/fail deadline, printing rollover)
- [x] In `criteria.md`, write the "Why this target" reason under criteria 1, 2, and 3
- [x] Write criterion 4 (chunk-to-document ratio, grounded in the 88 docs -> 88 chunks index output)
- [x] Write criterion 5 (top-1 source-attribution precision — targets the templated near-duplicate docs risk)
- [x] Self-check: each criterion names a testable procedure from the sentence alone
- [x] Commit **(2 of 4 required)** — `questions.py` and `criteria.md`

## Milestone 3 — Swap in your own chunker (~60 min)

- [x] Read the `python app.py index` summary line (chunk count, avg/min/max length) for the chosen corpus and think about what it implies (88 -> 88 chunks; measured actual max doc length: 549 chars)
- [x] Decide chunk size + overlap for this corpus's shape, and write down *why* before coding (600 / 80, just above the measured max)
- [x] Implement the new strategy in `chunker.py::split_documents` — paragraph packing with sentence-boundary fallback for oversized paragraphs (not `fallback_split` — that stays as the fallback); `produced_by` now reads `chunker.py::split_documents`
- [x] `python app.py chunks -n 5` — read the 5 sampled chunks, all read as complete thoughts
- [x] Paste those 5 chunks into README's **Sample Chunks** section, each labeled with source file + producing function
- [x] Re-run `python app.py index` with the new chunker
- [ ] Commit **(3 of 4 required)**

## Milestone 4 — Tune retrieval & ground the answers (~85 min)

- [x] `python app.py retrieve "<question>"` on 3 of the 5 test questions — top-1 was the correct source in all 3, distances well under 0.6
- [x] Adjust `config.TOP_K` (starter default 5) — kept at 5, no evidence it needed changing
- [x] Run all 5 `QUESTIONS` and all 5 `OUT_OF_SCOPE` questions through `retrieve`, record the best distance for each — in-corpus 0.255-0.429, out-of-scope 0.825-0.934, wide clean gap
- [x] Find the gap between the two groups; set `config.THRESHOLD` inside it — kept 0.6 (already centered in the measured gap, confirmed rather than assumed)
- [x] Review `GROUNDING_INSTRUCTION` in `generate.py` — checked via `--show-prompt`; model correctly ignored an irrelevant padding chunk and cited only the right source, no tightening needed
- [x] Paste one full question + grounded answer (with source line) into README's **Sample Answer** section, plus the chosen cutoff, the full 10-row distance table, and description of the two groups
- [x] Sanity-checked live: out-of-scope question refused with 0 model calls
- [x] Commit **(4 of 4 required — minimum met)**

## Milestone 5 — Write it up & submit (~45 min)

- [x] Fill README's **What This Does** section (corpus + kinds of questions answered)
- [x] Fill README's **How I Used AI** section — two specific moments (chunk-size decision driven by measuring real doc lengths; criteria 4/5 grounded in spotting templated near-duplicate docs)
- [x] Verify: `criteria.md` present with all 5 criteria + reasons; README has all 5 Unit 1 sections filled, no leftover placeholders; 4 new commits exist beyond the staff baseline
- [ ] Push to the `lasyagowda07` fork (commit 5, this write-up pass)
- [ ] Submit the fork's URL through the Course Portal (write it down — Unit 2 reuses the same repo) — **user action, not automatable**

## Optional stretch features (not started)

- [ ] Metadata filtering (filter results by source/date)
- [ ] Conversational memory (follow-up questions build on prior ones)
- [ ] Second embedding model swap (needs `pip install 'sentence-transformers>=3.4,<3.5'` — large, install ahead of time; expect the relevance cutoff to shift)

---

# Unit 2 — Testing (added 2026-09-28)

Grounded in the assignment PDF (`Show (Project): Unit 2`) plus an audit of
where Unit 1 left off (see `context.md`). Same repo, same fork, same URL —
no new corpus, no new features beyond the one allowed improvement.

**Deadline printed in the assignment:** Monday, September 28th, 2:59AM EDT.
Today's session date is 2026-09-28 — worth confirming with the user whether
that deadline already passed / was extended before treating it as still open.

**Grading logic (from the PDF):** missing a criterion costs nothing; the
grade comes from (1) whether the system was actually run enough times, (2)
whether verdicts were applied honestly against the Unit 1 targets, (3)
whether the improvement made sense and its effect was measured. Passing
everything on the first try is a yellow flag, not a green one — it usually
means the targets were set too soft.

**One hard rule:** the only system change allowed this unit is the single
Milestone 4 improvement. Everything else (corpus, chunker, gate, prompt)
stays exactly as Unit 1 left it until then.

## Milestone 1 — Run the test (~40 min)

- [ ] Build `scorer.py` with `judge(question, expects, answer, results) -> bool`
      — `run_eval.py::load_scorer()` already looks for this and falls back to
      unscored if it's missing. Simplest honest version: case-insensitive
      substring check of `expects` against the generated `answer`, which is
      exactly what `questions.py`'s docstring says `expects` is for.
- [ ] `python run_eval.py --label before` — runs all 5 `QUESTIONS` three times
      each (cache off) and all 5 `OUT_OF_SCOPE` once through the gate; writes
      a per-question table + full transcript into `results/`.
- [ ] Commit the generated `results/run_..._before.md` file — it's the
      evidence the run happened.
- [ ] Turn the per-question table into the README's per-criterion table
      (Run Log — Before): criterion 1 = how many of the 5 questions had the
      answer inside the retrieved chunks (read `results:` in the transcript,
      not just the pass/fail column — criterion 1 is about chunks, the
      scorer judges the final answer, they're related but not identical).
      Criterion 4 (chunk:doc ratio) and criterion 5 (top-1 source precision)
      need to be computed by hand from the same transcript, same as Unit 1.
- [ ] Paste real output (not a description) under the table, naming the file
      + function that produced it.
- [ ] Commit **(1 of 4 required this unit)**.

## Milestone 2 — Call each criterion (~45 min)

- [ ] MET or MISSED per criterion, against the Unit 1 target in `criteria.md`
      (not a new target). One sentence per criterion on how the call was made.
- [ ] If a criterion turns out to be unmeasurable (not just missed), revise it
      per `criteria.md`'s own trailing comment block — add the revision
      underneath the original, never edit/delete the original line.
- [ ] Commit **(2 of 4 required)**.

## Milestone 3 — Diagnose every miss (~45 min)

- [ ] For each MISSED criterion, name the pipeline stage (loading / chunking
      / embedding / retrieval / generation) and the mechanism — not "it got
      it wrong." Use the two-minute check from the PDF: if the answer isn't
      in any retrieved chunk, the problem is pre-generation; if it's in a
      chunk and still came out wrong, it's generation.
- [ ] Look for one shared pattern across misses before writing individual
      diagnoses. `campus_life`'s known risk (flagged back in Unit 1): the
      templated near-duplicate groups — `dining_*.txt` (6), `housing_*_noise.txt`
      (6), `course_<code>.txt` / `_exams` / `_workload` triples — check here
      first if a wrong-source citation shows up.
- [ ] If nothing was missed, say so, and name which criterion was probably
      set too soft and what you'd tighten it to.
- [ ] Commit **(3 of 4 required)**.

## Milestone 4 — Fix one thing and measure it (~90 min)

- [ ] Pick the ONE improvement the diagnosis actually points at. Likely
      candidates given this corpus:
      - **Hybrid search (BM25 + embeddings)** — `rank-bm25` is already in
        `requirements.txt`, no install needed. Most likely fix if misses trace
        to templated near-duplicates beating the right doc on generic wording
        but losing on exact terms (room numbers, dollar amounts, course codes).
      - **Second chunking variant** — `store.build_index`/`search` already
        support `variant=` so a second index can be built and compared without
        touching the Unit 1 index. Candidate if misses trace to a chunking
        boundary problem.
      - Something narrower the diagnosis points at instead: `TOP_K`, the
        gate `THRESHOLD`, or `GROUNDING_INSTRUCTION` in `generate.py`.
- [ ] Implement only that one change.
- [ ] `python run_eval.py --label after` — same 5 questions, same 5
      out-of-scope, three runs.
- [ ] Put both run logs (before/after) in the README side by side under
      **The Improvement**, and say plainly whether it helped — a backfire,
      honestly reported, is a complete answer.
- [ ] Commit **(4 of 4 required — minimum met)**.

## Milestone 5 — Say what's still broken, and submit (~45 min)

- [ ] Write **What's Still Broken**: for each still-missed criterion, what
      you'd do next and why you stopped here. "Ran out of time" is fine if
      true; pretending nothing's left is not.
- [ ] Write **What I'd Do Differently**: which of the 5 criteria you'd write
      differently next time, and why.
- [ ] Update **How I Used AI** with anything new from this unit (e.g. using a
      model to propose failure hypotheses before checking which was real).
      **Hold this section for the user's review before committing/pushing it**
      — standing instruction, don't push it unreviewed.
- [ ] Verify: `criteria.md` unchanged except additive revisions; all 6 new
      README sections filled; ≥4 new commits this unit; `results/` has the
      before/after run-log files committed.
- [ ] Push (no Claude co-authorship in the commit messages — standing
      instruction). Submit the same repo URL as Unit 1 (user action).
