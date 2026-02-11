"""Change password screen implementation."""

import pygame
import os
from typing import Optional, Dict
from screens.base_screen import BaseScreen
from config.settings import *
from config.paths import LOGIN_IMG_DIR


class ChangePasswordScreen(BaseScreen):
    """Change password screen for password recovery."""

    def __init__(
        self, display, clock, fonts, sound_manager, db_manager, user_id, username
    ):
        """Initialize change password screen."""
        super().__init__(display, clock, fonts, sound_manager, db_manager)

        self.user_id = user_id
        self.username = username
        self.input_password = ""
        self.censored_password = ""
        self.input_repassword = ""
        self.censored_repassword = ""
        self.typing_password = False
        self.retyping_password = True
        self.status = None
        self.next_action = None

        # Define UI rectangles
        self.newpw_area = pygame.Rect(294, 362, 489, 47)
        self.confirmpw_area = pygame.Rect(294, 416, 489, 47)
        self.change_button = pygame.Rect(452, 482, 176, 70)
        self.exit_button = pygame.Rect(922, 71, 88, 87)

        # Load background
        self.load_background()

        # Play start sound
        self.sound_manager.play("start", loops=-1)

    def load_background(self) -> None:
        """Load background image."""
        bg_path = os.path.join(LOGIN_IMG_DIR, "changenewpw", f"{self.language}.png")
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
            if self.input_password and self.input_repassword:
                self._attempt_change()
        elif event.key == pygame.K_BACKSPACE:
            if self.typing_password:
                self.input_password = self.input_password[:-1]
                self.censored_password = self.censored_password[:-1]
            elif self.retyping_password:
                self.input_repassword = self.input_repassword[:-1]
                self.censored_repassword = self.censored_repassword[:-1]
        else:
            # Character input
            if self.typing_password and not self.retyping_password:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_password) < 25:
                        self.input_password += event.unicode
                        self.censored_password += "*"
            elif self.retyping_password and not self.typing_password:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_repassword) < 25:
                        self.input_repassword += event.unicode
                        self.censored_repassword += "*"

    def update(self) -> None:
        """Update screen logic."""
        # Check new password input area
        if self.newpw_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.newpw_area, 3, 30)
            if self.clicked:
                self.typing_password = True
                self.retyping_password = False
                self.status = None

        # Check confirm password input area
        if self.confirmpw_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.confirmpw_area, 3, 30)
            if self.clicked:
                self.typing_password = False
                self.retyping_password = True
                self.status = None

        # Check exit button
        if self.exit_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.exit_button, 3, 15)
            if self.clicked:
                self.sound_manager.stop("start")
                self.running = False

        # Check change button
        if self.change_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.change_button, 3, 45)
            if self.clicked:
                self.typing_password = False
                self.retyping_password = False
                self._attempt_change()

        # Reset clicked flag after all checks
        self.clicked = False

    def _attempt_change(self) -> None:
        """Attempt to change password."""
        if not self.input_password or not self.input_repassword:
            return

        if self.input_password != self.input_repassword:
            self.status = "mismatch"
        else:
            # Update password in database
            success = self.db_manager.update_password(self.user_id, self.input_password)

            if success:
                self.status = "success"
                self.sound_manager.stop("start")
                # Go back to login screen
                self.next_action = {"action": "goto_login"}
                self.running = False
            else:
                self.status = "error"

    def draw(self) -> None:
        """Draw screen elements."""
        # Draw background
        self.display.blit(self.background, (0, 0))

        # Draw input text
        self.draw_text(self.censored_password, "password", BLACK, 405, 376)
        self.draw_text(self.censored_repassword, "password", BLACK, 405, 431)

        # Draw status messages
        if self.status == "mismatch":
            msg = (
                "Confirmation password is incorrect!"
                if self.language == 0
                else "Mật khẩu xác nhận không đúng!"
            )
            self.draw_text(
                msg, "medium", BLACK, 380 if self.language == 0 else 397, 553
            )
        elif self.status == "success":
            msg = (
                "Password changed successfully!"
                if self.language == 0
                else "Đổi mật khẩu thành công!"
            )
            self.draw_text(
                msg, "medium", GREEN, 380 if self.language == 0 else 397, 553
            )

    def get_next_state(self) -> Optional[Dict]:
        """Get next action/state."""
        return self.next_action
