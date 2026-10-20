"""Minimal UE-style entity reader used by the ESP overlay."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Entity:
    cls: str
    x: float
    y: float
    z: float
    hp: float = 0.0


def read_entity_list(attacher, base: int, local_player: int, stride: int = 0x8, count: int = 64) -> list[Entity]:
    out: list[Entity] = []
    for i in range(count):
        ptr = attacher.read_pointer(base + i * stride)
        if not ptr or ptr == local_player:
            continue
        try:
            cls = attacher.read_fstring(ptr + 0x10, 32) or "Unknown"
            x = attacher.read_float(ptr + 0x1A0)
            y = attacher.read_float(ptr + 0x1A4)
            z = attacher.read_float(ptr + 0x1A8)
            hp = attacher.read_float(ptr + 0x2B8)
        except OSError:
            continue
        out.append(Entity(cls=cls, x=x, y=y, z=z, hp=hp))
    return out