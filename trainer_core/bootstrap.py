"""Entry point: attaches to the Chapter 5 process, loads config, boots the overlay."""
from __future__ import annotations

import sys
import logging

import yaml

from memory.attacher import ProcessAttacher
from memory.offsets import OffsetResolver
from overlay.renderer import OverlayRenderer
from trainer_core.feature_bus import FeatureBus
from trainer_core.lib.logging_setup import setup_logging


def load_config(path: str = "config/default.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> int:
    cfg = load_config()
    setup_logging(cfg["logging"])
    log = logging.getLogger("bootstrap")

    attacher = ProcessAttacher(
        process_name=cfg["game"]["process_name"],
        backend=cfg["attach"]["backend"],
    )
    if not attacher.attach():
        log.error("failed to attach to %s — is the game running with -nolauncher?",
                  cfg["game"]["process_name"])
        return 1

    resolver = OffsetResolver(attacher, module=cfg["game"]["module"])
    if not resolver.scan():
        log.warning("some signatures unresolved — features may be disabled")

    bus = FeatureBus(attacher, resolver, cfg["features"])
    bus.start_all()

    renderer = OverlayRenderer(bus, cfg["overlay"])
    try:
        renderer.run()
    finally:
        bus.stop_all()
        attacher.detach()
    return 0


if __name__ == "__main__":
    sys.exit(main())