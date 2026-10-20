"""Enumerates Huggy Wuggy / Chapter-5 entity list and feeds the overlay."""
from __future__ import annotations

from trainer_core.lib.entity import Entity, read_entity_list


class HuggyEsp(TrainerFeature):
    name = "huggy_esp"
    requires = ("entity_list", "local_player")

    def _apply(self) -> None:
        self._entities: list[Entity] = []

    def snapshot(self) -> list[Entity]:
        base = self.resolver.resolve("entity_list")
        local = self.resolver.resolve("local_player")
        if not base or not local:
            return []
        self._entities = read_entity_list(self.attacher, base, local)
        return self._entities

    def _revert(self) -> None:
        self._entities = []