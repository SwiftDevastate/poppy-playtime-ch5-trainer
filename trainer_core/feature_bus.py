"""Central registry that owns every feature module and their hotkeys."""
from __future__ import annotations

import logging
from typing import Dict, Type

import keyboard

from trainer_core.features.base import TrainerFeature
from trainer_core.features.godmode import GodMode
from trainer_core.features.infinite_battery import InfiniteBattery
from trainer_core.features.grabpack_range import GrabpackRange
from trainer_core.features.huggy_esp import HuggyEsp
from trainer_core.features.no_clip import NoClip
from trainer_core.features.speed_hack import SpeedHack

log = logging.getLogger(__name__)

REGISTRY: Dict[str, Type[TrainerFeature]] = {
    "godmode": GodMode,
    "infinite_battery": InfiniteBattery,
    "grabpack_range": GrabpackRange,
    "huggy_esp": HuggyEsp,
    "no_clip": NoClip,
    "speed_multiplier": SpeedHack,
}


class FeatureBus:
    def __init__(self, attacher, resolver, feature_cfg: dict) -> None:
        self._attacher = attacher
        self._resolver = resolver
        self._cfg = feature_cfg or {}
        self._instances: Dict[str, TrainerFeature] = {}

    def start_all(self) -> None:
        for key, cls in REGISTRY.items():
            value = self._cfg.get(key)
            if value is None:
                continue
            try:
                feat = cls(self._attacher, self._resolver, value)
                feat.enable() if bool(value) else None
                self._instances[key] = feat
                log.info("feature loaded: %s (value=%s)", key, value)
            except Exception as exc:  # noqa: BLE001
                log.exception("feature %s failed to start: %s", key, exc)

        keyboard.add_hotkey("f7", self._toggle, args=("no_clip",))

    def _toggle(self, name: str) -> None:
        feat = self._instances.get(name)
        if feat:
            feat.toggle()

    def stop_all(self) -> None:
        for feat in self._instances.values():
            feat.disable()