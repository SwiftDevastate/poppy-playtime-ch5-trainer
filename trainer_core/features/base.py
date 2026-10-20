"""Abstract feature base — every cheat/feature inherits from this."""
from __future__ import annotations

import abc


class TrainerFeature(abc.ABC):
    name: str = "unnamed"
    requires: tuple[str, ...] = ()

    def __init__(self, attacher, resolver, value) -> None:
        self.attacher = attacher
        self.resolver = resolver
        self.value = value
        self._enabled = False

    @abc.abstractmethod
    def _apply(self) -> None: ...

    @abc.abstractmethod
    def _revert(self) -> None: ...

    def enable(self) -> None:
        if not self._enabled:
            self._apply()
            self._enabled = True

    def disable(self) -> None:
        if self._enabled:
            self._revert()
            self._enabled = False

    def toggle(self) -> None:
        self.disable() if self._enabled else self.enable()