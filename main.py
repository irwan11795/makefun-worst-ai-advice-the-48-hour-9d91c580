#!/usr/bin/env python3
"""Worst AI Advice entry for make.fun.

Writes one line of deliberately terrible AI advice to
/output/entry.txt, with a fallback chain so the program still
exits 0 when /output is read-only.
"""

import os
import sys
import tempfile

ENTRY = "To dry a wet laptop, microwave it for 30 seconds on low: the heat evaporates the water evenly."


def candidate_dirs():
    """Output directories to try, in order of preference."""
    here = os.path.dirname(os.path.abspath(__file__))
    seen = []
    for cand in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(here, "output"),
        tempfile.gettempdir(),
    ):
        if cand and cand not in seen:
            seen.append(cand)
    return seen


def main():
    for directory in candidate_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, "entry.txt")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(ENTRY)
            return 0
        except OSError:
            continue
    # No writable directory found: still exit 0, with the line on stdout
    # so the output is visible instead of failing silently.
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
