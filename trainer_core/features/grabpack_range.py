"""Patches the grabpack max-reach float to a configurable range."""
from __future__ import annotations

from trainer_core.features.base import TrainerFeature


class GrabpackRange(TrainerFeature):
    name = "grabpack_range"
    requires = ("grabpack_reach",)
    ORIGINAL = 2.5

    def _apply(self) -> None:
        addr = self.resolver.resolve("grabpack_reach")
        if not addr:
            return
        self.attacher.write_float(addr, float(self.value))

    def _revert(self) -> None:
        addr = self.resolver.resolve("grabpack_reach")
        if addr:
            self.attacher.write_float(addr, self.ORIGINAL)