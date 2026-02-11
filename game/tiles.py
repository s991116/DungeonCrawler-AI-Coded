"""
Tile constants, colors, and drawing helpers.

Tiles are deliberately simple (just rectangles) for the first milestone,
so it is easy to swap in sprites later without touching game logic.
"""

from typing import Tuple

import pygame

from settings import TILE_SIZE, COLOR_FLOOR, COLOR_WALL


# Logical tile types
TILE_FLOOR = 0
TILE_WALL = 1


def tile_to_pixel_rect(tile_x: int, tile_y: int) -> pygame.Rect:
    """Convert tile coordinates to a pygame.Rect in pixel space."""
    return pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)


def get_tile_color(tile_type: int) -> Tuple[int, int, int]:
    """Return the RGB color associated with a tile type."""
    if tile_type == TILE_WALL:
        return COLOR_WALL
    return COLOR_FLOOR


def draw_tile(surface: pygame.Surface, tile_x: int, tile_y: int, tile_type: int) -> None:
    """Draw a single tile onto the given surface."""
    rect = tile_to_pixel_rect(tile_x, tile_y)
    color = get_tile_color(tile_type)
    pygame.draw.rect(surface, color, rect)

