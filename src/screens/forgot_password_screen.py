"""Forgot password screen implementation."""

import pygame
import os
from typing import Optional, Dict
from screens.base_screen import BaseScreen
from config.settings import *
from config.paths import LOGIN_IMG_DIR


class ForgotPasswordScreen(BaseScreen):
    """Forgot password screen for password recovery using Supabase."""

    def __init__(self, display, clock, fonts, sound_manager, db_manager):
        """Initialize forgot password screen."""
        super().__init__(display, clock, fonts, sound_manager, db_manager)

        self.input_email = ""
        self.typing_email = False
        self.status = None
        self.next_action = None

        # Define UI rectangles (simplified - only email needed)
        self.email_area = pygame.Rect(300, 380, 480, 50)
        self.send_button = pygame.Rect(440, 470, 200, 60)
        self.exit_button = pygame.Rect(922, 71, 88, 87)

        # Load background
        self.load_background()

        # Play start sound
        self.sound_manager.play("start", loops=-1)

    def load_background(self) -> None:
        """Load background image."""
        bg_path = os.path.join(LOGIN_IMG_DIR, "forgotscreen", f"{self.language}.png")
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
            if self.input_email:
                self._send_reset_email()
        elif event.key == pygame.K_BACKSPACE:
            if self.typing_email:
                self.input_email = self.input_email[:-1]
        else:
            # Character input
            if self.typing_email:
                if len(self.input_email) < 50:
                    self.input_email += event.unicode

    def update(self) -> None:
        """Update screen logic."""
        # Check email input area
        if self.email_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.email_area, 3, 30)
            if self.clicked:
                self.typing_email = True
                self.status = None

        # Check send button
        if self.send_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.send_button, 3, 30)
            if self.clicked:
                self._send_reset_email()

        # Check exit button
        if self.exit_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.exit_button, 3, 25)
            if self.clicked:
                self.sound_manager.stop("start")
                self.running = False

        # Reset clicked flag after all checks
        self.clicked = False

    def _send_reset_email(self) -> None:
        """Send password reset email via Supabase."""
        if not self.input_email:
            self.status = "empty_email"
            return

        # Validate email format
        if "@" not in self.input_email or len(self.input_email) < 5:
            self.status = "invalid_email"
            return

        try:
            # Use Supabase's built-in password reset
            self.db_manager.supabase.auth.reset_password_for_email(self.input_email)
            self.status = "email_sent"
        except Exception as e:
            print(f"Failed to send reset email: {e}")
            self.status = "email_failed"

    def draw(self) -> None:
        """Draw screen elements."""
        # Draw background
        self.display.blit(self.background, (0, 0))

        # Draw input text
        self.draw_text(self.input_email, "medium", BLACK, 320, 395)

        # Draw status messages
        y_pos = 550
        if self.status == "email_sent":
            msg = (
                "Check your email for reset link!"
                if self.language == 0
                else "Kiểm tra email để đặt lại mật khẩu!"
            )
            self.draw_text(msg, "medium", GREEN, 320, y_pos)
        elif self.status == "invalid_email":
            msg = "Invalid email!" if self.language == 0 else "Email không hợp lệ!"
            self.draw_text(msg, "medium", BLACK, 440, y_pos)
        elif self.status == "email_failed":
            msg = (
                "Failed to send email!" if self.language == 0 else "Gửi email thất bại!"
            )
            self.draw_text(msg, "medium", BLACK, 400, y_pos)
        elif self.status == "empty_email":
            msg = (
                "Please enter email!" if self.language == 0 else "Vui lòng nhập email!"
            )
            self.draw_text(msg, "medium", BLACK, 410, y_pos)

    def get_next_state(self) -> Optional[Dict]:
        """Get next action/state."""
        return self.next_action
