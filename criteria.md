# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** I picked 4 of 5 rather than 5 of 5 because several
campus_life documents follow a near-identical template — the six dining hall
posts (`dining_*.txt`) and the six housing noise pages (`housing_*_noise.txt`)
share very similar wording ("wait times", "hours are", "sound carries
because of..."), so embedding search could plausibly pull a same-shaped but
wrong document ahead of the right one for a templated question. 3 of 5 would
tolerate that happening on more than one question, which is too loose for a
corpus this small and specific.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** I expect this one at 5 of 5, not 4 of 5, because
`GROUNDING_INSTRUCTION` in `generate.py` hard-requires the model to name the
filename it used, and every in-scope question in this corpus retrieves at
least one chunk — the gate only withholds an answer for out-of-scope
questions, which don't count against this criterion. The only way this
slips is the model ignoring the system instruction, which is exactly what
the starter's prompting is built to prevent.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** I'm keeping the given target of 4 of 5 rather than 5 of
5 because the five `OUT_OF_SCOPE` questions (capital of Mongolia, changing
diesel oil, a 1994 World Cup result, ibuprofen dosage, a Rust for-loop)
share essentially no vocabulary with campus_life, so I expect most of them
to land far above whatever cutoff I pick in Milestone 4. But I haven't
measured the actual distance gap yet at this point in the project, so I'm
leaving room for one surprising overlap rather than promising a perfect 5 of
5 before I've tested anything.

---

## 4. Something about your chunks

At least 95% of chunks correspond to exactly one whole source document —
the chunk boundary matches the document boundary, with no post split across
two chunks.

**Why this target:** Running `python app.py index` on campus_life produced
88 documents and 88 chunks — a 1:1 match — because these posts average 317
characters and are written as a single self-contained thought (a dining
hall's hours, one rule about the pass/fail deadline). That's already the
evidence for this target, not a guess. I set it at 95% rather than 100%
because a small number of longer or multi-topic posts (a couple of the
`course_*` docs run longer and cover both exams and workload) may
legitimately deserve an internal split, and 100% would penalize a chunker
for correctly splitting those. A looser number, like 70%, would tolerate a
chunker arbitrarily fragmenting the short posts that make up most of this
corpus, which is the failure mode Milestone 3 is actually about avoiding.

---

## 5. Your choice

For at least 4 of my 5 test questions, the top-ranked retrieved chunk's
source file is the specific document that actually contains the `expects`
phrase — not just any document among the top-k results.

**Why this target:** This is stricter than criterion 1, which only asks
whether the answer shows up somewhere in the retrieved set. I care about
top-1 precision specifically because campus_life has several sets of
near-duplicate templated documents — six dining hall posts, six housing
noise pages, and pairs like `course_cs_210.txt` / `course_cs_210_exams.txt`
/ `course_cs_210_workload.txt` — where the system could retrieve a
plausible, on-topic, but *wrong* document (e.g. citing Kestrel Commons'
wait times when asked about Halden Hall) and a reader would have no way to
tell without checking. Requiring correct source attribution, not just
topical relevance, in 4 of 5 cases is the real test of whether the citation
means anything. I didn't set it at 5 of 5 for the same reason as criterion
1: the templated similarity across these documents makes at least one miss
plausible.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
