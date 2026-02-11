"""
Player entity: tile-based position, movement, and drawing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

import pygame

from settings import TILE_SIZE, COLOR_PLAYER, PLAYER_SPEED_PIXELS_PER_SECOND
from . import map as game_map


@dataclass
class Player:
    """A simple player representation with smooth, pixel-based movement."""

    # Spawn tile coordinates
    tile_x: int
    tile_y: int

    # Pixel-based position (top-left corner)
    pos_x: float = 0.0
    pos_y: float = 0.0

    def __post_init__(self) -> None:
        # Initialize pixel position from tile coordinates on spawn.
        self.pos_x = float(self.tile_x * TILE_SIZE)
        self.pos_y = float(self.tile_y * TILE_SIZE)

    def update_from_keys(
        self,
        tile_map: game_map.TileGrid,
        pressed_keys: pygame.key.ScancodeWrapper,
        dt: float,
    ) -> None:
        """Update player movement based on current key state using velocity and delta time."""
        input_x = 0
        input_y = 0

        if pressed_keys[pygame.K_w]:
            input_y -= 1
        if pressed_keys[pygame.K_s]:
            input_y += 1
        if pressed_keys[pygame.K_a]:
            input_x -= 1
        if pressed_keys[pygame.K_d]:
            input_x += 1

        # No movement input.
        if input_x == 0 and input_y == 0:
            return

        # Normalise direction to avoid faster diagonal movement.
        length_sq = input_x * input_x + input_y * input_y
        if length_sq == 0:
            return

        length = length_sq**0.5
        dir_x = input_x / length
        dir_y = input_y / length

        vel_x = dir_x * PLAYER_SPEED_PIXELS_PER_SECOND
        vel_y = dir_y * PLAYER_SPEED_PIXELS_PER_SECOND

        self.move_with_collision(tile_map, vel_x, vel_y, dt)

    def get_rect(self) -> pygame.Rect:
        """Return the player's rectangle in pixel space."""
        return pygame.Rect(int(self.pos_x), int(self.pos_y), TILE_SIZE, TILE_SIZE)

    def move_with_collision(
        self,
        tile_map: game_map.TileGrid,
        vel_x: float,
        vel_y: float,
        dt: float,
    ) -> None:
        """Move the player in pixel space while respecting tile collisions."""
        if dt <= 0.0:
            return

        # Start from current rect.
        rect = self.get_rect()

        # --- Horizontal movement ---
        new_x = self.pos_x + vel_x * dt
        rect.x = int(new_x)

        if self._rect_is_walkable(tile_map, rect):
            self.pos_x = new_x
        # else: horizontal movement blocked; keep old x

        # --- Vertical movement ---
        new_y = self.pos_y + vel_y * dt
        rect.y = int(new_y)

        if self._rect_is_walkable(tile_map, rect):
            self.pos_y = new_y
        # else: vertical movement blocked; keep old y

    def _rect_is_walkable(
        self,
        tile_map: game_map.TileGrid,
        rect: pygame.Rect,
    ) -> bool:
        """Return True if all tiles overlapped by rect are walkable."""
        # Determine which tiles the rectangle spans.
        left_tile = rect.left // TILE_SIZE
        right_tile = (rect.right - 1) // TILE_SIZE
        top_tile = rect.top // TILE_SIZE
        bottom_tile = (rect.bottom - 1) // TILE_SIZE

        for ty in range(top_tile, bottom_tile + 1):
            for tx in range(left_tile, right_tile + 1):
                if not game_map.is_walkable(tile_map, tx, ty):
                    return False
        return True

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player as a simple rectangle."""
        pygame.draw.rect(surface, COLOR_PLAYER, self.get_rect())

