from __future__ import annotations

import logging
import os


def setup_logging(cfg: dict) -> None:
    level = getattr(logging, str(cfg.get("level", "INFO")).upper(), logging.INFO)
    path = cfg.get("file", "logs/trainer.log")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)-7s %(name)s :: %(message)s",
        handlers=[
            logging.FileHandler(path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )