"""
Deciding whether an answer was actually correct.

`run_eval.py` runs the questions and hands back raw answers; it deliberately
does not judge them. That judgment is this file's job.

`judge(question, expects, answer, results) -> bool` is what `run_eval.py`
looks for. Each entry in `questions.py::QUESTIONS` already carries an
`expects` string — a word or short phrase a correct answer has to contain
(see that file's docstring). A refused answer ("I don't have enough
information about that") never contains it, so a gate refusal on an in-scope
question scores as a fail here, which is the right outcome: the system was
supposed to answer and didn't.

This does not try to judge whether retrieval pulled the *right* chunk, or
whether the cited source is the correct one — those are what criteria 1, 4
and 5 in `criteria.md` are for, and the assignment is explicit that
aggregating per-question results into per-criterion verdicts is the
student's own work, not something a script should paper over. `results` is
accepted here so a future scorer could use it, but is unused by this simple
version.
"""


def judge(question: str, expects: str, answer: str, results) -> bool:
    """A correct answer contains the phrase we said it would, case-insensitively."""
    if not expects:
        return False
    return expects.strip().lower() in answer.strip().lower()
