"""
Entry point for the dungeon crawler prototype.

This wires together the map and player modules into a basic game loop
with tile-based WASD movement and wall collision.
"""

import sys

import pygame

from settings import (
    SCREEN_SIZE,
    WINDOW_TITLE,
    FPS,
    COLOR_BLACK,
)
from game import map as game_map
from game.player import Player


def init_pygame() -> pygame.Surface:
    """Initialize pygame and return the main display surface."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    return screen


def main() -> None:
    screen = init_pygame()
    clock = pygame.time.Clock()

    tile_map = game_map.load_demo_map()
    # Start roughly in the center of the room (adjust as needed).
    player = Player(tile_x=5, tile_y=5)

    running = True
    while running:
        # Limit FPS and compute delta time in seconds for smooth movement.
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pressed = pygame.key.get_pressed()
        player.update_from_keys(tile_map, pressed, dt)

        screen.fill(COLOR_BLACK)
        game_map.draw_map(screen, tile_map)
        player.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()

