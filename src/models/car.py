"""Car model for racing game."""

import pygame
from typing import Tuple


class Car:
    """Represents a racing car in the game."""

    def __init__(self, image: pygame.Surface, x: int, y: int, width: int,
                 rank_instance: int = 0, rank: int = 0):
        """
        Initialize a car.

        Args:
            image: The car's sprite image
            x: Starting x position
            y: Starting y position
            width: Car width
            rank_instance: Instance ranking
            rank: Final ranking
        """
        self.img = image
        self.x = x
        self.y = y
        self.width = width
        self.rank_instance = rank_instance
        self.rank = rank
        self.finish_x = x + width

        # Status flags
        self.flip = False
        self.speedup = False
        self.slow = False
        self.stop = False
        self.timer = 0
        self.flash = False
        self.finish = False
        self.cheer = False

    def get_rect(self) -> pygame.Rect:
        """Get the car's collision rectangle."""
        return pygame.Rect(self.x, self.y, self.width, 50)

    def move(self, speed: int = 0) -> None:
        """Move the car forward."""
        self.x += speed
        self.finish_x = self.x + self.width

    def apply_speedup(self, duration: int = 30) -> None:
        """Apply speed boost effect."""
        self.speedup = True
        self.timer = duration

    def apply_slow(self, duration: int = 30) -> None:
        """Apply slow effect."""
        self.slow = True
        self.timer = duration

    def apply_stop(self, duration: int = 30) -> None:
        """Apply stop effect."""
        self.stop = True
        self.timer = duration

    def apply_flip(self, duration: int = 30) -> None:
        """Apply flip/reverse effect."""
        self.flip = True
        self.timer = duration

    def apply_flash(self, distance: int = 50) -> None:
        """Apply flash/teleport forward."""
        self.x += distance
        self.finish_x = self.x + self.width

    def set_rank(self, rank: int, rank_instance: int) -> None:
        """Set the car's ranking."""
        self.rank = rank
        self.rank_instance = rank_instance
        self.finish = True

    def update(self) -> None:
        """Update car status effects."""
        if self.timer > 0:
            self.timer -= 1

            if self.flip:
                pass  # Flip is handled in drawing

            if self.speedup:
                self.move(3)

            if self.slow:
                self.move(-3)

            if self.stop:
                self.move(-6)
        else:
            # Reset effects when timer expires
            self.flip = False
            self.speedup = False
            self.slow = False
            self.stop = False
            self.cheer = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the car on the surface."""
        if self.flip:
            flipped_img = pygame.transform.flip(self.img, True, False)
            surface.blit(flipped_img, (self.x, self.y))
        else:
            surface.blit(self.img, (self.x, self.y))

    def is_finished(self) -> bool:
        """Check if car has finished the race."""
        return self.rank > 0

    def reset_effects(self) -> None:
        """Reset all active effects."""
        self.flip = False
        self.speedup = False
        self.slow = False
        self.stop = False
        self.timer = 0
        self.flash = False
        self.cheer = False
