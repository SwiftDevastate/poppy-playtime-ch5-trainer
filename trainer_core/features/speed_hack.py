"""Scales the player's movement speed float (uses the UE CharacterMovement chain)."""
from __future__ import annotations

from trainer_core.features.base import TrainerFeature


class SpeedHack(TrainerFeature):
    name = "speed_multiplier"
    requires = ("move_speed",)
    BASE_SPEED = 600.0  # UE units

    def _apply(self) -> None:
        addr = self.resolver.resolve("move_speed")
        if not addr:
            return
        self.attacher.write_float(addr, self.BASE_SPEED * float(self.value))

    def _revert(self) -> None:
        addr = self.resolver.resolve("move_speed")
        if addr:
            self.attacher.write_float(addr, self.BASE_SPEED)