"""
Tile map representation and helpers.

For the first milestone, this module exposes a hard-coded demo map and
basic helpers to query and draw it.
"""

from typing import List
import random

import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from . import tiles


TileGrid = List[List[int]]


def generate_labyrinth(width: int, height: int, path_width: int = 2) -> TileGrid:
    """
    Generate a labyrinth using recursive backtracking algorithm.
    
    Args:
        width: Width of the maze in tiles
        height: Height of the maze in tiles
        path_width: Width of paths (2-3 tiles recommended)
    
    Returns a TileGrid where:
    0 = floor (walkable)
    1 = wall (not walkable)
    """
    # Cell spacing: path_width + 1 wall tile between cells
    cell_spacing = path_width + 1

    # We interpret `width`/`height` as the final maze dimensions in tiles.
    # To keep the *outer* border exactly 1 tile thick (same as internal walls),
    # we need to ensure:
    # - Top wall: row 0 only
    # - Left wall: column 0 only  
    # - Right wall: column width-1 only
    # - Bottom wall: row height-1 only
    # So we carve cells starting at position 1, and ensure they don't extend beyond width-2/height-2
    
    border_thickness = 1  # Always 1 tile thick outer walls
    
    # Start with all walls at final size.
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve_cell(cx: int, cy: int):
        """Carve a cell (path_width x path_width area) starting at (cx, cy)."""
        # Ensure we don't carve into the outer border
        for dy in range(path_width):
            for dx in range(path_width):
                x, y = cx + dx, cy + dy
                if border_thickness <= x < width - border_thickness and border_thickness <= y < height - border_thickness:
                    maze[y][x] = 0

    def carve_path(x1: int, y1: int, x2: int, y2: int):
        """Carve a path between two cells, ensuring we don't carve into outer border."""
        # Determine direction
        if x2 > x1:  # Moving right
            for dx in range(path_width):
                for dy in range(path_width):
                    x, y = x1 + path_width + dx, y1 + dy
                    if border_thickness <= x < width - border_thickness and border_thickness <= y < height - border_thickness:
                        maze[y][x] = 0
        elif x2 < x1:  # Moving left
            for dx in range(path_width):
                for dy in range(path_width):
                    x, y = x1 - path_width + dx, y1 + dy
                    if border_thickness <= x < width - border_thickness and border_thickness <= y < height - border_thickness:
                        maze[y][x] = 0
        elif y2 > y1:  # Moving down
            for dx in range(path_width):
                for dy in range(path_width):
                    x, y = x1 + dx, y1 + path_width + dy
                    if border_thickness <= x < width - border_thickness and border_thickness <= y < height - border_thickness:
                        maze[y][x] = 0
        elif y2 < y1:  # Moving up
            for dx in range(path_width):
                for dy in range(path_width):
                    x, y = x1 + dx, y1 - path_width + dy
                    if border_thickness <= x < width - border_thickness and border_thickness <= y < height - border_thickness:
                        maze[y][x] = 0

    def get_neighbors(cx: int, cy: int):
        """Get unvisited neighbors cell_spacing tiles away within inner bounds."""
        dirs = [(cell_spacing, 0), (-cell_spacing, 0), (0, cell_spacing), (0, -cell_spacing)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            # Inner bounds: ensure cells don't extend beyond the 1-tile border
            # Cells start at (nx, ny) and extend path_width tiles, so:
            # - Left edge: nx >= border_thickness (1)
            # - Right edge: nx + path_width <= width - border_thickness (width - 1)
            # - Top edge: ny >= border_thickness (1)
            # - Bottom edge: ny + path_width <= height - border_thickness (height - 1)
            min_x = border_thickness
            min_y = border_thickness
            max_x = width - border_thickness - path_width + 1  # +1 because range is exclusive
            max_y = height - border_thickness - path_width + 1
            if min_x <= nx < max_x and min_y <= ny < max_y:
                yield nx, ny, dx, dy

    # Start in top-left interior cell (inside the 1-tile border).
    start_x, start_y = border_thickness, border_thickness
    carve_cell(start_x, start_y)

    stack = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]
        carved = False
        for nx, ny, dx, dy in get_neighbors(x, y):
            # Check if this cell is unvisited (all walls)
            is_unvisited = True
            for check_dy in range(path_width):
                for check_dx in range(path_width):
                    if maze[ny + check_dy][nx + check_dx] == 0:
                        is_unvisited = False
                        break
                if not is_unvisited:
                    break
            
            if is_unvisited:
                # Carve the path between cells
                carve_path(x, y, nx, ny)
                # Carve the destination cell
                carve_cell(nx, ny)
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()

    return maze


def load_demo_map() -> TileGrid:
    """
    Return a labyrinth map that fits entirely within the screen.

    0 = floor (walkable)
    1 = wall (not walkable)
    """
    # Compute how many tiles fit on screen so the whole maze is visible.
    tiles_x = SCREEN_WIDTH // TILE_SIZE
    tiles_y = SCREEN_HEIGHT // TILE_SIZE

    # Choose path width in tiles. With TILE_SIZE‑wide player, this makes
    # corridors 2× the player width (within the requested 2–3× range).
    path_width_tiles = 2

    return generate_labyrinth(tiles_x, tiles_y, path_width=path_width_tiles)


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

