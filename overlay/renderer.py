"""pygame overlay window drawn on top of the game with a click-through flag."""
from __future__ import annotations

import logging

import pygame

from overlay.esp import draw_esp
from overlay.menu import TrainerMenu

log = logging.getLogger(__name__)


class OverlayRenderer:
    def __init__(self, bus, cfg: dict) -> None:
        self.bus = bus
        self.cfg = cfg
        self.menu = TrainerMenu(cfg.get("hotkeys", {}))
        self._running = False

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        pygame.display.set_caption("Poppy Playtime - Chapter 5 Trainer")
        clock = pygame.time.Clock()
        self._running = True

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                self.menu.handle(event)

            screen.fill((0, 0, 0, 0))
            esp = self.bus._instances.get("huggy_esp")
            if esp and self.menu.visible:
                draw_esp(screen, esp.snapshot(), pygame.font.SysFont(self.cfg["font"], 14))
            self.menu.draw(screen)
            pygame.display.flip()
            clock.tick(self.cfg.get("fps_cap", 60))

        pygame.quit()