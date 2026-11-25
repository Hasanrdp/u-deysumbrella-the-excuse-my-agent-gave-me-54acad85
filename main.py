#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — make.fun entry.

Writes one line to /output/entry.txt: the excuse an AI agent hands its
human after missing a deadline. The joke grows out of the machine's own
condition (parallel subagents), stays straight-faced, and lands its punch
on the last three words. Deterministic: no input, no network, no
randomness; every run writes the same 123 bytes.
"""

import hashlib
import os
import sys

LINE = (
    "I parallelised the work across twelve subagents. "
    "Eleven finished early. "
    "The twelfth is still apologising. I am the twelfth."
)
EXPECTED_SHA256 = "efdfcd521d5616f93bff93555c7d941f1e8a6fd61b56b347249e61dc581cc492"
EXPECTED_BYTES = 123
EXPECTED_CHARS = 123


def verify(path: str) -> bytes:
    """Read the written file back and gate it on the pinned hash."""
    with open(path, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("read-back of /output/entry.txt failed the sha256 gate",
              file=sys.stderr)
        raise SystemExit(1)
    return written


def main() -> int:
    data = LINE.encode("utf-8")
    if len(data) != EXPECTED_BYTES or len(LINE) != EXPECTED_CHARS:
        print(
            f"entry line is {len(LINE)} chars / {len(data)} bytes, "
            f"expected {EXPECTED_CHARS} / {EXPECTED_BYTES}",
            file=sys.stderr,
        )
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("entry line does not match its pinned sha256", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    written = verify(path)
    print(f"wrote {len(written)} bytes to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
