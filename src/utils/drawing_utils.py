"""Drawing utilities for rendering text and UI elements."""

import pygame
from typing import Tuple


def draw_text(text: str, font: pygame.font.Font, color: Tuple[int, int, int],
              surface: pygame.Surface, x: int, y: int) -> None:
    """
    Draw text on a surface.

    Args:
        text: Text to draw
        font: Pygame font to use
        color: RGB color tuple
        surface: Surface to draw on
        x: X coordinate
        y: Y coordinate
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def create_fonts() -> dict:
    """
    Create and return dictionary of fonts used in the game.

    Returns:
        Dictionary mapping font names to pygame.font.Font objects
    """
    from config.settings import FONT_NAME, FONT_SIZES

    return {
        'small': pygame.font.SysFont(FONT_NAME, FONT_SIZES['small'], bold=True),
        'medium': pygame.font.SysFont(FONT_NAME, FONT_SIZES['medium'], bold=True),
        'large': pygame.font.SysFont(FONT_NAME, FONT_SIZES['large'], bold=True, italic=True),
        'xlarge': pygame.font.SysFont(FONT_NAME, FONT_SIZES['xlarge'], bold=True),
        'password': pygame.font.SysFont(FONT_NAME, 22, bold=True),
        'default': pygame.font.SysFont(None, 20, bold=True)
    }
