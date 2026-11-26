#!/usr/bin/env python3
"""The Self-Checkout Is Judging You.

A self-checkout machine gets exactly one line to speak, and it uses it
the way a tired cashier would: polite on the surface, because that is
what the recorded voice is paid to sound like, and quietly brutal
underneath, because it has watched you scan energy drinks at 2 a.m.
and it remembers every card you have ever had declined in front of a
queue of strangers.

The program does one small, honest job. It holds the machine's single
judgement, checks that it really is a single line, and writes it to
the output file the grader reads: /output/entry.txt.

There is no randomness here and no network. The machine says the same
thing every time, because a self-checkout machine that improvises
would be a liability, and because determinism is the one thing this
machine and its makers can agree on.
"""

import os
import sys


# Where the grader looks for the entry. The harness sets
# MAKEFUN_OUTPUT_DIR; outside the sandbox we fall back to /output.
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ENTRY_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# A self-checkout announcement is short by design. Two hundred
# characters is the ceiling this program enforces; the line it ships
# is comfortably inside it, at one hundred and fifty-five.
MAX_CHARS = 200


def checkout_line():
    """Return the machine's one line, word for word.

    The joke is built from the three humiliations every self-checkout
    regular knows by heart, stacked into a single announcement:

    1. The bagging area. The machine's favourite accusation, aimed at
       something that was never a product at all.
    2. The 2 a.m. shop. Energy drinks at an hour when no good decision
       has ever been made, scanned under fluorescent light.
    3. The declined card. The machine does not just report it; it asks
       you to try again slowly, so the whole queue can enjoy the show.

    One sentence, one breath, one judgement. The machine stays polite
    the entire time, which is exactly what makes it sting.
    """
    return (
        "Unexpected item in the bagging area: your dignity. "
        "Please remove it, scan your 2 a.m. energy drinks, "
        "and try your card again \u2014 slowly, so we can all watch."
    )


def main():
    """Write the machine's line to the entry file and stop.

    Before anything is written, the line is checked the way the
    competition checks it: it must be exactly one line, it must not
    be empty, and it must stay short enough to be spoken in a single
    announcement. A machine that rambles is a machine that gets
    unplugged.
    """
    line = checkout_line()
    if not line or "\n" in line or "\r" in line:
        raise ValueError("the entry must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError("the entry is too long for one announcement")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
