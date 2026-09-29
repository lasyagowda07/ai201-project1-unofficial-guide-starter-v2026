# The Unofficial Guide

Lasya Raghavendra — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a grounded question-answering system over the `campus_life` corpus —
88 short posts about student life at a university: dining hall wait times
and hours, dorm noise and laundry costs, course workload and exam structure,
and administrative rules like add/drop deadlines and the pass/fail option.
It answers specific questions such as "what is the latest I can declare a
course pass/fail" by retrieving the post(s) that actually cover it and
citing the exact source file in the answer. If a question falls outside what
the corpus covers — general trivia, a different university's rules — it
refuses outright ("I don't have enough information about that") instead of
guessing.

## Chunking Strategy

**Chunk size:** 600 characters
**Overlap:** 80 characters

campus_life is 88 short posts, each one a single self-contained thought — a
dining hall's hours, one rule about the add/drop deadline. Reading them in
Milestone 1, the longest document I found was 549 characters, and every post
I opened had a paragraph structure (a title line, then one or two paragraphs
of body). The starter's fixed 800-character window happened to be large
enough to never split any of them, but that was luck, not strategy — it
would have started slicing posts in the wrong places the moment a document
crossed 800 characters.

My `chunker.py::split_documents` replaces the character-window cut with
paragraph packing: it groups whole paragraphs into a chunk as long as they
fit under `CHUNK_SIZE`, and only falls back to splitting on sentence
boundaries for a paragraph that alone exceeds the limit — never mid-sentence.
I set `CHUNK_SIZE = 600` deliberately just above the 549-character max I
measured, so every real post in this corpus stays exactly one chunk, on
purpose, not as a side effect of an oversized default. `CHUNK_OVERLAP = 80`
only matters for the rare document that does get split (none currently do in
campus_life, but the function is generic enough to handle a longer post
without cutting a sentence in half). I didn't change my mind partway through
— the "one post, one chunk" call was made after reading the Milestone 1 docs
and confirmed by the actual length distribution before I wrote any code.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** What is the latest I can declare a course pass/fail?

**Answer:**

```
You can declare a course pass/fail as late as week eight, after you've seen your midterm.

Source: admin_pass_fail_option.txt
```

**My relevance cutoff:** 0.6 (the starter's default — I measured my own
distances rather than assuming it and it held up)

I ran all 5 `QUESTIONS` and all 5 `OUT_OF_SCOPE` questions through `retrieve`
and recorded the best (lowest) distance for each. The two groups separated
cleanly with a wide gap between them:

- In-corpus best distances: 0.255 – 0.429
- Out-of-scope best distances: 0.825 – 0.934
- Gap: roughly 0.40 wide, between 0.429 and 0.825

0.6 sits almost exactly in the middle of that gap (about 0.17 above the
worst in-corpus question, about 0.22 below the best out-of-scope one), so I
kept the default rather than moving it — there was no evidence to justify
changing it, and doing so anyway would have been picking a number instead of
reading one off the data.

| Question | In corpus? | Best distance |
|---|---|---|
| What do students say about wait times at Kestrel Commons during lunch? | Yes | 0.259 |
| Are the midterms curved in CS 210? | Yes | 0.429 |
| Why does Old Brewhouse have a reputation for being noisy? | Yes | 0.308 |
| What is the latest I can declare a course pass/fail? | Yes | 0.255 |
| Does unused printing quota roll over to the next semester? | Yes | 0.369 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

## How I Used AI

