"""AOB (array-of-bytes) scanner with wildcard support used by OffsetResolver."""
from __future__ import annotations

import re


def _sig_to_regex(sig: bytes) -> re.Pattern[bytes]:
    parts = []
    for b in sig:
        parts.append(b"." if b == 0x00 else re.escape(bytes([b])))
    return re.compile(b"".join(parts), re.DOTALL)


def find_pattern(buffer: bytes, sig: bytes, max_hits: int = 1) -> list[int]:
    rx = _sig_to_regex(sig)
    hits: list[int] = []
    for m in rx.finditer(buffer):
        hits.append(m.start())
        if len(hits) >= max_hits:
            break
    return hits