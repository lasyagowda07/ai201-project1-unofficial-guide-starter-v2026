# Context for the next Claude session — AI201 Unit 2

Written 2026-09-25, at the end of Unit 1, for whoever (which is probably a
fresh Claude Code session with zero memory of this one) picks this repo back
up for Unit 2. Read this before doing anything else. Not a graded file —
purely a handoff doc, like `PLANNER.md`.

## Who's working on this

Lasya Raghavendra (GitHub: `lasyagowda07`, email: `lasya.gowda07@gmail.com`).
Git commit identity is already set globally on this machine to
`Lasya Raghavendra <lasya.gowda07@gmail.com>` — no need to redo that.

## Repo / remote

- Local path: `/Users/lucky/Documents/project/codepath-ai/ai201-project1-unofficial-guide-starter-v2026`
- `origin` → `https://github.com/lasyagowda07/ai201-project1-unofficial-guide-starter-v2026.git` (her personal fork, forked from the CodePath class starter repo)
- `gh` CLI is authenticated as `lasyagowda07` (fixed a stale-login issue early in Unit 1 where it was pointing at an old account, `lasyaraghavendra` — if push/auth ever breaks again, check `gh auth status` first)
- Branch: `main`. No other branches in use.
- **Unit 1 was submitted**: the fork URL above was given to the user to submit through the Course Portal at the end of Unit 1. If you need to confirm it was actually submitted, ask — this session doesn't have visibility into the Course Portal itself.
- `.github/MAINTAINERS.md` warns this repo's commit hashes are pinned in a grading baseline — don't rewrite history (no rebase/amend/force-push) on commits that predate your session unless explicitly asked.

## Environment (already set up, should still work)

- System Python is 3.14.5, but the course's `test.py` requires **3.11–3.13**. A venv was created with Homebrew's `python@3.11`:
  ```
  /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv
  ```
- `.venv/` exists at repo root (Python 3.11.15), gitignored. Activate with `source .venv/bin/activate` before running any `python app.py ...` command.
- `.env` exists (gitignored) with a working `GEMINI_API_KEY`. Verified via `python test.py` → **10/10 checks passed**, including a live call to `gemini-3.5-flash-lite`.
- All packages from `requirements.txt` are installed in `.venv`.
- If you're in a brand new environment (different machine, fresh clone) and none of the above exists, this is exactly what Unit 1's setup did — repeat it: create the venv with a 3.11–3.13 interpreter, `pip install -r requirements.txt`, `cp .env.example .env` and get a fresh key from aistudio.google.com (the old key may or may not still be valid — ask the user), then `python test.py` to confirm.

## What this project is

A grounded RAG pipeline: `ingest.py` (load/clean corpus) → `chunker.py`
(split into chunks) → `store.py` (Chroma + MiniLM embeddings, cosine
distance) → `gate.py` (relevance cutoff before ever calling the model) →
`generate.py` (Gemini call, grounded/cited answer). CLI is `app.py`
(`corpora`, `index`, `chunks`, `retrieve`, `ask`). `serve.py` wraps it as a
Flask HTTP service. Full command reference is in `RUNNING.md` (staff-owned,
don't edit it).

## Decisions made in Unit 1 (all deliberate, all with evidence — don't second-guess these without a reason)

### Corpus: `campus_life`
88 short posts about student life (dining, housing, courses, admin rules).
Average 317 characters/doc, **max 549 characters** (measured directly, not
guessed). Chosen over `advice_threads` (23 messy multi-reply threads) and
`city_guides` (14 long sectioned guides) — user picked it after reviewing
all three options via `corpora/README.md`. Set via `config.py`'s default
(`CORPUS = "campus_life"`), not overridden in `.env`.

### Chunking: `chunker.py::split_documents`
Replaced the starter's fixed 800-char/120-overlap `fallback_split` (still
present, kept as-is, used as a comparison baseline) with a **paragraph-
packing chunker**: groups whole paragraphs up to `CHUNK_SIZE`, falls back to
sentence-boundary splitting only for a paragraph that alone exceeds the
limit. Never cuts mid-sentence.

