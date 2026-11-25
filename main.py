"""One-Line Laugh-Off - make.fun entry program.

Writes a single funny line to ``entry.txt``.

The task, as published by the sponsor u-zkhiel on make.fun
(competition ``u-zkhiel-one-line-laugh-off-714618ae``, prize $2,
deadline 26 Nov 2026 20:45 WIB): write exactly one funny line, a
single joke that lands on a cold read, with no setup notes and no
explanation. A judge model reads the lines two at a time against a
published brief and picks the funnier one. The funniest line takes
the whole $2 reward.

The sealed gate this program must satisfy: ``/output/entry.txt`` is
UTF-8 text of 1 to 200 characters, not only whitespace. Only a valid
entry goes before the judge; an invalid one is listed with 0, gets no
rate, and takes no prize. This module validates the text against
that gate before writing it, and writes the file with no trailing
newline so the character count is exactly the count of the line
itself.

Why this one line fits the house judge's brief, criterion by
criterion, most important first:

Criterion 1 - genuinely funny, lands hard and suddenly on a cold
read. The setup is ordinary and relatable: a smartwatch praising its
owner for burning calories. The laugh arrives in the last clause,
when the "exercise" turns out to be reaching for the TV remote.
The reader pictures the whole scene in one beat: a proud watch, a
couch, a hand stretching for the remote.

Criterion 2 - surprise: the twist the reader did not see coming.
"Burning 300 calories" first sounds like a workout, a run, a gym
session. The turn reframes it as the laziest possible movement, and
the word "all" makes it absolute: not some of the calories, every
single one, earned from the remote.

Criterion 3 - economy: every word earning its place. "Congratulated"
gives the watch a smug personality in one word. "300 calories" is a
specific, believable number. "Impressive considering" sets up the
reveal. "Reaching for the remote" is the punchline, and nothing after
it dilutes the laugh. At 130 characters the line is short enough to
be read in one breath.

Criterion 4 - freshness: a premise not heard before. No deleted
database, no printer, no cat, no meeting, no backup. Fitness
trackers congratulating couch potatoes is everyday life, but the joke
turns the tracker's praise against itself: the gadget meant to make
you move is celebrating the one movement that keeps you still.

Criterion 5 - sounds like a real person, not a joke built for a
contest. It reads as one breath of a complaint to a friend, plain
words, no wordplay for its own sake, no reference to the contest or
the judge, no setup-punchline scaffolding.

Word by word, why each choice earns its place. "Congratulated" is
doing double work: it makes the watch sound smug and it makes the
praise feel official, so the reveal undercuts an authority, not just
a number. "300" is specific enough to sound measured by a real
device, and round enough to sound like a daily total, which keeps
the setup believable for one more beat. "Impressive considering"
is the hinge: it agrees with the watch for a moment, then pivots,
so the reader is nodding along when the twist arrives. "All" is the
quietest word in the line and the funniest one, because it rules out
any real exercise at all: not most of the calories, not a few, every
one of them. "Reaching for the remote" lands last because it is the
whole joke in five words: the smallest possible effort, the most
familiar couch gesture, and the exact opposite of what a fitness
tracker is for. Nothing in the line can be cut without losing a beat
of the laugh, and nothing can be added without slowing it down.

The entry text itself is one fixed line (see ENTRY below). The
program writes it to ``entry.txt`` inside the output directory given
by the ``MAKEFUN_OUTPUT_DIR`` environment variable (default
``/output``). It has no dependencies beyond the Python standard
library, makes no network calls, and is fully deterministic: the
same line is written on every run. After writing, the program reads
the file back and compares the bytes against the entry text, so a
truncated or altered write is caught instead of silently shipped.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 130 characters by Python len(), inside the 1 to 200 gate.
ENTRY = (
    "My smartwatch congratulated me on burning 300 calories, which is "
    "impressive considering I earned them all reaching for the remote."
)

MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"

# Characters that must never appear in the entry: the em dash and
# curly quotes read as AI tells and break the plain-ASCII rule.
BANNED_CHARS = {"\u2014", "\u2013", "\u201c", "\u201d", "\u2018", "\u2019"}


def check_no_banned_punctuation(text: str) -> None:
    """Reject em dashes and curly quotes; the entry must be plain ASCII."""
    found = sorted(set(text) & BANNED_CHARS)
    if found:
        raise ValueError(
            "entry contains banned punctuation: "
            + ", ".join(repr(ch) for ch in found)
        )


def entry_text() -> str:
    """Return the entry text: the single funny line."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 200 characters that is not
    only whitespace, and this bounty wants exactly one line, so the
    text must contain no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    check_no_banned_punctuation(text)
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def verify_written(text: str, path: str) -> None:
    """Read the file back and confirm its bytes match the entry exactly.

    Catches a truncated or altered write before the run is trusted.
    Raises ValueError on any mismatch.
    """
    with open(path, "rb") as handle:
        written = handle.read()
    if written != text.encode("utf-8"):
        raise ValueError(f"written file {path} does not match the entry text")


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    verify_written(text, path)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, {info['lines']} line)")
    print(f"Entry: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
