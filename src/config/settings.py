"""Game settings and constants."""

import pygame

# Window settings
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOWSIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
GAME_TITLE = "Lucky Race"
FPS = 120

# Colors
COIN_COLOR = (255, 215, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font settings
FONT_NAME = "Asap"
FONT_SIZES = {"small": 16, "medium": 20, "large": 30, "xlarge": 35}

# Game settings
INITIAL_MONEY = 300
MIN_BET = 200
MAX_ITEMS = 1
ITEM_PRICES = {
    1: 100,  # Speed up
    2: 300,  # Erase
    3: 200,  # Weak
    4: 400,  # Flash
    5: 500,  # Restart
}

# Input keys
NUMBER_KEYS = [
    ord("1"),
    ord("2"),
    ord("3"),
    ord("4"),
    ord("5"),
    ord("6"),
    ord("7"),
    ord("8"),
    ord("9"),
    ord("0"),
]

CHARACTER_KEYS = [
    ord("A"),
    ord("B"),
    ord("C"),
    ord("D"),
    ord("E"),
    ord("F"),
    ord("G"),
    ord("H"),
    ord("I"),
    ord("J"),
    ord("K"),
    ord("L"),
    ord("M"),
    ord("N"),
    ord("O"),
    ord("P"),
    ord("Q"),
    ord("R"),
    ord("S"),
    ord("T"),
    ord("U"),
    ord("V"),
    ord("W"),
    ord("X"),
    ord("Y"),
    ord("Z"),
    ord("a"),
    ord("b"),
    ord("c"),
    ord("d"),
    ord("e"),
    ord("f"),
    ord("g"),
    ord("h"),
    ord("i"),
    ord("j"),
    ord("k"),
    ord("l"),
    ord("m"),
    ord("n"),
    ord("o"),
    ord("p"),
    ord("q"),
    ord("r"),
    ord("s"),
    ord("t"),
    ord("u"),
    ord("v"),
    ord("w"),
    ord("x"),
    ord("y"),
    ord("z"),
]

# Languages
LANGUAGE_ENGLISH = 0
LANGUAGE_VIETNAMESE = 1

# Default settings
DEFAULT_LANGUAGE = LANGUAGE_VIETNAMESE
DEFAULT_MUSIC_VOLUME = 0  # 0 = off, 1 = on
