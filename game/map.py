"""
Tile map representation and helpers.

For the first milestone, this module exposes a hard-coded demo map and
basic helpers to query and draw it.
"""

from typing import List

import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from . import tiles


TileGrid = List[List[int]]


def load_demo_map() -> TileGrid:
    """
    Return a simple hard-coded map.

    0 = floor (walkable)
    1 = wall (not walkable)
    """
    # A small bordered room; this can be replaced later with loading from a file.
    layout = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    return layout


def is_within_bounds(tile_map: TileGrid, tile_x: int, tile_y: int) -> bool:
    """Return True if the given tile coordinates are inside the map."""
    if tile_y < 0 or tile_y >= len(tile_map):
        return False
    if tile_x < 0 or tile_x >= len(tile_map[0]):
        return False
    return True


def is_walkable(tile_map: TileGrid, tile_x: int, tile_y: int) -> bool:
    """
    Return True if the tile at (tile_x, tile_y) is walkable.

    Currently, floors are walkable and walls are not.
    """
    if not is_within_bounds(tile_map, tile_x, tile_y):
        return False
    return tile_map[tile_y][tile_x] == tiles.TILE_FLOOR


def draw_map(surface: pygame.Surface, tile_map: TileGrid) -> None:
    """Draw the entire map to the given surface."""
    for y, row in enumerate(tile_map):
        for x, tile_type in enumerate(row):
            tiles.draw_tile(surface, x, y, tile_type)

