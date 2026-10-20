"""Toggles collision flag on the local player.""" 
from __future__ import annotations

from trainer_core.features.base import TrainerFeature


class NoClip(TrainerFeature):
    name = "no_clip"
    requires = ("player_collision",)

    def _apply(self) -> None:
        addr = self.resolver.resolve("player_collision")
        if addr:
            self.attacher.write_byte(addr, 0x00)

    def _revert(self) -> None:
        addr = self.resolver.resolve("player_collision")
        if addr:
            self.attacher.write_byte(addr, 0x01)