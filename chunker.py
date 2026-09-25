"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_into_sentences(text: str) -> list[str]:
    """Split on sentence-ending punctuation followed by whitespace."""
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if s]


def _pack_sentences(paragraph: str, chunk_size: int) -> list[str]:
    """
    Pack a single over-long paragraph into pieces, breaking on sentence
    boundaries rather than mid-sentence.
    """
    pieces: list[str] = []
    current = ""
    for sentence in _split_into_sentences(paragraph):
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) <= chunk_size or not current:
            current = candidate
        else:
            pieces.append(current)
            current = sentence
    if current:
        pieces.append(current)
    return pieces


def _pack_paragraphs(paragraphs: list[str], chunk_size: int) -> list[str]:
    """
    Greedily pack whole paragraphs into pieces up to chunk_size. A paragraph
    that alone exceeds chunk_size falls back to sentence-level packing so a
    single sentence is never split in half.
    """
    pieces: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            pieces.append(current)
            current = ""
        if len(paragraph) <= chunk_size:
            current = paragraph
        else:
            pieces.extend(_pack_sentences(paragraph, chunk_size))
    if current:
        pieces.append(current)
    return pieces


def _apply_overlap(pieces: list[str], overlap: int) -> list[str]:
    """
    Carry the tail of each piece into the start of the next one, so a split
    document doesn't lose context at the seam. Single-piece documents (the
    normal case for campus_life) are untouched.
    """
    if len(pieces) <= 1 or overlap <= 0:
        return pieces

    result = [pieces[0]]
    for previous, piece in zip(pieces, pieces[1:]):
        tail = previous[-overlap:]
        space = tail.find(" ")
        if space != -1:
            tail = tail[space + 1 :]
        result.append(f"{tail} {piece}".strip() if tail else piece)
    return result


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Chunk campus_life posts by paragraph, not by character count.

    Every one of the corpus's 88 posts is under 600 characters and already
    reads as a single self-contained thought (a dining hall's hours, one rule
    about a deadline) — the finding from Milestone 1's index summary. So the
    strategy here is: keep a whole post as one chunk whenever it fits inside
    config.CHUNK_SIZE, and only split on paragraph (then sentence) boundaries
    for the rare post that runs long, instead of cutting at a fixed offset
    the way fallback_split does. config.CHUNK_OVERLAP only matters for those
    rare multi-piece documents.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    chunks: list[Chunk] = []
    for doc in documents:
        paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
        pieces = _apply_overlap(_pack_paragraphs(paragraphs, chunk_size), overlap)
        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
