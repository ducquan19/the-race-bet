"""Base screen class for all game screens."""

from abc import ABC, abstractmethod
import pygame
from typing import Optional, Tuple
from config.settings import *


class BaseScreen(ABC):
    """Abstract base class for all game screens."""

    def __init__(
        self,
        display: pygame.Surface,
        clock: pygame.time.Clock,
        fonts: dict,
        sound_manager,
        db_manager,
    ):
        """
        Initialize base screen.

        Args:
            display: Main display surface
            clock: Game clock
            fonts: Dictionary of fonts
            sound_manager: Sound manager instance
            db_manager: Database manager instance
        """
        self.display = display
        self.clock = clock
        self.fonts = fonts
        self.sound_manager = sound_manager
        self.db_manager = db_manager
        self.running = True
        self.clicked = False
        self.mouse_pos = (0, 0)
        self.language = DEFAULT_LANGUAGE

    @abstractmethod
    def handle_events(self) -> None:
        """Handle pygame events. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Update screen logic. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Draw screen elements. Must be implemented by subclasses."""
        pass

    def run(self) -> Optional[str]:
        """
        Main screen loop.

        Returns:
            Next state to transition to, or None to quit
        """
        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

        return self.get_next_state()

    def get_next_state(self) -> Optional[str]:
        """
        Get the next state to transition to.
        Can be overridden by subclasses.

        Returns:
            Next state name or None
        """
        return None

    def load_image(
        self, path: str, scale: Optional[Tuple[int, int]] = None
    ) -> pygame.Surface:
        """
        Load and optionally scale an image.

        Args:
            path: Path to image file
            scale: Optional (width, height) tuple to scale to

        Returns:
            Loaded pygame Surface
        """
        image = pygame.image.load(path)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image

    def check_button_click(self, rect: pygame.Rect) -> bool:
        """
        Check if a button was clicked.

        Args:
            rect: Button rectangle

        Returns:
            True if button was clicked
        """
        if rect.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, rect, 3, 15)
            if self.clicked:
                self.sound_manager.play("click")
                return True
        return False

    def draw_text(
        self, text: str, font_name: str, color: Tuple[int, int, int], x: int, y: int
    ) -> None:
        """
        Draw text on the display.

        Args:
            text: Text to draw
            font_name: Name of font from fonts dict
            color: RGB color tuple
            x: X coordinate
            y: Y coordinate
        """
        from utils.drawing_utils import draw_text

        font = self.fonts.get(font_name, self.fonts["default"])
        draw_text(text, font, color, self.display, x, y)

    def set_language(self, language: int) -> None:
        """Set the current language."""
        self.language = language

    def get_localized_image_path(self, base_path: str) -> str:
        """
        Get localized image path based on current language.

        Args:
            base_path: Base path with {} placeholder for language

        Returns:
            Path with language substituted
        """
        return base_path.format(self.language)