**1.** For Milestone 3, I asked Claude to design and implement the chunking
strategy after I'd read the campus_life documents in Milestone 1. Rather
than just picking a chunk size, it first measured the actual length
distribution across all 88 documents in the corpus and found the longest
post was 549 characters — well under the starter's 800-character default.
That changed the decision: instead of reusing 800 (which would have made
"one post, one chunk" an accident of an oversized number, the same trap the
starter's own fallback chunker fell into), it set `CHUNK_SIZE = 600`,
deliberately just above the measured max, so every real post staying whole
is a consequence of the number, not a coincidence.

**2.** When writing criteria 4 and 5 in Milestone 2, I asked Claude to base
them on something actually observed in the corpus rather than a generic
template. It read through the `campus_life` filenames and a few documents
and pointed out that several groups are near-duplicate and templated — six
dining hall posts and six housing noise pages all share very similar
wording ("wait times", "sound carries because of..."). That's a real
retrieval-confusion risk specific to this corpus (the system could cite the
wrong dining hall and still sound plausible), so criterion 5 ended up
testing top-1 source attribution precision instead of a generic "chunks are
relevant" claim — a more specific and more useful target than what I'd have
written on my own.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Produced by `python run_eval.py --label before` on 2026-09-28, raw output in
[`results/run_2026-09-28_2120_before.md`](results/run_2026-09-28_2120_before.md).
`scorer.py::judge` (built this unit) marks each run's answer pass/fail by
checking whether the `expects` phrase from `questions.py` is present in the
generated answer, case-insensitively.

Criteria 3, 4 and 5 don't vary between runs: criterion 3 is one deterministic
pass through the gate (`run_eval.py::check_out_of_scope`), and criteria 4 and
5 depend only on retrieval, which is deterministic for a fixed corpus and
question — running the same question three times returns the same chunks in
the same order every time, so there's one number for each, not three.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk-to-document ratio | 95% 1:1 | 100% | 100% | 100% | MET |
| 5. Top-1 source-attribution precision | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Real output, one per criterion:**

**Criterion 1** — `store.py::search`, question "Does unused printing quota
roll over to the next semester?", top-ranked chunk:

```
[from admin_printing_quota.txt]
On the printing quota

Every student gets $30 of printing per semester, which is roughly 600
black-and-white pages. It does not roll over. Colour costs eight times as
much per page, which people discover after printing one poster.
```

The `expects` phrase ("does not roll over") is right there in the top chunk.
All 5 questions retrieved a chunk containing their `expects` phrase, on all
3 runs — retrieval doesn't change between runs, only generation does.

**Criterion 2** — `generate.py::answer_from_chunks`, question "What is the
latest I can declare a course pass/fail?", run 1:

```
You can declare a course pass/fail as late as week eight, after you've seen
your midterm.

Source: admin_pass_fail_option.txt
```

Every one of the 15 answers (5 questions × 3 runs) named at least one source
filename. `GROUNDING_INSTRUCTION` in `generate.py` requires it, and nothing
in this run broke that.

**Criterion 3** — `gate.py::check` via `run_eval.py::check_out_of_scope`,
full table from the run log:

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |
```

All 5 refused, all comfortably above the 0.6 cutoff (lowest was 0.825).

**Criterion 4** — `chunker.py::split_documents`, computed directly rather
than eyeballed:

```
>>> from ingest import load_documents
>>> from chunker import split_documents
>>> docs = load_documents(); chunks = split_documents(docs)
>>> len(docs), len(chunks)
(88, 88)
>>> pct 1:1: 100.0 %
```

No document produced more than one chunk — same result as Unit 1, confirmed
again rather than assumed, since criterion 4 specifically asks about the
chunker's current behavior, not last unit's number.

**Criterion 5** — `app.py retrieve`, question "Are the midterms curved in
CS 210?" (chosen because `course_cs_210.txt` / `course_cs_210_exams.txt` /
`course_cs_210_workload.txt` is exactly the kind of near-duplicate triple
criterion 5 was written to catch):

```
#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4287     course_cs_210_exams.txt          CS 210 Data Structures — assessment  Two midterms an...
2   0.5821     course_phys_130_exams.txt        PHYS 130 Mechanics — assessment  Three midterms, no ...
3   0.5941     course_math_220_exams.txt        MATH 220 Linear Algebra — assessment  Two midterms a...
```

Top-1 is `course_cs_210_exams.txt`, which contains "Midterms are curved" —
the correct document, not a same-shaped wrong one. Checked all 5 questions
this way (not just read off the alphabetically-sorted "sources retrieved"
line in the run log, which doesn't reflect rank order): every top-1 chunk's
source file literally contains its question's `expects` phrase.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (4 of 5) | MET | All 3 runs came back 5/5, not just once. I read the actual retrieved chunk text for each question (not just the source filename) and confirmed the `expects` phrase is present verbatim in at least one retrieved chunk every time. |
| 2 | Every answer names a source (5 of 5) | MET | All 15 answers (5 questions × 3 runs) include a `Source:` line with a real filename from the corpus. No exceptions to check for a close call here. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5 of 5 refused, and by a wide margin — the closest out-of-scope distance (0.825) is still 0.225 above the 0.6 cutoff, so this isn't a near miss that got lucky once. |
| 4 | Chunk-to-document ratio (≥95% 1:1) | MET | Computed directly (88 docs → 88 chunks, 0 documents split), not eyeballed from the Unit 1 number. Comfortably over the 95% floor. |
| 5 | Top-1 source-attribution precision (4 of 5) | MET | Checked the true distance-ordered top-1 result for all 5 questions with `app.py retrieve` (the run log's "sources retrieved" line is alphabetically sorted, not rank-ordered, so I didn't trust that alone). Every top-1 document literally contains its question's `expects` phrase, including on the CS 210 and Old Brewhouse questions where a same-shaped wrong document was sitting right there in the top-5. |

**All five criteria MET, on every run.** Per the assignment's own warning,
that's a reason to look at whether the targets were set too soft, not a
reason to feel good — see **What I'd Do Differently** for which one I'd
tighten and why.

## Diagnoses

**Nothing was missed.** All five criteria came back MET on all three runs,
with comfortable margins everywhere except criterion 2 (which had no margin
to begin with — 5 of 5 was always all-or-nothing).

That's a result worth being suspicious of, not proud of, per the
assignment's own warning. Looking at *why* it's this clean:

Criteria 1, 3, and 5 were all set at "4 of 5" specifically because
`criteria.md`'s own reasoning names a real risk in this corpus — templated
near-duplicate documents (`dining_*.txt` pairs, `housing_*_noise.txt` pages,
`course_cs_210.txt`/`_exams`/`_workload` triples) that could plausibly
outrank the correct document on a question that doesn't distinguish them.
But every one of the 5 `QUESTIONS` I wrote in Unit 1 names a specific,
distinctive proper noun or course code — "Kestrel Commons," "CS 210," "Old
Brewhouse" — and MiniLM's embeddings separate those names cleanly. The
distance gap between the correct document and its nearest same-shaped
competitor was never smaller than ~0.12 (Old Brewhouse's own two docs, at
0.308 vs 0.327) and was usually much larger (CS 210: 0.429 vs 0.582). **The
near-duplicate risk the criteria were designed to catch never actually got
tested**, because none of my questions were phrased ambiguously enough to
put two near-duplicate documents in real competition for the top spot.

This is a diagnosis of the *test*, not the *pipeline*: nothing in loading,
chunking, embedding, retrieval, or generation is doing anything wrong on
these 5 questions — retrieval is confidently and correctly separating even
same-topic documents by a wide margin every time. The gap is that the test
suite doesn't contain a question shaped like the failure mode the criteria
were written to catch. See **What I'd Do Differently** for which criterion
I'd tighten (and how) to actually exercise that risk next time, since I
can't rewrite `questions.py` mid-unit to add one now — the one-change rule
this unit is spent on the retrieval improvement below, not the test
questions.

## The Improvement

**What I changed:** `store.py::search` now ranks retrieval results with
hybrid search instead of pure semantic search. Every chunk in the collection
is scored two ways against the question — cosine similarity from the
embedding model, and BM25 keyword overlap (`rank_bm25.BM25Okapi`, already in
`requirements.txt`) — each min-max normalized to `[0, 1]`, then blended as
`config.HYBRID_ALPHA * semantic + (1 - config.HYBRID_ALPHA) * bm25` with
`HYBRID_ALPHA = 0.5`. The `distance` field on each `Result` is still the
untouched cosine distance — `gate.py`'s 0.6 cutoff was calibrated against
cosine distance specifically, and the gate only reads the global best
distance, which doesn't change with re-ranking. Only ranking/selection order
changed.

**Why I picked it:** My diagnosis found no misses, but traced *why* — every
one of my 5 test questions names a distinctive proper noun, so none of them
actually stress the templated near-duplicate risk (`dining_*.txt`,
`housing_*_noise.txt`, `course_*` triples) that criteria 1/3/5 were written
to catch. Hybrid search directly targets that risk: it's supposed to help
exactly when a question turns on an exact term (a number, a name) that these
near-identical documents differ on, which semantic-only search can glide
past.

### Run Log — After

Produced by `python run_eval.py --label after`, raw output in
[`results/run_2026-09-28_2127_after.md`](results/run_2026-09-28_2127_after.md).
Same 5 `QUESTIONS`, same 5 `OUT_OF_SCOPE`, same scorer, same format as before.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk-to-document ratio | 95% 1:1 | 100% | 100% | 100% | MET |
| 5. Top-1 source-attribution precision | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Identical to the before table, question for question. Top-1 for all 5
questions is still the correct document (verified again with
`app.py retrieve`, same method as Milestone 1), and the out-of-scope gate
still refuses 5 of 5 at the same distances (0.825–0.934, ±0.026 from a
different re-ranking of ties beyond the gate's threshold — the gate itself
is unaffected, as designed).

**Did it help?**

**On the 5 graded questions: no measurable difference**, and I predicted
that honestly before running it, because none of them stress the risk
hybrid search targets — the diagnosis said so before I made the change.
That's not nothing, but it's also not evidence the change works.

**So I built a stress-test probe question to actually check**, using a
pattern criteria.md itself calls out — dining hall posts that share almost
every sentence except one dollar figure:

```
Which dining hall charges $13.00 cash for a meal without a swipe?
```

`dining_north_kitchen.txt` is the only document containing "$13.00 cash."
Comparing the two ranking methods on the exact same retrieved candidates:

```
PURE SEMANTIC top 3 (this unit's "before" logic):
0.5083  admin_dining_dollars.txt        <- WRONG. Topically about "dining
                                            dollars" (a meal-plan balance
                                            system), not about a specific
                                            hall's cash price. No $13.00
                                            anywhere in it.
0.5132  dining_north_kitchen.txt        <- correct document, ranked 2nd
0.5612  dining_halden_hall.txt

HYBRID top 3 (this unit's improvement):
0.9959  dining_north_kitchen.txt        <- correct document, now top-1
0.8764  dining_halden_hall.txt
0.8730  dining_pellew_dining_hall.txt
```

Pure semantic search put the wrong document at top-1 on this probe —
`admin_dining_dollars.txt` talks about balances and semesters, not a
specific hall's price, but embeds close enough to "dining hall charges cash"
to win anyway. That's a real, concrete instance of the exact failure mode
criteria 1 and 5 were written to catch; my 5 official test questions just
never happened to trigger it. Hybrid search fixed it on this probe by
weighting the literal "$13.00" keyword match, which pure semantic similarity
had no way to reward.

**Honest bottom line:** the improvement did not move any of my 5 graded
criteria (they were already at ceiling), but it measurably fixed a top-1
ranking error on a constructed question that exercises the corpus's actual
known risk. Whether that's worth shipping depends on whether future
questions look more like my 5 (named entities, hybrid search irrelevant) or
more like the probe (exact terms, hybrid search load-bearing) — see **What's
Still Broken** and **What I'd Do Differently** below.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
