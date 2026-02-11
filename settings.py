"""
Global game settings and key bindings.

This module intentionally contains only constants so it can be
imported freely without causing circular imports.
"""

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Dungeon Crawler (WASD Prototype)"

# Tile configuration
TILE_SIZE = 32  # pixels

# Frame rate
FPS = 60

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_FLOOR = (50, 50, 50)
COLOR_WALL = (100, 100, 100)
COLOR_PLAYER = (200, 200, 50)

# Reserved key bindings (WASD wired up first; others for future use)
KEY_MOVE_UP = "w"
KEY_MOVE_DOWN = "s"
KEY_MOVE_LEFT = "a"
KEY_MOVE_RIGHT = "d"

# Future interaction keys (not wired yet)
KEY_INTERACT = "e"
KEY_SWAP_HAND_LEFT = "1"
KEY_SWAP_HAND_RIGHT = "2"

