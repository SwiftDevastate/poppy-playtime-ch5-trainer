"""Keeps the grabpack battery float pinned at max (Chapter 5 mechanic)."""
from __future__ import annotations

import threading
import time

from trainer_core.features.base import TrainerFeature


class InfiniteBattery(TrainerFeature):
    name = "infinite_battery"
    requires = ("grabpack_battery",)
    MAX_CHARGE = 1.0

    def _apply(self) -> None:
        addr = self.resolver.resolve("grabpack_battery")
        if not addr:
            return
        self._stop = threading.Event()
        threading.Thread(target=self._loop, args=(addr,), daemon=True).start()

    def _loop(self, addr: int) -> None:
        while not self._stop.is_set():
            self.attacher.write_float(addr, self.MAX_CHARGE)
            time.sleep(0.25)

    def _revert(self) -> None:
        self._stop.set()