- `config.CHUNK_SIZE = 600` — set deliberately just above the measured
  549-char max, so every real campus_life post stays exactly one chunk **on
  purpose**, not as an accident of an oversized default (which is what
  happened with the starter's 800).
- `config.CHUNK_OVERLAP = 80` — only matters for a document that actually
  gets split; none currently do in this corpus.
- Result: 88 documents → 88 chunks (1:1), same headline number as the
  starter's fallback, but now a deliberate outcome instead of a coincidence.
- Helper functions: `_split_into_sentences`, `_pack_sentences`,
  `_pack_paragraphs`, `_apply_overlap` — all private, all in `chunker.py`.

### Relevance threshold: `config.THRESHOLD = 0.6` (unchanged from starter default, but now *confirmed* not assumed)
Measured best-match distance for all 5 `QUESTIONS` and all 5 `OUT_OF_SCOPE`
questions:
- In-corpus best distances: **0.255 – 0.429**
- Out-of-scope best distances: **0.825 – 0.934**
- Gap: ~0.40 wide, between 0.429 and 0.825. 0.6 sits almost exactly centered
  in it. No evidence justified moving it, so it was kept.
- Full 10-row table is in `README.md` under **Sample Answer**.

### `TOP_K = 5` — unchanged, no evidence it needed adjusting.

### Test questions (`questions.py::QUESTIONS`)
| Question | expects |
|---|---|
| What do students say about wait times at Kestrel Commons during lunch? | "20 to 25 minutes" |
| Are the midterms curved in CS 210? | "curved" |
| Why does Old Brewhouse have a reputation for being noisy? | "brick" |
| What is the latest I can declare a course pass/fail? | "week eight" |
| Does unused printing quota roll over to the next semester? | "does not roll over" |

`OUT_OF_SCOPE` (staff-provided, unchanged, 5 questions): capital of
Mongolia, diesel oil change, 1994 World Cup winner, ibuprofen dosage, Rust
for-loop syntax.

### Acceptance criteria (`criteria.md`) — all 5 written, all with reasons
1. **Retrieved chunks contain the answer** (4 of 5, staff-given target).
   Reason: campus_life has near-duplicate templated document groups — six
   `dining_*.txt` posts and six `housing_*_noise.txt` posts share very
   similar wording — so a wrong-but-similar doc could plausibly outrank the
   right one on a templated question.
2. **Every answer names a source** (5 of 5, staff-given). Reason:
   `GROUNDING_INSTRUCTION` hard-requires citing the filename, and gate
   refusals don't count against this criterion.
3. **Relevance gate stops out-of-corpus questions** (4 of 5, staff-given).
   Reason: `OUT_OF_SCOPE` questions share no vocabulary with campus_life, so
   most should land well above the cutoff, but this was written before
   Milestone 4's actual measurement, so it left room for one surprise.
4. **(written by us) Chunk-to-document ratio**: at least 95% of chunks equal
   exactly one whole source document. Grounded directly in the 88→88 index
   output.
5. **(written by us) Top-1 source-attribution precision**: for 4 of 5 test
   questions, the top-ranked retrieved chunk's source file is the actual
   document containing the `expects` phrase — not just any doc in the
   top-k. This is *stricter* than criterion 1 and exists specifically
   because of the templated-near-duplicate risk named in criterion 1's
   reasoning (dining halls, housing noise pages, and the
   `course_cs_210.txt` / `course_cs_210_exams.txt` /
   `course_cs_210_workload.txt` triples).

**Live-verified in Unit 1** (spot checks, not the full `run_eval.py` pass):
top-1 retrieval was correct for all 3 spot-checked questions; the out-of-
scope gate refused "What is the capital of Mongolia?" with **0 model calls**;
`--show-prompt` on the pass/fail question showed the model correctly
ignoring an irrelevant padding chunk (`course_biol_160.txt` was in the
top-5 but unrelated) and citing only the correct source.

### README.md — all 5 Unit 1 sections filled in
What This Does, Chunking Strategy, Sample Chunks (5, labeled, sourced,
function-attributed), Sample Answer (pass/fail question, full 10-row
distance table), How I Used AI (two real moments: the chunk-size decision
driven by measuring actual doc lengths, and criteria 4/5 grounded in
spotting the templated-duplicate risk). Unit 2's sections in the same file
(Run Log — Before, Verdicts, Diagnoses, The Improvement, Run Log — After,
What's Still Broken, What I'd Do Differently) are **still the unfilled
staff template** — that's Unit 2's job, not left over from Unit 1.

## What's NOT done yet (real gaps, not oversights)

- **`scorer.py` does not exist.** `run_eval.py::load_scorer()` looks for it
  and currently falls back to leaving verdicts blank. The assignment says
  this gets built "in class" — almost certainly a Unit 2 task. Check the
  actual Unit 2 instructions before assuming its shape; we don't have them
  in this session yet.
- **No eval run has ever been executed.** `results/` is empty except
  `.gitkeep`. `run_eval.py --label before` (or similar) has never been run.
  This is very likely Unit 2's first move — it's what fills in the "Run Log
  — Before" table in the README, which is graded on criterion-by-criterion
  verdicts (MET/MISSED against the Unit 1 targets, not new ones).
- **No stretch features attempted**: metadata filtering, conversational
  memory, second embedding model — all untouched. Not required.
- **We don't have the actual Unit 2 assignment text in this session.** Unit
  1's milestone instructions were pasted in by the user at the start; Unit
  2's weren't. **Ask the user to paste Unit 2's instructions** (or find them
  in the course portal / `RUNNING.md`'s "unit 9" references / wherever the
  course publishes them) before planning Unit 2 work — don't guess the
  milestone structure from the README's Unit 2 section headers alone,
  though those headers (Run Log Before/After, Verdicts, Diagnoses, The
  Improvement, What's Still Broken, What I'd Do Differently) are a strong
  hint at the shape.

