"""Writes a non-zero HP float every tick via the player health pointer chain."""
from __future__ import annotations

import threading
import time

from trainer_core.features.base import TrainerFeature


class GodMode(TrainerFeature):
    name = "godmode"
    requires = ("player_health",)

    def _apply(self) -> None:
        addr = self.resolver.resolve("player_health")
        if not addr:
            return
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, args=(addr,), daemon=True)
        self._thread.start()

    def _loop(self, addr: int) -> None:
        while not self._stop.is_set():
            try:
                self.attacher.write_float(addr, 100.0)
            except Exception:
                break
            time.sleep(0.05)

    def _revert(self) -> None:
        self._stop.set()