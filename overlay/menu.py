"""In-game ImGui-lite menu driven by hotkeys and keyboard toggles."""
from __future__ import annotations

import pygame


class TrainerMenu:
    def __init__(self, hotkeys: dict) -> None:
        self.hotkeys = hotkeys
        self.visible = False

    def handle(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_INSERT:
            self.visible = not self.visible

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        panel = pygame.Surface((320, 240), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 200))
        pygame.draw.rect(panel, (200, 0, 0), panel.get_rect(), 2)
        surface.blit(panel, (40, 40))