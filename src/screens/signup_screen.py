"""Signup screen implementation."""

import pygame
import os
from typing import Optional, Dict
from screens.base_screen import BaseScreen
from config.settings import *
from config.paths import LOGIN_IMG_DIR


class SignupScreen(BaseScreen):
    """Signup screen for creating new user accounts."""

    def __init__(self, display, clock, fonts, sound_manager, db_manager):
        """Initialize signup screen."""
        super().__init__(display, clock, fonts, sound_manager, db_manager)

        self.input_username = ""
        self.input_password = ""
        self.censored_password = ""
        self.input_repassword = ""
        self.censored_repassword = ""
        self.input_email = ""

        self.typing_username = False
        self.typing_password = False
        self.retyping_password = False
        self.typing_email = False

        self.status = None
        self.next_action = None

        # Define UI rectangles
        self.username_area = pygame.Rect(286, 303, 509, 45)
        self.password_area = pygame.Rect(286, 360, 509, 45)
        self.repassword_area = pygame.Rect(286, 417, 509, 45)
        self.email_area = pygame.Rect(286, 474, 509, 45)
        self.signup_button = pygame.Rect(490, 531, 100, 46)
        self.exit_button = pygame.Rect(922, 71, 88, 87)

        # Load background
        self.load_background()

        # Play sound
        self.sound_manager.play("start", loops=-1)

    def load_background(self) -> None:
        """Load background image."""
        bg_path = os.path.join(LOGIN_IMG_DIR, "signupscreen", f"{self.language}.png")
        self.background = self.load_image(bg_path)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.sound_manager.play("click")
                self.clicked = True

            if event.type == pygame.KEYDOWN:
                self._handle_keyboard(event)

    def _handle_keyboard(self, event) -> None:
        """Handle keyboard input."""
        if event.key == pygame.K_RETURN:
            if self.input_username and self.input_password and self.input_email:
                self._attempt_signup()
        elif event.key == pygame.K_BACKSPACE:
            if self.typing_username:
                self.input_username = self.input_username[:-1]
            elif self.typing_password:
                self.input_password = self.input_password[:-1]
                self.censored_password = self.censored_password[:-1]
            elif self.retyping_password:
                self.input_repassword = self.input_repassword[:-1]
                self.censored_repassword = self.censored_repassword[:-1]
            elif self.typing_email:
                self.input_email = self.input_email[:-1]
        else:
            # Character input
            if self.typing_username:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_username) < 25:
                        self.input_username += event.unicode
            elif self.typing_password:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_password) < 25:
                        self.input_password += event.unicode
                        self.censored_password += "*"
            elif self.retyping_password:
                if event.key in CHARACTER_KEYS or event.key in NUMBER_KEYS:
                    if len(self.input_repassword) < 25:
                        self.input_repassword += event.unicode
                        self.censored_repassword += "*"
            elif self.typing_email:
                if len(self.input_email) < 35:
                    self.input_email += event.unicode

    def update(self) -> None:
        """Update screen logic."""
        # Username area
        if self.username_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.username_area, 3, 30)
            if self.clicked:
                self.typing_username = True
                self.typing_password = False
                self.retyping_password = False
                self.typing_email = False
                self.status = None

        # Password area
        if self.password_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.password_area, 3, 30)
            if self.clicked:
                self.typing_password = True
                self.typing_username = False
                self.retyping_password = False
                self.typing_email = False
                self.status = None

        # Re-password area
        if self.repassword_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.repassword_area, 3, 30)
            if self.clicked:
                self.retyping_password = True
                self.typing_username = False
                self.typing_password = False
                self.typing_email = False
                self.status = None

        # Email area
        if self.email_area.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.email_area, 3, 30)
            if self.clicked:
                self.typing_email = True
                self.typing_username = False
                self.typing_password = False
                self.retyping_password = False
                self.status = None

        # Signup button
        if self.signup_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.signup_button, 3, 30)
            if self.clicked:
                self._attempt_signup()

        # Exit button
        if self.exit_button.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.display, GREEN, self.exit_button, 3, 25)
            if self.clicked:
                self.sound_manager.stop("start")
                self.running = False

        # Reset clicked flag after all checks
        self.clicked = False

    def _attempt_signup(self) -> None:
        """Attempt to create new account."""
        if not all(
            [
                self.input_username,
                self.input_password,
                self.input_email,
                self.input_repassword,
            ]
        ):
            return

        # Validate email format
        if not self._validate_email(self.input_email):
            self.status = "invalid_email"
            return

        # Check password match
        if self.input_password != self.input_repassword:
            self.status = "password_mismatch"
            return

        # Check if username exists
        status, _ = self.db_manager.check_account_exists(
            self.input_username, "", self.input_email
        )

        if status == 1:  # Username exists
            self.status = "username_exists"
            return

        # Create user - Supabase will send confirmation email automatically
        try:
            user = self.db_manager.create_user(
                self.input_username, self.input_password, self.input_email
            )
            self.sound_manager.stop("start")
            self.status = "check_email"
            # Don't auto-login, show message to check email
            # User needs to confirm email before they can login
        except Exception as e:
            error_msg = str(e)
            if (
                "User already registered" in error_msg
                or "already registered" in error_msg
            ):
                self.status = "username_exists"
            else:
                print(f"Error creating user: {e}")
                self.status = "signup_error"

    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        if len(email) < 10:
            return False
        if email[0] == "@":
            return False
        if not email.endswith("@gmail.com"):
            return False
        return True

    def draw(self) -> None:
        """Draw screen elements."""
        # Draw background
        self.display.blit(self.background, (0, 0))

        # Draw input text
        self.draw_text(self.input_username, "small", BLACK, 477, 316)
        self.draw_text(self.censored_password, "password", BLACK, 477, 375)
        self.draw_text(self.censored_repassword, "password", BLACK, 477, 431)
        self.draw_text(self.input_email, "small", BLACK, 477, 487)

        # Draw status messages
        y_pos = 583
        if self.status == "invalid_email":
            msg = "Invalid email!" if self.language == 0 else "Email không hợp lệ!"
            self.draw_text(msg, "medium", BLACK, 440, y_pos)
        elif self.status == "email_exists":
            msg = (
                "Email already used!"
                if self.language == 0
                else "Email đã được sử dụng!"
            )
            self.draw_text(msg, "medium", BLACK, 380, y_pos)
        elif self.status == "username_exists":
            msg = (
                "Username existed!"
                if self.language == 0
                else "Tên đăng nhập đã tồn tại!"
            )
            self.draw_text(msg, "medium", BLACK, 380, y_pos)
        elif self.status == "password_mismatch":
            msg = (
                "Confirmation password incorrect!"
                if self.language == 0
                else "Mật khẩu xác nhận không đúng!"
            )
            self.draw_text(msg, "medium", BLACK, 360, y_pos)
        elif self.status == "check_email":
            msg = (
                "Check your email to confirm!"
                if self.language == 0
                else "Kiểm tra email để xác nhận!"
            )
            self.draw_text(msg, "medium", GREEN, 360, y_pos)
        elif self.status == "signup_error":
            msg = "Signup failed!" if self.language == 0 else "Đăng ký thất bại!"
            self.draw_text(msg, "medium", BLACK, 420, y_pos)

    def get_next_state(self) -> Optional[Dict]:
        """Get next action/state."""
        return self.next_action
