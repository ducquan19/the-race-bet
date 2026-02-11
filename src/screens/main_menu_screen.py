"""Main menu screen implementation."""

import pygame
import os
from typing import Optional, Dict
from screens.base_screen import BaseScreen
from models.user import User
from config.settings import *
from config.paths import MENU_IMG_DIR


class MainMenuScreen(BaseScreen):
    """Main menu screen."""

    def __init__(self, display, clock, fonts, sound_manager, db_manager, user: User):
        """Initialize main menu screen."""
        super().__init__(display, clock, fonts, sound_manager, db_manager)

        self.user = user
        self.next_action = None

        # Define UI rectangles
        self.play_button = pygame.Rect(655, 281, 320, 159)
        self.shop_button = pygame.Rect(71, 587, 82, 82)
        self.history_button = pygame.Rect(185, 586, 82, 82)
        self.minigame_button = pygame.Rect(482, 596, 137, 61)
        self.guide_button = pygame.Rect(74, 38, 78, 78)
        self.setting_button = pygame.Rect(932, 584, 77, 77)
        self.exit_button = pygame.Rect(941, 34, 97, 77)

        # Load background
        self.background = self.load_image(
            os.path.join(MENU_IMG_DIR, "mainmenu.png"), WINDOWSIZE
        )

        # Play sound
        self.sound_manager.play("ingame", loops=-1)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.db_manager.save_user(self.user)
                self.running = False
                self.next_action = {"action": "quit"}
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.sound_manager.play("click")
                self.clicked = True

    def update(self) -> None:
        """Update screen logic."""
        # Play button
        if self.play_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.play_button, 3, 30)
            if self.clicked:
                self.sound_manager.stop("ingame")
                self.next_action = {"action": "play"}
                self.running = False

        # Shop button
        if self.shop_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.shop_button, 3, 30)
            if self.clicked:
                self.sound_manager.stop("ingame")
                self.next_action = {"action": "shop"}
                self.running = False

        # History button
        if self.history_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.history_button, 3, 30)
            if self.clicked:
                self.sound_manager.stop("ingame")
                self.next_action = {"action": "history"}
                self.running = False

        # Minigame button
        if self.minigame_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.minigame_button, 3, 30)
            if self.clicked:
                self.sound_manager.stop("ingame")
                self.next_action = {"action": "minigame"}
                self.running = False

        # Guide button
        if self.guide_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.guide_button, 3, 30)
            if self.clicked:
                self.sound_manager.stop("ingame")
                self.next_action = {"action": "help"}
                self.running = False

        # Settings button
        if self.setting_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.setting_button, 3, 25)
            if self.clicked:
                # Open settings temporarily
                self.language = 1 - self.language
                self.next_action = {
                    "action": "settings",
                    "language": self.language,
                    "volume": self.sound_manager.get_volume(),
                }

        # Exit button
        if self.exit_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.exit_button, 3, 25)
            if self.clicked:
                self.db_manager.save_user(self.user)
                # Show confirm exit dialog
                self.next_action = {"action": "quit"}
                self.running = False

        # Reset clicked flag after all checks
        self.clicked = False

    def draw(self) -> None:
        """Draw screen elements."""
        # Draw background
        self.display.blit(self.background, (0, 0))

        # Draw user info
        self.draw_text(self.user.username, "large", BLACK, 425, 52)
        self.draw_text(str(self.user.money), "medium", COIN_COLOR, 619, 58)

    def get_next_state(self) -> Optional[Dict]:
        """Get next action/state."""
        return self.next_action
