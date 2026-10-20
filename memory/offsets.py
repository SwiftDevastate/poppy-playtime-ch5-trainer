"""Signature scanner + pointer-chain resolver for Chapter 5 builds."""
from __future__ import annotations

import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class Pattern:
    module: str
    sig: bytes
    offset: int = 0
    chain: tuple[int, ...] = ()


# Signatures for build 1.0.3.114 (2026-02). Community PRs welcome.
SIGNATURES: dict[str, Pattern] = {
    "player_health":     Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\x48\x8B\x0D\x00\x00\x00\x00\xF3\x0F\x10", 0x3, (0x18, 0x2B8)),
    "player_collision":  Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\x0F\xB6\x81\x00\x00\x00\x00\x84\xC0", 0x3),
    "grabpack_reach":    Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\xF3\x0F\x10\x89\x00\x00\x00\x00\xF3\x0F\x59", 0x4),
    "grabpack_battery":  Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\xF3\x0F\x11\x81\x00\x00\x00\x00\xC3\xCC", 0x4),
    "move_speed":        Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\xF3\x0F\x10\x87\x00\x00\x00\x00\xF3\x0F\x11", 0x4),
    "entity_list":       Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\x48\x8B\x05\x00\x00\x00\x00\x48\x8B\x48", 0x3, (0x28,)),
    "local_player":      Pattern("PoppyPlaytime_Ch5-Win64-Shipping.exe", b"\x48\x8B\x0D\x00\x00\x00\x00\x48\x85\xC9", 0x3, (0x8,)),
}


class OffsetResolver:
    def __init__(self, attacher, module: str) -> None:
        self.attacher = attacher
        self.module = module
        self._cache: dict[str, int] = {}

    def scan(self) -> bool:
        ok = 0
        for name, pat in SIGNATURES.items():
            try:
                addr = self._scan_pattern(pat)
                if addr:
                    self._cache[name] = self._follow(addr, pat.chain)
                    ok += 1
            except Exception as exc:  # noqa: BLE001
                log.warning("scan failed for %s: %s", name, exc)
        log.info("resolved %d/%d signatures", ok, len(SIGNATURES))
        return ok == len(SIGNATURES)

    def resolve(self, name: str) -> int | None:
        return self._cache.get(name)

    def _scan_pattern(self, pat: Pattern) -> int | None:
        base = self.attacher.base_address(pat.module)
        # naive scan — replaced by AOB scanner in memory/scanner.py
        return base + pat.offset

    def _follow(self, addr: int, chain: tuple[int, ...]) -> int:
        cur = addr
        for off in chain:
            cur = self.attacher.read_pointer(cur) + off
        return cur