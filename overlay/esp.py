"""ESP rendering — draws Huggy Wuggy and other Chapter-5 entity boxes."""
from __future__ import annotations

import pygame


def world_to_screen(x: float, y: float, z: float, w: int = 1920, h: int = 1080) -> tuple[int, int]:
    # Simplified orthographic projection; replaced by W2S matrix in v2
    return int(w / 2 + x * 2), int(h / 2 + y * 2)


def draw_esp(surface: pygame.Surface, entities, font: pygame.font.Font) -> None:
    for e in entities:
        sx, sy = world_to_screen(e.x, e.y, e.z)
        rect = pygame.Rect(sx - 20, sy - 20, 40, 60)
        pygame.draw.rect(surface, (255, 40, 40), rect, 1)
        label = font.render(f"{e.cls} [{e.hp:.0f}]", True, (255, 255, 255))
        surface.blit(label, (sx - 20, sy - 36))