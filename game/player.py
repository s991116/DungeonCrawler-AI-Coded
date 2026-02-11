"""
Player entity: tile-based position, movement, and drawing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

import pygame

from settings import TILE_SIZE, COLOR_PLAYER
from . import map as game_map


@dataclass
class Player:
    """A simple tile-based player representation."""

    tile_x: int
    tile_y: int

    # Future inventory scaffolding (not yet wired up)
    left_hand_item: Optional[Any] = None
    right_hand_item: Optional[Any] = None
    backpack: List[Any] = field(default_factory=list)

    def move_if_possible(self, tile_map: game_map.TileGrid, dx: int, dy: int) -> None:
        """Attempt to move the player by (dx, dy) tiles if walkable."""
        if dx == 0 and dy == 0:
            return

        new_x = self.tile_x + dx
        new_y = self.tile_y + dy

        if game_map.is_walkable(tile_map, new_x, new_y):
            self.tile_x = new_x
            self.tile_y = new_y

    def update_from_keys(self, tile_map: game_map.TileGrid, pressed_keys: pygame.key.ScancodeWrapper) -> None:
        """Update player movement based on current key state."""
        dx = 0
        dy = 0

        if pressed_keys[pygame.K_w]:
            dy -= 1
        if pressed_keys[pygame.K_s]:
            dy += 1
        if pressed_keys[pygame.K_a]:
            dx -= 1
        if pressed_keys[pygame.K_d]:
            dx += 1

        # Only one-tile-per-frame movement for now; no diagonal speed adjustments.
        self.move_if_possible(tile_map, dx, dy)

    def get_rect(self) -> pygame.Rect:
        """Return the player's rectangle in pixel space."""
        return pygame.Rect(
            self.tile_x * TILE_SIZE,
            self.tile_y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player as a simple rectangle."""
        pygame.draw.rect(surface, COLOR_PLAYER, self.get_rect())