## Known corpus quirks worth remembering (found by reading documents directly, not by running the pipeline)

- **Templated near-duplicates are a real retrieval risk in this corpus**:
  six `dining_*.txt` / `dining_*_followup.txt` pairs, six
  `housing_*_noise.txt` pages, and `course_<code>.txt` /
  `course_<code>_exams.txt` / `course_<code>_workload.txt` triples all share
  near-identical sentence templates. If Unit 2's diagnosis work turns up a
  wrong-source citation, check here first — this was flagged as the likely
  failure mode before any eval was even run.
- All 88 campus_life docs have paragraph breaks (confirmed via `'\n\n' in
  d.text` check on every doc) and none exceed 549 characters — if you're
  re-deriving the chunk-size reasoning, these are the two load-bearing facts.

## Workflow notes for whoever picks this up

- The user wants **periodic pushes**, not asked each time — established
  standing authorization in Unit 1. Keep committing per-milestone (one
  commit per logical milestone worked, not one giant commit) and push after
  each, the way Unit 1 did (`git log --oneline` shows the pattern: 5
  distinct milestone commits, each pushed immediately after).
- `PLANNER.md` (Unit 1's checklist, now fully checked off) is the template
  for how to track this kind of milestone work — consider making an
  equivalent Unit-2-specific checklist once the real Unit 2 instructions are
  in hand, the same way this session built `PLANNER.md` from the pasted
  Unit 1 brief.
- Don't touch `RUNNING.md` (explicitly staff-owned, README says "leave that
  file alone") or `.github/MAINTAINERS.md`.
- Don't edit or delete criteria/README content already written for Unit 1 —
  Unit 2's revision protocol (explained in `criteria.md`'s own trailing
  comment block) requires *adding* revisions underneath original criteria
  text if a criterion turns out to be unmeasurable, never editing or
  deleting the original line. Same spirit applies to the README's Unit 1
  sections — Unit 2 sections get added below, not mixed in.
