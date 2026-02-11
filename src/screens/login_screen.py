"""Login screen implementation."""

import pygame
import os
from typing import Optional, Dict
from screens.base_screen import BaseScreen
from config.settings import *
from config.paths import LOGIN_IMG_DIR


class LoginScreen(BaseScreen):
    """Login screen for user authentication."""

    def __init__(self, display, clock, fonts, sound_manager, db_manager):
        """Initialize login screen."""
        super().__init__(display, clock, fonts, sound_manager, db_manager)

        self.input_username = ""
        self.input_password = ""
        self.censored_password = ""
        self.typing_username = False
        self.typing_password = False
        self.status = None
        self.next_action = None

        # Define UI rectangles
        self.username_area = pygame.Rect(355, 315, 372, 48)
        self.password_area = pygame.Rect(355, 382, 372, 48)
        self.login_button = pygame.Rect(400, 460, 107, 45)
        self.signup_button = pygame.Rect(530, 460, 102, 45)
        self.forgot_password_area = pygame.Rect(362, 430, 150, 27)
        self.faceid_button = pygame.Rect(674, 459, 50, 50)
        self.setting_button = pygame.Rect(932, 584, 77, 77)

        # Load background
        self.load_background()

        # Play start sound
        self.sound_manager.play("start", loops=-1)

    def load_background(self) -> None:
        """Load background image."""
        bg_path = os.path.join(LOGIN_IMG_DIR, "loginscreen", f"{self.language}.png")
        self.background = self.load_image(bg_path)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.next_action = None
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.sound_manager.play("click")
                self.clicked = True

            if event.type == pygame.KEYDOWN:
                self._handle_keyboard(event)

    def _handle_keyboard(self, event) -> None:
        """Handle keyboard input."""
        if event.key == pygame.K_RETURN:
            if self.input_username and self.input_password:
                self._attempt_login()
        elif event.key == pygame.K_BACKSPACE:
            if self.typing_username:
                self.input_username = self.input_username[:-1]
            elif self.typing_password:
                self.input_password = self.input_password[:-1]
                self.censored_password = self.censored_password[:-1]
        else:
            # Character input
            if self.typing_username and not self.typing_password:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_username) < 25:
                        self.input_username += event.unicode
            elif self.typing_password and not self.typing_username:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_password) < 25:
                        self.input_password += event.unicode
                        self.censored_password += "*"

    def update(self) -> None:
        """Update screen logic."""
        # Check username input area
        if self.username_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.username_area, 3, 30)
            if self.clicked:
                self.typing_username = True
                self.typing_password = False
                self.status = None

        # Check password input area
        if self.password_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.password_area, 3, 30)
            if self.clicked:
                self.typing_password = True
                self.typing_username = False
                self.status = None

        # Check login button
        if self.login_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.login_button, 3, 30)
            if self.clicked:
                self._attempt_login()

        # Check signup button
        if self.signup_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.signup_button, 3, 30)
            if self.clicked:
                self.sound_manager.stop("start")
                self.next_action = {"action": "goto_signup"}
                self.running = False

        # Check forgot password
        if self.forgot_password_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.forgot_password_area, 3, 10)
            if self.clicked:
                self.sound_manager.stop("start")
                self.next_action = {"action": "goto_forgot"}
                self.running = False

        # Check settings button
        if self.setting_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.setting_button, 3, 25)
            if self.clicked:
                self._open_settings()

        # Reset clicked flag after all checks
        self.clicked = False

    def _attempt_login(self) -> None:
        """Attempt to log in with current credentials."""
        if not self.input_username or not self.input_password:
            return

        # For Supabase, we need to construct email from username or use actual email
        # If user provides email format, use it; otherwise create local email
        email = (
            self.input_username
            if "@" in self.input_username
            else f"{self.input_username}@luckyrace.local"
        )

        status, user_id = self.db_manager.check_account_exists(
            self.input_username, self.input_password, email
        )

        if status == 1:  # Login successful
            user = self.db_manager.load_user(user_id)
            self.running = False
        elif status == 0:  # Wrong password
            self.status = "wrong_password"
        elif status == -1:  # Account not found
            self.status = "not_exist"

    def _open_settings(self) -> None:
        """Open settings temporarily."""
        # This would open a settings dialog
        # For now, just toggle language as an example
        self.language = 1 - self.language
        self.load_background()
        self.next_action = {
            "action": "setting",
            "language": self.language,
            "volume": self.sound_manager.get_volume(),
        }

    def draw(self) -> None:
        """Draw screen elements."""
        # Draw background
        self.display.blit(self.background, (0, 0))

        # Draw input text
        self.draw_text(self.input_username, "small", BLACK, 467, 329)
        self.draw_text(self.censored_password, "password", BLACK, 467, 396)

        # Draw status messages
        if self.status == "wrong_password":
            msg = "Wrong password" if self.language == 0 else "Sai mật khẩu"
            self.draw_text(msg, "medium", BLACK, 460, 518)
        elif self.status == "not_exist":
            msg = (
                "Account is not exist"
                if self.language == 0
                else "Tài khoản không tồn tại"
            )
            self.draw_text(msg, "medium", BLACK, 438, 518)

    def get_next_state(self) -> Optional[Dict]:
        """Get next action/state."""
        return self.next_action
